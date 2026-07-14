// AI Engineer: Ticket-Summary in TypeScript
// Quelle: chapters/01_ai_engineer_rolle.tex (Zeile 378)
import OpenAI from "openai";

const client = new OpenAI();

interface TicketSummary {
  category: string;
  sentiment: string;
  summary: string;
  keyIssues: string[];
}

async function summarizeTicket(ticketText: string): Promise<TicketSummary> {
  const resp = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "Du bist ein Assistent." },
      { role: "user", content: `Analysiere: ${ticketText}` },
    ],
    response_format: { type: "json_object" },
    temperature: 0.1,
  });
  return JSON.parse(resp.choices[0]?.message?.content ?? "{}");
}

const summary = await summarizeTicket("Betreff: Rechnung falsch berechnet");
console.log(`Kategorie: ${summary.category}`);

