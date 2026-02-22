'use client';
import { useEffect, useState } from "react";

import AnalyzePanel from "@/components/AnalyzePanel";
import MarketList from "@/components/MarketList";
import { analyzeMarket, fetchMarkets } from "@/lib/api";
import type { AnalysisResult, Market } from "@/types/market";

export default function Home() {
  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [analyzeLoading, setAnalyzeLoading] = useState(false);
  const [analyzeError, setAnalyzeError] = useState<string | null>(null);

  const [markets, setMarkets] = useState<Market[]>([]);
  const [marketsLoading, setMarketsLoading] = useState(true);

  useEffect(() => {
    setMarketsLoading(true);
    fetchMarkets()
      .then(setMarkets)
      .catch((err) => console.error(err))
      .finally(() => setMarketsLoading(false));
  }, []);

  const handleAnalyze = async () => {
    if (!ticker.trim()) return;
    setAnalyzeLoading(true);
    setAnalyzeError(null);
    setResult(null);
    try {
      const data = await analyzeMarket(ticker);
      setResult(data);
    } catch (err: any) {
      setAnalyzeError(err.message);
    } finally {
      setAnalyzeLoading(false);
    }
  };

  return (
    <main className="max-w-6xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Kalshi Trading Dashboard</h1>

      <AnalyzePanel
        ticker={ticker}
        result={result}
        loading={analyzeLoading}
        error={analyzeError}
        onTickerChange={setTicker}
        onAnalyze={handleAnalyze}
      />

      <section>
        <h2 className="text-xl font-bold mb-4">Available Markets</h2>
        <MarketList
          markets={markets}
          loading={marketsLoading}
          onSelect={(t) => {
            setTicker(t);
            window.scrollTo({ top: 0, behavior: "smooth" });
          }}
        />
      </section>
    </main>
  );
}
