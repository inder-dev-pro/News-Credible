
import React, { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "@/components/ui/use-toast";

type BiasResult = {
  label: string;
  confidence: number;
  explanation?: string;
};

const apiEndpoint = "/api/bias-check"; // TODO: Replace with your actual backend API route

const BiasCheckerTool = () => {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<BiasResult | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setResult(null);
    setLoading(true);

    try {
      // Placeholder API call
      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });
      if (!response.ok) throw new Error("Failed to check bias");
      const data = await response.json();

      setResult({
        label: data.label ?? "Unknown",
        confidence: data.confidence ?? 0,
        explanation: data.explanation,
      });
    } catch (err: any) {
      toast({ title: "Error", description: err.message || "API error" });
    }
    setLoading(false);
  };

  return (
    <form className="space-y-7" onSubmit={onSubmit}>
      <Textarea
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Paste a news headline, excerpt, or article here..."
        rows={5}
        required
      />
      <Button type="submit" disabled={loading || !input} className="w-full">
        {loading ? "Analyzing..." : "Analyze Bias"}
      </Button>

      {result && (
        <Card className="mt-6 animate-fade-in">
          <CardContent className="pt-5">
            <div className="flex flex-col gap-2">
              <div>
                <span className="font-medium">Detected Bias:</span>{" "}
                <span className="inline-block rounded px-2 py-0.5 font-bold text-base"
                  style={{ background: "#e0e7ff" }}>{result.label}</span>
              </div>
              <div>
                <span className="font-medium">Confidence:</span>{" "}
                {(result.confidence * 100).toFixed(1)}%
              </div>
              {result.explanation && (
                <div>
                  <span className="font-medium">Explanation:</span>{" "}
                  <span className="block text-muted-foreground text-sm">{result.explanation}</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </form>
  );
};

export default BiasCheckerTool;
