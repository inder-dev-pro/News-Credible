
import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/components/ui/use-toast";
import { ExternalLink, AlertCircle, CheckCircle, TrendingUp, TrendingDown } from "lucide-react";

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
};

const apiEndpoint = "/api/analyze-article"; // TODO: Replace with your FastAPI backend endpoint

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
          {/* Article Info */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ExternalLink size={20} />
                Article Information
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {result.title && (
                  <div>
                    <span className="font-medium">Title:</span> {result.title}
                  </div>
                )}
                <div>
                  <span className="font-medium">URL:</span> 
                  <a 
                    href={result.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-primary hover:underline ml-1"
                  >
                    {result.url}
                  </a>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Analysis Results */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Bias Analysis */}
            {result.bias && (
              <Card>
                <CardHeader>
                  <CardTitle>Political Bias</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Badge className={getBiasColor(result.bias.label)}>
                        {result.bias.label}
                      </Badge>
                      <span className="text-sm text-muted-foreground">
                        {(result.bias.confidence * 100).toFixed(1)}% confidence
                      </span>
                    </div>
                    {result.bias.explanation && (
                      <p className="text-sm text-muted-foreground">
                        {result.bias.explanation}
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Credibility Score */}
            {result.credibility && (
              <Card>
                <CardHeader>
                  <CardTitle>Credibility</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      {result.credibility.score >= 0.7 ? (
                        <CheckCircle className="text-green-600" size={20} />
                      ) : (
                        <AlertCircle className="text-red-600" size={20} />
                      )}
                      <span className={`font-bold ${getCredibilityColor(result.credibility.score)}`}>
                        {(result.credibility.score * 100).toFixed(0)}%
                      </span>
                    </div>
                    {result.credibility.factors.length > 0 && (
                      <div>
                        <p className="text-sm font-medium mb-1">Key Factors:</p>
                        <ul className="text-sm text-muted-foreground space-y-1">
                          {result.credibility.factors.map((factor, index) => (
                            <li key={index}>• {factor}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Sentiment Analysis */}
            {result.sentiment && (
              <Card>
                <CardHeader>
                  <CardTitle>Sentiment</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-2">
                    {result.sentiment.label === 'positive' ? (
                      <TrendingUp className="text-green-600" size={20} />
                    ) : result.sentiment.label === 'negative' ? (
                      <TrendingDown className="text-red-600" size={20} />
                    ) : (
                      <div className="w-5 h-5 rounded-full bg-gray-400" />
                    )}
                    <span className={`font-medium ${getSentimentColor(result.sentiment.label)}`}>
                      {result.sentiment.label}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      ({result.sentiment.score.toFixed(2)})
                    </span>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Factuality Check */}
            {result.factuality && (
              <Card>
                <CardHeader>
                  <CardTitle>Factuality</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <span className={`font-bold ${getCredibilityColor(result.factuality.score)}`}>
                        {(result.factuality.score * 100).toFixed(0)}%
                      </span>
                      <span className="text-sm text-muted-foreground">
                        ({result.factuality.claims_verified} claims verified)
                      </span>
                    </div>
                    {result.factuality.issues_found.length > 0 && (
                      <div>
                        <p className="text-sm font-medium mb-1 text-red-600">Issues Found:</p>
                        <ul className="text-sm text-muted-foreground space-y-1">
                          {result.factuality.issues_found.map((issue, index) => (
                            <li key={index}>• {issue}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Summary */}
          {result.summary && (
            <Card>
              <CardHeader>
                <CardTitle>Analysis Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">{result.summary}</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

export default ArticleAnalyzerTool;
