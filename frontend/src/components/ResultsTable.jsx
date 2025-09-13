export default function ResultsTable({ data }) {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return <p className="text-gray-500 italic">No data to display.</p>;
  }
  const columns = Object.keys(data[0]);
  const formatValue = (value) =>
    typeof value === 'number'
      ? value > 1000
        ? value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
        : value.toString()
      : value;
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-300 rounded-lg shadow-sm">
        <thead>
          <tr className="bg-gray-50 border-b">
            {columns.map((column) => (
              <th key={column} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{column}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {data.map((row, index) => (
            <tr key={index} className="hover:bg-gray-50">
              {columns.map((column) => (
                <td key={column} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{formatValue(row[column])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}