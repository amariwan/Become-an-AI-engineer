// Streaming-Client in TypeScript
// Quelle: chapters/05_openai_plattform.tex (Zeile 364)
import OpenAI from "openai";

const client = new OpenAI();

async function streamChat(message: string) {
  const stream = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: message }],
    stream: true,
  });

  let fullText = "";
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || "";
    fullText += content;
    updateUI(fullText);  // Echtzeit-Update im Browser
  }
}

