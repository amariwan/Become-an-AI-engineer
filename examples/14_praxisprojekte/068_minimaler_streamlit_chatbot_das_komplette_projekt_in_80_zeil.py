# Minimaler Streamlit-Chatbot -- das komplette Projekt in ~80 Zeilen
# Quelle: chapters/14_praxisprojekte.tex (Zeile 68)
import streamlit as st
import openai
from tiktoken import encoding_for_model

st.set_page_config(page_title="AI Chatbot", page_icon=":robot_face:")
st.title("Mein AI-Assistent")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False

if not st.session_state.api_key_set:
    api_key = st.text_input("OpenAI API Key:", type="password")
    if api_key:
        client = openai.OpenAI(api_key=api_key)
        st.session_state.api_key_set = True

if st.session_state.api_key_set:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Schreibe eine Nachricht..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        encoding = encoding_for_model("gpt-4o-mini")
        total_tokens = sum(
            len(encoding.encode(m["content"]))
            for m in st.session_state.messages
        )

        if total_tokens > 120_000:
            st.warning(f"Kontext-Limit nahe! ({total_tokens}/128000 Tokens)")
            st.session_state.messages = st.session_state.messages[-5:]

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            for chunk in client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
                max_tokens=1024,
            ):
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "...")

            message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

st.sidebar.title("Info")
st.sidebar.info(f"Token-Verbrauch: {total_tokens:,} / 128000")
st.sidebar.text("Gewaehlt: gpt-4o-mini (EUR0,0015/1K Input)")

