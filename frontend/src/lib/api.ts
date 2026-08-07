const API_URL = process.env.NEXT_PUBLIC_API_URL;

import { InjuryExtraction, InjuryHistoryEntry } from "./injury-schema";

export async function extractInjury(text: string): Promise<InjuryExtraction> {
  if (!API_URL) {
    throw new Error("NEXT_PUBLIC_API_URL is not configured");
  }

  const response = await fetch(`${API_URL}/extract`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || "Failed to extract injury");
  }

  const data = await response.json();

  return {
    injuryName: data.injury_name,
    bodyArea: data.body_area,
    painLevel: data.pain_level,
    symptoms: data.symptoms,
    possibleCauses: data.possible_causes,
  };
}

export async function getInjuryHistory(): Promise<InjuryHistoryEntry[]> {
  if (!API_URL) {
    throw new Error("NEXT_PUBLIC_API_URL is not configured");
  }

  const response = await fetch(`${API_URL}/injuries`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || "Failed to fetch injury history");
  }

  const data = await response.json();

  return data;
}
