import streamlit as st
from agent import agent_chat

# Page config
st.set_page_config(page_title="Verité Research Assistant", layout="centered")

# Title and trial warning
st.title("Verity — Verité Research Assistant")
st.markdown(
    "<div style='color: white; font-size: 14px; margin-bottom: 10px;'>"
    "⚠️ You have only a limited number of trials as this is a free trial."
    "</div>",
    unsafe_allow_html=True
)

# Initialize chat session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# User input box
user_input = st.chat_input("Ask about Verité publications")

if user_input:
    response, sources = agent_chat(user_input)
    st.session_state.chat.append(("user", user_input))
    st.session_state.chat.append(("assistant", {"answer": response, "sources": sources}))

# Display chat messages
for role, msg in st.session_state.chat:
    if role == "user":
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: flex-end;
            margin-top: 10px;
        ">
            <div style="
                max-width: 70%;
                background-color: rgb(177, 56, 91);
                color: white;              
                padding: 10px 25px;
                border-radius: 25px;
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
        # Assistant answer
        st.markdown(f"""
        <div style="
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
                border-radius: 25px;
                border-bottom-left-radius: 0px;
                font-size: 16px;
            ">
                {msg['answer']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Show sources only for valid content-related answers
        valid_sources = [s for s in msg["sources"] if s.get("source")]
        if valid_sources:
            st.markdown('<div style="margin-left: 50px; margin-top:5px;"><b>Sources:</b></div>', unsafe_allow_html=True)
            for s in valid_sources:
                st.markdown(f"""
                <div style="margin-left: 60px; color:#cccccc; margin-bottom:10px;">
                    <b>{s['source']} - page {s['page']}</b><br>
                    {s['text']}
                </div>
                """, unsafe_allow_html=True)