import { useState } from "react";
import axios from "axios";

export default function QueryForm({ onResponse, setLoading }) {
  const [question, setQuestion] = useState("");
  const [chartType, setChartType] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading?.(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", {
        question,
        chart_type: chartType || null,
      }, {
        headers: { "Content-Type": "application/json" }
      });
      onResponse(res.data);
    } catch (err) {
      console.error("❌ API Error:", err);
      alert("Error: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading?.(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white shadow rounded p-4">
      <textarea
        className="border p-2 w-full rounded focus:outline-blue-400"
        rows={3}
        placeholder="Ask your SQL question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        required
      />
      <div>
        <label className="mr-2 font-medium">Chart type:</label>
        <select
          className="border p-2 rounded"
          value={chartType}
          onChange={(e) => setChartType(e.target.value)}
        >
          <option value="">None</option>
          <option value="bar">Bar</option>
          <option value="pie">Pie</option>
          <option value="line">Line</option>
        </select>
      </div>
      <button
        type="submit"
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition"
      >
        Ask
      </button>
    </form>
  );
}