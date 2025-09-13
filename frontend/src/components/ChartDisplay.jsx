import {
  BarChart, Bar, PieChart, Pie, LineChart, Line,
  XAxis, YAxis, Tooltip, Legend, CartesianGrid, Cell
} from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8"];

export default function ChartDisplay({ chart }) {
  if (!chart || chart.error) return <p className="text-gray-500 italic">No chart data available.</p>;

  const data = chart.labels.map((label, i) => ({
    name: label,
    value: chart.values[i],
  }));

  if (chart.type === "bar") {
    return (
      <BarChart width={500} height={300} data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <CartesianGrid strokeDasharray="3 3" />
        <Bar dataKey="value" fill="#8884d8" />
      </BarChart>
    );
  }

  if (chart.type === "pie") {
    return (
      <PieChart width={400} height={300}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={100}
          label
        >
          {data.map((_, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    );
  }

  if (chart.type === "line") {
    return (
      <LineChart width={500} height={300} data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <CartesianGrid strokeDasharray="3 3" />
        <Line type="monotone" dataKey="value" stroke="#82ca9d" />
      </LineChart>
    );
  }

  return <p>Unsupported chart type: {chart.type}</p>;
}
