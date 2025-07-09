
import React from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const MediaVerifier = () => (
  <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <Header />
    <main className="flex-1 max-w-3xl mx-auto px-5 py-16 w-full">
      <div className="text-center mb-8">
        <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent flex items-center justify-center gap-3">
          <span>🕵️‍♂️</span>
          Media Verifier
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Verify authenticity of images & videos using AI, EXIF, and reverse image tools. Detects edited, deepfaked, or repurposed content from news and social channels.
        </p>
      </div>
      
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-green-200/50 shadow-xl p-8 text-center">
        <div className="text-6xl mb-6">🚧</div>
        <h3 className="text-2xl font-bold text-gray-800 mb-4">Coming Soon!</h3>
        <p className="text-gray-600 mb-6 max-w-md mx-auto">
          We're working hard to bring you advanced media verification tools. This feature will help you detect manipulated images and videos using cutting-edge AI technology.
        </p>
        <div className="bg-gradient-to-r from-green-100 to-emerald-100 rounded-lg p-4 border border-green-200">
          <h4 className="font-semibold text-green-800 mb-2">What's coming:</h4>
          <ul className="text-sm text-green-700 space-y-1 text-left max-w-sm mx-auto">
            <li>• AI-powered image forgery detection</li>
            <li>• Deepfake video analysis</li>
            <li>• EXIF metadata analysis</li>
            <li>• Reverse image search integration</li>
            <li>• Real-time verification results</li>
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

export default MediaVerifier;
