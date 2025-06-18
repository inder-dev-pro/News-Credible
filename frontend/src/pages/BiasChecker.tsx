
import React from "react";
import Header from "@/components/Header";
import BiasCheckerTool from "@/components/BiasCheckerTool";

const BiasChecker = () => (
  <div className="min-h-screen bg-background">
    <Header />
    <main className="max-w-2xl mx-auto px-5 py-16">
      <h2 className="text-3xl font-bold mb-4 text-primary">🧠 News Bias Checker</h2>
      <p className="mb-7 text-md text-muted-foreground">
        Enter or paste news headlines or articles below to detect political or rhetorical bias using our fine-tuned AI model.
      </p>
      <BiasCheckerTool />
    </main>
  </div>
);

export default BiasChecker;
