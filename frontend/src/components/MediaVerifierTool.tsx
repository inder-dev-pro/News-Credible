
import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "@/components/ui/use-toast";

type MediaResult = {
  verdict: "genuine" | "forged" | "deepfake" | "repurposed" | "unknown";
  details?: string;
  metadata?: Record<string, any>;
  evidenceUrls?: string[];
};

const apiEndpoint = "/api/media-verify"; // TODO: Replace with your backend route

const MediaVerifierTool = () => {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MediaResult | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    setResult(null);
    if (f) {
      setFile(f);
      setPreviewUrl(URL.createObjectURL(f));
    }
  };

  const onUploadClick = () => fileInputRef.current?.click();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("file", file);

      // Placeholder API call
      const resp = await fetch(apiEndpoint, {
        method: "POST",
        body: formData,
      });
      if (!resp.ok) throw new Error("Verification failed");
      const data = await resp.json();

      setResult({
        verdict: data.verdict ?? "unknown",
        details: data.details,
        metadata: data.metadata,
        evidenceUrls: data.evidenceUrls,
      });
    } catch (err: any) {
      toast({ title: "Error", description: err.message || "API error" });
    }
    setLoading(false);
  };

  return (
    <form className="space-y-7" onSubmit={onSubmit}>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*,video/*"
        className="hidden"
        onChange={handleFileChange}
      />
      <Button type="button" variant="outline" onClick={onUploadClick} className="w-full">
        {file ? "Change File" : "Upload Image or Video"}
      </Button>
      {previewUrl && (
        <div className="mt-3 flex justify-center">
          {file?.type.startsWith("image") ? (
            <img src={previewUrl} alt="preview" className="max-h-52 max-w-full rounded-lg border" />
          ) : (
            <video src={previewUrl} controls className="max-h-52 max-w-full rounded-lg border" />
          )}
        </div>
      )}
      <Button type="submit" disabled={loading || !file} className="w-full">
        {loading ? "Verifying..." : "Analyze Media"}
      </Button>
      {result && (
        <Card className="mt-6 animate-fade-in">
          <CardContent className="pt-5">
            <div>
              <div className="mb-2">
                <span className="font-medium">Result:</span>{" "}
                <span className="capitalize font-bold">{result.verdict}</span>
              </div>
              {result.details && (
                <div className="mb-2">
                  <span className="font-medium">Details:</span>{" "}
                  <span className="text-muted-foreground">{result.details}</span>
                </div>
              )}
              {result.metadata && (
                <div className="mb-2">
                  <span className="font-medium">Metadata:</span>
                  <pre className="bg-muted px-2 py-1 rounded text-xs overflow-x-auto">
                    {JSON.stringify(result.metadata, null, 2)}
                  </pre>
                </div>
              )}
              {result.evidenceUrls?.length ? (
                <div>
                  <span className="font-medium">Evidence:</span>
                  <ul className="list-disc list-inside pl-2">
                    {result.evidenceUrls.map(url => (
                      <li key={url}><a href={url} target="_blank" rel="noopener noreferrer" className="text-primary underline">{url}</a></li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>
          </CardContent>
        </Card>
      )}
    </form>
  );
};

export default MediaVerifierTool;
