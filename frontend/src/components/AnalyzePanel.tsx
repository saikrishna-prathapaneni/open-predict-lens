import type { AnalysisResult } from "@/types/market";

interface Props {
  ticker: string;
  result: AnalysisResult | null;
  loading: boolean;
  error: string | null;
  onTickerChange: (value: string) => void;
  onAnalyze: () => void;
}

export default function AnalyzePanel({
  ticker,
  result,
  loading,
  error,
  onTickerChange,
  onAnalyze,
}: Props) {
  return (
    <section className="mb-10">
      <h2 className="text-xl font-bold mb-4">Analyze Market</h2>
      <div className="flex gap-2">
        <input
          className="border p-2 rounded text-black flex-1"
          value={ticker}
          onChange={(e) => onTickerChange(e.target.value)}
          placeholder="Enter or select a ticker below"
        />
        <button
          onClick={onAnalyze}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Analyzing…" : "Analyze"}
        </button>
      </div>

      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-gray-50 border rounded space-y-2">
          <p className="text-sm">
            <span className="font-semibold">Ticker:</span> {result.ticker}
          </p>
          <p className="text-sm">
            <span className="font-semibold">Market probability:</span>{" "}
            {result.market_probability ?? "N/A"}
          </p>
          <p className="text-sm">
            <span className="font-semibold">LLM insight:</span>{" "}
            {result.llm_insight}
          </p>
        </div>
      )}
    </section>
  );
}
