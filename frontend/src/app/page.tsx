import { Header } from "@/components/Header/Header";
import Link from "next/link";
import { ShieldCheck, BarChart2, Zap } from "lucide-react";

export default function LandingPage() {
  const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === "true";

  return (
    <div className="min-h-screen bg-gray-50/30 flex flex-col font-sans">
      <Header />
      
      <main className="flex-1 w-full max-w-[1200px] mx-auto px-6 flex flex-col justify-center mt-8 pb-12">
        <section className="py-16 mx-auto flex flex-col lg:flex-row gap-16 justify-center items-center">
          
          {/* Left Column - Hero */}
          <div className="max-w-xl space-y-6 text-center lg:text-left">
            <h1 className="text-5xl md:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Market Intelligence for <span className="text-blue-600">Prediction Markets</span>
            </h1>
            <p className="text-xl text-slate-600">
              Aggregate data from Kalshi & Polymarket, analyzed by cutting-edge AI to give you the winning edge.
            </p>
            
            <div className="flex flex-col gap-4 mt-8 pt-8 border-t border-gray-200 text-sm font-medium text-gray-500">
              <span className="flex items-center justify-center lg:justify-start gap-2 text-base">
                <ShieldCheck className="h-5 w-5 text-green-500" /> AI Risk Assessment
              </span>
              <span className="flex items-center justify-center lg:justify-start gap-2 text-base">
                <BarChart2 className="h-5 w-5 text-blue-500" /> Real-time Aggregation
              </span>
              <span className="flex items-center justify-center lg:justify-start gap-2 text-base">
                <Zap className="h-5 w-5 text-yellow-500" /> Instant Analysis
              </span>
            </div>
          </div>

          {/* Right Column - Sign Up Form */}
          <div className="w-full max-w-md bg-white border border-gray-200 rounded-2xl p-8 shadow-xl">
            <h2 className="text-2xl font-bold text-slate-900 mb-6 text-center">Create your account</h2>
            
            <form className="space-y-5" action="/explore">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Full Name</label>
                <input 
                  type="text" 
                  required 
                  className="w-full rounded-lg border border-gray-300 px-4 py-3 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow" 
                  placeholder="John Doe" 
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Email</label>
                <input 
                  type="email" 
                  required 
                  className="w-full rounded-lg border border-gray-300 px-4 py-3 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow" 
                  placeholder="you@example.com" 
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Password</label>
                <input 
                  type="password" 
                  required 
                  className="w-full rounded-lg border border-gray-300 px-4 py-3 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow" 
                  placeholder="••••••••" 
                />
              </div>
              
              <button 
                type="submit" 
                className="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold text-lg px-8 py-3.5 rounded-lg shadow-md transition-transform active:scale-[0.98] mt-2"
              >
                Sign Up for Access
              </button>
            </form>

            <p className="text-center text-sm text-slate-500 mt-6 font-medium">
              Already have an account? <a href="#" className="text-blue-600 hover:underline">Log in</a>
            </p>

            {isDevMode && (
              <div className="mt-8 p-4 bg-orange-50 border border-orange-200 rounded-xl text-center shadow-inner">
                <p className="text-xs text-orange-800 font-bold uppercase tracking-wider mb-3">Developer Environment</p>
                <Link href="/explore">
                  <button className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold text-sm px-4 py-2.5 rounded-lg transition-transform active:scale-[0.98] shadow-sm">
                    Bypass Login to App
                  </button>
                </Link>
              </div>
            )}
          </div>
          
        </section>
      </main>
    </div>
  );
}