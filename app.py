import streamlit as st
import google.generativeai as genai

# ૧. વેબસાઈટની ડિઝાઇન અને ટાઈટલ સેટ કરવા માટે
st.set_page_config(page_title="AI Support Bot", page_icon="🤖")
st.title("🤖 AI Customer Support Assistant")
st.write("નમસ્તે! હું તમારી શું મદદ કરી શકું?")

# ૨. ગૂગલ આઈ સ્ટુડિયોમાંથી લાવેલી નવી API Key અહીં મૂકો
# (ચેક કરી લેજો કે કી સાચી હોય, નહિતર 401 એરર આવશે)
GEMINI_API_KEY = "AQ.Ab8RN6KHCVz0OTdMva6Rx4WVYHFlQ7Xqjc0OsuOAzPSltzTQTQ"

# ૩. જેમીની મોડેલ કન્ફિગર કરો
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ૪. ચેટ હિસ્ટ્રી (જૂની ચેટ) સાચવવા માટે
if "messages" not in st.session_state:
    st.session_state.messages = []

# ૫. જૂની ચેટને સ્ક્રીન પર બતાવવા માટે
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ૬. જ્યારે યુઝર નવો મેસેજ ટાઈપ કરીને મોકલે ત્યારે
if user_input := st.chat_input("અહીં ટાઈપ કરો..."):
    
    # યુઝરનો મેસેજ સ્ક્રીન પર બતાવો
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # જેમીની AI પાસે જવાબ લેવા માટે
    with st.chat_message("assistant"):
        with st.spinner("વિચારી રહ્યો છું..."):
            try:
                # બોટને ઓર્ડર આપવા માટે સિસ્ટમ ઇન્સ્ટ્રક્શન
                system_instruction = "Tame ek helpful Customer Support Assistant chho. User na prashno na javab saral ane polite bhasha ma aapo."
                full_prompt = f"{system_instruction}\nUser: {user_input}\nAssistant:"
                
                # AI નો જવાબ જનરેટ કરવો
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                
                # AI નો જવાબ હિસ્ટ્રીમાં સેવ કરવો
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error આવી: {e}")