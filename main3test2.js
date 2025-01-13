// main.js

document.addEventListener('DOMContentLoaded', initializeGrid);

const CONFIG = {
    API_URL: 'http://localhost:7190/api/GetPaginatedData',
    API_SUB_URL: 'http://localhost:7190/api/GetSubtableData',
    TABLE_NAME: 'pocGLcsv',
    API_PIVOT_URL: 'http://localhost:7190/api/RunSQL',
    API_PIVOTCHART_URL: 'http://localhost:7190/api/getchart',
    PAGE_SIZE: 20, // Number of rows per page
    GRID_CONTAINER_ID: '#myPivotChartGrid',
    CHART_CONTAINER_ID: '#columnChart',
};

// Grid API references
let gridPivotChartApi = null;
let gridPivotChartColumnApi = null;

/**
 * Initializes the ag-Grid with the specified configurations.
 */
function initializeGrid() {
    const gridOptions = getGridOptions();
    const gridDiv = document.querySelector(CONFIG.GRID_CONTAINER_ID);
    agGrid.createGrid(gridDiv, gridOptions);
}

/**
 * Returns the grid options configuration for ag-Grid.
 */
function getGridOptions() {
    return {
        columnDefs: getColumnDefs(),
        defaultColDef: getDefaultColDef(),
        rowModelType: "serverSide", // Using server-side row model
        serverSideStoreType: 'partial', // 'partial' for infinite scrolling, 'full' for entire data
        pagination: true,
        paginationPageSize: CONFIG.PAGE_SIZE,
        maxConcurrentDatasourceRequests: 1,
        maxBlocksInCache: 2,
        pivotMode: false,
        purgeClosedRowNodes: true,
        enableCharts: true,
        enableRangeSelection: true,
        chartThemes: ['ag-default', 'ag-pastel', 'ag-material', 'ag-vivid'],
        onFirstDataRendered: onFirstDataRendered,
        onGridReady: onGridReady,
        // Additional configurations can be added here
    };
}

/**
 * Defines the column configurations for the grid.
 */
function getColumnDefs() {
    return [
        { 
            field: "glAccountNumber", 
            chartDataType: "category",
            sortable: true,
            filter: "agTextColumnFilter",
            editable: false, // Making column non-editable
        },
        { 
            field: "risk_label", 
            chartDataType: "category",
            sortable: true,
            filter: "agTextColumnFilter",
            editable: false, // Making column non-editable
        },
        {
            field: "risk_count",
            maxWidth: 160,
            aggFunc: "sum",
            filter: "agNumberColumnFilter",
            chartDataType: "series",
            sortable: true,
            editable: true, // This column remains editable
        },
        {
            field: "month",
            maxWidth: 160,
            filter: "agSetColumnFilter",
            chartDataType: "category",
            sortable: true,
            editable: false, // Making column non-editable
        },
    ];
}

/**
 * Defines the default column definitions.
 */
function getDefaultColDef() {
    return {
        flex: 1,
        editable: true,
        filter: "agMultiColumnFilter",
        floatingFilter: true,
        sortable: true, // Enable sorting by default
    };
}

/**
 * Callback when the grid is ready.
 * Sets up the server-side datasource.
 */
function onGridReady(params) {
    gridPivotChartApi = params.api;
    gridPivotChartColumnApi = params.columnApi;

    // Create server-side datasource
    const datasource = createPivotServerSideDatasource(CONFIG.API_PIVOTCHART_URL, CONFIG.TABLE_NAME);
    params.api.setGridOption("serverSideDatasource",datasource);
}

/**
 * Callback when the first data is rendered.
 * Initializes the chart.
 */
function onFirstDataRendered(params) {
    createQuarterlySalesChart(params.api);
    // You can uncomment and implement additional charts as needed
    // createSalesByRefChart(params.api);
    // createHandsetSalesChart(params.api);
}

/**
 * Creates a column chart based on the grid data.
 * @param {GridApi} api - The ag-Grid API instance.
 */
function createQuarterlySalesChart(api) {
    api.createCrossFilterChart({
        chartType: "column",
        cellRange: {
            columns: ["risk_count"],
        },
        aggFunc: "sum",
        chartContainer: document.querySelector("#columnChart"),
        // Additional chart options can be added here
    });
}

/**
 * Creates the server-side datasource for the grid.
 * @param {string} apiUrl - The API URL to fetch data.
 * @param {string} tableName - The table name for data fetching.
 */
function createPivotServerSideDatasource(apiUrl, tableName) {
    return {
        getRows: async function (params) {
            console.log('[Datasource] - rows requested by grid:', params.request);

            try {
                // Construct payload based on the request
                const payload = {
                    tableName: tableName,
                    requestModel: params.request,
                };

                const fetchOptions = {
                    method: 'GET', // Use POST to send request body
                    headers: {
                        'Content-Type': 'application/json',
                        // Add other headers if necessary, e.g., Authorization
                    },
//                    body: JSON.stringify(payload),
                };
		                    const url = `${apiUrl}?chart=chart5`;
                const response = await fetch(url, fetchOptions);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const result = await response.json();
                console.log('Fetched Data:', result);

                // Assuming the API returns { data: [...], total: number }
                // Adjust based on your API response
                    params.success({ rowData: result, rowCount: result.length });
            } catch (error) {
                console.error('Error fetching data:', error);
                params.failCallback();
            }
        },
    };
}

/**
 * (Optional) Creates additional charts based on grid data.
 * Implement similar to createQuarterlySalesChart as needed.
 */
/*
function createSalesByRefChart(api) {
    api.createCrossFilterChart({
        chartType: "bar",
        cellRange: {
            columns: ["salesByRef"],
        },
        aggFunc: "sum",
        chartContainer: document.querySelector("#salesByRefChart"),
    });
}

function createHandsetSalesChart(api) {
    api.createCrossFilterChart({
        chartType: "pie",
        cellRange: {
            columns: ["handsetSales"],
        },
        aggFunc: "sum",
        chartContainer: document.querySelector("#handsetSalesChart"),
    });
}
*/
