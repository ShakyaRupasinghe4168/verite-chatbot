import streamlit as st
from agent import agent_chat

st.set_page_config(page_title="Verité Research Assistant", layout="centered")

st.title("Verité — Verité Research Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Ask about Verité publications")

if user_input:
    response, sources = agent_chat(user_input)
    st.session_state.chat.append(("user", user_input))
    st.session_state.chat.append(("assistant", {"answer": response, "sources": sources}))

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


        if msg["sources"]:
            st.markdown('<div style="margin-left: 50px; margin-top:5px;"><b>Sources:</b></div>', unsafe_allow_html=True)
            for s in msg["sources"]:
                st.markdown(f'<div style="margin-left: 60px; color:#cccccc;">- {s}</div>', unsafe_allow_html=True)