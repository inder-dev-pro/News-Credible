
import React from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const FactCheckLookup = () => (
  <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <Header />
    <main className="flex-1 max-w-3xl mx-auto px-5 py-16 w-full">
      <div className="text-center mb-8">
        <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-yellow-600 to-orange-600 bg-clip-text text-transparent flex items-center justify-center gap-3">
          <span>🔎</span>
          Fact-Check Lookup
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Search across leading fact-check sites for claims, news, or links. Integrated with PolitiFact, Snopes, BoomLive, AltNews, and more.
        </p>
      </div>
      
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-yellow-200/50 shadow-xl p-8 text-center">
        <div className="text-6xl mb-6">🚧</div>
        <h3 className="text-2xl font-bold text-gray-800 mb-4">Coming Soon!</h3>
        <p className="text-gray-600 mb-6 max-w-md mx-auto">
          We're building a comprehensive fact-checking database that will help you verify claims and find reliable information from trusted sources.
        </p>
        <div className="bg-gradient-to-r from-yellow-100 to-orange-100 rounded-lg p-4 border border-yellow-200">
          <h4 className="font-semibold text-yellow-800 mb-2">What's coming:</h4>
          <ul className="text-sm text-yellow-700 space-y-1 text-left max-w-sm mx-auto">
            <li>• Instant fact-checking across multiple sources</li>
            <li>• Integration with PolitiFact, Snopes, and more</li>
            <li>• Claim verification and debunking</li>
            <li>• Source credibility ratings</li>
            <li>• Historical fact-checking data</li>
          </ul>
        </div>
        <a href="/article-analyzer" className="inline-block mt-6 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300">
          Try Article Analyzer Instead
        </a>
      </div>
    </main>
    <Footer />
  </div>
);

export default FactCheckLookup;
