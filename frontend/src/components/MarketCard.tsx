import type { Market } from "@/types/market";

interface Props {
  market: Market;
  onSelect: (ticker: string) => void;
}

export default function MarketCard({ market, onSelect }: Props) {
  return (
    <div className="border p-4 rounded shadow-sm hover:shadow-md transition-shadow flex flex-col gap-1">
      <h3 className="font-semibold text-base leading-snug">{market.title}</h3>
      <p className="text-xs text-gray-500 font-mono break-all">{market.ticker}</p>
      <p className="text-sm">
        Status:{" "}
        <span
          className={`capitalize font-medium ${
            market.status === "active" ? "text-green-600" : "text-red-500"
          }`}
        >
          {market.status}
        </span>
      </p>
      {market.last_price_dollars && (
        <p className="text-sm text-gray-700">
          Last price: <span className="font-medium">${market.last_price_dollars}</span>
        </p>
      )}
      <button
        onClick={() => onSelect(market.ticker)}
        className="mt-auto pt-2 text-blue-500 hover:underline text-sm text-left"
      >
        Select for analysis →
      </button>
    </div>
  );
}
