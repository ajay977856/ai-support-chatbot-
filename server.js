const express = require('express');
// નવીનતમ ગૂગલ જેમિની મોડ્યુલ લોડ કરવાની સાચી પદ્ધતિ
const { GoogleGenAI } = require('@google/generative-ai');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static('public'));

// ચેક કરો કે કી લોડ થાય છે કે નહીં, નહિતર ડિફોલ્ટ ખાલી સ્ટ્રિંગ આપો જેથી ક્રેશ ન થાય
const apiKey = process.env.GEMINI_API_KEY || "";

let ai = null;
try {
    if (apiKey) {
        ai = new GoogleGenAI({ apiKey: apiKey });
    }
} catch (e) {
    console.error("Gemini initialization error:", e);
}

// Chat API Endpoint
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        if (!message) return res.status(400).json({ error: "Message is required!" });
        if (!ai) return res.status(500).json({ error: "AI configuration is missing. Check GEMINI_API_KEY." });

        const model = ai.getGenerativeModel({ model: "gemini-1.5-flash" });
        
        const systemPrompt = "You are a helpful customer support AI assistant. Keep responses brief, clear, and polite.";
        const result = await model.generateContent(`${systemPrompt}\nUser: ${message}`);
        const response = await result.response;
        
        res.json({ reply: response.text() });
    } catch (error) {
        console.error("Error details:", error);
        res.status(500).json({ error: "Something went wrong on the server!" });
    }
});

// Render માટે પોર્ટ સેટિંગ
const PORT = process.env.PORT || 10000; 
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on port ${PORT}`));
