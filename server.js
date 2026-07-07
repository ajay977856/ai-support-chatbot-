const express = require('express');
const { GoogleGenAI } = require('@google/genai');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(express.json());

// આ લાઇનથી ફ્રન્ટએન્ડ ફોલ્ડર બરાબર લોડ થશે
app.use(express.static(path.join(__dirname, 'public')));

const apiKey = process.env.GEMINI_API_KEY || "";
const ai = apiKey ? new GoogleGenAI({ apiKey: apiKey }) : null;

app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        if (!message) return res.status(400).json({ error: "Message required" });
        if (!ai) return res.status(500).json({ error: "API Key Missing" });

        // નવી લાઈબ્રેરી મુજબ સાચો મોડેલ કૉલ
        const response = await ai.models.generateContent({
            model: 'gemini-1.5-flash',
            contents: `You are a helpful customer support AI assistant. Keep responses brief and polite.\nUser: ${message}`,
        });

        res.json({ reply: response.text });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Server Error" });
    }
});

// જો હોમ પેજ ડાયરેક્ટ લોડ ન થાય તો આ રૂટ મદદ કરશે
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on port ${PORT}`));
