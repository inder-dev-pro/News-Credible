
import React from "react";

const Header = () => (
  <header className="w-full bg-gradient-to-r from-blue-100 via-purple-100 to-pink-100/80 backdrop-blur-sm border-b border-blue-200/50 sticky top-0 z-30 shadow-md">
    <div className="container max-w-6xl mx-auto flex items-center justify-between py-5 px-4">
      <div className="flex items-center space-x-3">
        <img 
          src="/fake_news_debunker_logo.svg" 
          alt="NewsCredible Logo" 
          className="w-10 h-10"
        />
        <span className="font-extrabold text-2xl tracking-tight bg-gradient-to-r from-blue-600 via-purple-600 to-pink-500 bg-clip-text text-transparent">NewsCredible</span>
      </div>
      <nav className="hidden md:flex gap-7">
        <a href="/" className="text-gray-700 hover:text-blue-700 font-medium transition-colors relative group px-2 py-1 rounded-lg hover:bg-gradient-to-r hover:from-blue-200 hover:to-purple-200">
          Home
          <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-600 to-purple-600 transition-all duration-300 group-hover:w-full"></span>
        </a>
        <a href="/article-analyzer" className="text-blue-700 font-semibold transition-colors relative group px-2 py-1 rounded-lg hover:bg-gradient-to-r hover:from-blue-200 hover:to-purple-200">
          Article Analyzer
          <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-600 to-purple-600 transition-all duration-300 group-hover:w-full"></span>
        </a>
        <a href="/media-verifier" className="text-green-700 font-semibold transition-colors relative group px-2 py-1 rounded-lg hover:bg-gradient-to-r hover:from-green-200 hover:to-emerald-200 flex items-center gap-1">
          Media Verifier
          <span className="ml-1 px-2 py-0.5 rounded-full text-xs font-bold bg-gradient-to-r from-green-400 to-emerald-400 text-white">Soon</span>
        </a>
        <a href="/fact-check-lookup" className="text-yellow-700 font-semibold transition-colors relative group px-2 py-1 rounded-lg hover:bg-gradient-to-r hover:from-yellow-200 hover:to-orange-200 flex items-center gap-1">
          Fact-Check Lookup
          <span className="ml-1 px-2 py-0.5 rounded-full text-xs font-bold bg-gradient-to-r from-yellow-400 to-orange-400 text-white">Soon</span>
        </a>
      </nav>
    </div>
  </header>
);

export default Header;
