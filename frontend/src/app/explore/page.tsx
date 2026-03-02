'use client';
import { useEffect, useState, useMemo } from "react";
import { Search, ArrowUpDown } from "lucide-react";

import { Header } from "@/components/Header/Header";
import MarketList from "@/components/MarketList/MarketList";
import AnalyzePanel from "@/components/AnalyzePanel/AnalyzePanel";
import { fetchMarkets } from "@/lib/api";
import type { Market } from "@/types/market";

const CATEGORIES = ["All", "Cryptocurrency", "Business", "Climate", "Space", "Economics", "Technology"];

export default function Explore() {
  const [search, setSearch] = useState("");
  const [platformFilter, setPlatformFilter] = useState<"All" | "Kalshi" | "Polymarket">("All");
  const [categoryFilter, setCategoryFilter] = useState("All");
  
  const [markets, setMarkets] = useState<Market[]>([]);
  const [marketsLoading, setMarketsLoading] = useState(true);
  
  // Refactor state for panel
  const [selectedTicker, setSelectedTicker] = useState<string | null>(null);
  const [isPanelOpen, setIsPanelOpen] = useState(false);

  useEffect(() => {
    setMarketsLoading(true);
    fetchMarkets()
      .then(setMarkets)
      .catch((err) => console.error(err))
      .finally(() => setMarketsLoading(false));
  }, []);

  const filteredMarkets = useMemo(() => {
    return markets.filter((m) => {
      // Search filter
      const searchLower = search.toLowerCase();
      const matchesSearch = !search || 
        m.ticker.toLowerCase().includes(searchLower) ||
        m.title.toLowerCase().includes(searchLower);
      
      // Platform filter
      const matchesPlatform = platformFilter === "All" || m.platform === platformFilter;
      
      // Category filter
      const matchesCategory = categoryFilter === "All" || m.category === categoryFilter;

      return matchesSearch && matchesPlatform && matchesCategory;
    }).sort((a, b) => (b.score || 0) - (a.score || 0)); // default sort by score descending
  }, [markets, search, platformFilter, categoryFilter]);

  return (
    <div className="min-h-screen bg-gray-50/30 flex flex-col font-sans">
      <Header />
      
      <main className="flex-1 w-full max-w-[1200px] mx-auto px-6 pb-12 pt-8">
        {/* Search pushed to the top */}
        <div className="relative mb-8 shadow-sm">
          <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search markets (e.g., 'Bitcoin', 'Election', 'SpaceX')..."
            className="w-full h-14 pl-12 pr-4 rounded-xl border border-gray-200 bg-white text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow text-base"
          />
        </div>

        {/* Filters Section */}
        <div className="flex flex-col md:flex-row items-start md:items-center gap-4 mb-8 w-full overflow-x-auto pb-2">
          {/* Platform Tabs */}
          <div className="flex bg-white rounded-lg border border-gray-200 p-1 shadow-sm shrink-0">
            {["All", "Kalshi", "Polymarket"].map((tab) => (
              <button
                key={tab}
                onClick={() => setPlatformFilter(tab as any)}
                className={`px-5 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  platformFilter === tab
                    ? "bg-gray-100 text-gray-900 shadow-sm"
                    : "text-gray-500 hover:text-gray-900 hover:bg-gray-50"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Sort Button */}
          <button className="flex items-center gap-2 bg-white border border-gray-200 rounded-lg px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 shrink-0">
            <ArrowUpDown className="h-4 w-4 text-gray-400" />
            Sort by: Score
          </button>

          {/* Vertical Divider */}
          <div className="hidden md:block w-px h-8 bg-gray-200 mx-2"></div>

          {/* Categories */}
          <div className="flex items-center gap-2 text-sm shrink-0">
            <span className="text-gray-500 mr-1 flex items-center gap-1">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
              </svg>
              Categories:
            </span>
            <div className="flex gap-2 overflow-x-auto custom-scrollbar pb-1">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setCategoryFilter(cat)}
                  className={`px-3 py-1.5 rounded-full border transition-colors whitespace-nowrap ${
                    categoryFilter === cat
                      ? "bg-slate-800 text-white border-slate-800"
                      : "bg-white text-gray-600 border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Market Grid Header */}
        <div className="flex items-center gap-3 mb-6">
          <h2 className="text-xl font-bold text-gray-900">Explore Opportunities</h2>
          <span className="bg-gray-100 text-gray-600 px-2.5 py-0.5 rounded-full text-xs font-semibold">
            {filteredMarkets.length}
          </span>
        </div>

        {/* Markets Output */}
        <MarketList
          markets={filteredMarkets}
          loading={marketsLoading}
          onSelect={(ticker) => {
            setSelectedTicker(ticker);
            setIsPanelOpen(true);
          }}
        />

        {/* Analyze Panel Integration */}
        {isPanelOpen && (
          <AnalyzePanel 
            isOpen={isPanelOpen} 
            onClose={() => setIsPanelOpen(false)} 
            selectedTicker={selectedTicker} 
          />
        )}
      </main>
    </div>
  );
}