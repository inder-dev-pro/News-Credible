
import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "@/components/ui/use-toast";

type Fact = {
  title: string;
  source: string;
  url: string;
  verdict: string;
  summary: string;
};

const apiEndpoint = "/api/fact-check-lookup"; // TODO: Replace with your endpoint

const FactCheckLookupTool = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Fact[]>([]);

  const fetchFacts = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResults([]);

    try {
      // Placeholder API call
      const resp = await fetch(`${apiEndpoint}?q=${encodeURIComponent(query)}`);
      if (!resp.ok) throw new Error("Search failed");
      const data = await resp.json();

      setResults(data.facts ?? []);
      if (!data.facts || data.facts.length === 0) {
        toast({ title: "No results found", description: "No matching fact-checks found for this query." });
      }
    } catch (err: any) {
      toast({ title: "Error", description: err.message || "API error" });
    }
    setLoading(false);
  };

  return (
    <form onSubmit={fetchFacts} className="space-y-7">
      <Input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Enter a claim, news link, or article..."
        required
      />
      <Button type="submit" disabled={loading || !query} className="w-full">
        {loading ? "Searching..." : "Search Fact-Checks"}
      </Button>
      {results.length > 0 && (
        <div className="space-y-4 mt-6 animate-fade-in">
          {results.map((fact, idx) => (
            <Card key={idx}>
              <CardContent className="pt-5">
                <div>
                  <div className="font-semibold mb-1">{fact.title}</div>
                  <div className="mb-2 text-xs text-muted-foreground">
                    Source: <a href={fact.url} target="_blank" rel="noopener noreferrer" className="underline text-primary">{fact.source}</a>
                  </div>
                  <div>
                    <span className="font-medium">Verdict:</span>{" "}
                    <span className="inline-block rounded px-2 font-bold"
                      style={{ background: "#fef9c3" }}>{fact.verdict}</span>
                  </div>
                  <div className="mt-2 text-sm text-muted-foreground">{fact.summary}</div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </form>
  );
};

export default FactCheckLookupTool;
