import { useState, useEffect } from "react";
import { X, Cpu, TrendingUp, AlertTriangle } from "lucide-react";
import type { Market } from "@/types/market";
import styles from "./AnalyzePanel.module.scss";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  selectedTicker: string | null;
}

export default function AnalyzePanel({ isOpen, onClose, selectedTicker }: Props) {
  const [market, setMarket] = useState<Market | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isOpen || !selectedTicker) return;

    const fetchMarket = async () => {
      setLoading(true);
      try {
        const res = await fetch(`http://localhost:9000/api/v1/markets/${selectedTicker}`);
        if (!res.ok) throw new Error("Failed to fetch market details");
        const data = await res.json();
        setMarket(data.market);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMarket();
  }, [isOpen, selectedTicker]);

  if (!isOpen) return null;

  const isBearish = market?.ai_outlook?.includes("Bearish");
  const isNeutral = !isBearish && !market?.ai_outlook?.includes("Bullish");
  const aiBoxClass = isBearish ? styles.bearish : isNeutral ? styles.neutral : styles.bullish;

  return (
    <div className={styles.overlay}>
      <div className={styles.panel}>
        
        {/* Header */}
        <div className={styles.header}>
          <div className={styles.titleGroup}>
            <h2><Cpu className={styles.icon} /> Prediction Lens</h2>
            <p>AI Deep Dive</p>
          </div>
          <button onClick={onClose} className={styles.closeButton}>
            <X className={styles.icon} />
          </button>
        </div>

        {/* Content */}
        <div className={styles.content}>
          {loading ? (
            <div className={styles.loadingState}>
              <div className={styles.spinnerWrapper}>
                <svg className={styles.spinner} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 4V2M12 22v-2M4 12H2m20 0h-2m-2.05-6.95l1.414-1.414M4.636 19.364l1.414-1.414m12.728 0l-1.414-1.414M4.636 4.636l1.414 1.414" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <p>Synthesizing insights for {selectedTicker}...</p>
            </div>
          ) : market ? (
             <div className={styles.section}>
              <h3>Market Context</h3>
              <div className={styles.detailBox}>
                <div className={styles.marketTitle}>{market.title}</div>
                <div className={styles.badges}>
                  <span className={`${styles.badge} ${styles.platform}`}>{market.platform}</span>
                  <span className={`${styles.badge} ${styles.category}`}>{market.category}</span>
                </div>
              </div>

              <h3>Lens AI Analysis</h3>
              <div className={`${styles.aiBox} ${aiBoxClass}`}>
                <div className={styles.aiHeader}>
                  {isBearish ? <AlertTriangle className={styles.icon} /> : <TrendingUp className={styles.icon} />}
                  {market.ai_outlook || "Pending Outlook"}
                </div>
                <p className={styles.aiDescription}>
                  {market.ai_description || "No detailed AI analysis available for this market yet. The oracle is currently analyzing incoming order flows and world events."}
                </p>

                <div className={styles.metricsGrid}>
                  <div className={styles.metric}>
                     <span className={styles.label}>AI CONFIDENCE</span>
                     <span className={styles.value}>{market.ai_confidence || 0}%</span>
                  </div>
                  <div className={styles.metric}>
                     <span className={styles.label}>OPPORTUNITY SCORE</span>
                     <span className={styles.value}>{market.score || 0}/100</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className={styles.loadingState}>
              <p>Failed to load market data.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

