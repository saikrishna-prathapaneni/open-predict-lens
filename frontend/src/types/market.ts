export interface Market {
  ticker: string;
  title: string;
  status: string;
  yes_bid_dollars?: string;
  last_price_dollars?: string;
  event_ticker?: string;
  close_time?: string;
  volume?: number;
}

export interface AnalysisResult {
  ticker: string;
  market_probability: string | null;
  llm_insight: string;
}
