#//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2//POC2
import pickle
import math
import locale
from collections import namedtuple
from tarfile import NUL
from typing import Type
#from turtle import width
from app2 import main2
from app2 import mainPivot
from app2 import mainPivotChart
from app2 import mainPowerBI
from app2 import mainDashboard

import threading
import streamlit as st
import requests
import pandas as pd
import json
import streamlit_highcharts as hct
import asyncio

import streamlit as st
from azure.storage.blob import BlobServiceClient
import requests
import json
import uuid
import time
from PIL import Image
from io import BytesIO
import ast
# Configuration№
#FUNCTION_BASE_URL = "http://localhost:7190/api" # e.g., https://<function-app>.azurewebsites.net/api/
version="2.3a"
FUNCTION_BASE_URL = "https://glauditpoc2azurefunction.azurewebsites.net/api"

GENERATE_SAS_TOKEN_ENDPOINT = f"{FUNCTION_BASE_URL}/GenerateSASToken"
START_ORCHESTRATOR_ENDPOINT = f"{FUNCTION_BASE_URL}/start-orchestrator"
EXTRACT_COLUMNS_ENDPOINT = f"{FUNCTION_BASE_URL}/start-column-extraction"  # New endpoint for column extraction
CHECK_JOB_STATUS_ENDPOINT = f"{FUNCTION_BASE_URL}/check-job-status"
GETCHART_ENDPOINT = f"{FUNCTION_BASE_URL}/getchart"
RUNNOTEBOOK_ENDPOINT = f"{FUNCTION_BASE_URL}/RunDatabricksNotebook"
GETRESULT_ENDPOINT = f"{FUNCTION_BASE_URL}/GetResult"
API_URL_DATA = f"{FUNCTION_BASE_URL}/GetPaginatedData"
API_URL_DOWNLOAD = f"{FUNCTION_BASE_URL}/DownloadTableCsv"
storage_connection_string="DefaultEndpointsProtocol=https;AccountName=zuscutaargpletoaudi9020;AccountKey=i2Fs+bpmHyCWzk/lwpkclGW6gWaGQumksWbQgjDmverFwG+O/lmz1aTTvHxawzyT+rRDfxw3DKQ9+ASt8RFXow==;EndpointSuffix=core.windows.net"
storage_account = "zuscutaargpletoaudi9020"
container = "testcontainer"

class Task:
    def __init__(self, id):
        self.id = id
        self.progress = 0
        self.status = 'Running'
        self.weight = 25
        self.count=0
        self.name=""
        self.amount=0
        self.lock = threading.Lock()

    def update_progress(self, value):
        with self.lock:
            self.progress = value

    def set_status(self, status):
        with self.lock:
            self.status = status

    def get_progress(self):
        with self.lock:
            return self.progress

    def get_status(self):
        with self.lock:
            return self.status

    def get_weight(self):
        with self.lock:
            return self.weight
    def set_weight(self, weight):
        with self.lock:
            self.weight= weight
    def get_name(self):
        with self.lock:
            return self.name
    def set_name(self, name):
        with self.lock:
            self.weight= name

#FUNCTION_KEY = os.getenv("FUNCTION_KEY")  # If using function keys for authentication
FUNCTION_KEY=""

data = [
    {
        "firmId": 1,
        "customer_name": "John & Associates",
        "engagements": [
            {"engagementId": 1, "engagement_name": "Financial Audit 2024"},
            {"engagementId": 2, "engagement_name": "Tax Consulting 2024"}
        ]
    },
    {
        "firmId": 2,
        "customer_name": "Global Audit Co",
        
        
        "engagements": [
            {"engagementId": 3, "engagement_name": "Internal Controls Review"},
            {"engagementId": 4, "engagement_name": "Test Audit - 2024"}
        ]
    }
]



test_data = {
        "UnusualTest": {
            "status": "Not started",
            "start_time": None,
            "end_time": None,
            "error": None,
            "name": "Unusual Account Combinations",
            "weight": 50,
            "parameters": {},
            "count": 0,
            "sumAmount": 0
        },
        "DuplicateTest": {
            "status": "Not started",
            "start_time": None,
            "end_time": None,
            "error": None,
            "name": "Duplicate Entries",
            "weight": 50,
            "parameters": {},
            "count": 0,
            "sumAmount": 0
        },
        "OutlierTest": {
            "status": "Not started",
            "start_time": None,
            "end_time": None,
            "error": None,
            "name": "Outlier Amounts Detection",
            "weight": 50,
            "parameters": {},
            "count": 0,
            "sumAmount": 0
        },
        "RoundedTest": {
            "status": "Not started",
            "start_time": None,
            "end_time": None,
            "error": None,
            "name": "Rounded Amounts",
            "weight": 50,
            "parameters": {},
            "count": 0,
            "sumAmount": 0
        },
        
        "UnexpectedposterTest": {
            "status": "Not started",
            "start_time": None,
            "end_time": None,
            "error": None,
            "name": "Unexpected Poster",
            "weight": 50,
            "parameters": {},
            "count": 0,
            "sumAmount": 0
        },
        "WeekendTest": {
            "status": "Not started",
            "start_time": None,
            "end_time": None,
            "error": None,
            "name": "Entries Posted During Weekends",
            "weight": 50,
            "parameters": {},
            "count": 0,
            "sumAmount": 0
        },
            "SuspiciousTest": {
            "status": "Not started",
            "start_time": None,
            "end_time": None,
            "error": None,
            "name": "Suspicious keywords",
            "weight": 50,
            "parameters": {"words":[
                                    "accrue", "accrual", "adjust", "alter", "request", "audit", "bonus", "bury",
                                    "cancel", "capital", "ceo", "cfo", "classify", "confidential", "correct",
                                    "correction", "coverup", "director", "ebit", "error", "estimate", "fix",
                                    "fraud", "gift", "hide", "incentive", "issue", "kite", "kiting", "lease",
                                    "mis", "net", "per", "plug", "problem", "profit", "reclass", "rectify",
                                    "reduce", "remove", "reverse", "reversing", "screen", "switch", "temp",
                                    "test", "transfer"
                                    ]

                },
            "count": 0,
            "sumAmount": 0
        }
       
    }

@st.cache_data(ttl=6900)
def fetch_data(tablename,page, page_size,filter,engagementId):
    params = {
        'page': page,
        'pageSize': page_size,
        'tablename':tablename,
        'filter':filter
        
    }
    response = requests.get(API_URL_DATA, params=params)
    if response.status_code == 200:
        result = response.json()
        columns = result['columns']
        data = result['data']
        df = pd.DataFrame(data)
        df = df[columns]
        return df
    else:
        
        st.error("Error fetching data"+str(response))
        return pd.DataFrame()
    
@st.cache_data
def get_sas_url(file_name=None):
    params = {"container": "testcontainer"}
    # print(GENERATE_SAS_TOKEN_ENDPOINT)
    if file_name:
        params["fileName"] = file_name
    headers = {}
    # if FUNCTION_KEY:
    #     headers["x-functions-key"] = FUNCTION_KEY
    response = requests.get(GENERATE_SAS_TOKEN_ENDPOINT, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()['sasUrl']
    else:
        st.error("Failed to get SAS token.")
        st.stop()

#@st.cache_data
def upload_file_to_blob( file,filename):
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string, max_block_size=1024*1024*4,        max_single_put_size=1024*1024*8 )

    blob_client = blob_service_client.get_blob_client(container="testcontainer", blob=filename)
    
    ret=blob_client.upload_blob(file, overwrite=True,max_concurrency=4)
    st.success("File uploaded to Azure Blob Storage."+str(storage_connection_string))

    #print(ret)
    
#@st.cache_data
def start_orchestration(input_data):
    headers = {"Content-Type": "application/json"}
    # if FUNCTION_KEY:
    #     headers["x-functions-key"] = FUNCTION_KEY
    print ("!!!!!!")
    #print(input_data)
    response = requests.post(START_ORCHESTRATOR_ENDPOINT, headers=headers, data=json.dumps(input_data))
    if response.status_code == 200:
        return response.json()['instanceId']
    else:
        st.error(f"Failed to start orchestration: {response.text}")
        st.stop()


def run_notebook(input_data):
    headers = {"Content-Type": "application/json"}
    # if FUNCTION_KEY:
    #     headers["x-functions-key"] = FUNCTION_KEY
    
    #print(input_data)
    
    response = requests.post(RUNNOTEBOOK_ENDPOINT, headers=headers, data=json.dumps(input_data))
    print("run_notebook"+ str(response) )
    if response.status_code == 200:
        return "SUCCESS"
    else:
        st.error(f"Failed to start orchestration: {response.text}")
        st.stop()

def get_result(input_data):
    headers = {"Content-Type": "application/json"}
    # if FUNCTION_KEY:
    #     headers["x-functions-key"] = FUNCTION_KEY
    
    #print(input_data)
    
    response = requests.post(GETRESULT_ENDPOINT, headers=headers, data=json.dumps(input_data))
    print("run_notebook"+ str(response) )
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to start orchestration: {response.text}")
        st.stop()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def check_job_status(instance_id,typeid):
    headers = {}
    # if FUNCTION_KEY:
    #     headers["x-functions-key"] = FUNCTION_KEY
#    st.write(f"{CHECK_JOB_STATUS_ENDPOINT}/{instance_id}/{typeid}")
    response = requests.get(f"{CHECK_JOB_STATUS_ENDPOINT}/{instance_id}/{typeid}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to check job status: {response.text}")
        st.stop()

def update_tests(test_dest, status):
    print("UODATE TESTS!!!!")
    for test_name, test_info in status.items():
        print(test_name)
        if test_name in test_dest:
            for key, value in test_info.items():
                # Update only if the value is not None or different from the existing status
                if value is not None and test_dest[test_name].get(key) != value:
                    test_dest[test_name][key] = value
    return test_dest

#@st.cache_data
def extract_columns( file_name,file_nameCA,firmId,engagementId):
    # Prepare input data for column extraction
    input_data = {
        
        
        "FileName": file_name,
        "FileNameCA":file_nameCA,
        "firmId":  str(firmId),
        "engagementId":  str(engagementId),
        #"DatabricksJobId": 447087718645534 #old
        #"DatabricksJobId": 775618648147406
        "DatabricksJobId":1108437370948679
    }

    headers = {"Content-Type": "application/json"}
    #if FUNCTION_KEY:
        #headers["x-functions-key"] = FUNCTION_KEY

    # Trigger the column extraction orchestrator
    
    response = requests.post(EXTRACT_COLUMNS_ENDPOINT, headers=headers, data=json.dumps(input_data))
    
    if response.status_code == 200:
        return response.json()['instanceId']
    else:
        st.error(f"Failed to start column extraction: {response.text}")
        st.stop()


def create_chart():
    df = st.session_state.get('df')
    if df is not None and not df.empty:
        series = [
            {
                'name': 'Benford Prediction',
                'data': df['BenfordPrediction'].tolist(),
                'type': 'line'
            },
            {
                'name': 'Sample Occurrence',
                'data': df['SampleOccurrence'].tolist(),
                'type': 'line'
            },
            {
                'name': 'Lower Limit',
                'data': df['LowerLimit'].tolist(),
                'type': 'line',
                'dashStyle': 'ShortDot'
            },
            {
                'name': 'Upper Limit',
                'data': df['UpperLimit'].tolist(),
                'type': 'line',
                'dashStyle': 'ShortDot'
            }
        ]

        options = {
            'chart': {'type': 'line'},
            'title': {'text': 'Benford Analysis'},
            'xAxis': {
                'categories': df['digit'].astype(str).tolist(),
                'title': {'text': 'Digit'}
            },
            'yAxis': {'title': {'text': 'Value'}},
            'series': series
        }

        hct.streamlit_highcharts(options)
        st.dataframe(df)
    else:
        st.error("No data to display")

def display_parameters(test_key):
    #test = test_data[test_key]
    test = st.session_state['test_data'][test_key]
    st.write("Set parameters for:", test["name"])
  
    # Add specific parameter inputs here based on test type
    if test_key == "UnusualTest":
        test["parameters"]["threshold"] = st.number_input(
            "Threshold for Unusual Account Combinations (X)", min_value=1, value=5, key=test_key + "_param_x")
    elif test_key == "OutlierTest":
        test["parameters"]["std_dev"] = st.number_input(
            "Standard Deviations for Outlier Detection (Y)", min_value=1, value=3, key=test_key + "_param_y")
    elif test_key == "RoundedTest":
        test["parameters"]["rounding_base"] = st.selectbox(
            "Select Rounding Base", [10, 100, 1000, 10000, 100000, 1000000], key=test_key + "_param_rounding")
    elif test_key == "UnexpectedposterTest":
        if( "postedbyList" in  st.session_state['test_data']):
            test["parameters"]['selectPostedBy' ]= st.multiselect(            "Select posted by",            options=st.session_state['test_data']["postedbyList"],            key="postedbyList",placeholder="None selected"        )
            #st.write("You selected:",             test["parameters"]['selectPostedBy' ])
    elif test_key == "SuspiciousTest":

        new_word = st.text_input("Enter a word to add:", key="add_word_input")
        if st.button("Add Word", key="add_word_button"):
            if new_word and new_word not in test["parameters"]["words"] :
                test["parameters"]["words"].append(new_word)
                st.success(f"Word '{new_word}' added to the list.")
            elif not new_word:
                st.warning("Please enter a valid word.")
            else:
                st.warning("Word already exists in the list.")
    
        # Section to remove a word
        st.subheader("Remove a Word")
        selected_words = st.multiselect(
            "Select words to remove:",
            options=test["parameters"]["words"],
            key="remove_word_listbox"
        )
        if st.button("Remove Selected Words", key="remove_word_button"):
            if selected_words:
                for word in selected_words:
                    if word in test["parameters"]["words"]:
                        test["parameters"]["words"].remove(word)
                st.success(f"Removed words: {', '.join(selected_words)}")
            else:
                st.warning("No words selected for removal.")



        # Display the list of words dynamically in a listbox
        st.subheader("  Suspicious Words       ")
        num_columns = 3
        rows = [test["parameters"]["words"][i:i+num_columns] for i in range(0, len(test["parameters"]["words"]), num_columns)]
        df = pd.DataFrame(rows)
        df.columns=[f"Column {i+1}" for i in range(num_columns)]
        st.dataframe(df,hide_index=True)
        

def display_tableTests():
    test_data= st.session_state['test_data']
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    
    
    
    for test_key, test in test_data.items():
        # print("!!!!!")    
        # print(test_key)    
        if isinstance(test, pd.Series):
                if (test == 0).any():
                    continue
                else:
                    print("No zero values in the Series.")
        elif isinstance(test, (int, float, bool)):  # Scalar case
                if test == 0:
                    continue
                else:
                    print("Test is not zero.")
        
        
        
        if("name" not in test):
               continue
        
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 2, 2, 1, 1])
        
        with col1:
            st.text(test["name"])
        with col2:
            st.text(test["status"])
        with col3:
            test["weight"] = st.slider("Weight", 1,100, test["weight"], key=test_key + "_weight",label_visibility="collapsed")
        with col4:
            with st.popover("", icon=":material/settings:"):
                display_parameters(test_key)
        with col5:
            st.text(test["count"])
        with col6:
            st.text(locale.currency(test["sumAmount"], grouping=True))
    

def poll_for_columns(test_data, firmId,engagementId,polling_interval=4, max_attempts=1120):
    columns = []
    print("start poll_for_columns poll_for_columns")
    
    input_data = {
            
                    "ContainerName": "uploads",
                    "FileName": test_data['unique_file_name'],
                    "FileNameCA":  test_data.get('unique_file_nameCA', ""),
                    "firmId":  str(firmId),
                    "engagementId":  str(engagementId),
                    "SelectedColumns": "",  
                     #"DatabricksJobId": 447087718645534  #old
                    #"DatabricksJobId": 447087718645534 #poc1
                    "DatabricksJobId":1108437370948679
                }
    instance_id= extract_columns(test_data['unique_file_name'],test_data.get('unique_file_nameCA', ""), str(firmId),str(engagementId))
    print("poll for coll"+instance_id)
    for _ in range(max_attempts):
        time.sleep(polling_interval)
        print("start 2")
        #st.session_state['polling_status'] = "completed"
        status = check_job_status(instance_id, "columns")
        
        if status["output"] is not None:
            
            test_data["status_column"]="Completed"
            output_data= json.loads(status["output"] )
            test_data["postedbyList"] = output_data["postedbyList"]
            print("poll_for_columns is Completed!!!!")  
            return
     #   else:
           #st.session_state['polling_status'] = "in_progress"
    
    if not columns:
        # status_queue.put( "failed")
        # st.session_state['polling_status'] = "failed"
        test_data["status_column"]="Failed"

def poll_for_chart(test_data,out_data, polling_interval=4, max_attempts=1120):
    summary= []
    input_data={}
    

    
    #input_data['DatabricksJobId']=488644182429847 #Chart old
    input_data['DatabricksJobId']=822693125667863 #Chart
    input_data['FileName']=test_data['unique_file_name']
    
    input_data['Params']= json.dumps(test_data)
    #del out_data['summary_chart']


    print("Start poll_for_chart1")        
    #print(input_data)
    print("Start poll_for_chart1")        
    instance_id = start_orchestration( input_data)
    print("Start poll_for_chart"+instance_id )        
    for _ in range(max_attempts):
        time.sleep(polling_interval)
        
        status = check_job_status(instance_id,"summary")
        print("poll_for_chart:"+str(status))
        #print("poll_for_task2:"+type(status))
        
        #print(status)
        
            
        if status["output"] is not None:
            print("Chart Complted !")
            
            
            outp=json.loads(status['output'])

            out_data['summary']= outp
            
            
            #out_data['summary']= status["output"]["RunTasks_Main"]
            test_data["status_chart"]="completed"
            print("Completed CHART")
            
            break
        else:
            test_data["status"]="in_progress"

def poll_for_task(test_data,out_data,firmId,engagementId, polling_interval=10, max_attempts=1120):
    summary= []
    input_data={}
    #input_data['DatabricksJobId']=861358873659712 #old
    #input_data['DatabricksJobId']=58242941415312 # poc1
    input_data['DatabricksJobId']=192398946403965 #
    
    
    input_data['FileName']=test_data['unique_file_name']
    input_data['Params']= json.dumps(test_data)
    input_data["firmId"]=  str(firmId)
    input_data["engagementId"]=  str(engagementId)
    
    instance_id = start_orchestration( input_data)
    print("Start poll_for_task"+instance_id +str(input_data['FileName']))        
    for _ in range(max_attempts):
        time.sleep(polling_interval)
        
        status = check_job_status(instance_id,"summary")
    
        #print("poll_for_task2:"+type(status))
        
        
        if 'log' in status:
            log_json = status['log']
            #print("LOG:"+str(log_json) )
            if(log_json):
                
                update_tests(test_data,json.loads(log_json))
            
        if status["output"] is not None:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # Parse the 'columns' field, which is a JSON string
            outp=json.loads(status['output'])

            out_data['summary']= outp
            
            
            
            update_tests(test_data,outp['log'])
            test_data["status"]="completed"
            print("Completed poll_for_task")
            
            break
        else:
            test_data["status"]="in_progress"
        

    
    if not summary:
        test_data["status"]="failed"
        


def init():
    if 'runbutton_enabled' not in st.session_state:
        st.session_state['runbutton_enabled'] = False
        
    if  'IsLoadedChart' not in st.session_state:
        st.session_state['IsLoadedChart']=True
        st.session_state["prev_selected_engagements"]=""
    if  'test_dataChart' not in st.session_state:
        st.session_state['test_dataChart']={}
    if 'filtered_df' not in st.session_state:
        st.session_state['filtered_df']=[]  
    if  'out_data' not in st.session_state:
        st.session_state['out_data']={}
    if  'test_data' not in st.session_state:
        st.session_state['test_data']=test_data
        st.session_state['test_data']['status_column']="Not started"
        st.session_state['test_data']['status']="Not started"
        #placeholder= st.empty()
    if 'IsLoadedChartTab1' not in st.session_state:
        st.session_state['IsLoadedChartTab1'] = True
    if 'IsLoadedChartTab2' not in st.session_state:
        st.session_state['IsLoadedChartTab2'] = False
    if st.session_state['test_data']["status_column"]=="Completed":
            st.success("Column extraction completed.")
            st.session_state["columns"]=2
            st.session_state['runbutton_enabled'] = True
            st.session_state['col_status']="Completed"
            
    if  st.session_state['test_data']["status_column"]== "failed":
            st.error("Failed to extract columns.")
    if st.session_state['test_data']["status_column"]== "in_progress":
            st.info("Column extraction is still in progress...")
@st.cache_data    
def load_data_from_blob(sas_url):
    #return pd.read_parquet(sas_url)
#    print("------111:")
    #print (sas_url)
    parsed_data = [json.loads(item) for item in sas_url]
    return parsed_data 
    #return pd.read_json(sas_url)
    #return pd.read_csv(sas_url)

@st.cache_data 
def load_data_from_URL(chart,filter,filtered_df,tablanamem,engagementId):
    
    
    #return pd.read_json(GETCHART_ENDPOINT+"?chart="+chart"" );
    return pd.read_json(f"{GETCHART_ENDPOINT}?chart={chart}&firmId={st.session_state["firmId"] }&engagementId={st.session_state["engagementId"] } ")
    #return pd.read_csv(sas_url)

@st.cache_data
def applyfilter( filter, filtered_df):
    print("applyfilter")
    input_data={}
    parameters={}
    parameters["filter"]=filter
    parameters['tablename']= st.session_state['test_data']['unique_file_name']
    if filtered_df!="":
       parameters['filtered_df']=json.dumps(filtered_df)
    
    
    input_data['parameters']= parameters
    print(input_data)
    instance_id = run_notebook( input_data)
    print("applyflter"+str(instance_id) )


def applyGlobalfilter( firmId,engagementId):
    print("applyfilter")
    input_data={}
    input_data["firmId"]=str(firmId)
    input_data["engagementId"]=str(engagementId)
    parameters={}
    #parameters["filter"]=filter
    parameters['tablename']= st.session_state['test_data']['unique_file_name']
    parameters["firmId"]=str(firmId)
    parameters["engagementId"]=str(engagementId)
    
    
    
    input_data['parameters']= parameters
    print(input_data)
    instance_id = run_notebook( input_data)
    print("applyGlobalflter"+str(instance_id) )


@st.cache_data
def load_chart(test_data, filter, polling_interval=2, max_attempts=1120):
    
    input_data={}
    parameters={}
    parameters["filter"]=filter
    parameters['tablename']=test_data['unique_file_name']
    if "filtered_df" in test_data:
        parameters['filtered_df']=test_data['filtered_df']
    
    
    input_data['parameters']= parameters
    
    instance_id = run_notebook( input_data)
    print("load_chart"+str(instance_id) )
    
    
    # #test_data=st.session_state['test_dataChart']
    # print("!!Loading chart "+str(filter))
    # if str(filter) =="none" and 'filtered_df' not in test_data :
        
    #     return st.session_state['out_data']['summary']
    # input_data={}

    # #input_data['DatabricksJobId']=822693125667863 #Chart old
    # input_data['DatabricksJobId']=488644182429847 #Chart 
    # input_data['FileName']=test_data['unique_file_name']
    # input_data['Filter']=filter
    # input_data['Params']= json.dumps(test_data)
    


    # print("Start poll_for_chart1")        
    # instance_id = start_orchestration( input_data)
    # print("Start poll_for_chart"+instance_id )        
    # for _ in range(max_attempts):
    #     time.sleep(polling_interval)
        
    #     status = check_job_status(instance_id,"summary")
    #     #print("poll_for_chart:"+str(status))
    #     print(status)
        
    #     if status["output"] is not None:
    #         print("Chart Complted !")
    #         test_data["status"]="Completed"
    #         outp=json.loads(status['output'])
            
    #         st.session_state["IsLoadedChart"]=False        
    #         return outp

    #     else:
    #         test_data["status"]="in_progress"

    





    # thread = threading.Thread(
    #     target=poll_for_chart,
    #     args=(st.session_state['test_dataChart'],st.session_state['out_data'])                )
    # thread.start()
    # with st.spinner("Waiting for task to complete..."):
    #     while not thread.is_alive():  # Check if the thread is still running
    #         time.sleep(1)  # Adjust the
    #     st.rerun()
    

def DisplayChart():
    print("Display0")
    left_col, right_col = st.columns([20,100])
    st.session_state["IsLoadedChart"]=True
    with left_col:
        with st.expander("Filters", expanded=True):
            
            account_df= fetch_data("accounts_type",1, 1,"",st.session_state["engagementId"])
            
            account_type = st.multiselect("Filter by Account Type", options=account_df["accountType"].unique(), default=None)
            subtype = st.multiselect("Filter by Subtype", options=account_df["accountSubType"].unique(), default=None)

            filtered_df = ""
            if account_type:
                filtered_df = account_df[account_df["accountType"].isin(account_type)]["glAccountNumber"].astype(int).to_list()
                filtered_df =",".join(map(str, filtered_df ))
            if subtype:
                filtered_df = account_df[account_df["accountSubType"].isin(subtype)]["glAccountNumber"].astype(int).to_list()
                filtered_df =",".join(map(str, filtered_df ))

            
            #st.dataframe(filtered_df)
            if st.button("Apply"):
    
                #st.session_state['test_dataChart']={}
                st.session_state["filtered_df"]=filtered_df 
                #st.session_state["filtered_df"]=filtered_df["glAccountNumber"] 
                st.session_state['test_data']["filtered_df"]=filtered_df     
                st.session_state['test_dataChart']["filtered_df"]=filtered_df
                st.session_state['out_data']['summary']=applyfilter(st.session_state.get("filter","none"),st.session_state["filtered_df"])
                
                
        
                
    with right_col:
        print("Display1")
        if( 'summary' in st.session_state['out_data']):
            col1, col2 = st.columns(2)
            with col1:
                createChart4(st.session_state.get("filter","none"),st.session_state["filtered_df"])
                createChart1(st.session_state.get("filter","none"),st.session_state["filtered_df"])
            with col2:
                createChart2(st.session_state.get("filter","none"),st.session_state["filtered_df"])
                createChart3(st.session_state.get("filter","none"),st.session_state["filtered_df"])
            

def createChart1(filter,filtered_df):
    # Load data from the blob
    #chart1url = out_data['summary']['chart1url']
    #st.write(f"Data source URL: {chart1url}")
    #data = load_data_from_blob(chart1url)
    print("Chart1"+str(st.session_state.get("filter","none"))+"!!!"+str(st.session_state["filtered_df"]))
    
    data = load_data_from_URL("chart1",st.session_state.get("filter","none"),st.session_state["filtered_df"],st.session_state['test_data']['unique_file_name'],st.session_state["engagementId"] )
    df = pd.DataFrame(data)





    st.subheader("Visualization 1: High-Risk Journals Per Month")

    # Check if data is valid
    if len(df) > 0 and 'month' in df.columns and 'high_risk_count' in df.columns:
        # Prepare data for JavaScript
        categories = df['month'].tolist()
        data_points = df['high_risk_count'].tolist()

        # JavaScript + HTML for Highcharts
        html_code = f"""
        <div id="container" style="width: 100%; height: 400px;"></div>
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function () {{
                Highcharts.chart('container', {{
                    chart: {{
                        type: 'line'
                    }},
                    title: {{
                        text: 'High-Risk Journals Per Month'
                    }},
                    xAxis: {{
                        categories: {categories}
                    }},
                    yAxis: {{
                        title: {{
                            text: 'Count of High-Risk Journals'
                        }}
                    }},
                    series: [{{
                        name: 'High Risk',
                        data: {data_points}
                    }}]
                }});
            }});
        </script>
        """

        # Render the chart in Streamlit
        st.components.v1.html(html_code, height=600)
    else:
        st.info("Chart is empty or data is invalid.")

def createChart2(filter,filtered_df):
    try:
        # Load data from the blob URL
        #chart2url = out_data['summary']['chart2url']
        #st.write(f"Data source URL: {chart2url}")  # Display the URL for debugging
        #//data = load_data_from_blob(chart2url)  # Ensure this function works correctly
        data = load_data_from_URL("chart2",st.session_state.get("filter","none"),st.session_state["filtered_df"],st.session_state['test_data']['unique_file_name'],st.session_state["engagementId"] )
        risk_per_account_df = pd.DataFrame(data)

        # Validate the DataFrame
        if len(risk_per_account_df) == 0 or 'glAccountNumber' not in risk_per_account_df.columns or 'risk_label' not in risk_per_account_df.columns or 'risk_count' not in risk_per_account_df.columns:
            st.info("The dataset does not contain valid data for the chart.")
            return

        # Ensure 'risk_count' is a numeric type
        risk_per_account_df['risk_count'] = risk_per_account_df['risk_count'].astype(int)

        # Prepare data for JavaScript
        categories = sorted(risk_per_account_df['glAccountNumber'].unique().tolist())
        risks = sorted(risk_per_account_df['risk_label'].unique().tolist())

        # Prepare series for Highcharts
        series = []
        for risk in risks:
            data = []
            for account in categories:
                count = risk_per_account_df[
                    (risk_per_account_df['glAccountNumber'] == account) & 
                    (risk_per_account_df['risk_label'] == risk)
                ]['risk_count'].sum()
                data.append(int(count))
            series.append({'name': risk, 'data': data})

        # Embed JavaScript + HTML into Streamlit
        html_code = f"""
        <div id="container" style="width: 100%; height: 400px;"></div>
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/modules/exporting.js"></script>
        <script src="https://code.highcharts.com/modules/export-data.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function () {{
                Highcharts.chart('container', {{
                    chart: {{
                        type: 'column'
                    }},
                    title: {{
                        text: 'Risk Journals per Account'
                    }},
                    xAxis: {{
                        categories: {categories},
                        title: {{
                            text: 'Accounts'
                        }}
                    }},
                    yAxis: {{
                        min: 0,
                        title: {{
                            text: 'Risk Count',
                            align: 'high'
                        }}
                    }},
                    plotOptions: {{
                        column: {{
                            stacking: 'normal'
                        }}
                    }},
                    series: {series}
                }});
            }});
        </script>
        """

        # Render the HTML/JavaScript in Streamlit
        st.write("### Stacked Column Chart: Risk Journals per Account")
        st.components.v1.html(html_code, height=600)

    except Exception as e:
        st.error(f"An error occurred while creating the chart: {e}")


def createChart3(filter,filtered_df):
    try:
        # Load data from the blob URL
        #chart3url = out_data['summary']['chart3url']
        #st.write(f"Data source URL: {chart3url}")  # Display the URL for debugging
        #//data = load_data_from_blob(chart3url)  # Ensure this function works correctly
        data = load_data_from_URL("chart3",st.session_state.get("filter","none"),st.session_state["filtered_df"],st.session_state['test_data']['unique_file_name'] ,st.session_state["engagementId"])
        df = pd.DataFrame(data)

        # Validate the DataFrame
        if len(df) == 0 or 'risk_label' not in df.columns or 'overall_risk_count' not in df.columns:
            st.info("The dataset does not contain valid data for the chart.")
            return

        # Prepare data for Highcharts
        pie_data = [
            {'name': str(row['risk_label']), 'y': int(row['overall_risk_count'])}
            for _, row in df.iterrows()
        ]

        # Embed JavaScript + HTML into Streamlit
        html_code = f"""
        <div id="container" style="width: 100%; height: 400px;"></div>
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/modules/exporting.js"></script>
        <script src="https://code.highcharts.com/modules/export-data.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function () {{
                Highcharts.chart('container', {{
                    chart: {{
                        type: 'pie'
                    }},
                    title: {{
                        text: 'Overall Number of Low/Medium/High Risk Journals'
                    }},
                    series: [{{
                        name: 'Journals Count',
                        colorByPoint: true,
                        data: {pie_data}
                    }}]
                }});
            }});
        </script>
        """

        # Render the HTML/JavaScript in Streamlit
        st.write("### Risk Distribution Pie Chart")
        st.components.v1.html(html_code, height=500)

    except Exception as e:
        st.error(f"An error occurred while creating the chart: {e}")
def createChart4(filter,filtered_df):
    
    #test_data=st.session_state['test_data']
    
    #chart4url= out_data['summary']['chart4url']
    #chart4url="https://vsstoragelake.blob.core.windows.net/results/csv/sunburn_df/part-00000-tid-976918198008392936-f35bf24a-ff10-4cac-a4c5-f1c217ba3642-738-1-c000.csv?se=2024-12-05T11%3A11%3A58Z&sp=r&sv=2023-11-03&sr=b&sig=axvfW4upFwSMwIxyL1ku%2BOtd1aRMbUjpN3hATkuM9yI%3D"
    # print(chart1url)
    ##data = load_data_from_blob(chart4url)
    
    data = load_data_from_URL("chart4",st.session_state.get("filter","none"),st.session_state["filtered_df"],st.session_state['test_data']['unique_file_name'],st.session_state["engagementId"] )
    df = pd.DataFrame(data)
    #data = build_hierarchy(df)

# Highcharts configuration
    chart_title    ="xx"
# Highcharts configuration
    data = build_hierarchy(df)
    st.write("### General Ledger Account Hierarchy")
    #st.title("General Ledger Account Hierarchy")
    sunburst_html = generate_sunburst_html(data )
    st.components.v1.html(sunburst_html, height=600)

    # Render the chart in Streamlit

    #hct.streamlit_highcharts(options)
def build_hierarchy(df):
    data = []
    id_counter = 0  # To generate unique IDs

    # Create a root node
    data.append({'id': 'root', 'name': 'General Ledger', 'parent': '', 'value': None})

    # Keep track of unique nodes at each level to avoid duplicates
    level1_nodes = {}
    level2_nodes = {}
    level3_nodes = {}

    for _, row in df.iterrows():
        # Level names
        level1_name = str(row['accountType'])
        level2_name = str(row['accountSubType'])
        level3_name = str(row['fsCaption'])
        level4_name = str(row['glAccountName'])
        value = row['total_amount']

        # Level 1
        if level1_name not in level1_nodes:
            level1_id = f"L1_{level1_name}"
            level1_nodes[level1_name] = level1_id
            data.append({'id': level1_id, 'name': level1_name, 'parent': 'root', 'value': None})
        else:
            level1_id = level1_nodes[level1_name]

        # Level 2
        if level2_name not in level2_nodes:
            level2_id = f"L2_{level2_name}"
            level2_nodes[level2_name] = level2_id
            data.append({'id': level2_id, 'name': level2_name, 'parent': level1_id, 'value': None})
        else:
            level2_id = level2_nodes[level2_name]

        # Level 3
        if level3_name not in level3_nodes:
            level3_id = f"L3_{level3_name}"
            level3_nodes[level3_name] = level3_id
            data.append({'id': level3_id, 'name': level3_name, 'parent': level2_id, 'value': None})
        else:
            level3_id = level3_nodes[level3_name]

        # Level 4 (Leaf Node)
        level4_id = f"L4_{level4_name}_{id_counter}"
        id_counter += 1  # Increment ID counter to ensure uniqueness
        data.append({'id': level4_id, 'name': level4_name, 'parent': level3_id, 'value': value})

    return data



    

def generate_sunburst_html(data):
    data_json = json.dumps(data)  # Convert Python data to JSON for JavaScript
    return f"""
    <div id="container" style="height:600px; width:100%;"></div>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/sunburst.js"></script>
    <script>
        const colors = [
            "#4caf50", "#f44336", "#8bc34a", "#cddc39", "#e91e63", "#ffc107",
            "#03a9f4", "#9c27b0", "#ff5722", "#607d8b"
        ];

        let colorIndex = 0;

        // Add colors dynamically without modifying the original data
        const dataWithColors = {data_json}.map(item => {{
            return {{
                ...item,
                color: colors[colorIndex++ % colors.length]
            }};
        }});

        Highcharts.chart('container', {{

            chart: {{
                height: '600'
            }},

            title: {{
                text: 'General Ledger Account Hierarchy'
            }},

      
            series: [{{
                type: 'sunburst',
                data: dataWithColors,
                name: 'Root',
                allowTraversingTree: true,
                borderRadius: 3,
                cursor: 'pointer',
                dataLabels: {{
                    format: '{{point.name}}',
                    filter: {{
                        property: 'innerArcLength',
                        operator: '>',
                        value: 16
                    }}
                }},
                levels: [{{
                    level: 1,
                    levelIsConstant: false,
                    dataLabels: {{
                        filter: {{
                            property: 'outerArcLength',
                            operator: '>',
                            value: 64
                        }}
                    }}
                }}, {{
                    level: 2,
                    colorByPoint: true
                }},
                {{
                    level: 3,
                    colorVariation: {{
                        key: 'brightness',
                        to: -0.5
                    }}
                }}, {{
                    level: 4,
                    colorVariation: {{
                        key: 'brightness',
                        to: 0.5
                    }}
                }}]

            }}],

            tooltip: {{
                headerFormat: '',
                pointFormat: 'The population of <b>{{point.name}}</b> is <b>' +
                    '{{point.value}}</b>'
            }}
        }});
    </script>
    """


def get_risk_class(risk_level):
    if risk_level == "LOW":
        return "low-risk"
    elif risk_level == "MEDIUM":
        return "medium-risk"
    elif risk_level == "HIGH":
        return "high-risk"
    else:
        return "no-risk"

def DisplayCard(test_data):
    
    out_data=st.session_state['out_data']
    print("DisplCard0")

    #chart3url= out_data['summary']['chart3url']
    
    if  "cards_data" not in st.session_state:
        st.session_state["cards_data"]= load_data_from_URL("chart3","",st.session_state['filtered_df'],st.session_state['test_data']['unique_file_name'],st.session_state["engagementId"] )
        #st.session_state["cards_data"]= load_data_from_blob(chart3url)
        
    data =st.session_state["cards_data"]
    df = pd.DataFrame(data)
    table_scorecard=""

    num_cols = 3
    cards_per_row = num_cols

    # Open the main container div
    total_cards = len(df)
    total_rows = math.ceil(total_cards / cards_per_row)

# Create a container div for the cards
    

    # Iterate over the DataFrame in chunks of three
    for row_num in range(total_rows):
        # Create a set of columns for the current row
        cols = st.columns(num_cols)
    
        for col_num in range(num_cols):
            # Calculate the index of the card
            idx = row_num * cards_per_row + col_num
        
            if idx < total_cards:
                row_data = df.iloc[idx]
                with cols[col_num]:
                    # Render the card HTML
                    st.markdown(f"""
                        <div class="card" >
                            <div class="{get_risk_class(row_data['risk_label'])}">
                                <div class="header">{row_data['risk_label']}</div>
                                <div class="meta">Risk Level</div>
                            </div>
                            <div class="kpi">
                                <div class="metric">
                                    <div class="number">{row_data['overall_risk_count']}</div>
                                    <div class="label">Total Journals</div>
                                </div>
                                <div class="metric">
                                    <div class="number">${row_data['sum_amount']:,.2f}</div>
                                    <div class="label">Total Debit Amount </div>
                                </div>
                            </div>
                            <div class="full-width-button">
                                <!-- Streamlit button will be rendered here -->
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                    # Add a button below the card with a unique key
                    if st.button("View", key=f"action_{idx}"):
                        st.session_state.page = 1
                        st.session_state.filter=row_data['risk_label']
                        st.session_state.IsLoadedChart=False
                        st.session_state['out_data']['summary']=applyfilter(st.session_state.get("filter","none"),st.session_state["filtered_df"])
    num_cols = 5
    cards_per_row=5
    col_num=-1
    row_num =-1
    cols = st.columns(num_cols)
    
    for test_key, row_data in test_data.items():
        if("name" not in row_data ):
                continue
        
        col_num+=1
        if col_num>=cards_per_row :
            col_num=0
            row_num +=1
        # Calculate the index of the card
        idx = row_num * cards_per_row + col_num
        
        if idx < total_cards:
            
            with cols[col_num]:
                # Render the card HTML
                st.markdown(f"""
                    <div class="card">
                        <div class="{get_risk_class("d")}">
                            <div class="header">{row_data['name']}</div>
                            <div class="meta">Test name</div>
                        </div>
                        <div class="kpi">
                            <div class="metric">
                                <div class="number">{row_data['count']}</div>
                                <div class="label">Total Journals</div>
                            </div>
                            <div class="metric">
                                <div class="number">${row_data['sumAmount']:,.2f}</div>
                                <div class="label">Total Debit Amount </div>
                            </div>
                        </div>
                        <div class="full-width-button">
                            <!-- Streamlit button will be rendered here -->
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add a button below the card with a unique key
                if st.button("View", key=f"action2_{idx}"):
                    print("Clicked"+str(test_key))
                    st.session_state.page = 1
                    st.session_state.filter=test_key
                    st.session_state.IsLoadedChart=False
                    st.session_state['out_data']['summary']=applyfilter(st.session_state.get("filter","none"),st.session_state["filtered_df"])
                    
def download_data(tablename,filter):
    params = {
        
        'tablename':tablename,
        'filter':filter
        
    }
    with st.spinner("Preparing link for download"):
        response = requests.get(API_URL_DOWNLOAD, params=params)
    if response.status_code == 200:
             st.download_button(
                            label=f"Download CSV file",
                            data=response.content,
                            file_name=f"{tablename}_{filter}.csv",
                            mime="text/csv"
                        )
    else:
        st.error("Error download data")
        return pd.DataFrame()
import copy
def update_test_data(test_data, json_obj):
    
    try:
        # Parse the JSON string from 'result'
        result_data = json.loads(json_obj.get('result', '{}'))
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return test_data

        # Define the fields to update
    fields_to_update = ['status', 'start_time', 'end_time', 'error', 'count', 'sumAmount']
    test_data1=copy.copy(test_data)
    for test_key, test_value in result_data.items():
            if test_key in test_data:
                for field in fields_to_update:
                    if field in test_value:
                        test_data1[test_key][field] = test_value[field]
            else:
                st.warning(f"Test key '{test_key}' not found in test_data.")

            return test_data1

   
    

def on_engagement_change():
    input_data = {
        
        
        "firmId":  str(st.session_state["firmId"]),
        "engagementId":  str(st.session_state["engagementId"]),
        
    }
    print("ENG change"+str(input_data))
    
    res=get_result(input_data)
    
    if  "cards_data" in st.session_state:
        del st.session_state["cards_data"]
    if 'data_array' in res['output']:
        res_test=res['output']['data_array'][0][0]
        json_obj = json.loads(res_test)["result"]
        #data=update_test_data(test_data,json_obj)
        #st.session_state['test_data']=data
        #result = res["result"]
        print("result"+json_obj )
        #display_tableTests()
        st.session_state['out_data']['summary']="emg"
        
        update_tests(test_data,json.loads(json_obj))
        st.session_state['test_data']=test_data
        st.session_state['test_data']['status_column']="Completed"
        st.session_state['test_data']['status']="Completed"
        st.session_state['test_data']['unique_file_name']="None"
    else:
        print("")
        if 'summary' in st.session_state['out_data']:
            del st.session_state['out_data']['summary']
        if 'unique_file_name' in st.session_state['test_data']:
            del st.session_state['test_data']['unique_file_name']
        for test_key, test_info in test_data.items():
            test_info['status'] = "Not started"      # Update status to "Nine"
            test_info['count'] = 0            # Reset count to 0
            test_info['sumAmount'] = 0 
            
        st.session_state['test_data']=test_data
        st.session_state['test_data']['status_column']="Not started"
        st.session_state['test_data']['status']="Not started"
        print(test_data)


def main():

    # Page Configuration
    st.set_page_config(page_title="General Ledger testing ", layout="wide")
    local_css("style.css")   
#     st.components.v1.html(
#     """
#     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-grid.css">
#     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-theme-alpine.css">
#     """,
#     height=0,  # No visible height
#     width=0    # No visible width
# )
    st.markdown("<img src='https://cdn.wolterskluwer.io/wk/fundamentals/1.15.2/logo/assets/medium.svg' alt='Wolters Kluwer Logo' width='190px' height='31px'>", unsafe_allow_html=True)
    st.title("General Ledger testing v"+version)
    init()
    

    
    df = pd.DataFrame(data)


    col1, col2,col3 = st.columns([1, 1, 1])
    with col1:
        # 1) Create a selectbox to choose the customer by customer_name
        customers = df["customer_name"].tolist()
        selected_customer_name = st.selectbox("Select a Customer", customers)

        # 2) Find the selected customer's row in the DataFrame
        selected_customer = df[df["customer_name"] == selected_customer_name].iloc[0]

        # Extract details of the selected customer
        st.session_state["firmId"] = selected_customer["firmId"]
        st.session_state["selected_engagements"] = selected_customer["engagements"]
    
    with col2:

        engagement_names = [eng["engagement_name"] for eng in st.session_state["selected_engagements"]]
        selected_engagement_name = st.selectbox(
            "Select an Engagement",
            engagement_names,
            key='selected_engagement_name',
        
        )
        
        selected = st.session_state.selected_engagement_name
        selected_engagement_details = next(
            eng for eng in st.session_state["selected_engagements"] if eng["engagement_name"] == selected 
        )
        st.session_state["engagementId"] = selected_engagement_details["engagementId"]
        #st.session_state["selected_engagements"]=selected_engagement_name
    with col3:
         st.markdown("<br>", unsafe_allow_html=True) 
         load_clicked = st.button('Load '+selected_engagement_name, use_container_width=True)
         if load_clicked:

                on_engagement_change()
                #st.session_state['out_data']['summary']=applyfilter(st.session_state.get("firmId","1"),st.session_state["engagementId"])
                st.session_state['out_data']['summary']=applyGlobalfilter(st.session_state["firmId"] ,st.session_state["engagementId"])
                
    
    
    

   
    
    
    #selected_engagements = selected_customer["engagements"]
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader(f"#STEP2: Choose General Ledger file", type=['zip', 'csv'] ,key="x2" )
    with col2:
        uploaded_file_CA= st.file_uploader("#STEP1:Choose Charts of Account file", type=[ 'csv'],key="x1" )
    col1, col2,col3 = st.columns([1, 1,1])
    with col1:
        exccel_clicked = st.button('CSV file', disabled=not st.session_state['runbutton_enabled'],use_container_width=True)
#    with col2:
        
    with col3:
        runbutton_clicked = st.button('Run tests', disabled=not st.session_state['runbutton_enabled'],use_container_width=True)
    

    if runbutton_clicked:
        
        thread = threading.Thread(
                target=poll_for_task,
                args=(st.session_state['test_data'],st.session_state['out_data'], st.session_state["firmId"] ,st.session_state["engagementId"])                )
        thread.start()
        with st.spinner("Waiting for task to complete..."):
            while thread.is_alive():  
                time.sleep(1)  
        thread=None
    
    
    if uploaded_file_CA:
            if 'fileUploadedCA' not in st.session_state:
                with st.spinner("Uploading file..."):
                    #unique_file_name = f"{uuid.uuid4()}{original_file_name}"
                    original_file_name = uploaded_file_CA.name
                    unique_file_name = f"ca{original_file_name}"
                    
                    supload_urlCA = upload_file_to_blob( uploaded_file_CA,unique_file_name)
                    st.session_state['test_data']['unique_file_nameCA']=unique_file_name
                    
                    st.session_state['fileUploadedCA']=True


    if uploaded_file:
        if 'columns' not in st.session_state:
            original_file_name = uploaded_file.name
            
            
            if 'fileUploaded' not in st.session_state:
                with st.spinner("Uploading file..."):
                    #unique_file_name = f"{uuid.uuid4()}{original_file_name}"
                    unique_file_name = f"poc{original_file_name}"
                    st.session_state['test_data']['unique_file_name']=unique_file_name
                    st.session_state['test_dataChart']['unique_file_name']=st.session_state['test_data']['unique_file_name']
                    st.session_state['test_dataChart']['unique_file_nameCA']=st.session_state['test_data']['unique_file_nameCA']
                    supload_url = upload_file_to_blob( uploaded_file,unique_file_name)
                    st.session_state['fileUploaded']=True
                    
    
        
        if 'col_status' not in st.session_state :
            
            st.session_state['col_status']="in progress"
            st.session_state['test_data']['status_column']="in progess"
            st.session_state['threadUpload']= threading.Thread(target=poll_for_columns,args=(st.session_state['test_data'],st.session_state["firmId"] ,st.session_state["engagementId"])                )       
            st.session_state['threadUpload'].start()
            
            
            
        
        if(st.session_state['test_data']['status_column']=="Completed"):
            st.session_state['runbutton_enabled']=True
        if(st.session_state['test_data']['status_column']=="in progess"):
            st.info("CSV extraction is running in the background. You can continue using the UI.")
        if(st.session_state['test_data']['status_column']=="Failed"):
            st.error("Isssue in uploading")

    if exccel_clicked:
         tablename=st.session_state['test_data']['unique_file_name'] 
         download_data(tablename,st.session_state.get("filter","none"))   

    
        
    st.subheader("Select Tests to Run")
       
    
    display_tableTests()
        
    if 'summary' in st.session_state['out_data']:   
        print("Try to DisplayCard")
        DisplayCard(st.session_state['test_data']) 
    st.markdown(f"### {st.session_state.get('filter','')}")
    tab1, tab2 ,tab3,tab4,tab5,tab6= st.tabs(["📈 Chart", "🗃 Tables","📊 Pivot table","📉 Pivot cross chart","🔌 Power BI","🧮 Dashboard"])
    print("IsLoadedChart: "+str(st.session_state.IsLoadedChart)+str(st.session_state['IsLoadedChartTab1']))
    
    with tab1:
        st.session_state['active_tab'] = 1 
        #print("ssss"+st.session_state.IsLoadedChart)
        #if  st.session_state.IsLoadedChart==False:
        print("try to load chart")
        
        if( 'summary' in st.session_state['out_data']):
            print("try to load chart1"+str(st.session_state.get("filter","None")))
            #st.session_state['out_data']['summary']=load_chart(st.session_state['test_dataChart'],st.session_state.get("filter","none")) 

        if(st.session_state['out_data']):
            print("Chart try1 ")
            
            DisplayChart()
        st.session_state['IsLoadedChartTab1'] = True
                    
    with tab2:
        print("tab2")
        
        if 'summary' in st.session_state['out_data']:
            main2(st.session_state['test_data'],st.session_state['out_data'])
        st.session_state['IsLoadedChartTab2'] = True   
    with tab3:
        print("tab3")
        #st.session_state['test_data']['unique_file_name']="pocglcsv"
        #mainPivot(st.session_state['test_data'],"")
        
        if 'summary' in st.session_state['out_data']:
            mainPivot(st.session_state['test_data'],st.session_state['out_data'])
        # st.session_state['IsLoadedChartTab2'] = True   
    with tab4:
        print("tab4")
    #    st.session_state['test_data']['unique_file_name']="pocglcsv"
     #   mainPivotChart(st.session_state['test_data'],"")
        
        if 'summary' in st.session_state['out_data']:
            mainPivotChart(st.session_state['test_data'],st.session_state['out_data'])
        # st.session_state['IsLoadedChartTab2'] = True   
    with tab5:
        print("tab5")
       # st.session_state['test_data']['unique_file_name']="pocglcsv"
       # mainPowerBI(st.session_state['test_data'],"")
        if 'summary' in st.session_state['out_data']:
           new_page_url = "https://app.powerbi.com/reportEmbed?reportId=861832a8-e09f-4e27-a693-f014d5701b74&autoAuth=true&ctid=8ac76c91-e7f1-41ff-a89c-3553b2da2c17"
           st.markdown(f'<a href="{new_page_url}" target="_blank">Open Power BI</a>', unsafe_allow_html=True)

            #mainPowerBI(st.session_state['test_data'],st.session_state['out_data'])
        # st.session_state['IsLoadedChartTab2'] = True   
    with tab6:
        #st.session_state['test_data']['unique_file_name']="pocglcsv"
        #mainDashboard(st.session_state['test_data'],"")
       
        if 'summary' in st.session_state['out_data']:
            mainDashboard(st.session_state['test_data'],st.session_state['out_data'])
        

    if st.button("."):
        print(st.session_state['test_data'])
        
    if 'threadUpload'  in st.session_state:
        if st.session_state['threadUpload'].is_alive():  # Check if the thread is still running
            print("Thread uploading")
            time.sleep(1)  # Adjust the
            st.rerun() 
                                    



if __name__ == "__main__":

    main()
    #create_chart()
        
