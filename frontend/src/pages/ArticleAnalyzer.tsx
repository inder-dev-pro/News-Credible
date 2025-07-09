
import React from "react";
import Header from "@/components/Header";
import ArticleAnalyzerTool from "@/components/ArticleAnalyzerTool";
import Footer from "@/components/Footer";

const ArticleAnalyzer = () => (
  <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <Header />
    <main className="flex-1 max-w-3xl mx-auto px-5 py-16 w-full">
      <div className="text-center mb-8">
        <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent flex items-center justify-center gap-3">
          <span>📰</span>
          Article Analyzer
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Enter a news article URL to analyze bias, credibility, sentiment, and factual accuracy using our AI models. The analyzer uses advanced language models, credibility scoring, sentiment analysis, and fact-checking against trusted sources to provide a transparent, data-driven report.
        </p>
      </div>
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-blue-200/50 shadow-xl p-8">
        <ArticleAnalyzerTool />
      </div>
    </main>
    <Footer />
  </div>
);

export default ArticleAnalyzer;
