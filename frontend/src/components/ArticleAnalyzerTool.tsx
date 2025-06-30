import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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

const API_URL = import.meta.env.VITE_API_URL;
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
    <div className="space-y-7">
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <Input
            type="url"
            value={url}
            onChange={e => setUrl(e.target.value)}
            placeholder="https://example.com/news-article"
            required
            className="text-base"
          />
        </div>
        <Button 
          type="submit" 
          disabled={loading || !url} 
          className="w-full"
        >
          {loading ? "Analyzing Article..." : "Analyze Article"}
        </Button>
      </form>

      {result && (
        <div className="space-y-6 animate-fade-in">
          <Card>
            <CardHeader>
              <CardTitle>Article Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div>
                <div>
                  <span className="font-medium">Truth Score:</span> {result.truth_score}
                </div>
                <div>
                  <span className="font-medium">Confidence:</span> {result.confidence}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ArticleAnalyzerTool;
