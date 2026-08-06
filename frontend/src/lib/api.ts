const API_URL = `${process.env.NEXT_PUBLIC_API_URL}/extract`;

export async function extractInjury(text: string) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to extract injury");
  }

  return response.json();
}
