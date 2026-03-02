import type { Market } from "@/types/market";
import { BarChart, Calendar, TrendingUp } from "lucide-react";
import styles from "./MarketCard.module.scss";

interface Props {
  market: Market;
  onSelect?: (ticker: string) => void;
}

export default function MarketCard({ market, onSelect }: Props) {
  // Format volume if available
  const formattedVolume = market.volume 
    ? new Intl.NumberFormat('en-US', {
        notation: "compact",
        compactDisplay: "short",
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 1
      }).format(market.volume)
    : "$0";

  const closeDate = market.close_time 
    ? new Date(market.close_time).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    : "TBD";

  const platformClass = market.platform === "Kalshi" ? styles.kalshi : styles.polymarket;
  const isBearish = market.ai_outlook?.includes("Bearish");
  const insightClass = isBearish ? styles.bearish : market.ai_outlook?.includes("Bullish") ? styles.bullish : styles.neutral;
  const scoreClass = (market.score || 0) > 70 ? styles.high : (market.score || 0) > 40 ? styles.med : styles.low;

  return (
    <div className={styles.card} onClick={() => onSelect?.(market.ticker)}>
      {/* Top Header Row */}
      <div className={styles.headerRow}>
        <div className={styles.badges}>
          <span className={`${styles.platformBadge} ${platformClass}`}>
            {market.platform || "Unknown"}
          </span>
          <span className={styles.categoryBadge}>
            {market.category || "General"}
          </span>
        </div>
        
        {/* Score Ring */}
        <div className={styles.scoreContainer}>
          <div className={styles.ringWrapper}>
              <svg className={styles.svg}>
                  <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="3" fill="transparent" className={styles.bgCircle} />
                  <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="3" fill="transparent"
                    strokeDasharray={20 * 2 * Math.PI}
                    strokeDashoffset={20 * 2 * Math.PI - ((market.score || 0) / 100) * 20 * 2 * Math.PI}
                    className={`${styles.progressCircle} ${scoreClass}`} 
                  />
              </svg>
              <div className={styles.scoreValue}>
                <span>{market.score || 0}</span>
              </div>
          </div>
          <span className={styles.scoreLabel}>SCORE</span>
        </div>
      </div>
      
      <h3 className={styles.title}>
        {market.title}
      </h3>

      <div className={styles.detailsRow}>
         <div className={styles.detailItem}>
           <BarChart className={styles.icon} />
           <span><span className={styles.value}>{formattedVolume}</span> Vol</span>
         </div>
         <div className={styles.detailItem}>
           <Calendar className={styles.icon} />
           <span><span className={styles.value}>{closeDate}</span> Ends</span>
         </div>
      </div>

      <div className={`${styles.insightBox} ${insightClass}`}>
        <div className={styles.insightHeader}>
          <TrendingUp className={`${styles.icon} ${isBearish ? styles.bearish : styles.bullish}`} />
          {market.ai_outlook || "AI Insight"}
        </div>
        <p className={styles.insightText}>
          {market.ai_description || "Analyzing market conditions..."}
        </p>
      </div>

      <div className={styles.footer}>
        <div className={styles.confidenceRow}>
          <span>AI Confidence</span>
          <span>{market.ai_confidence || 0}%</span>
        </div>
        <div className={styles.progressBarWrapper}>
          <div 
            className={styles.progressBarFill} 
            style={{ width: `${market.ai_confidence || 0}%` }}
          ></div>
        </div>
      </div>

    </div>
  );
}