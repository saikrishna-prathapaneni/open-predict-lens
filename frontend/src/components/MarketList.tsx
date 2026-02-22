import type { Market } from "@/types/market";
import MarketCard from "./MarketCard";

interface Props {
  markets: Market[];
  loading: boolean;
  onSelect: (ticker: string) => void;
}

export default function MarketList({ markets, loading, onSelect }: Props) {
  if (loading) {
    return <p className="text-gray-500">Loading markets…</p>;
  }

  if (markets.length === 0) {
    return <p className="text-gray-500">No markets available.</p>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {markets.map((m) => (
        <MarketCard key={m.ticker} market={m} onSelect={onSelect} />
      ))}
    </div>
  );
}
