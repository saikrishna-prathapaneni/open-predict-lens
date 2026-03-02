export interface Market {
  ticker: string;
  title: string;
  status: string;
  platform: 'Kalshi' | 'Polymarket';
  category: string;
  score: number;
  ai_confidence: number;
  ai_outlook: string;
  ai_description: string;
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
