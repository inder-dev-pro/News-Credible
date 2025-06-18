
import React from "react";
import Header from "@/components/Header";
import MediaVerifierTool from "@/components/MediaVerifierTool";

const MediaVerifier = () => (
  <div className="min-h-screen bg-background">
    <Header />
    <main className="max-w-2xl mx-auto px-5 py-16">
      <h2 className="text-3xl font-bold mb-4 text-primary">🕵️‍♂️ Media Verifier</h2>
      <p className="mb-7 text-md text-muted-foreground">
        Upload an image or video to run AI-driven forgery, deepfake, and provenance checks.
      </p>
      <MediaVerifierTool />
    </main>
  </div>
);

export default MediaVerifier;
