const express = require('express');
const { GoogleGenAI } = require('@google/generative-ai');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(express.json());

// ફ્રન્ટએન્ડ ફોલ્ડર
app.use(express.static(path.join(__dirname, 'public')));

const apiKey = process.env.GEMINI_API_KEY || "";
let ai = null;

if (apiKey) {
    // સાચી પદ્ધતિ: GoogleGenAI નો નવો ઓબ્જેક્ટ બનાવવો
    ai = new GoogleGenAI({ apiKey: apiKey });
}

app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        if (!message) return res.status(400).json({ error: "Message required" });
        if (!ai) return res.status(500).json({ error: "API Key missing" });

        const model = ai.getGenerativeModel({ model: "gemini-1.5-flash" });
        const systemPrompt = "You are a helpful customer support AI assistant. Keep responses brief and polite.";
        
        const result = await model.generateContent(`${systemPrompt}\nUser: ${message}`);
        const response = await result.response;
        
        res.json({ reply: response.text() });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Server Error" });
    }
});

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on port ${PORT}`));
