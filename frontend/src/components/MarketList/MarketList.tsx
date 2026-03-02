import type { Market } from "@/types/market";
import MarketCard from "../MarketCard/MarketCard";
import styles from "./MarketList.module.scss";

interface Props {
  markets: Market[];
  loading: boolean;
  onSelect?: (ticker: string) => void;
}

export default function MarketList({ markets, loading, onSelect }: Props) {
  if (loading) {
    return (
      <div className={styles.loading}>
        Loading markets…
      </div>
    );
  }

  if (markets.length === 0) {
    return (
      <div className={styles.emptyState}>
        No markets match your criteria.
      </div>
    );
  }

  return (
    <div className={styles.grid}>
      {markets.map((m) => (
        <MarketCard key={m.ticker} market={m} onSelect={onSelect} />
      ))}
    </div>
  );
}
