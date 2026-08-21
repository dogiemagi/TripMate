/**
 * VoyageAI - Main Application Controller
 */

let mapInstance = null;
let mapMarkers = [];

document.addEventListener('DOMContentLoaded', () => {
  initLucideIcons();
  initNavigationTabs();
  initMultimodalVision();
  initWeatherDashboard();
  initItineraryPlanner();
  initFoodExplorer();
  initCurrencyBudget();
  initPackingAssistant();
  initPhrasebook();
  initGlobalCitySearch();

  // Trigger initial loads
  loadWeatherData('Tokyo');
  loadFoodData('Rome');
  loadPhrases('Japanese');
});

function initLucideIcons() {
  if (window.lucide) {
    lucide.createIcons();
  }
}

// ---------------------------------------------------------
// Navigation Tabs Controller
// ---------------------------------------------------------
function initNavigationTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      tabButtons.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const activePane = document.getElementById(targetTab);
      if (activePane) {
        activePane.classList.add('active');
      }

      if (targetTab === 'tab-itinerary' && mapInstance) {
        setTimeout(() => { mapInstance.invalidateSize(); }, 200);
      }
      initLucideIcons();
    });
  });
}

// ---------------------------------------------------------
// Multimodal Vision Handler
// ---------------------------------------------------------
function initMultimodalVision() {
  const dropzone = document.getElementById('vision-dropzone');
  const fileInput = document.getElementById('vision-file-input');
  const previewBox = document.getElementById('vision-preview-box');
  const previewImg = document.getElementById('vision-preview-img');
  const analyzeBtn = document.getElementById('vision-analyze-btn');
  const resultsContainer = document.getElementById('vision-results');
  let selectedFile = null;

  dropzone.addEventListener('click', () => fileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  });

  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  });

  function handleFile(file) {
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (event) => {
      previewImg.src = event.target.result;
      previewBox.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }

  // Sample Chips
  document.querySelectorAll('.sample-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const sampleName = chip.getAttribute('data-sample');
      document.getElementById('vision-prompt').value = `Analyze sample: ${sampleName}`;
      const canvas = document.createElement('canvas');
      canvas.width = 400; canvas.height = 300;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#1e293b'; ctx.fillRect(0, 0, 400, 300);
      ctx.fillStyle = '#38bdf8'; ctx.font = '20px Outfit';
      ctx.fillText(sampleName, 50, 150);
      canvas.toBlob((blob) => {
        const file = new File([blob], `${sampleName.toLowerCase().replace(/\s+/g, '_')}.jpg`, { type: 'image/jpeg' });
        handleFile(file);
      });
    });
  });

  analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) {
      alert('Please upload or select an image first.');
      return;
    }

    const mode = document.getElementById('vision-mode-select').value;
    const prompt = document.getElementById('vision-prompt').value;

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `<div class="spinner"></div> Analyzing Image...`;

    try {
      const data = await API.analyzeVision(selectedFile, mode, prompt);
      displayVisionResults(data);
    } catch (err) {
      resultsContainer.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);">❌ Vision analysis failed. ${err.message}</div>`;
    } finally {
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = `<i data-lucide="sparkles"></i> Run AI Multimodal Analysis`;
      initLucideIcons();
    }
  });

  function displayVisionResults(data) {
    const rawMarkdown = data.analysis_markdown || '';
    const formattedHtml = formatMarkdown(rawMarkdown);

    resultsContainer.innerHTML = `
      <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h2 style="font-size: 1.35rem; font-weight: 700; color: #fff;">${data.title || 'Visual Recognition'}</h2>
            <p style="color: var(--accent-cyan); font-size: 0.88rem;">${data.location || data.category || 'Multimodal Intelligence'}</p>
          </div>
          <span class="brand-badge">${data.engine || 'Voyage AI'}</span>
        </div>
        <div class="vision-results-content">
          ${formattedHtml}
        </div>
      </div>
    `;
    initLucideIcons();
  }
}

// ---------------------------------------------------------
// Weather Dashboard Handler
// ---------------------------------------------------------
function initWeatherDashboard() {
  const searchBtn = document.getElementById('weather-search-btn');
  const cityInput = document.getElementById('weather-city-input');

  searchBtn.addEventListener('click', () => {
    const city = cityInput.value.trim() || 'Tokyo';
    loadWeatherData(city);
  });

  cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const city = cityInput.value.trim() || 'Tokyo';
      loadWeatherData(city);
    }
  });
}

async function loadWeatherData(city) {
  const container = document.getElementById('weather-content');
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><div class="spinner"></div><p style="margin-top:1rem; color:var(--text-secondary);">Fetching atmospheric radar for ${city}...</p></div>`;

  try {
    const data = await API.getWeather(city, 7);
    const curr = data.current;

    let forecastHtml = '';
    (data.forecast || []).forEach(f => {
      forecastHtml += `
        <div class="forecast-card">
          <div style="font-weight: 600; font-size: 0.9rem; color: #fff;">${f.day_name}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${f.date}</div>
          <div class="forecast-icon"><i data-lucide="${f.icon || 'sun'}"></i></div>
          <div style="font-weight: 700; font-size: 1.1rem; color: #fff;">${f.temp_max_c}°C</div>
          <div style="font-size: 0.8rem; color: var(--text-muted);">${f.temp_min_c}°C</div>
          <div style="font-size: 0.72rem; color: var(--accent-cyan); margin-top: 0.5rem;">💧 ${f.precipitation_chance_pct}% rain</div>
        </div>
      `;
    });

    container.innerHTML = `
      <div class="weather-hero">
        <div>
          <span class="brand-badge">${data.country}</span>
          <h2 style="font-size: 2.2rem; font-weight: 800; margin-top: 0.35rem;">${data.city}</h2>
          <p style="color: var(--text-secondary); font-size: 1rem; margin-bottom: 1rem;">${curr.condition}</p>
          <div>
            <span class="weather-metric-badge"><i data-lucide="wind"></i> ${curr.windspeed_kmh} km/h</span>
            <span class="weather-metric-badge"><i data-lucide="shield-check"></i> Travel Score: ${data.travel_climate_score}/100</span>
          </div>
        </div>
        <div style="text-align: right;">
          <div class="weather-hero-temp">${curr.temperature_c}°C</div>
          <div style="color: var(--text-secondary); font-size: 1.1rem;">${curr.temperature_f}°F</div>
        </div>
      </div>

      <div class="glass-card" style="margin-bottom: 1.5rem;">
        <h3 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; display:flex; align-items:center; gap: 0.5rem;">
          <i data-lucide="compass" style="color: var(--accent-cyan);"></i> AI Travel Climate Advisory
        </h3>
        <p style="color: var(--text-secondary); font-size: 0.95rem;">${curr.advice}</p>
        <p style="color: var(--accent-cyan); font-size: 0.88rem; margin-top: 0.5rem;"><strong>🎒 Packing Tip:</strong> ${data.packing_recommendation}</p>
      </div>

      <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 1rem;">7-Day Travel Outlook</h3>
      <div class="grid-4" style="grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));">
        ${forecastHtml}
      </div>
    `;
    initLucideIcons();
  } catch (err) {
    container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);">❌ Failed to load weather for ${city}.</div>`;
  }
}

// ---------------------------------------------------------
// Smart Itinerary Planner & Map
// ---------------------------------------------------------
function initItineraryPlanner() {
  const generateBtn = document.getElementById('itinerary-generate-btn');
  generateBtn.addEventListener('click', generateTripPlan);

  const mapElement = document.getElementById('itinerary-map');
  if (mapElement && !mapInstance && window.L) {
    mapInstance = L.map('itinerary-map').setView([35.6762, 139.6503], 12);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap & CartoDB',
      maxZoom: 19
    }).addTo(mapInstance);
  }
}

async function generateTripPlan() {
  const dest = document.getElementById('itinerary-dest').value.trim() || 'Tokyo, Japan';
  const days = parseInt(document.getElementById('itinerary-days').value, 10) || 3;
  const style = document.getElementById('itinerary-style').value;
  const pace = document.getElementById('itinerary-pace').value;
  const budget = document.getElementById('itinerary-budget').value;

  const btn = document.getElementById('itinerary-generate-btn');
  const container = document.getElementById('itinerary-results');

  btn.disabled = true;
  btn.innerHTML = `<div class="spinner"></div> Synthesizing Day-by-Day Route...`;

  try {
    const data = await API.generateItinerary({
      destination: dest,
      days: days,
      travel_style: style,
      pace: pace,
      budget_level: budget,
      interests: ["Sightseeing", "Food", "Culture", "Photography"]
    });

    renderItinerary(data);
  } catch (err) {
    container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);">❌ Could not generate itinerary: ${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i data-lucide="sparkles"></i> Generate AI Itinerary`;
    initLucideIcons();
  }
}

function renderItinerary(data) {
  const container = document.getElementById('itinerary-results');
  let daysHtml = '';
  const mapCoords = [];

  mapMarkers.forEach(m => mapInstance.removeLayer(m));
  mapMarkers = [];

  (data.days || []).forEach(day => {
    let actHtml = '';
    (day.activities || []).forEach(act => {
      if (act.lat && act.lon && mapInstance) {
        mapCoords.push([act.lat, act.lon]);
        const marker = L.marker([act.lat, act.lon])
          .addTo(mapInstance)
          .bindPopup(`<b>${act.title}</b><br>${act.time} | Cost: ${act.cost}`);
        mapMarkers.push(marker);
      }

      actHtml += `
        <div class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <span style="font-weight: 700; color: var(--accent-cyan); font-size: 0.85rem;">⏰ ${act.time}</span>
              <span class="activity-badge">${act.category}</span>
            </div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 0.35rem;">${act.title}</h4>
            <p style="color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 0.5rem;">${act.desc}</p>
            <div style="display: flex; gap: 1rem; font-size: 0.78rem; color: var(--text-muted);">
              <span>⏳ Duration: ${act.duration}</span>
              <span>💵 Approx. Cost: ${act.cost}</span>
            </div>
          </div>
        </div>
      `;
    });

    daysHtml += `
      <div class="glass-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h3 style="font-size: 1.2rem; font-weight: 800; color: #fff;">${day.theme}</h3>
            <p style="color: var(--accent-cyan); font-size: 0.85rem;">🌟 Highlights: ${day.highlight}</p>
          </div>
          <span class="brand-badge">Day ${day.day}</span>
        </div>
        <div class="timeline-container">
          ${actHtml}
        </div>
      </div>
    `;
  });

  container.innerHTML = `
    <div class="glass-card" style="margin-bottom: 1.5rem; background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1));">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
          <h2 style="font-size: 1.5rem; font-weight: 800;">${data.destination} - ${data.total_days} Day Masterplan</h2>
          <p style="color: var(--text-secondary); font-size: 0.9rem;">Style: ${data.travel_style} | Pace: ${data.pace} | Est. Total: $${data.estimated_total_cost_usd} USD</p>
        </div>
        <span class="brand-badge">${data.summary.recommended_transit_pass}</span>
      </div>
      <p style="color: #94a3b8; font-size: 0.88rem; margin-top: 0.75rem;">💡 ${data.summary.smart_tip}</p>
    </div>
    ${daysHtml}
  `;

  if (mapCoords.length > 0 && mapInstance) {
    const bounds = L.latLngBounds(mapCoords);
    mapInstance.fitBounds(bounds, { padding: [40, 40] });
  }
  initLucideIcons();
}

// ---------------------------------------------------------
// Gastronomy & Food Explorer
// ---------------------------------------------------------
function initFoodExplorer() {
  const searchBtn = document.getElementById('food-search-btn');
  const cityInput = document.getElementById('food-city-input');

  searchBtn.addEventListener('click', () => {
    const city = cityInput.value.trim() || 'Rome';
    loadFoodData(city);
  });

  cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const city = cityInput.value.trim() || 'Rome';
      loadFoodData(city);
    }
  });

  document.querySelectorAll('.diet-filter-cb').forEach(cb => {
    cb.addEventListener('change', () => {
      const city = cityInput.value.trim() || 'Rome';
      loadFoodData(city);
    });
  });
}

async function loadFoodData(city) {
  const container = document.getElementById('food-content');
  const activeDiets = Array.from(document.querySelectorAll('.diet-filter-cb:checked')).map(cb => cb.value);

  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><div class="spinner"></div><p style="margin-top:1rem; color:var(--text-secondary);">Curating culinary map for ${city}...</p></div>`;

  try {
    const data = await API.getFood(city, activeDiets);
    let dishesHtml = '';

    (data.signature_dishes || []).forEach(d => {
      const pills = (d.dietary || []).map(tag => `<span class="dish-diet-pill">${tag}</span>`).join(' ');
      dishesHtml += `
        <div class="dish-card">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
              <h4 style="font-size: 1.15rem; font-weight: 700; color: #fff;">${d.name}</h4>
              <span style="font-weight: 700; color: var(--accent-amber); font-size: 0.9rem;">${d.price_range}</span>
            </div>
            <div style="font-size: 0.78rem; color: var(--accent-cyan); margin-bottom: 0.5rem;">🗣️ Pronunciation: <i>${d.pronunciation}</i></div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.6;">${d.description}</p>
          </div>
          <div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.75rem;">${pills}</div>
            <div style="font-size: 0.8rem; color: #93c5fd;">📍 <strong>Top Spot:</strong> ${d.must_try_spot}</div>
          </div>
        </div>
      `;
    });

    let tipsHtml = (data.street_food_tips || []).map(t => `<li>${t}</li>`).join('');

    container.innerHTML = `
      <div class="glass-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <span class="brand-badge">Foodie Score: ${data.foodie_rating}/10</span>
            <h2 style="font-size: 1.6rem; font-weight: 800; margin-top: 0.35rem;">${data.city} Gastronomy Guide</h2>
            <p style="color: var(--text-secondary); font-size: 0.95rem;">${data.culinary_tradition}</p>
          </div>
        </div>
      </div>

      <div class="grid-2" style="margin-bottom: 1.5rem;">
        ${dishesHtml}
      </div>

      <div class="glass-card">
        <h3 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 0.75rem; display:flex; align-items:center; gap: 0.5rem;">
          <i data-lucide="utensils" style="color: var(--accent-amber);"></i> Street Food & Dining Etiquette
        </h3>
        <ul style="padding-left: 1.25rem; color: var(--text-secondary); line-height: 1.7;">
          ${tipsHtml}
        </ul>
      </div>
    `;
    initLucideIcons();
  } catch (err) {
    container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);">❌ Failed to load culinary recommendations.</div>`;
  }
}

// ---------------------------------------------------------
// Currency & Budget Assistant
// ---------------------------------------------------------
function initCurrencyBudget() {
  const convertBtn = document.getElementById('currency-convert-btn');
  convertBtn.addEventListener('click', async () => {
    const from = document.getElementById('currency-from').value;
    const to = document.getElementById('currency-to').value;
    const amount = document.getElementById('currency-amount').value || 100;

    const resultBox = document.getElementById('currency-result-box');
    resultBox.innerHTML = `<div class="spinner"></div>`;

    try {
      const data = await API.convertCurrency(from, to, amount);
      resultBox.innerHTML = `
        <div style="font-size: 0.88rem; color: var(--text-muted);">${data.amount} ${data.from_currency} =</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: var(--accent-cyan); line-height: 1.1; margin: 0.35rem 0;">
          ${data.symbol}${data.converted_amount.toLocaleString()} <span style="font-size: 1rem; color: #fff;">${data.to_currency}</span>
        </div>
        <div style="font-size: 0.78rem; color: var(--text-secondary);">1 ${data.from_currency} = ${data.exchange_rate} ${data.to_currency}</div>
      `;
    } catch (err) {
      resultBox.innerHTML = `<span style="color: var(--accent-rose);">Conversion failed</span>`;
    }
  });

  const estimateBtn = document.getElementById('budget-estimate-btn');
  estimateBtn.addEventListener('click', async () => {
    const city = document.getElementById('budget-city').value || 'Tokyo';
    const days = parseInt(document.getElementById('budget-days').value, 10) || 5;
    const style = document.getElementById('budget-style').value;
    const breakdownBox = document.getElementById('budget-breakdown-content');

    breakdownBox.innerHTML = `<div class="spinner"></div>`;

    try {
      const data = await API.getBudgetEstimate(city, days, style);
      let itemsHtml = '';
      for (const [key, val] of Object.entries(data.cost_breakdown || {})) {
        itemsHtml += `
          <div style="display: flex; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid var(--glass-border);">
            <span style="color: var(--text-secondary); font-size: 0.9rem;">${key}</span>
            <span style="font-weight: 700; color: #fff;">$${val}</span>
          </div>
        `;
      }

      breakdownBox.innerHTML = `
        <div style="margin-bottom: 1rem;">
          <div style="font-size: 0.85rem; color: var(--text-muted);">Est. Total (${days} Days in ${city}):</div>
          <div style="font-size: 2rem; font-weight: 800; color: var(--accent-emerald);">$${data.total_budget_usd} USD</div>
          <div style="font-size: 0.85rem; color: var(--accent-cyan);">$${data.daily_budget_usd} USD / day (${data.budget_tier} Tier)</div>
        </div>
        <div style="margin-bottom: 1.25rem;">${itemsHtml}</div>
        <div>
          <h4 style="font-size: 0.9rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">💡 Smart Savings Tips:</h4>
          <ul style="padding-left: 1.2rem; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">
            ${(data.money_saving_hacks || []).map(h => `<li>${h}</li>`).join('')}
          </ul>
        </div>
      `;
    } catch (err) {
      breakdownBox.innerHTML = `<span style="color: var(--accent-rose);">Failed to calculate budget.</span>`;
    }
  });
}

// ---------------------------------------------------------
// Smart Packing Checklist
// ---------------------------------------------------------
function initPackingAssistant() {
  const generateBtn = document.getElementById('packing-generate-btn');
  generateBtn.addEventListener('click', async () => {
    const dest = document.getElementById('packing-dest').value || 'Kyoto';
    const days = parseInt(document.getElementById('packing-days').value, 10) || 5;
    const season = document.getElementById('packing-season').value;
    const container = document.getElementById('packing-checklist-container');

    generateBtn.disabled = true;
    generateBtn.innerHTML = `<div class="spinner"></div> Generating Checklist...`;

    try {
      const data = await API.generatePacking({
        destination: dest,
        days: days,
        season: season,
        activities: ["Sightseeing", "Dining", "Photography", "Walking"]
      });

      let itemsHtml = '';
      (data.checklist || []).forEach((item, idx) => {
        itemsHtml += `
          <div class="checklist-item" onclick="toggleCheckItem(this)">
            <input type="checkbox" class="checklist-checkbox" id="chk-${idx}" />
            <div style="flex: 1;">
              <span style="font-size: 0.92rem; color: #fff;">${item.item}</span>
              <span style="font-size: 0.72rem; color: var(--accent-cyan); margin-left: 0.5rem; text-transform: uppercase;">[${item.category}]</span>
            </div>
            ${item.essential ? '<span class="dish-diet-pill" style="color:var(--accent-rose); border-color:rgba(244,63,94,0.3); background:rgba(244,63,94,0.15);">Essential</span>' : ''}
          </div>
        `;
      });

      container.innerHTML = `
        <div class="glass-card" style="margin-bottom: 1rem;">
          <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff;">${data.destination} (${data.season}) - ${data.trip_duration_days} Days</h3>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">🎒 ${data.luggage_advice}</p>
        </div>
        <div>${itemsHtml}</div>
      `;
    } catch (err) {
      container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);">❌ Failed to generate checklist.</div>`;
    } finally {
      generateBtn.disabled = false;
      generateBtn.innerHTML = `<i data-lucide="check-square"></i> Generate Packing Checklist`;
      initLucideIcons();
    }
  });
}

function toggleCheckItem(el) {
  const cb = el.querySelector('input[type="checkbox"]');
  cb.checked = !cb.checked;
  el.classList.toggle('checked', cb.checked);
}

// ---------------------------------------------------------
// Multilingual Audio Phrasebook & Web Speech TTS
// ---------------------------------------------------------
function initPhrasebook() {
  const langSelect = document.getElementById('phrasebook-lang');
  const catSelect = document.getElementById('phrasebook-cat');

  langSelect.addEventListener('change', () => {
    loadPhrases(langSelect.value, catSelect.value);
  });

  catSelect.addEventListener('change', () => {
    loadPhrases(langSelect.value, catSelect.value);
  });
}

async function loadPhrases(language, category = 'All') {
  const container = document.getElementById('phrasebook-content');
  container.innerHTML = `<div style="text-align:center; padding: 2rem;"><div class="spinner"></div></div>`;

  try {
    const data = await API.getPhrases(language, category);
    let phrasesHtml = '';

    (data.phrases || []).forEach(p => {
      phrasesHtml += `
        <div class="phrase-card">
          <div style="flex: 1;">
            <span class="activity-badge" style="font-size: 0.65rem;">${p.category}</span>
            <h4 style="font-size: 1.15rem; font-weight: 700; color: #fff; margin: 0.35rem 0 0.15rem;">${p.foreign}</h4>
            <div style="font-size: 0.85rem; color: var(--accent-cyan);">🗣️ <i>${p.romanized}</i></div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">Meaning: "${p.english}"</div>
          </div>
          <button class="audio-play-btn" onclick="playSpeech('${p.audio_text.replace(/'/g, "\\'")}', '${data.speech_lang_code}')" title="Play Pronunciation">
            <i data-lucide="volume-2"></i>
          </button>
        </div>
      `;
    });

    container.innerHTML = `
      <div class="grid-2">
        ${phrasesHtml}
      </div>
    `;
    initLucideIcons();
  } catch (err) {
    container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);">❌ Failed to load phrases.</div>`;
  }
}

function playSpeech(text, langCode = 'en-US') {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = langCode;
    utterance.rate = 0.85;
    window.speechSynthesis.speak(utterance);
  } else {
    alert('Web Speech Synthesis is not supported in this browser.');
  }
}

// ---------------------------------------------------------
// Global Header City Search Synchronization
// ---------------------------------------------------------
function initGlobalCitySearch() {
  const globalInput = document.getElementById('global-city-search');
  globalInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const city = globalInput.value.trim();
      if (city) {
        document.getElementById('weather-city-input').value = city;
        document.getElementById('food-city-input').value = city;
        document.getElementById('itinerary-dest').value = city;
        document.getElementById('budget-city').value = city;
        document.getElementById('packing-dest').value = city;

        loadWeatherData(city);
        loadFoodData(city);
      }
    }
  });
}

function formatMarkdown(text) {
  return text
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/^\- (.*$)/gim, '<li>$1</li>')
    .replace(/\n\n/gim, '<br/><br/>');
}
