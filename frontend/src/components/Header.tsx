
import React from "react";

const Header = () => (
  <header className="w-full bg-white dark:bg-background border-b border-border sticky top-0 z-30">
    <div className="container max-w-6xl mx-auto flex items-center justify-between py-5 px-4">
      <div className="flex items-center space-x-3">
        {/* Simple credible logo emoji for now */}
        <span className="text-3xl">📰</span>
        <span className="font-extrabold text-2xl tracking-tight text-primary">NewsCredible</span>
      </div>
      <nav className="hidden md:flex gap-7">
        <a href="/" className="text-muted-foreground hover:text-primary font-medium transition-colors">Home</a>
        <a href="/article-analyzer" className="text-muted-foreground hover:text-primary font-medium transition-colors">Article Analyzer</a>
        <a href="/media-verifier" className="text-muted-foreground hover:text-primary font-medium transition-colors">Media Verifier</a>
        <a href="/fact-check-lookup" className="text-muted-foreground hover:text-primary font-medium transition-colors">Fact-Check Lookup</a>
      </nav>
    </div>
  </header>
);

export default Header;
