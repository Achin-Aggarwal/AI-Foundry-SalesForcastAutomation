import './App.css';
import { useState } from "react";
import QueryForm from "./components/QueryForm";
import ChartDisplay from "./components/ChartDisplay";
import ForecastChart from "./components/ForecastChart";
import ResultsTable from "./components/ResultsTable";

export default function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="p-6 max-w-6xl mx-auto bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-blue-700">Northwind SQL Assistant</h1>
      <QueryForm onResponse={setResponse} setLoading={setLoading} />
      {loading && (
        <div className="mt-6 text-center">
          <div className="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-blue-600 bg-white">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading...
          </div>
        </div>
      )}
      {response && !loading && (
        <div className="mt-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">Results</h2>
          {response.insights && (
            <div className="mb-4 p-4 bg-blue-50 border-l-4 border-blue-400 rounded">
              <h3 className="font-semibold text-blue-800 mb-1">Insights</h3>
              <p className="text-blue-700">{response.insights}</p>
            </div>
          )}
          {response.forecast ? (
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold mb-4 text-green-700">Sales Forecast</h3>
              <div className="mb-6">
                <ForecastChart history={response.forecast.history} forecast={response.forecast.forecast} />
              </div>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-2 text-gray-700">Historical Data (Last 2 years)</h4>
                  <div className="bg-gray-50 p-3 rounded max-h-64 overflow-y-auto">
                    <pre className="text-sm">{JSON.stringify(response.forecast.history, null, 2)}</pre>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold mb-2 text-gray-700">
                    Forecast (Next {response.periods || Object.keys(response.forecast.forecast).length} months)
                  </h4>
                  <div className="bg-green-50 p-3 rounded max-h-64 overflow-y-auto">
                    <pre className="text-sm">{JSON.stringify(response.forecast.forecast, null, 2)}</pre>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow">
              <div className="p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-700">Query Results</h3>
                {response.error ? (
                  <div className="p-4 bg-red-50 border border-red-200 rounded text-red-700">
                    <strong>Error:</strong> {response.error}
                  </div>
                ) : (
                  <ResultsTable data={response.result} />
                )}
              </div>
              {response.chart && !response.error && (
                <div className="border-t p-6">
                  <h3 className="text-lg font-semibold mb-4 text-gray-700">Visualization</h3>
                  <ChartDisplay chart={response.chart} />
                </div>
              )}
            </div>
          )}
          {response.adjusted_sql && (
            <div className="mt-4 bg-white rounded-lg shadow">
              <details>
                <summary className="p-4 cursor-pointer font-medium text-gray-700 hover:bg-gray-50">
                  View SQL Query Details
                </summary>
                <div className="p-4 border-t">
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-semibold text-sm text-gray-600 mb-1">Generated SQL:</h4>
                      <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">{response.adjusted_sql}</pre>
                    </div>
                  </div>
                </div>
              </details>
            </div>
          )}
        </div>
      )}
    </div>
  );
}