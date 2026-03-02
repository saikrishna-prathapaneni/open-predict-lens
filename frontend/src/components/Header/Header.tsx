import { Activity, Sun } from "lucide-react";
import Link from "next/link";
import styles from "./Header.module.scss";

export function Header() {
  return (
    <header className={styles.header}>
      <Link href="/" className={styles.logoContainer} style={{ textDecoration: 'none' }}>
        <div className={styles.iconWrapper}>
          <Activity size={20} className={styles.icon} />
        </div>
        <span className={styles.title}>
          OpenPredictLens
        </span>
      </Link>
      
      <div className={styles.navContainer}>
        <Link href="/explore" className={styles.link}>Explore Markets</Link>
        <a href="#" className={styles.link}>Methodology</a>
        
        <div className={styles.actions}>
          <button className={styles.themeToggle}>
            <Sun size={16} />
          </button>
          <button className={styles.regionBadge}>
            US
          </button>
        </div>
      </div>
    </header>
  );
}