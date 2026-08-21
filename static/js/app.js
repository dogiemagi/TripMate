/**
 * VoyageAI - Main Application Controller with Dynamic Map & Currency Support
 */

let mapInstance = null;
let mapMarkers = [];
let mapPolyline = null;
let activeCurrency = 'INR';
let currentItineraryData = null;

const FX_RATES_FROM_INR = {
  INR: 1.0,
  USD: 0.01198,
  EUR: 0.01102,
  GBP: 0.00946,
  AED: 0.04395,
  JPY: 1.85,
  SGD: 0.01617,
  AUD: 0.0182,
  CAD: 0.0164
};

const CURRENCY_SYMBOLS = {
  INR: '₹',
  USD: '$',
  EUR: '€',
  GBP: '£',
  AED: 'AED ',
  JPY: '¥',
  SGD: 'S$',
  AUD: 'A$',
  CAD: 'C$'
};

document.addEventListener('DOMContentLoaded', () => {
  initLucideIcons();
  initNavigationTabs();
  initGlobalCurrencySwitcher();
  initMultimodalVision();
  initWeatherDashboard();
  initItineraryPlanner();
  initFoodExplorer();
  initCurrencyBudget();
  initPackingAssistant();
  initPhrasebook();
  initGlobalCitySearch();
  initVoiceInput();

  // Set default weather dates (today to +6 days)
  const today = new Date();
  const nextWeek = new Date();
  nextWeek.setDate(today.getDate() + 6);
  
  const fromInput = document.getElementById('weather-from-date');
  const toInput = document.getElementById('weather-to-date');
  if (fromInput) fromInput.value = today.toISOString().split('T')[0];
  if (toInput) toInput.value = nextWeek.toISOString().split('T')[0];

  // Initial Data Loads
  loadWeatherData('Delhi', fromInput ? fromInput.value : null, toInput ? toInput.value : null);
  loadFoodData('Delhi');
  loadPhrases('Hindi');

  // Trigger initial itinerary
  setTimeout(() => {
    generateTripPlan();
  }, 400);
});

function initLucideIcons() {
  if (window.lucide) {
    lucide.createIcons();
  }
}

// ---------------------------------------------------------
// Global Currency Switcher
// ---------------------------------------------------------
function initGlobalCurrencySwitcher() {
  const select = document.getElementById('global-currency-select');
  if (!select) return;

  select.addEventListener('change', () => {
    activeCurrency = select.value;
    updateCurrencyAcrossApp();
  });
}

function updateCurrencyAcrossApp() {
  if (currentItineraryData) {
    renderItinerary(currentItineraryData);
  }

  const fromSelect = document.getElementById('currency-from');
  if (fromSelect) {
    fromSelect.value = activeCurrency;
  }

  const budgetBtn = document.getElementById('budget-estimate-btn');
  if (budgetBtn) {
    budgetBtn.click();
  }
}

function formatCostFromINR(inrAmount) {
  const rate = FX_RATES_FROM_INR[activeCurrency] || 1.0;
  const converted = inrAmount * rate;
  const sym = CURRENCY_SYMBOLS[activeCurrency] || '₹';
  
  if (activeCurrency === 'INR' || activeCurrency === 'JPY') {
    return `${sym}${Math.round(converted).toLocaleString()}`;
  } else {
    return `${sym}${converted.toFixed(2)}`;
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

      if (targetTab === 'tab-itinerary') {
        setTimeout(() => {
          if (mapInstance) {
            mapInstance.invalidateSize();
            if (mapMarkers.length > 0) {
              const group = new L.featureGroup(mapMarkers);
              mapInstance.fitBounds(group.getBounds(), { padding: [50, 50], maxZoom: 15 });
            } else if (currentItineraryData && currentItineraryData.center_coordinates) {
              mapInstance.setView([currentItineraryData.center_coordinates.lat, currentItineraryData.center_coordinates.lon], 13);
            }
          } else {
            initLeafletMap();
            if (currentItineraryData) {
              renderItinerary(currentItineraryData);
            }
          }
        }, 180);
      }
      initLucideIcons();
    });
  });
}

// ---------------------------------------------------------
// Leaflet Map Initialization
// ---------------------------------------------------------
function initLeafletMap() {
  const mapElement = document.getElementById('itinerary-map');
  if (mapElement && !mapInstance && window.L) {
    mapInstance = L.map('itinerary-map', {
      zoomControl: true,
      attributionControl: true
    }).setView([28.6139, 77.2090], 12);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap contributors & CARTO',
      maxZoom: 19
    }).addTo(mapInstance);
  }
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

  document.querySelectorAll('.sample-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const sampleName = chip.getAttribute('data-sample');
      document.getElementById('vision-prompt').value = `Analyze: ${sampleName}`;
      
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
      resultsContainer.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Vision analysis failed. ${err.message}</div>`;
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
// Weather Dashboard Handler (With Date Range From-To Filter)
// ---------------------------------------------------------
function initWeatherDashboard() {
  const searchBtn = document.getElementById('weather-search-btn');
  const cityInput = document.getElementById('weather-city-input');
  const fromInput = document.getElementById('weather-from-date');
  const toInput = document.getElementById('weather-to-date');
  const presetChips = document.querySelectorAll('.date-preset-chip');

  function formatDateIso(d) {
    return d.toISOString().split('T')[0];
  }

  function applyPreset(presetType) {
    const today = new Date();
    let startDate = new Date(today);
    let endDate = new Date(today);

    if (presetType === 'today') {
      // today -> today
    } else if (presetType === '3days') {
      endDate.setDate(today.getDate() + 2);
    } else if (presetType === '7days') {
      endDate.setDate(today.getDate() + 6);
    } else if (presetType === '14days') {
      endDate.setDate(today.getDate() + 13);
    } else if (presetType === 'weekend') {
      // Find upcoming Saturday
      const dayOfWeek = today.getDay(); // 0 is Sunday, 6 is Saturday
      const daysUntilSaturday = (6 - dayOfWeek + 7) % 7;
      startDate.setDate(today.getDate() + (daysUntilSaturday === 0 ? 0 : daysUntilSaturday));
      endDate = new Date(startDate);
      endDate.setDate(startDate.getDate() + 1); // Sunday
    }

    if (fromInput) fromInput.value = formatDateIso(startDate);
    if (toInput) toInput.value = formatDateIso(endDate);

    presetChips.forEach(chip => {
      chip.classList.toggle('active', chip.getAttribute('data-preset') === presetType);
    });
  }

  presetChips.forEach(chip => {
    const preset = chip.getAttribute('data-preset');
    if (preset) {
      chip.addEventListener('click', () => {
        applyPreset(preset);
        const city = cityInput.value.trim() || 'Delhi';
        loadWeatherData(city, fromInput.value, toInput.value);
      });
    }
  });

  if (fromInput) {
    fromInput.addEventListener('change', () => {
      presetChips.forEach(c => c.classList.remove('active'));
      if (toInput && toInput.value && fromInput.value > toInput.value) {
        toInput.value = fromInput.value;
      }
    });
  }

  if (toInput) {
    toInput.addEventListener('change', () => {
      presetChips.forEach(c => c.classList.remove('active'));
      if (fromInput && fromInput.value && toInput.value < fromInput.value) {
        fromInput.value = toInput.value;
      }
    });
  }

  // ---------------------------------------------------------
  // Interactive Visual Calendar Modal Handler
  // ---------------------------------------------------------
  const calModal = document.getElementById('calendar-range-modal');
  const openCalBtn = document.getElementById('open-calendar-modal-btn');
  const closeCalBtn = document.getElementById('close-calendar-modal');
  const calPrevMonthBtn = document.getElementById('cal-prev-month');
  const calNextMonthBtn = document.getElementById('cal-next-month');
  const calMonthYearLabel = document.getElementById('cal-month-year-label');
  const calDaysGrid = document.getElementById('calendar-days-grid');
  const calSelectedRangeText = document.getElementById('cal-selected-range-text');
  const calResetBtn = document.getElementById('cal-reset-btn');
  const calApplyBtn = document.getElementById('cal-apply-btn');

  let calViewDate = new Date();
  let calSelectedStart = fromInput ? fromInput.value : null;
  let calSelectedEnd = toInput ? toInput.value : null;

  const MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  function openCalendarModal() {
    if (fromInput && fromInput.value) {
      calSelectedStart = fromInput.value;
      try {
        calViewDate = new Date(fromInput.value + 'T00:00:00');
      } catch (e) {
        calViewDate = new Date();
      }
    }
    if (toInput && toInput.value) {
      calSelectedEnd = toInput.value;
    }
    renderCalendarGrid();
    if (calModal) calModal.style.display = 'flex';
    initLucideIcons();
  }

  function closeCalendarModal() {
    if (calModal) calModal.style.display = 'none';
  }

  if (openCalBtn) openCalBtn.addEventListener('click', openCalendarModal);
  if (closeCalBtn) closeCalBtn.addEventListener('click', closeCalendarModal);
  if (calModal) {
    calModal.addEventListener('click', (e) => {
      if (e.target === calModal) closeCalendarModal();
    });
  }

  if (calPrevMonthBtn) {
    calPrevMonthBtn.addEventListener('click', () => {
      calViewDate.setMonth(calViewDate.getMonth() - 1);
      renderCalendarGrid();
    });
  }

  if (calNextMonthBtn) {
    calNextMonthBtn.addEventListener('click', () => {
      calViewDate.setMonth(calViewDate.getMonth() + 1);
      renderCalendarGrid();
    });
  }

  if (calResetBtn) {
    calResetBtn.addEventListener('click', () => {
      calSelectedStart = null;
      calSelectedEnd = null;
      renderCalendarGrid();
    });
  }

  if (calApplyBtn) {
    calApplyBtn.addEventListener('click', () => {
      if (calSelectedStart) {
        const finalStart = calSelectedStart;
        const finalEnd = calSelectedEnd || calSelectedStart;
        if (fromInput) fromInput.value = finalStart;
        if (toInput) toInput.value = finalEnd;

        presetChips.forEach(chip => {
          chip.classList.toggle('active', chip.id === 'open-calendar-modal-btn');
        });

        closeCalendarModal();
        const city = cityInput.value.trim() || 'Delhi';
        loadWeatherData(city, finalStart, finalEnd);
      } else {
        closeCalendarModal();
      }
    });
  }

  function renderCalendarGrid() {
    if (!calDaysGrid || !calMonthYearLabel) return;

    const year = calViewDate.getFullYear();
    const month = calViewDate.getMonth();
    calMonthYearLabel.textContent = `${MONTH_NAMES[month]} ${year}`;

    const firstDayIndex = new Date(year, month, 1).getDay(); // 0 is Sunday
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    calDaysGrid.innerHTML = '';

    // Empty cells before month starts
    for (let i = 0; i < firstDayIndex; i++) {
      const emptyCell = document.createElement('div');
      emptyCell.className = 'cal-day-cell empty';
      calDaysGrid.appendChild(emptyCell);
    }

    // Days in current month
    for (let d = 1; d <= daysInMonth; d++) {
      const dayStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const cell = document.createElement('div');
      cell.className = 'cal-day-cell';
      cell.textContent = d;
      cell.setAttribute('data-date', dayStr);

      if (calSelectedStart && dayStr === calSelectedStart) {
        cell.classList.add('range-start');
      }
      if (calSelectedEnd && dayStr === calSelectedEnd) {
        cell.classList.add('range-end');
      }
      if (calSelectedStart && calSelectedEnd && dayStr > calSelectedStart && dayStr < calSelectedEnd) {
        cell.classList.add('range-between');
      }

      cell.addEventListener('click', () => {
        if (!calSelectedStart || (calSelectedStart && calSelectedEnd)) {
          calSelectedStart = dayStr;
          calSelectedEnd = null;
        } else if (calSelectedStart && !calSelectedEnd) {
          if (dayStr < calSelectedStart) {
            calSelectedEnd = calSelectedStart;
            calSelectedStart = dayStr;
          } else {
            calSelectedEnd = dayStr;
          }
        }
        renderCalendarGrid();
      });

      calDaysGrid.appendChild(cell);
    }

    // Update range label
    if (calSelectedRangeText) {
      if (calSelectedStart && calSelectedEnd) {
        calSelectedRangeText.textContent = `${calSelectedStart} → ${calSelectedEnd}`;
      } else if (calSelectedStart) {
        calSelectedRangeText.textContent = `From: ${calSelectedStart} (Select End Date)`;
      } else {
        calSelectedRangeText.textContent = 'Click start & end dates';
      }
    }
    initLucideIcons();
  }

  searchBtn.addEventListener('click', () => {
    const city = cityInput.value.trim() || 'Delhi';
    const startDate = fromInput ? fromInput.value : null;
    const endDate = toInput ? toInput.value : null;
    loadWeatherData(city, startDate, endDate);
  });

  cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const city = cityInput.value.trim() || 'Delhi';
      const startDate = fromInput ? fromInput.value : null;
      const endDate = toInput ? toInput.value : null;
      loadWeatherData(city, startDate, endDate);
    }
  });
}

async function loadWeatherData(city, startDate = null, endDate = null) {
  const container = document.getElementById('weather-content');
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><div class="spinner"></div><p style="margin-top:1rem; color:var(--text-secondary);">Fetching atmospheric radar for ${sanitizeAndConvertEmojis(city)}...</p></div>`;

  try {
    const data = await API.getWeather(city, startDate, endDate, 7);
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
          <div style="font-size: 0.72rem; color: var(--accent-cyan); margin-top: 0.5rem; display:flex; align-items:center; justify-content:center; gap:0.25rem;">
            <i data-lucide="droplets" style="width:12px; height:12px;"></i> ${f.precipitation_chance_pct}% rain
          </div>
        </div>
      `;
    });

    const dateRangeLabel = data.date_range ? `${data.date_range.from} to ${data.date_range.to} (${data.date_range.total_days} Days)` : 'Active Period';
    const cityLabel = data.display_location || data.city;

    container.innerHTML = `
      <div class="weather-hero">
        <div>
          <span class="brand-badge">${data.country || 'Global'}</span>
          <h2 style="font-size: 2.2rem; font-weight: 800; margin-top: 0.35rem;">${cityLabel}</h2>
          <p style="color: var(--text-secondary); font-size: 1rem; margin-bottom: 1rem;">${curr.condition} | <strong>${dateRangeLabel}</strong></p>
          <div>
            <span class="weather-metric-badge"><i data-lucide="wind"></i> ${curr.windspeed_kmh} km/h Wind</span>
            <span class="weather-metric-badge"><i data-lucide="shield-check"></i> Travel Index: ${data.travel_climate_score}/100</span>
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
        <p style="color: var(--accent-cyan); font-size: 0.88rem; margin-top: 0.5rem; display:flex; align-items:center; gap:0.4rem;">
          <i data-lucide="backpack"></i> <strong>Packing Advisory:</strong> ${data.packing_recommendation}
        </p>
      </div>

      <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 1rem; display:flex; align-items:center; gap:0.5rem;">
        <i data-lucide="calendar-check"></i> Forecast Timeline (${dateRangeLabel})
      </h3>
      <div class="grid-4" style="grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));">
        ${forecastHtml}
      </div>
    `;
    initLucideIcons();
  } catch (err) {
    container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Failed to load weather for ${sanitizeAndConvertEmojis(city)}.</div>`;
    initLucideIcons();
  }
}

// ---------------------------------------------------------
// Smart Itinerary Planner & Dynamic Map Routing
// ---------------------------------------------------------
function initItineraryPlanner() {
  initLeafletMap();
  const generateBtn = document.getElementById('itinerary-generate-btn');
  if (generateBtn) {
    generateBtn.addEventListener('click', generateTripPlan);
  }

  const recenterBtn = document.getElementById('recenter-map-btn');
  if (recenterBtn) {
    recenterBtn.addEventListener('click', () => {
      if (mapInstance && mapMarkers.length > 0) {
        const group = new L.featureGroup(mapMarkers);
        mapInstance.fitBounds(group.getBounds(), { padding: [50, 50], maxZoom: 15 });
      } else if (currentItineraryData && currentItineraryData.center_coordinates && mapInstance) {
        mapInstance.setView([currentItineraryData.center_coordinates.lat, currentItineraryData.center_coordinates.lon], 13);
      }
    });
  }
}

function focusMapActivity(lat, lon, title, cost) {
  if (mapInstance) {
    mapInstance.flyTo([lat, lon], 14, { duration: 0.8 });
    
    // Find matching marker and open popup
    const targetMarker = mapMarkers.find(m => {
      const pos = m.getLatLng();
      return Math.abs(pos.lat - lat) < 0.0001 && Math.abs(pos.lng - lon) < 0.0001;
    });

    if (targetMarker) {
      setTimeout(() => {
        targetMarker.openPopup();
      }, 850);
    }
  }
}

async function generateTripPlan() {
  initLeafletMap();
  const dest = document.getElementById('itinerary-dest').value.trim() || 'Delhi, India';
  const days = parseInt(document.getElementById('itinerary-days').value, 10) || 2;
  const style = document.getElementById('itinerary-style').value;
  const pace = document.getElementById('itinerary-pace').value;
  const budget = document.getElementById('itinerary-budget').value;

  const btn = document.getElementById('itinerary-generate-btn');
  const container = document.getElementById('itinerary-results');

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<div class="spinner"></div> Synthesizing Day-by-Day Route...`;
  }

  try {
    const data = await API.generateItinerary({
      destination: dest,
      days: days,
      travel_style: style,
      pace: pace,
      budget_level: budget,
      interests: ["Sightseeing", "Food", "Culture", "Photography"]
    });

    currentItineraryData = data;
    renderItinerary(data);
  } catch (err) {
    container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Could not generate itinerary: ${sanitizeAndConvertEmojis(err.message)}</div>`;
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `<i data-lucide="sparkles"></i> Generate AI Itinerary`;
    }
    initLucideIcons();
  }
}

function renderItinerary(data) {
  const container = document.getElementById('itinerary-results');
  initLeafletMap();

  let daysHtml = '';
  const mapCoords = [];
  let globalPointIdx = 0;

  // Clear previous markers & route lines
  if (mapInstance) {
    mapMarkers.forEach(m => mapInstance.removeLayer(m));
    mapMarkers = [];
    if (mapPolyline) {
      mapInstance.removeLayer(mapPolyline);
      mapPolyline = null;
    }
  }

  // Update map status badge with resolved location
  const statusBadge = document.getElementById('map-status-badge');
  if (statusBadge) {
    statusBadge.textContent = `${data.city || 'Destination'} Mapped`;
  }

  (data.days || []).forEach(day => {
    let actHtml = '';
    (day.activities || []).forEach((act, actIdx) => {
      globalPointIdx++;
      const pointNum = globalPointIdx;
      const formattedActCost = act.cost_inr > 0 ? formatCostFromINR(act.cost_inr) : "Free";

      if (act.lat && act.lon && mapInstance) {
        mapCoords.push([act.lat, act.lon]);

        const customPinIcon = L.divIcon({
          className: 'custom-map-pin-container',
          html: `<div class="custom-map-pin" title="${act.title}">${pointNum}</div>`,
          iconSize: [32, 32],
          iconAnchor: [16, 16],
          popupAnchor: [0, -18]
        });
        
        const marker = L.marker([act.lat, act.lon], { icon: customPinIcon })
          .addTo(mapInstance)
          .bindPopup(`
            <div style="font-family:'Outfit',sans-serif; padding:4px; min-width:180px;">
              <strong style="color:#0284c7; font-size:0.95rem;">#${pointNum} Day ${day.day}: ${sanitizeAndConvertEmojis(act.title)}</strong><br/>
              <span style="color:#64748b; font-size:0.82rem;">Time: ${act.time} | Cost: ${formattedActCost}</span><br/>
              <p style="font-size:0.8rem; margin-top:4px; color:#334155;">${sanitizeAndConvertEmojis(act.desc)}</p>
            </div>
          `);
        mapMarkers.push(marker);
      }

      const escapedTitle = act.title.replace(/'/g, "\\'");
      actHtml += `
        <div class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-card" onclick="focusMapActivity(${act.lat}, ${act.lon}, '${escapedTitle}', '${formattedActCost}')" title="Click to view on interactive map">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <span style="font-weight: 700; color: var(--accent-cyan); font-size: 0.85rem; display:flex; align-items:center; gap:0.35rem;">
                <i data-lucide="clock" style="width:14px; height:14px;"></i> ${act.time}
              </span>
              <span class="activity-badge"><i data-lucide="map-pin" style="width:11px; height:11px; margin-right:3px;"></i> Pin #${pointNum} | ${act.category}</span>
            </div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 0.35rem;">${sanitizeAndConvertEmojis(act.title)}</h4>
            <p style="color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 0.5rem;">${sanitizeAndConvertEmojis(act.desc)}</p>
            <div style="display: flex; gap: 1.25rem; font-size: 0.78rem; color: var(--text-muted);">
              <span style="display:flex; align-items:center; gap:0.25rem;"><i data-lucide="hourglass" style="width:12px; height:12px;"></i> ${act.duration}</span>
              <span style="display:flex; align-items:center; gap:0.25rem; color:var(--accent-emerald); font-weight:600;"><i data-lucide="banknote" style="width:12px; height:12px;"></i> ${formattedActCost}</span>
              <span style="display:flex; align-items:center; gap:0.25rem; color:var(--accent-cyan); margin-left:auto;"><i data-lucide="crosshair" style="width:12px; height:12px;"></i> View on Map</span>
            </div>
          </div>
        </div>
      `;
    });

    daysHtml += `
      <div class="glass-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div>
            <h3 style="font-size: 1.2rem; font-weight: 800; color: #fff;">${sanitizeAndConvertEmojis(day.theme)}</h3>
            <p style="color: var(--accent-cyan); font-size: 0.85rem; display:flex; align-items:center; gap:0.35rem;">
              <i data-lucide="sparkles" style="width:14px; height:14px;"></i> Highlights: ${sanitizeAndConvertEmojis(day.highlight)}
            </p>
          </div>
          <span class="brand-badge">Day ${day.day}</span>
        </div>
        <div class="timeline-container">
          ${actHtml}
        </div>
      </div>
    `;
  });

  const formattedTotalTrip = formatCostFromINR(data.estimated_total_cost_inr);
  const formattedDailyRate = formatCostFromINR(data.estimated_daily_cost_inr);

  container.innerHTML = `
    <div class="glass-card" style="margin-bottom: 1.5rem; background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1));">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
          <h2 style="font-size: 1.5rem; font-weight: 800;">${data.destination} - ${data.total_days} Day Masterplan</h2>
          <p style="color: var(--text-secondary); font-size: 0.9rem;">
            Style: ${data.travel_style} | Pace: ${data.pace} | Est. Total: <strong style="color:var(--accent-emerald); font-size:1.05rem;">${formattedTotalTrip}</strong> (${formattedDailyRate}/day)
          </p>
        </div>
        <span class="brand-badge"><i data-lucide="train" style="width:12px; height:12px; margin-right:4px;"></i> ${data.summary.recommended_transit_pass}</span>
      </div>
      <p style="color: #94a3b8; font-size: 0.88rem; margin-top: 0.75rem; display:flex; align-items:center; gap:0.4rem;">
        <i data-lucide="lightbulb" style="color:var(--accent-amber); width:16px; height:16px;"></i> ${sanitizeAndConvertEmojis(data.summary.smart_tip)}
      </p>
    </div>
    ${daysHtml}
  `;

  // Draw Leaflet map route polyline & dynamically center on queried destination
  if (mapInstance) {
    if (mapCoords.length > 0) {
      mapPolyline = L.polyline(mapCoords, {
        color: '#06b6d4',
        weight: 3.5,
        opacity: 0.9,
        dashArray: '6, 8'
      }).addTo(mapInstance);

      const bounds = L.latLngBounds(mapCoords);
      mapInstance.fitBounds(bounds, { padding: [50, 50], maxZoom: 15 });
    } else if (data.center_coordinates) {
      mapInstance.setView([data.center_coordinates.lat, data.center_coordinates.lon], 13);
    }
    setTimeout(() => { mapInstance.invalidateSize(); }, 200);
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
    const city = cityInput.value.trim() || 'Delhi';
    loadFoodData(city);
  });

  cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const city = cityInput.value.trim() || 'Delhi';
      loadFoodData(city);
    }
  });

  document.querySelectorAll('.diet-filter-cb').forEach(cb => {
    cb.addEventListener('change', () => {
      const city = cityInput.value.trim() || 'Delhi';
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
      const priceDisplay = d.price_range_inr || d.price_range || 'INR 300 - INR 600';

      dishesHtml += `
        <div class="dish-card">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
              <h4 style="font-size: 1.15rem; font-weight: 700; color: #fff;">${d.name}</h4>
              <span style="font-weight: 700; color: var(--accent-amber); font-size: 0.9rem;">${priceDisplay}</span>
            </div>
            <div style="font-size: 0.78rem; color: var(--accent-cyan); margin-bottom: 0.5rem; display:flex; align-items:center; gap:0.35rem;">
              <i data-lucide="volume-2" style="width:14px; height:14px;"></i> Pronunciation: <i>${d.pronunciation}</i>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.6;">${d.description}</p>
          </div>
          <div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.75rem;">${pills}</div>
            <div style="font-size: 0.8rem; color: #93c5fd; display:flex; align-items:center; gap:0.35rem;">
              <i data-lucide="map-pin" style="width:14px; height:14px; color:var(--accent-rose);"></i> <strong>Top Spot:</strong> ${d.must_try_spot}
            </div>
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
    container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Failed to load culinary recommendations.</div>`;
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
    const amount = document.getElementById('currency-amount').value || 1000;

    const resultBox = document.getElementById('currency-result-box');
    resultBox.innerHTML = `<div class="spinner"></div>`;

    try {
      const data = await API.convertCurrency(from, to, amount);
      const sym = CURRENCY_SYMBOLS[data.to_currency] || '';
      resultBox.innerHTML = `
        <div style="font-size: 0.88rem; color: var(--text-muted);">${data.amount.toLocaleString()} ${data.from_currency} =</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: var(--accent-cyan); line-height: 1.1; margin: 0.35rem 0;">
          ${sym}${data.converted_amount.toLocaleString()} <span style="font-size: 1rem; color: #fff;">${data.to_currency}</span>
        </div>
        <div style="font-size: 0.78rem; color: var(--text-secondary);">1 ${data.from_currency} = ${data.exchange_rate} ${data.to_currency}</div>
      `;
    } catch (err) {
      resultBox.innerHTML = `<span style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Conversion failed</span>`;
      initLucideIcons();
    }
  });

  const estimateBtn = document.getElementById('budget-estimate-btn');
  estimateBtn.addEventListener('click', async () => {
    const city = document.getElementById('budget-city').value || 'Delhi';
    const days = parseInt(document.getElementById('budget-days').value, 10) || 5;
    const style = document.getElementById('budget-style').value;
    const breakdownBox = document.getElementById('budget-breakdown-content');

    breakdownBox.innerHTML = `<div class="spinner"></div>`;

    try {
      const data = await API.getBudgetEstimate(city, days, style);
      const sym = CURRENCY_SYMBOLS[activeCurrency] || '₹';
      
      let itemsHtml = '';
      for (const [key, val] of Object.entries(data.cost_breakdown || {})) {
        itemsHtml += `
          <div style="display: flex; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid var(--glass-border);">
            <span style="color: var(--text-secondary); font-size: 0.9rem;">${key}</span>
            <span style="font-weight: 700; color: #fff;">${sym}${val.toLocaleString()}</span>
          </div>
        `;
      }

      breakdownBox.innerHTML = `
        <div style="margin-bottom: 1rem;">
          <div style="font-size: 0.85rem; color: var(--text-muted);">Est. Total (${days} Days in ${city}):</div>
          <div style="font-size: 2rem; font-weight: 800; color: var(--accent-emerald);">${sym}${data.total_budget.toLocaleString()} ${activeCurrency}</div>
          <div style="font-size: 0.85rem; color: var(--accent-cyan);">${sym}${data.daily_budget.toLocaleString()} / day (${data.budget_tier} Tier)</div>
        </div>
        <div style="margin-bottom: 1.25rem;">${itemsHtml}</div>
        <div>
          <h4 style="font-size: 0.9rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; display:flex; align-items:center; gap:0.4rem;">
            <i data-lucide="sparkles" style="color:var(--accent-cyan);"></i> Smart Savings Tips:
          </h4>
          <ul style="padding-left: 1.2rem; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">
            ${(data.money_saving_hacks || []).map(h => `<li>${h}</li>`).join('')}
          </ul>
        </div>
      `;
      initLucideIcons();
    } catch (err) {
      breakdownBox.innerHTML = `<span style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Failed to calculate budget.</span>`;
      initLucideIcons();
    }
  });
}

// ---------------------------------------------------------
// Smart Packing Checklist with Live Completion Progress
// ---------------------------------------------------------
function initPackingAssistant() {
  const generateBtn = document.getElementById('packing-generate-btn');
  if (!generateBtn) return;

  generateBtn.addEventListener('click', async () => {
    const dest = document.getElementById('packing-dest').value || 'Goa';
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
          <div class="checklist-item" onclick="toggleCheckItem(this, event)">
            <input type="checkbox" class="checklist-checkbox" id="chk-${idx}" onchange="updateChecklistProgress()" />
            <div style="flex: 1;">
              <span class="item-title" style="font-size: 0.92rem; color: #fff;">${item.item}</span>
              <span style="font-size: 0.72rem; color: var(--accent-cyan); margin-left: 0.5rem; text-transform: uppercase;">[${item.category}]</span>
            </div>
            ${item.essential ? '<span class="dish-diet-pill" style="color:var(--accent-rose); border-color:rgba(244,63,94,0.3); background:rgba(244,63,94,0.15);">Essential</span>' : ''}
          </div>
        `;
      });

      container.innerHTML = `
        <div class="checklist-progress-card">
          <div class="checklist-progress-header">
            <div>
              <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff;">${data.destination} (${data.season}) - ${data.trip_duration_days} Days</h3>
              <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.2rem; display:flex; align-items:center; gap:0.4rem;">
                <i data-lucide="briefcase"></i> ${data.luggage_advice}
              </p>
            </div>
            <div style="text-align: right;">
              <span id="checklist-pct-badge" class="checklist-pct-badge">0%</span>
              <div id="checklist-count-badge" style="font-size: 0.75rem; color: var(--text-muted);">0 of ${(data.checklist || []).length} items packed</div>
            </div>
          </div>

          <div class="checklist-progress-track">
            <div id="checklist-progress-fill" class="checklist-progress-fill" style="width: 0%;"></div>
          </div>

          <div class="checklist-actions">
            <span>Luggage Readiness Meter</span>
            <div style="display: flex; gap: 0.5rem;">
              <button type="button" class="checklist-action-btn" onclick="selectAllChecklist(true)">
                <i data-lucide="check-check" style="width:13px; height:13px; display:inline-block; vertical-align:middle;"></i> Check All
              </button>
              <button type="button" class="checklist-action-btn" onclick="selectAllChecklist(false)">
                <i data-lucide="rotate-ccw" style="width:13px; height:13px; display:inline-block; vertical-align:middle;"></i> Clear All
              </button>
            </div>
          </div>

          <div id="checklist-complete-badge" class="checklist-complete-badge" style="display: none;">
            <i data-lucide="sparkles" style="width: 18px; height: 18px;"></i>
            <span>100% Ready for Departure! Everything is packed and ready.</span>
          </div>
        </div>
        <div id="checklist-items-list">${itemsHtml}</div>
      `;

      updateChecklistProgress();
    } catch (err) {
      container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Failed to generate checklist.</div>`;
    } finally {
      generateBtn.disabled = false;
      generateBtn.innerHTML = `<i data-lucide="check-square"></i> Generate Packing Checklist`;
      initLucideIcons();
    }
  });
}

function updateChecklistProgress() {
  const checkboxes = document.querySelectorAll('.checklist-checkbox');
  const total = checkboxes.length;
  if (total === 0) return;

  let checkedCount = 0;
  checkboxes.forEach(cb => {
    if (cb.checked) checkedCount++;
    const parent = cb.closest('.checklist-item');
    if (parent) parent.classList.toggle('checked', cb.checked);
  });

  const pct = Math.round((checkedCount / total) * 100);

  const pctBadge = document.getElementById('checklist-pct-badge');
  if (pctBadge) pctBadge.innerText = `${pct}%`;

  const countBadge = document.getElementById('checklist-count-badge');
  if (countBadge) countBadge.innerText = `${checkedCount} of ${total} items packed`;

  const fillBar = document.getElementById('checklist-progress-fill');
  if (fillBar) fillBar.style.width = `${pct}%`;

  const completeBadge = document.getElementById('checklist-complete-badge');
  if (completeBadge) {
    completeBadge.style.display = pct === 100 ? 'flex' : 'none';
  }
}

function toggleCheckItem(el, event) {
  const cb = el.querySelector('input[type="checkbox"]');
  if (!cb) return;
  if (event && event.target === cb) {
    el.classList.toggle('checked', cb.checked);
  } else {
    cb.checked = !cb.checked;
    el.classList.toggle('checked', cb.checked);
  }
  updateChecklistProgress();
}

function selectAllChecklist(checkAll = true) {
  const checkboxes = document.querySelectorAll('.checklist-checkbox');
  checkboxes.forEach(cb => {
    cb.checked = checkAll;
  });
  updateChecklistProgress();
  initLucideIcons();
}

// ---------------------------------------------------------
// Multilingual Audio Phrasebook & Dual-Engine TTS Audio
// ---------------------------------------------------------
let speechVoices = [];
let currentAudioPlayer = null;

function populateSpeechVoices() {
  if ('speechSynthesis' in window) {
    speechVoices = window.speechSynthesis.getVoices() || [];
  }
}

if ('speechSynthesis' in window) {
  populateSpeechVoices();
  window.speechSynthesis.onvoiceschanged = populateSpeechVoices;
}

function initPhrasebook() {
  const langSelect = document.getElementById('phrasebook-lang');
  const catSelect = document.getElementById('phrasebook-cat');

  if (langSelect) {
    langSelect.addEventListener('change', () => {
      loadPhrases(langSelect.value, catSelect ? catSelect.value : 'All');
    });
  }

  if (catSelect) {
    catSelect.addEventListener('change', () => {
      loadPhrases(langSelect ? langSelect.value : 'Hindi', catSelect.value);
    });
  }
}

async function loadPhrases(language = 'Hindi', category = 'All') {
  const container = document.getElementById('phrasebook-content');
  if (!container) return;
  container.innerHTML = `<div style="text-align:center; padding: 2.5rem;"><div class="spinner"></div><p style="margin-top:0.75rem; color:var(--text-secondary);">Loading audio phrasebook for ${language}...</p></div>`;

  try {
    const data = await API.getPhrases(language, category);
    let phrasesHtml = '';

    (data.phrases || []).forEach(p => {
      const encNative = encodeURIComponent(p.audio_text || p.foreign || '');
      const encRomanized = encodeURIComponent(p.romanized || '');
      const langCode = data.speech_lang_code || 'hi-IN';

      phrasesHtml += `
        <div class="phrase-card">
          <div style="flex: 1;">
            <span class="activity-badge" style="font-size: 0.65rem;">${p.category}</span>
            <h4 style="font-size: 1.25rem; font-weight: 700; color: #fff; margin: 0.35rem 0 0.15rem;">${p.foreign}</h4>
            <div style="font-size: 0.88rem; color: var(--accent-cyan); display:flex; align-items:center; gap:0.35rem;">
              <i data-lucide="mic" style="width:13px; height:13px;"></i> <i>${p.romanized}</i>
            </div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">Meaning: "${p.english}"</div>
          </div>
          <button type="button" class="audio-play-btn" onclick="playSpeech('${encNative}', '${encRomanized}', '${langCode}', this)" title="Click to listen out loud">
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
    container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Failed to load phrases. ${err.message}</div>`;
    initLucideIcons();
  }
}

function playSpeech(encNative, encRomanized, langCode = 'hi-IN', btn = null) {
  const nativeText = decodeURIComponent(encNative || '');
  const romanizedText = decodeURIComponent(encRomanized || '');
  const langClean = (langCode || 'hi-IN').split('-')[0].toLowerCase();

  // Stop any active audio instance
  if (currentAudioPlayer) {
    currentAudioPlayer.pause();
    currentAudioPlayer.currentTime = 0;
    currentAudioPlayer = null;
  }

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }

  document.querySelectorAll('.audio-play-btn.audio-playing').forEach(b => b.classList.remove('audio-playing'));

  if (btn) {
    btn.classList.add('audio-playing');
  }

  const cleanup = () => {
    if (btn) btn.classList.remove('audio-playing');
    currentAudioPlayer = null;
  };

  // Primary: Native Neural Audio stream from server TTS endpoint
  const audioUrl = `/api/v1/phrasebook/audio?text=${encodeURIComponent(nativeText || romanizedText)}&lang=${langClean}`;
  const audio = new Audio(audioUrl);
  currentAudioPlayer = audio;

  audio.onended = cleanup;
  audio.onerror = (e) => {
    console.warn('Backend audio stream failed, falling back to Web Speech Synthesis:', e);
    playSpeechSynthesisFallback(nativeText, romanizedText, langCode, btn, cleanup);
  };

  const playPromise = audio.play();
  if (playPromise !== undefined) {
    playPromise.catch(err => {
      console.warn('Audio play failed or autoplay restricted, falling back to Web Speech Synthesis:', err);
      playSpeechSynthesisFallback(nativeText, romanizedText, langCode, btn, cleanup);
    });
  }
}

function playSpeechSynthesisFallback(nativeText, romanizedText, langCode, btn, cleanup) {
  if (!('speechSynthesis' in window)) {
    cleanup();
    showNotificationToast('Speech synthesis not supported in this browser.', 'info');
    return;
  }

  window.speechSynthesis.cancel();
  window.speechSynthesis.resume();

  if (speechVoices.length === 0) {
    populateSpeechVoices();
  }

  const langPrefix = (langCode || 'hi-IN').split('-')[0].toLowerCase();

  let matchedVoice = speechVoices.find(v => {
    const vLang = v.lang.toLowerCase();
    const vName = v.name.toLowerCase();
    return vLang === langCode.toLowerCase() ||
           vLang.startsWith(langPrefix + '-') ||
           vLang === langPrefix ||
           vName.includes(langPrefix);
  });

  let textToSpeak = nativeText;
  let targetLang = langCode;

  if (matchedVoice) {
    textToSpeak = nativeText;
    targetLang = matchedVoice.lang;
  } else {
    const fallbackVoice = speechVoices.find(v => {
      const vLang = v.lang.toLowerCase();
      const vName = v.name.toLowerCase();
      return vLang.includes('en-in') || vName.includes('india') || vLang.startsWith('en');
    });

    if (fallbackVoice) {
      matchedVoice = fallbackVoice;
      targetLang = fallbackVoice.lang;
    } else {
      targetLang = 'en-US';
    }
    textToSpeak = romanizedText || nativeText;
  }

  const utterance = new SpeechSynthesisUtterance(textToSpeak);
  utterance.lang = targetLang;
  if (matchedVoice) utterance.voice = matchedVoice;
  utterance.rate = 0.85;

  window._activeUtterance = utterance;

  utterance.onend = () => {
    cleanup();
    window._activeUtterance = null;
  };
  utterance.onerror = () => {
    cleanup();
    window._activeUtterance = null;
  };

  setTimeout(() => {
    try {
      window.speechSynthesis.speak(utterance);
    } catch (err) {
      cleanup();
    }
  }, 30);
}

// ---------------------------------------------------------
// Speech-to-Text Voice Input Engine (Microphone)
// ---------------------------------------------------------
function initVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  function setupMicButton(btnId, inputId, onResultCallback = null) {
    const btn = document.getElementById(btnId);
    const input = document.getElementById(inputId);
    if (!btn || !input) return;

    if (!SpeechRecognition) {
      btn.style.opacity = '0.5';
      btn.title = 'Voice recognition not supported in this browser';
      return;
    }

    let recognition = null;
    let isListening = false;

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      if (isListening && recognition) {
        recognition.stop();
        return;
      }

      try {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
          isListening = true;
          btn.classList.add('mic-listening');
          showNotificationToast('Listening... Speak now into your microphone.', 'info');
        };

        recognition.onresult = (event) => {
          if (event.results && event.results[0] && event.results[0][0]) {
            const transcript = event.results[0][0].transcript;
            if (transcript) {
              input.value = transcript;
              input.focus();
              showNotificationToast(`Captured voice: "${transcript}"`, 'success');
              if (onResultCallback) {
                onResultCallback(transcript);
              }
            }
          }
        };

        recognition.onerror = (event) => {
          console.warn('Speech recognition error:', event.error);
          if (event.error === 'not-allowed') {
            showNotificationToast('Microphone access was denied in browser permissions.', 'info');
          }
        };

        recognition.onend = () => {
          isListening = false;
          btn.classList.remove('mic-listening');
        };

        recognition.start();
      } catch (err) {
        console.error('Failed to start voice input:', err);
        btn.classList.remove('mic-listening');
      }
    });
  }

  // Bind to each input in the platform
  setupMicButton('global-mic-btn', 'global-city-search', () => {
    const searchBtn = document.getElementById('global-search-btn');
    if (searchBtn) searchBtn.click();
  });

  setupMicButton('vision-mic-btn', 'vision-prompt');

  setupMicButton('weather-mic-btn', 'weather-city-input', () => {
    const searchBtn = document.getElementById('weather-search-btn');
    if (searchBtn) searchBtn.click();
  });

  setupMicButton('itinerary-mic-btn', 'itinerary-dest', () => {
    const genBtn = document.getElementById('itinerary-generate-btn');
    if (genBtn) genBtn.click();
  });

  setupMicButton('food-mic-btn', 'food-city-input', () => {
    const searchBtn = document.getElementById('food-search-btn');
    if (searchBtn) searchBtn.click();
  });

  setupMicButton('packing-mic-btn', 'packing-dest', () => {
    const genBtn = document.getElementById('packing-generate-btn');
    if (genBtn) genBtn.click();
  });

  setupMicButton('budget-mic-btn', 'budget-city', () => {
    const calcBtn = document.getElementById('budget-estimate-btn');
    if (calcBtn) calcBtn.click();
  });
}

// ---------------------------------------------------------
// Global Header City Search Synchronization & Navigation
// ---------------------------------------------------------
function initGlobalCitySearch() {
  const globalInput = document.getElementById('global-city-search');
  const searchBtn = document.getElementById('global-search-btn');
  const searchIcon = document.getElementById('global-search-icon');

  function executeGlobalSearch() {
    if (!globalInput) return;
    const city = globalInput.value.trim();
    if (!city) {
      globalInput.focus();
      return;
    }

    // Synchronize city across all module inputs
    const weatherInput = document.getElementById('weather-city-input');
    const foodInput = document.getElementById('food-city-input');
    const itinInput = document.getElementById('itinerary-dest');
    const budgetInput = document.getElementById('budget-city');
    const packingInput = document.getElementById('packing-dest');

    if (weatherInput) weatherInput.value = city;
    if (foodInput) foodInput.value = city;
    if (itinInput) itinInput.value = city;
    if (budgetInput) budgetInput.value = city;
    if (packingInput) packingInput.value = city;

    // Refresh weather & food
    const fromDate = document.getElementById('weather-from-date') ? document.getElementById('weather-from-date').value : null;
    const toDate = document.getElementById('weather-to-date') ? document.getElementById('weather-to-date').value : null;
    loadWeatherData(city, fromDate, toDate);
    loadFoodData(city);
    generateTripPlan();

    // If on vision tab or static view, switch to Smart Itinerary & Map tab to display results
    const activePane = document.querySelector('.tab-pane.active');
    if (activePane && activePane.id === 'tab-vision') {
      switchToTab('tab-itinerary');
    }

    const formattedCity = city.charAt(0).toUpperCase() + city.slice(1);
    showNotificationToast(`Destination set to ${formattedCity}. Synced across all travel modules!`, 'success');
  }

  if (globalInput) {
    globalInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        executeGlobalSearch();
      }
    });
  }

  if (searchBtn) {
    searchBtn.addEventListener('click', executeGlobalSearch);
  }

  if (searchIcon) {
    searchIcon.addEventListener('click', () => {
      if (globalInput && globalInput.value.trim()) {
        executeGlobalSearch();
      } else if (globalInput) {
        globalInput.focus();
      }
    });
  }
}

function switchToTab(tabId) {
  const tabBtn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
  if (tabBtn) {
    tabBtn.click();
  }
}

function showNotificationToast(message, type = 'info') {
  let toastContainer = document.getElementById('voyage-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'voyage-toast-container';
    toastContainer.className = 'voyage-toast-container';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = `voyage-toast voyage-toast-${type}`;
  toast.innerHTML = `
    <i data-lucide="${type === 'success' ? 'check-circle-2' : 'info'}" style="width:18px; height:18px; flex-shrink:0;"></i>
    <span>${message}</span>
  `;
  toastContainer.appendChild(toast);
  initLucideIcons();

  setTimeout(() => {
    toast.classList.add('show');
  }, 20);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 350);
  }, 4000);
}

function sanitizeAndConvertEmojis(text) {
  if (!text || typeof text !== 'string') return text || '';
  
  return text
    .replace(/[\u{1F300}-\u{1F5FF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

/**
 * Robust Markdown-to-HTML Parser:
 * - Accurately parses headings (h1 to h6) in descending hierarchy
 * - Groups list items into semantic <ul> and <ol> containers
 * - Parses bold (**text**), italic (*text*), and inline elements
 * - Ensures zero raw markdown symbols (#, *) leak into the rendered DOM
 */
function formatMarkdown(text) {
  if (!text) return '';
  let clean = sanitizeAndConvertEmojis(text);

  // Normalize line endings
  clean = clean.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  // Parse inline formatting first
  clean = clean.replace(/\*\*\s*([^\*]+?)\s*\*\*/g, '<strong>$1</strong>');
  clean = clean.replace(/__\s*([^_]+?)\s*__/g, '<strong>$1</strong>');
  clean = clean.replace(/\*\s*([^\*]+?)\s*\*/g, '<em>$1</em>');

  // Split into lines to parse block elements
  const lines = clean.split('\n');
  const output = [];
  let inUnorderedList = false;
  let inOrderedList = false;

  function closeLists() {
    if (inUnorderedList) {
      output.push('</ul>');
      inUnorderedList = false;
    }
    if (inOrderedList) {
      output.push('</ol>');
      inOrderedList = false;
    }
  }

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i].trim();

    if (!line) {
      closeLists();
      continue;
    }

    // Check for Headings in descending order
    if (/^######\s+(.+)$/.test(line)) {
      closeLists();
      const content = line.replace(/^######\s+/, '');
      output.push(`<h6>${content}</h6>`);
    } else if (/^#####\s+(.+)$/.test(line)) {
      closeLists();
      const content = line.replace(/^#####\s+/, '');
      output.push(`<h5>${content}</h5>`);
    } else if (/^####\s+(.+)$/.test(line)) {
      closeLists();
      const content = line.replace(/^####\s+/, '');
      output.push(`<h4>${content}</h4>`);
    } else if (/^###\s+(.+)$/.test(line)) {
      closeLists();
      const content = line.replace(/^###\s+/, '');
      output.push(`<h3>${content}</h3>`);
    } else if (/^##\s+(.+)$/.test(line)) {
      closeLists();
      const content = line.replace(/^##\s+/, '');
      output.push(`<h2>${content}</h2>`);
    } else if (/^#\s+(.+)$/.test(line)) {
      closeLists();
      const content = line.replace(/^#\s+/, '');
      output.push(`<h1>${content}</h1>`);
    } else if (/^[\-\*\+]\s+(.+)$/.test(line)) {
      // Unordered list item
      if (inOrderedList) {
        output.push('</ol>');
        inOrderedList = false;
      }
      if (!inUnorderedList) {
        output.push('<ul>');
        inUnorderedList = true;
      }
      const itemContent = line.replace(/^[\-\*\+]\s+/, '');
      output.push(`<li>${itemContent}</li>`);
    } else if (/^\d+\.\s+(.+)$/.test(line)) {
      // Ordered list item
      if (inUnorderedList) {
        output.push('</ul>');
        inUnorderedList = false;
      }
      if (!inOrderedList) {
        output.push('<ol>');
        inOrderedList = true;
      }
      const itemContent = line.replace(/^\d+\.\s+/, '');
      output.push(`<li>${itemContent}</li>`);
    } else {
      // Standard paragraph text
      closeLists();
      // Clean any isolated stray hash or asterisk markers that are not part of valid syntax
      let sanitizedLine = line
        .replace(/(^|\s)#{1,6}\s*/g, '$1')
        .replace(/(^|\s)\*{1,3}\s*/g, '$1');
      output.push(`<p>${sanitizedLine}</p>`);
    }
  }

  closeLists();
  return output.join('\n');
}


