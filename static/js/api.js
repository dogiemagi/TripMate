/**
 * VoyageAI - Client API Service Layer
 */
const API = {
  baseUrl: window.location.origin,

  async getWeather(city = 'Delhi', startDate = null, endDate = null, days = 7) {
    let url = `${this.baseUrl}/api/v1/weather?city=${encodeURIComponent(city)}&days=${days}`;
    if (startDate) url += `&start_date=${encodeURIComponent(startDate)}`;
    if (endDate) url += `&end_date=${encodeURIComponent(endDate)}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error('Weather API request failed');
    return await res.json();
  },

  async analyzeVision(file, mode = 'landmark', prompt = '') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('mode', mode);
    if (prompt) formData.append('prompt', prompt);

    const res = await fetch(`${this.baseUrl}/api/v1/vision/analyze`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) throw new Error('Vision analysis failed');
    return await res.json();
  },

  async generateItinerary(payload) {
    const res = await fetch(`${this.baseUrl}/api/v1/itinerary/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Itinerary generation failed');
    return await res.json();
  },

  async getFood(city = 'Delhi', dietaryPreferences = []) {
    const res = await fetch(`${this.baseUrl}/api/v1/food/explore`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ city, dietary_preferences: dietaryPreferences })
    });
    if (!res.ok) throw new Error('Food API request failed');
    return await res.json();
  },

  async convertCurrency(from, to, amount) {
    const res = await fetch(`${this.baseUrl}/api/v1/budget/convert`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ from_currency: from, to_currency: to, amount: parseFloat(amount) })
    });
    if (!res.ok) throw new Error('Currency conversion failed');
    return await res.json();
  },

  async getBudgetEstimate(city = 'Delhi', days = 5, style = 'midrange') {
    const res = await fetch(`${this.baseUrl}/api/v1/budget/estimate?city=${encodeURIComponent(city)}&days=${days}&style=${style}`);
    if (!res.ok) throw new Error('Budget estimation failed');
    return await res.json();
  },

  async generatePacking(payload) {
    const res = await fetch(`${this.baseUrl}/api/v1/packing/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Packing checklist generation failed');
    return await res.json();
  },

  async getPhrases(language = 'Hindi', category = 'All') {
    const res = await fetch(`${this.baseUrl}/api/v1/phrasebook/phrases`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language, category })
    });
    if (!res.ok) throw new Error('Phrasebook request failed');
    return await res.json();
  },

  async translatePhrase(text, sourceLanguage = 'English', targetLanguage = 'Tamil') {
    const res = await fetch(`${this.baseUrl}/api/v1/phrasebook/translate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        source_language: sourceLanguage,
        target_language: targetLanguage
      })
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || errData.message || 'Translation request failed');
    }
    return await res.json();
  },

  async translateVoice(audioBlob, sourceLanguage = 'English', targetLanguage = 'Tamil') {
    const formData = new FormData();
    formData.append('audio_file', audioBlob, 'recording.wav');
    formData.append('source_language', sourceLanguage);
    formData.append('target_language', targetLanguage);

    const res = await fetch(`${this.baseUrl}/api/v1/phrasebook/voice-translate`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || errData.message || 'Voice translation request failed');
    }
    return await res.json();
  },

  async sendChatMessage(messages, destination = '') {
    const res = await fetch(`${this.baseUrl}/api/v1/chat/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages, destination })
    });
    if (!res.ok) throw new Error('Chat request failed');
    return await res.json();
  }
};

