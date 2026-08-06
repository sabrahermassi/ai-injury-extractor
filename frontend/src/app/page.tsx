"use client";

import { useState } from "react";
import { extractInjury } from "@/lib/api";

export default function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setLoading(true);

    try {
      const data = await extractInjury(text);
      setResult(data);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  }

  return (
    <main className="min-h-screen p-10">
      <h1 className="text-3xl font-bold mb-6">AI Injury Extractor</h1>

      <textarea
        className="border p-3 w-full max-w-xl h-40"
        placeholder="Describe your injury..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br />

      <button
        className="mt-4 px-5 py-2 bg-black text-white rounded"
        onClick={handleSubmit}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {result && (
        <div className="mt-8 border p-5 max-w-xl">
          <h2 className="font-bold text-xl">Result</h2>

          <p>Injury: {result.injury_name}</p>

          <p>Body area: {result.body_area}</p>

          <p>
            Symptoms:
            {result.symptoms?.join(", ")}
          </p>

          <p>
            Possible causes:
            {result.possible_causes?.join(", ")}
          </p>
        </div>
      )}
    </main>
  );
}
