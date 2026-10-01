"use client";

import { useState } from "react";
import { API_URL } from "@/lib/api";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("No answer yet.");
  const [sources, setSources] = useState<string[]>([]);
  const [status, setStatus] = useState("Ready");
  const [fileName, setFileName] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a PDF file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setStatus("Uploading and indexing PDF...");

    try {
      const response = await fetch(`${API_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setFileName(data.file_name);
      setStatus(data.message || "Upload successful");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!fileName || !question.trim()) {
      setStatus("Upload a PDF and enter a question.");
      return;
    }

    setLoading(true);
    setStatus("Searching the document...");

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, file_name: fileName }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not answer the question.");
      }

      setAnswer(data.answer || "No answer found.");
      setSources(data.sources || []);
      setStatus("Answer ready");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Failed to get answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-6 px-4 py-10">
      <header className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 shadow-2xl backdrop-blur">
        <p className="text-sm uppercase tracking-[0.2em] text-cyan-400">AI PDF Chatbot</p>
        <h1 className="mt-2 text-3xl font-bold text-white">Ask questions from your uploaded PDFs</h1>
      </header>

      <section className="grid gap-6 lg:grid-cols-[1fr_2fr]">
        <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 shadow-xl">
          <h2 className="mb-4 text-xl font-semibold text-white">Upload PDF</h2>

          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="mb-4 block w-full rounded-xl border border-slate-600 bg-slate-800 px-3 py-2 text-sm text-slate-200"
          />

          <button
            onClick={handleUpload}
            disabled={loading || !file}
            className="w-full rounded-xl bg-cyan-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Processing..." : "Upload & Index PDF"}
          </button>

          <div className="mt-6 rounded-xl border border-slate-700 bg-slate-800/70 p-3 text-sm text-slate-300">
            <span className="font-semibold text-white">Status:</span> {status}
          </div>

          {fileName && (
            <div className="mt-4 rounded-xl border border-emerald-700 bg-emerald-900/30 p-3 text-sm text-emerald-200">
              Current file: <span className="font-semibold">{fileName}</span>
            </div>
          )}
        </div>

        <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 shadow-xl">
          <h2 className="mb-4 text-xl font-semibold text-white">Ask a question</h2>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            rows={5}
            placeholder="Example: What are the key takeaways from this document?"
            className="w-full rounded-xl border border-slate-600 bg-slate-800 px-3 py-3 text-slate-100 outline-none ring-0 placeholder:text-slate-400"
          />

          <button
            onClick={handleAsk}
            disabled={loading || !fileName}
            className="mt-4 w-full rounded-xl bg-violet-500 px-4 py-3 font-semibold text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Thinking..." : "Ask Document"}
          </button>

          <div className="mt-6 rounded-xl border border-slate-700 bg-slate-800/70 p-4">
            <h3 className="mb-3 text-lg font-semibold text-white">Answer</h3>
            <p className="whitespace-pre-line text-slate-200">{answer}</p>
          </div>

          {sources.length > 0 && (
            <div className="mt-6 rounded-xl border border-slate-700 bg-slate-800/70 p-4">
              <h3 className="mb-3 text-lg font-semibold text-white">Sources</h3>
              <ul className="list-disc space-y-2 pl-5 text-slate-300">
                {sources.map((source, index) => (
                  <li key={`${source}-${index}`}>{source}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
