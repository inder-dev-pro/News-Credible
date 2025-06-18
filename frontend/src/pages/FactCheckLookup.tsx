
import React from "react";
import Header from "@/components/Header";
import FactCheckLookupTool from "@/components/FactCheckLookupTool";

const FactCheckLookup = () => (
  <div className="min-h-screen bg-background">
    <Header />
    <main className="max-w-2xl mx-auto px-5 py-16">
      <h2 className="text-3xl font-bold mb-4 text-primary">🔎 Fact-Check Lookup</h2>
      <p className="mb-7 text-md text-muted-foreground">
        Search across leading fact-check sites for claims, news, or links.
      </p>
      <FactCheckLookupTool />
    </main>
  </div>
);

export default FactCheckLookup;
