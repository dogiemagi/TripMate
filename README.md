# VoyageAI - Multimodal Travel Intelligence Platform


🌐 **Live Application:** [https://tripmate-xqei.onrender.com/](https://tripmate-xqei.onrender.com/)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-voyage--ai--platform.onrender.com-06b6d4?style=for-the-badge&logo=render&logoColor=white)](https://voyage-ai-platform.onrender.com/)
[![API Docs](https://img.shields.io/badge/API%20Docs-Swagger%20UI-3b82f6?style=for-the-badge&logo=fastapi&logoColor=white)](https://voyage-ai-platform.onrender.com/docs)

---

## 🌟 Core Feature Matrix

1. 📸 **Multimodal Vision AI Hub**
   - Landmark recognition, historical background, visiting window, and photography angles.
   - Foreign restaurant menu and dish translator with allergen warnings (gluten, dairy, nuts).
   - Powered by Gemini 2.5 Vision with robust hybrid neural fallback.

2. 🌦️ **Global Weather & Climate Radar**
   - Live atmospheric conditions, 7-day temperature forecasts, UV index, and precipitation probabilities.
   - Travel climate suitability index (0-100) and packing recommendations.

3. 🗺️ **AI Smart Itinerary Planner**
   - Day-by-day sequenced travel schedules with timing, duration, and approximate cost.
   - Interactive dark-mode **Leaflet.js** map with geolocation markers.
   - Pacing and budget tier customization (Backpacker, Moderate, Premium, Luxury).

4. 🍜 **Gastronomy & Culinary Guide**
   - Signature authentic dishes with phonetic pronunciations.
   - Dietary safety filters (Vegetarian, Vegan, Gluten-Free, Halal).
   - Street food etiquette and local dining customs.

5. 💱 **Currency FX & Travel Budget Estimator**
   - Live foreign exchange rate converter across all major global currencies.
   - Realistic multi-day trip budget calculator with category expense breakdown.

6. 🎒 **Smart Packing Assistant**
   - Climate, season, and activity-aware checklist generator.
   - Interactive checkbox state persistence.

7. 🗣️ **Multilingual Audio Phrasebook**
   - Essential greetings, dining, transport, and emergency phrases.
   - Native Web Speech API audio synthesis for live spoken pronunciation.

---

## 🚀 Local Development Setup

### 1. Requirements
- Python 3.10+
- Pip

### 2. Install Dependencies
```bash
cd D:\voyage-ai-platform
pip install -r requirements.txt
```

### 3. Run FastAPI Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at `http://localhost:8000` to view the web app, or `http://localhost:8000/docs` for the interactive Swagger API documentation.

---

## ☁️ Deploying to Render

This project is pre-configured for Render:
- **`render.yaml`**: Infrastructure-as-code blueprint.
- **`Dockerfile`**: Containerized deployment option.
- **`Procfile`**: Native Python web service runner.

### Steps to Deploy:
1. Push this repository to GitHub or GitLab.
2. In the [Render Dashboard](https://dashboard.render.com), click **New +** -> **Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml` and deploy your web service!
