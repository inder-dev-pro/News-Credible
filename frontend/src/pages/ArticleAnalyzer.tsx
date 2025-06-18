
import React from "react";
import Header from "@/components/Header";
import ArticleAnalyzerTool from "@/components/ArticleAnalyzerTool";

const ArticleAnalyzer = () => (
  <div className="min-h-screen bg-background">
    <Header />
    <main className="max-w-2xl mx-auto px-5 py-16">
      <h2 className="text-3xl font-bold mb-4 text-primary">📰 Article Analyzer</h2>
      <p className="mb-7 text-md text-muted-foreground">
        Enter a news article URL to analyze bias, credibility, sentiment, and factual accuracy using our AI models.
      </p>
      <ArticleAnalyzerTool />
    </main>
  </div>
);

export default ArticleAnalyzer;
