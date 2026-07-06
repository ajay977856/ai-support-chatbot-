import streamlit as st
import google.generativeai as genai

# UI ની ડિઝાઈન સેટ કરવા માટે
st.set_page_config(page_title="AI Support Bot", page_icon="🤖")
st.title("🤖 AI Customer Support Assistant")
st.write("નમસ્તે! હું તમારી શું મદદ કરી શકું?")

# Gemini API Key સેટ કરો (તમારી સાચી કી અહીં મૂકજો)
GEMINI_API_KEY = "AQ.Ab8RN6KHCVz0OTdMva6Rx4WVYHFlQ7Xqjc0OsuOAzPSltzTQTQ"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Chat history સેવ કરવા માટે
if "messages" not in st.session_state:
    st.session_state.messages = []

# જૂની ચેટ સ્ક્રીન પર બતાવવા માટે
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# યુઝર પાસેથી ઇનપુટ લેવા માટે
if user_input := st.chat_input("અહીં ટાઈપ કરો..."):
    # યુઝરનો મેસેજ સ્ક્રીન પર બતાવો
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI પાસે જવાબ લેવા માટે
    with st.chat_message("assistant"):
        with st.spinner("વિચારી રહ્યો છું..."):
            try:
                system_instruction = "Tame ek helpful Customer Support Assistant chho. User na prashno na javab saral ane polite bhasha ma aapo."
                full_prompt = f"{system_instruction}\nUser: {user_input}\nAssistant:"
                
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error આવી: {e}")
