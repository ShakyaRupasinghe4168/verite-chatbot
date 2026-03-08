import os
import streamlit as st
from agent import agent_chat
from memory_store import load_memory, save_memory

if "chat" not in st.session_state:
    st.session_state.chat = []

st.set_page_config(page_title="Verité Research Assistant", layout="centered")

st.markdown(
    """
    <div style="
        background-color: rgb(123, 9, 42);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    ">
        Verity — The Research Assistant Chatbot
    </div>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown(
        """
        <div style="
            color: white;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 10px;
        ">
            ⚠️ You have only a limited number of trials as this is a free trial.
        </div>
        """,
        unsafe_allow_html=True
    )
    
col1, col2, col3 = st.columns([1, 2, 1])  
with col2:
    c1, c2 = st.columns(2, gap="large") 
    with c1:
        if st.button("Clear Chat", help="Clears the chat messages from the UI only. Memory is preserved."):
            st.session_state.chat = []  
    with c2:
        if st.button("Clear memory", help="Clears the UI and deletes all saved chat memory permanently."):
            st.session_state.chat = []  
            if os.path.exists("memory/chat_memory.json"):
                os.remove("memory/chat_memory.json")  
            st.experimental_rerun() 

user_input = st.chat_input("Ask about Verité publications")

if user_input:
    memory = load_memory()
    response, sources = agent_chat(user_input)
    memory.append({"role": "user", "content": user_input})
    memory.append({"role": "assistant", "content": response})
    save_memory(memory)

    st.session_state.chat.append(("user", user_input))
    st.session_state.chat.append(("assistant", {"answer": response, "sources": sources}))

for idx, (role, msg) in enumerate(st.session_state.chat):
    container_id = f"msg_{idx}"  

    if role == "user":
        st.markdown(f"""
        <div id="{container_id}" style="
            display: flex;
            justify-content: flex-end;
            margin-top: 10px;
        ">
            <div style="
                max-width: 70%;
                background-color: rgb(177, 56, 91);
                color: white;              
                padding: 10px 25px;
                border-radius: 10px;
                border-bottom-right-radius: 0px;
                font-size: 16px;
            ">
                {msg}
            </div>
            <div style="margin-left: 10px; display:flex; align-items:center;">
                <img src="https://img.icons8.com/fluency/48/000000/user-male-circle.png" width="30"/>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div id="{container_id}" style="
            display: flex;
            justify-content: flex-start;
            margin-top: 10px;
        ">
            <div style="margin-right: 10px; display:flex; align-items:center;">
                <img src="https://img.icons8.com/fluency/48/000000/chatbot.png" width="30"/>
            </div>
            <div style="
                max-width: 70%;
                background-color: #333333;  
                color: white; 
                padding: 10px 25px;
                border-radius: 10px;
                border-bottom-left-radius: 0px;
                font-size: 16px;
                margin-bottom: 10px;
            ">
                {msg['answer']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        valid_sources = [s for s in msg["sources"] if s.get("source")]
        if valid_sources:
            for idx_s, s in enumerate(valid_sources, start=1):
                with st.expander(f"Source [{idx_s}]: {s['source']} - page {s['page']}", expanded=False):
                    st.markdown(f"""
                        <div style="
                            background-color: #333333;
                            color: white;
                            padding: 10px 25px;
                            border-radius: 15px;
                            border: 2px solid rgb(177, 56, 91);
                            font-size: 15px;
                            margin-bottom: 5px;
                        ">
                            {s['text']}
                        </div>
                    """, unsafe_allow_html=True)

st.markdown("""
    <script>
        const messages = document.querySelectorAll('[id^="msg_"]');
        if (messages.length > 0) {
            messages[messages.length - 1].scrollIntoView({behavior: "smooth"});
        }
    </script>
""", unsafe_allow_html=True)