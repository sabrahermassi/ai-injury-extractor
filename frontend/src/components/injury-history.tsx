"use client";

import { useEffect, useState } from "react";
import { getInjuryHistory } from "@/lib/api";
import { InjuryHistoryEntry } from "@/lib/injury-schema";

export function InjuryHistory() {
  const [injuries, setInjuries] = useState<InjuryHistoryEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchHistory() {
      try {
        const data = await getInjuryHistory();
        setInjuries(data);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load injury history",
        );
      } finally {
        setLoading(false);
      }
    }

    fetchHistory();
  }, []);

  if (loading) {
    return <p>Loading injury history...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (injuries.length === 0) {
    return <p>No injury history found.</p>;
  }

  return (
    <div>
      <h2>Injury History</h2>

      {injuries.map((injury) => (
        <div key={injury.entryId}>
          <h3>{injury.extractedData.injury_name}</h3>

          <p>Body area: {injury.extractedData.body_area}</p>

          <p>Pain level: {injury.extractedData.pain_level ?? "Not provided"}</p>

          <p>Symptoms: {injury.extractedData.symptoms.join(", ")}</p>

          <p>
            Possible causes: {injury.extractedData.possible_causes.join(", ")}
          </p>

          <p>Date: {new Date(injury.timestamp).toLocaleDateString()}</p>

          <hr />
        </div>
      ))}
    </div>
  );
}
