
import React from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header />
      <main className="flex-1 container max-w-4xl mx-auto py-12 px-4 flex flex-col items-center">
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
            NewsCredible
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl leading-relaxed">
            NewsCredible is your AI-powered toolkit for analyzing the credibility, bias, sentiment, and factual accuracy of news articles. Our mission is to empower readers with transparent, data-driven insights so you can make informed decisions in a world of information overload.
          </p>
        </div>

        <section className="w-full mb-12">
          <div className="bg-white/80 backdrop-blur-sm rounded-3xl border border-blue-200/50 shadow-xl p-8 mb-8">
            <h2 className="text-3xl font-bold mb-6 text-gray-800 flex items-center gap-3">
              <span className="text-blue-600">🔍</span>
              How does the Article Analyzer work?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-blue-600 font-bold text-sm">1</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-1">Bias Detection</h3>
                    <p className="text-gray-600 text-sm">Uses advanced language models to detect political or ideological bias in the article's language and framing.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-green-600 font-bold text-sm">2</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-1">Credibility Scoring</h3>
                    <p className="text-gray-600 text-sm">Evaluates the source, writing style, and factual consistency to assign a credibility score.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-purple-600 font-bold text-sm">3</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-1">Sentiment Analysis</h3>
                    <p className="text-gray-600 text-sm">Analyzes the overall tone (positive, negative, neutral) to reveal emotional framing.</p>
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-orange-600 font-bold text-sm">4</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-1">Factuality Check</h3>
                    <p className="text-gray-600 text-sm">Cross-references claims with trusted fact-checking databases and highlights potential inaccuracies.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-indigo-600 font-bold text-sm">5</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-1">Summary & Transparency</h3>
                    <p className="text-gray-600 text-sm">Provides a concise summary and explains the reasoning behind each score.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-12">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="text-3xl mb-4">📰</div>
            <h3 className="text-xl font-bold mb-2">Article Analyzer</h3>
            <p className="text-blue-100 mb-4">Analyze news articles for bias, credibility, sentiment, and factual accuracy using our AI models.</p>
            <a href="/article-analyzer" className="inline-block bg-white/20 hover:bg-white/30 text-white font-semibold py-2 px-4 rounded-lg transition-colors">
              Try Now
            </a>
          </div>

          <div className="bg-gradient-to-br from-gray-400 to-gray-500 rounded-2xl p-6 text-white shadow-lg opacity-75">
            <div className="text-3xl mb-4">🕵️‍♂️</div>
            <h3 className="text-xl font-bold mb-2">Media Verifier</h3>
            <p className="text-gray-200 mb-4">Verify authenticity of images & videos using AI, EXIF, and reverse image tools.</p>
            <div className="inline-block bg-white/20 text-white font-semibold py-2 px-4 rounded-lg">
              Coming Soon
            </div>
          </div>

          <div className="bg-gradient-to-br from-gray-400 to-gray-500 rounded-2xl p-6 text-white shadow-lg opacity-75">
            <div className="text-3xl mb-4">🔎</div>
            <h3 className="text-xl font-bold mb-2">Fact-Check Lookup</h3>
            <p className="text-gray-200 mb-4">Search trusted fact-check sources for claims, articles, or links.</p>
            <div className="inline-block bg-white/20 text-white font-semibold py-2 px-4 rounded-lg">
              Coming Soon
            </div>
          </div>
        </div>

        <div className="text-center">
          <a href="/article-analyzer" className="inline-block bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 text-lg">
            Start Analyzing Articles
          </a>
        </div>

        <div className="mt-16 text-sm text-gray-500 text-center max-w-2xl mx-auto">
          <span>
            NewsCredible makes no editorial decisions — it uses best-in-class open datasets and AI models to assist critical thinking and transparency.
          </span>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Index;
