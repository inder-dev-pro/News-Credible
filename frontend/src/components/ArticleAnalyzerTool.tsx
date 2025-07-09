import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { toast } from "@/components/ui/use-toast";


type AnalysisResult = {
  url: string;
  title?: string;
  bias?: {
    label: string;
    confidence: number;
    explanation?: string;
  };
  credibility?: {
    score: number;
    factors: string[];
  };
  sentiment?: {
    label: string;
    score: number;
  };
  factuality?: {
    score: number;
    claims_verified: number;
    issues_found: string[];
  };
  summary?: string;
  truth_score: number;
  confidence: number;
};

const API_URL = "http://localhost:8000";
const apiEndpoint = `${API_URL}/api/v1/analyze/url`;
// Or use an environment variable for the base URL if you prefer // TODO: Replace with your FastAPI backend endpoint

const ArticleAnalyzerTool = () => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const isValidUrl = (string: string) => {
    try {
      new URL(string);
      return true;
    } catch (_) {
      return false;
    }
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isValidUrl(url)) {
      toast({ 
        title: "Invalid URL", 
        description: "Please enter a valid URL starting with http:// or https://" 
      });
      return;
    }

    setResult(null);
    setLoading(true);

    try {
      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      
      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      console.error("Analysis error:", err);
      toast({ 
        title: "Analysis Error", 
        description: err.message || "Failed to analyze article" 
      });
    }
    
    setLoading(false);
  };

  const getBiasColor = (label: string) => {
    switch (label?.toLowerCase()) {
      case 'left': return 'bg-blue-100 text-blue-800';
      case 'right': return 'bg-red-100 text-red-800';
      case 'center': return 'bg-green-100 text-green-800';
      case 'neutral': return 'bg-gray-100 text-gray-800';
      default: return 'bg-yellow-100 text-yellow-800';
    }
  };

  const getSentimentColor = (label: string) => {
    switch (label?.toLowerCase()) {
      case 'positive': return 'text-green-600';
      case 'negative': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getCredibilityColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-8">
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-200/50">
        <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <span className="text-blue-600">🔗</span>
          Enter Article URL
        </h3>
        <form onSubmit={onSubmit} className="space-y-4">
          <div>
            <Input
              type="url"
              value={url}
              onChange={e => setUrl(e.target.value)}
              placeholder="https://example.com/news-article"
              required
              className="text-base border-blue-200 focus:border-blue-400 focus:ring-blue-400"
            />
          </div>
          <Button 
            type="submit" 
            disabled={loading || !url} 
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 text-lg shadow-lg hover:shadow-xl transition-all duration-300"
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Analyzing Article...
              </div>
            ) : (
              "Analyze Article"
            )}
          </Button>
        </form>
      </div>

      {result && (
        <div className="animate-fade-in">
          <Card className="border-0 shadow-xl bg-gradient-to-br from-white to-blue-50/30">
            <CardHeader className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-lg">
              <CardTitle className="text-xl mb-1 flex items-center gap-2">
                <span>📊</span>
                Article Analysis Results
              </CardTitle>
              <CardDescription className="text-blue-100">
                Comprehensive breakdown of the article's credibility, bias, sentiment, and factuality.
              </CardDescription>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
              {result.title && (
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                  <span className="font-semibold text-blue-800">Article Title:</span>
                  <div className="text-gray-700 mt-1">{result.title}</div>
                </div>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg p-4 border border-green-200">
                    <div className="font-semibold text-green-800 mb-2">Truth Score</div>
                    <div className="text-3xl font-bold text-green-600 mb-1">{result.truth_score}</div>
                    <div className="text-sm text-green-600">Overall reliability</div>
                  </div>
                  
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
                    <div className="font-semibold text-blue-800 mb-2">Confidence</div>
                    <div className="text-2xl font-bold text-blue-600 mb-1">{result.confidence}</div>
                    <div className="text-sm text-blue-600">Analysis confidence</div>
                  </div>
                </div>
                
                <div className="space-y-4">
                  {result.bias && (
                    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-4 border border-purple-200">
                      <div className="font-semibold text-purple-800 mb-2">Bias Detection</div>
                      <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${getBiasColor(result.bias.label)}`}>
                        {result.bias.label} ({Math.round(result.bias.confidence * 100)}%)
                      </span>
                      {result.bias.explanation && (
                        <div className="text-xs text-purple-600 mt-2">{result.bias.explanation}</div>
                      )}
                    </div>
                  )}
                  
                  {result.sentiment && (
                    <div className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-lg p-4 border border-orange-200">
                      <div className="font-semibold text-orange-800 mb-2">Sentiment</div>
                      <span className={`font-semibold text-lg ${getSentimentColor(result.sentiment.label)}`}>
                        {result.sentiment.label} ({Math.round(result.sentiment.score * 100)}%)
                      </span>
                    </div>
                  )}
                </div>
              </div>
              
              {result.credibility && (
                <div className="bg-gradient-to-br from-teal-50 to-cyan-50 rounded-lg p-4 border border-teal-200">
                  <div className="font-semibold text-teal-800 mb-2">Credibility Score</div>
                  <div className="flex items-center gap-3 mb-3">
                    <span className={`text-2xl font-bold ${getCredibilityColor(result.credibility.score)}`}>
                      {Math.round(result.credibility.score * 100)}%
                    </span>
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${getCredibilityColor(result.credibility.score).replace('text-', 'bg-')}`}
                        style={{ width: `${result.credibility.score * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="text-sm text-teal-700">
                    <div className="font-medium mb-1">Factors:</div>
                    <ul className="list-disc pl-5 space-y-1">
                      {result.credibility.factors.map((factor, i) => (
                        <li key={i} className="text-xs">{factor}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
              
              {result.factuality && (
                <div className="bg-gradient-to-br from-red-50 to-pink-50 rounded-lg p-4 border border-red-200">
                  <div className="font-semibold text-red-800 mb-2">Factuality Check</div>
                  <div className="flex items-center gap-3 mb-3">
                    <span className="text-2xl font-bold text-red-600">{Math.round(result.factuality.score * 100)}%</span>
                    <div className="text-sm text-red-600">Claims Verified: {result.factuality.claims_verified}</div>
                  </div>
                  {result.factuality.issues_found.length > 0 && (
                    <div className="text-sm text-red-700">
                      <div className="font-medium mb-1">Issues Found:</div>
                      <ul className="list-disc pl-5 space-y-1">
                        {result.factuality.issues_found.map((issue, i) => (
                          <li key={i} className="text-xs">{issue}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
              
              {result.summary && (
                <div className="bg-gradient-to-br from-gray-50 to-slate-50 rounded-lg p-4 border border-gray-200">
                  <div className="font-semibold text-gray-800 mb-2">Summary</div>
                  <div className="text-sm text-gray-700 leading-relaxed">{result.summary}</div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ArticleAnalyzerTool;
