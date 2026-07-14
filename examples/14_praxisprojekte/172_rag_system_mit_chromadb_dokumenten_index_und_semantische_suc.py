# RAG-System mit ChromaDB -- Dokumenten-Index und semantische Suche
# Quelle: chapters/14_praxisprojekte.tex (Zeile 172)
import streamlit as st
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pdfplumber import open as open_pdf

st.set_page_config(page_title="RAG Document Q&A", layout="wide")
st.title("Dokumenten-Fragebeantwortung")

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "db" not in st.session_state:
    st.session_state.db = None

st.sidebar.header("Dokumente")
uploaded = st.sidebar.file_uploader(
    "PDF oder TXT hochladen", type=["pdf", "txt"]
)
if uploaded and st.sidebar.button("Index erstellen"):
    with st.spinner("Lese und indiziere..."):
        text = ""
        if uploaded.name.endswith(".pdf"):
            with open_pdf(uploaded) as pdf:
                text = "\n".join(
                    page.extract_text()
                    for page in pdf.pages
                    if page.extract_text()
                )
        else:
            text = uploaded.getvalue().decode("utf-8")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=512, chunk_overlap=64,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_text(text)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        db = Chroma(
            collection_name="user_docs",
            embedding_function=embeddings,
            persist_directory="./chroma_db"
        )
        db.add_texts(chunks)
        st.session_state.db = db

        retriever = db.as_retriever(search_kwargs={"k": 5})

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Beantworte die Frage basierend auf den folgenden "
                       "Dokumenten. Wenn du es nicht weisst: "
                       "'Dazu habe ich keine Daten.' Zitiere die Quelle."),
            ("human", "Relevante Abschnitte:\n{context}\n\nFrage: {question}")
        ])

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        rag_chain = (
            {"context": retriever, "question": lambda x: x}
            | prompt | llm | StrOutputParser()
        )
        st.session_state.rag_chain = rag_chain

        st.sidebar.success("Index erstellt!")

if st.session_state.db and (
    prompt := st.text_input(
        "Stelle deine Frage:",
        placeholder="Was steht im Dokument ueber ...?"
    )
):
    with st.spinner("Durchsuche Dokumente..."):
        answer = st.session_state.rag_chain.invoke(prompt)

    st.markdown("---")
    st.subheader("Antwort:")
    st.markdown(answer)

