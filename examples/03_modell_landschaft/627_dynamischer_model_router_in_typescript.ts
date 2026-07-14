// Dynamischer Model-Router in TypeScript
// Quelle: chapters/03_modell_landschaft.tex (Zeile 627)
import OpenAI from "openai";
import Anthropic from "@anthropic-ai/sdk";

type Complexity = "simple" | "medium" | "complex" | "reasoning";

interface RouterConfig {
  simple: string;    // model name
  medium: string;
  complex: string;
  reasoning: string;
}

const config: RouterConfig = {
  simple: "gpt-4o-mini",
  medium: "claude-sonnet-4",
  complex: "gpt-4o",
  reasoning: "deepseek-r1",
};

async function routeRequest(
  prompt: string,
  complexity: Complexity,
): Promise<string> {
  const model = config[complexity];
  const client = new OpenAI();

  const resp = await client.chat.completions.create({
    model,
    messages: [{ role: "user", content: prompt }],
  });
  return resp.choices[0]?.message?.content ?? "";
}

