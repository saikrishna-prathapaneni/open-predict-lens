import type { AnalysisResult, Market } from "@/types/market";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:9000";

export async function fetchMarkets(limit = 100): Promise<Market[]> {
  const res = await fetch(`${BASE_URL}/markets?limit=${limit}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch markets: ${res.status}`);
  }
  const data = await res.json();
  return data.markets ?? [];
}

export async function analyzeMarket(ticker: string): Promise<AnalysisResult> {
  const res = await fetch(
    `${BASE_URL}/analyze/${encodeURIComponent(ticker)}`
  );
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Request failed (${res.status}): ${errorText}`);
  }
  return res.json();
}
