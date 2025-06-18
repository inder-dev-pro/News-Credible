
import React from "react";
import Header from "@/components/Header";
import { ArrowRight } from "lucide-react";

// Maincard component for reuse
const FeatureCard = ({
  title,
  description,
  icon,
  href,
}: {
  title: string;
  description: string;
  icon: React.ReactNode;
  href: string;
}) => (
  <a
    href={href}
    className="group relative flex flex-col items-start bg-card rounded-2xl border border-border shadow-md p-8 min-h-[240px] hover-scale hover:shadow-xl transition-all duration-200 focus:outline-primary outline-none"
  >
    <div className="mb-5 text-primary text-3xl">{icon}</div>
    <div className="font-semibold text-xl mb-1 group-hover:text-primary">{title}</div>
    <div className="text-muted-foreground mb-5 text-sm">{description}</div>
    <span className="flex items-center gap-1 mt-auto pt-3 font-medium text-primary group-hover:underline transition-colors story-link">
      Go to Tool <ArrowRight size={20} />
    </span>
  </a>
);

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container max-w-5xl mx-auto py-12 px-4 flex flex-col items-center">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-center mb-8 text-primary">
          <span>NewsCredible</span>
        </h1>
        <h2 className="text-lg md:text-xl text-muted-foreground text-center mb-12 max-w-2xl">
          The one-stop AI-powered toolkit for media authenticity and news analysis.
        </h2>
        <section className="grid grid-cols-1 md:grid-cols-3 gap-5 w-full animate-fade-in">
          <FeatureCard
            title="Article Analyzer"
            description="Analyze news articles by URL for bias, credibility, sentiment, and factual accuracy. Our AI provides comprehensive insights into article quality and reliability."
            icon={<span className="text-blue-500">📰</span>}
            href="/article-analyzer"
          />
          <FeatureCard
            title="Media Verifier"
            description="Verify authenticity of images & videos using AI, EXIF, and reverse image tools. Detects edited, deepfaked, or repurposed content from news and social channels."
            icon={<span className="text-green-600">🕵️‍♂️</span>}
            href="/media-verifier"
          />
          <FeatureCard
            title="Fact-Check Lookup"
            description="Instantly search trusted fact-check sources for user-submitted claims, articles, or links. Integrated with PolitiFact, Snopes, BoomLive, AltNews, and more."
            icon={<span className="text-yellow-500">🔎</span>}
            href="/fact-check-lookup"
          />
        </section>
        <div className="mt-16 text-xs text-muted-foreground text-center max-w-xl mx-auto">
          <span>
            NewsCredible makes no editorial decisions — it uses best-in-class open datasets and AI models to assist critical thinking and transparency.
          </span>
        </div>
      </main>
    </div>
  );
};

export default Index;
