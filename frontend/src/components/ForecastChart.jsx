import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from "recharts";

export default function ForecastChart({ history, forecast }) {
  const historyPoints = Object.entries(history || {}).map(([date, value]) => ({ date, history: value, forecast: null }));
  const forecastPoints = Object.entries(forecast || {}).map(([date, value]) => ({ date, history: null, forecast: value }));
  const data = [...historyPoints, ...forecastPoints].sort((a, b) => new Date(a.date) - new Date(b.date));
  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="history" stroke="#8884d8" dot={false} name="History" />
        <Line type="monotone" dataKey="forecast" stroke="#82ca9d" strokeDasharray="6 4" dot={{ stroke: "#82ca9d", strokeWidth: 2 }} name="Forecast" />
      </LineChart>
    </ResponsiveContainer>
  );
}