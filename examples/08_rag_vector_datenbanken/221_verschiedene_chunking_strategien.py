# Verschiedene Chunking-Strategien
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 221)
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
)

class ChunkingStrategy:
    @staticmethod
    def recursive(docs: list[str], chunk_size: int = 512,
                  overlap: int = 64) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        return splitter.split_documents(docs)

    @staticmethod
    def markdown_headers(docs: list[str]) -> list[str]:
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "H1"),
                ("##", "H2"),
                ("###", "H3"),
            ]
        )
        return splitter.split_text(docs[0])

    @staticmethod
    def semantic(chunks: list[str],
                 model: str = "gpt-4o-mini") -> list[str]:
        result = []
        current = ""
        for chunk in chunks:
            if current and len(current) > 256:
                result.append(current)
                current = chunk
            else:
                current += "\n" + chunk
        if current:
            result.append(current)
        return result

    @staticmethod
    def agentic(doc: str) -> list[str]:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": (
                    "Teile das Dokument in semantische Abschnitte. "
                    "Gib JSON: [{'content': '...', 'heading': '...'}]"
                )
            }, {
                "role": "user",
                "content": doc[:8000],
            }],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

