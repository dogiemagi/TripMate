/**
 * VoyageAI - Main Application Controller with Dynamic Map & Currency Support
 */

let mapInstance = null;
let mapMarkers = [];
let mapPolyline = null;
let activeCurrency = 'INR';
let currentItineraryData = null;
let activePackingList = [];

const FX_RATES_FROM_INR = {
  INR: 1.0,
  USD: 0.01198,
  EUR: 0.01102,
  GBP: 0.00946,
  AED: 0.04395,
  JPY: 1.85,
  SGD: 0.01617,
  AUD: 0.0182,
  CAD: 0.0164,
  THB: 0.44,
  IDR: 194.5
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
  CAD: 'C$',
  THB: '฿',
  IDR: 'Rp '
};

// Comprehensive Global City / Country to Local Currency Matrix
const CITY_CURRENCY_MAP = {
  tokyo: 'JPY', kyoto: 'JPY', osaka: 'JPY', sapporo: 'JPY', fukuoka: 'JPY', japan: 'JPY',
  paris: 'EUR', rome: 'EUR', berlin: 'EUR', madrid: 'EUR', barcelona: 'EUR',
  milan: 'EUR', amsterdam: 'EUR', vienna: 'EUR', athens: 'EUR', venice: 'EUR',
  florence: 'EUR', dublin: 'EUR', lisbon: 'EUR', brussels: 'EUR', munich: 'EUR',
  frankfurt: 'EUR', nice: 'EUR', lyon: 'EUR', france: 'EUR', italy: 'EUR',
  germany: 'EUR', spain: 'EUR', greece: 'EUR', portugal: 'EUR', netherlands: 'EUR',
  london: 'GBP', manchester: 'GBP', edinburgh: 'GBP', birmingham: 'GBP', uk: 'GBP',
  england: 'GBP', 'united kingdom': 'GBP', scotland: 'GBP',
  'new york': 'USD', 'los angeles': 'USD', chicago: 'USD', 'san francisco': 'USD',
  miami: 'USD', 'las vegas': 'USD', seattle: 'USD', boston: 'USD', washington: 'USD',
  orlando: 'USD', hawaii: 'USD', usa: 'USD', 'united states': 'USD',
  dubai: 'AED', 'abu dhabi': 'AED', sharjah: 'AED', uae: 'AED', 'united arab emirates': 'AED',
  singapore: 'SGD',
  sydney: 'AUD', melbourne: 'AUD', brisbane: 'AUD', perth: 'AUD', cairns: 'AUD', australia: 'AUD',
  toronto: 'CAD', vancouver: 'CAD', montreal: 'CAD', calgary: 'CAD', ottawa: 'CAD', canada: 'CAD',
  bangkok: 'THB', phuket: 'THB', 'chiang mai': 'THB', pattaya: 'THB', krabi: 'THB', thailand: 'THB',
  bali: 'IDR', jakarta: 'IDR', lombok: 'IDR', yogyakarta: 'IDR', indonesia: 'IDR',
  delhi: 'INR', 'new delhi': 'INR', mumbai: 'INR', chennai: 'INR', bengaluru: 'INR',
  bangalore: 'INR', kolkata: 'INR', hyderabad: 'INR', jaipur: 'INR', goa: 'INR',
  kashmir: 'INR', srinagar: 'INR', ladakh: 'INR', leh: 'INR', kerala: 'INR',
  kochi: 'INR', agra: 'INR', varanasi: 'INR', pune: 'INR', ahmedabad: 'INR',
  udaipur: 'INR', amritsar: 'INR', rishikesh: 'INR', shimla: 'INR', manali: 'INR',
  india: 'INR'
};

function detectCityCurrency(city) {
  if (!city) return 'INR';
  const clean = city.trim().toLowerCase();
  for (const [key, cur] of Object.entries(CITY_CURRENCY_MAP)) {
    if (clean === key || clean.includes(key) || key.includes(clean)) {
      return cur;
    }
  }
  return 'INR';
}

function updateFromCurrencyForCity(city) {
  const detected = detectCityCurrency(city);
  const fromSelect = document.getElementById('currency-from');
  if (fromSelect) {
    fromSelect.value = detected;
    // Auto-trigger currency conversion so user sees live result
    const convertBtn = document.getElementById('currency-convert-btn');
    if (convertBtn) {
      setTimeout(() => convertBtn.click(), 100);
    }
  }
}

// ---------------------------------------------------------
// Nearest-Neighbor & 2-Opt TSP Route Optimizer
// ---------------------------------------------------------
function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function optimizeActivitiesTSP(activities, startCoord = null) {
  if (!activities || activities.length <= 1) return activities;

  const unvisited = [...activities];
  const route = [];

  // Start with waypoint closest to reference start coordinates or index 0
  let currentIdx = 0;
  if (startCoord && startCoord.lat && startCoord.lon) {
    let minDist = Infinity;
    unvisited.forEach((act, idx) => {
      if (act.lat && act.lon) {
        const d = calculateHaversineDistance(startCoord.lat, startCoord.lon, act.lat, act.lon);
        if (d < minDist) {
          minDist = d;
          currentIdx = idx;
        }
      }
    });
  }

  let current = unvisited.splice(currentIdx, 1)[0];
  route.push(current);

  // Greedily find nearest unvisited spot at each step
  while (unvisited.length > 0) {
    let nearestIdx = 0;
    let nearestDist = Infinity;
    for (let i = 0; i < unvisited.length; i++) {
      if (unvisited[i].lat && unvisited[i].lon && current.lat && current.lon) {
        const dist = calculateHaversineDistance(current.lat, current.lon, unvisited[i].lat, unvisited[i].lon);
        if (dist < nearestDist) {
          nearestDist = dist;
          nearestIdx = i;
        }
      }
    }
    current = unvisited.splice(nearestIdx, 1)[0];
    route.push(current);
  }

  // 2-Opt refinement algorithm to untangle intersecting segments
  if (route.length >= 4) {
    let improved = true;
    let maxIters = 25;
    while (improved && maxIters-- > 0) {
      improved = false;
      for (let i = 0; i < route.length - 2; i++) {
        for (let j = i + 2; j < route.length; j++) {
          if (!route[i].lat || !route[i + 1].lat || !route[j].lat) continue;

          const d1 = calculateHaversineDistance(route[i].lat, route[i].lon, route[i + 1].lat, route[i + 1].lon);
          const d2 = (j + 1 < route.length && route[j + 1].lat) ?
            calculateHaversineDistance(route[j].lat, route[j].lon, route[j + 1].lat, route[j + 1].lon) : 0;
          const d3 = calculateHaversineDistance(route[i].lat, route[i].lon, route[j].lat, route[j].lon);
          const d4 = (j + 1 < route.length && route[j + 1].lat) ?
            calculateHaversineDistance(route[i + 1].lat, route[i + 1].lon, route[j + 1].lat, route[j + 1].lon) : 0;

          if (d3 + d4 < d1 + d2 - 0.0001) {
            const sub = route.slice(i + 1, j + 1).reverse();
            route.splice(i + 1, sub.length, ...sub);
            improved = true;
          }
        }
      }
    }
  }

  return route;
}

document.addEventListener('DOMContentLoaded', () => {
  initLucideIcons();
  initNavigationTabs();
  initGlobalCurrencySwitcher();
  initMultimodalVision();
  initWeatherDashboard();
  initItineraryPlanner();
  initCustomSpotBuilder();
  initFoodExplorer();
  initCurrencyBudget();
  initPackingAssistant();
  initCustomPackingBuilder();
  initPhrasebook();
  initTranslationStudio();
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

  // Set initial currency based on default city
  updateFromCurrencyForCity('Delhi');

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

  if (activeCurrency === 'INR' || activeCurrency === 'JPY' || activeCurrency === 'IDR') {
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
// Smart Itinerary Planner, TSP Map Routing & Visited Tracker
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

  // Mark all / Reset visited actions
  const markAllBtn = document.getElementById('mark-all-visited-btn');
  if (markAllBtn) {
    markAllBtn.addEventListener('click', () => {
      if (!currentItineraryData || !currentItineraryData.days) return;
      currentItineraryData.days.forEach(day => {
        (day.activities || []).forEach(act => { act.visited = true; });
      });
      renderItinerary(currentItineraryData);
      showNotificationToast('All visiting spots marked as visited! 🎉', 'success');
    });
  }

  const resetVisitedBtn = document.getElementById('reset-visited-btn');
  if (resetVisitedBtn) {
    resetVisitedBtn.addEventListener('click', () => {
      if (!currentItineraryData || !currentItineraryData.days) return;
      currentItineraryData.days.forEach(day => {
        (day.activities || []).forEach(act => { act.visited = false; });
      });
      renderItinerary(currentItineraryData);
      showNotificationToast('Exploration progress reset to 0%.', 'info');
    });
  }
}

function initCustomSpotBuilder() {
  const addBtn = document.getElementById('add-custom-spot-btn');
  const nameInput = document.getElementById('custom-spot-name');
  const catSelect = document.getElementById('custom-spot-cat');
  const daySelect = document.getElementById('custom-spot-day');
  const durInput = document.getElementById('custom-spot-duration');
  const costInput = document.getElementById('custom-spot-cost');

  if (!addBtn) return;

  addBtn.addEventListener('click', () => {
    const name = nameInput.value.trim();
    if (!name) {
      nameInput.focus();
      showNotificationToast('Please enter a place or landmark name.', 'info');
      return;
    }

    if (!currentItineraryData || !currentItineraryData.days || currentItineraryData.days.length === 0) {
      showNotificationToast('Please generate an itinerary first before adding custom spots.', 'info');
      return;
    }

    const dayNum = parseInt(daySelect.value, 10) || 1;
    const targetDayIndex = Math.min(dayNum - 1, currentItineraryData.days.length - 1);
    const targetDay = currentItineraryData.days[targetDayIndex];

    const centerLat = (currentItineraryData.center_coordinates && currentItineraryData.center_coordinates.lat) || 28.6139;
    const centerLon = (currentItineraryData.center_coordinates && currentItineraryData.center_coordinates.lon) || 77.2090;

    // Realistic small coordinate displacement based on existing activity count
    const count = (targetDay.activities || []).length;
    const angle = (count * 1.25) + 0.5;
    const radius = 0.008 + (count * 0.003);
    const newLat = roundCoord(centerLat + radius * Math.cos(angle));
    const newLon = roundCoord(centerLon + radius * Math.sin(angle));

    const costNum = parseFloat(costInput.value) || 0;
    const newActivity = {
      time: targetDay.activities.length > 0 ? "Flexible Time" : "10:00 AM",
      title: name,
      category: catSelect.value,
      duration: durInput.value.trim() || "1.5 hrs",
      cost_inr: costNum,
      cost_display: costNum > 0 ? `INR ${costNum.toLocaleString()}` : "Free",
      lat: newLat,
      lon: newLon,
      desc: `Custom user-added spot: ${name} in ${currentItineraryData.city || 'destination'}. Sequenced via AI TSP routing.`,
      visited: false,
      is_custom: true
    };

    targetDay.activities.push(newActivity);

    // Re-run Traveling Salesperson route optimizer over this day's waypoints
    targetDay.activities = optimizeActivitiesTSP(targetDay.activities, currentItineraryData.center_coordinates);

    // Update total costs
    currentItineraryData.estimated_total_cost_inr += costNum;

    // Reset input
    nameInput.value = '';

    // Re-render Itinerary with updated TSP path, pins, and circular progress
    renderItinerary(currentItineraryData);
    showNotificationToast(`Added "${name}"! Route re-optimized for shortest travel distance.`, 'success');
  });
}

function roundCoord(num) {
  return Math.round(num * 100000) / 100000;
}

function focusMapActivity(lat, lon, title, cost, pinNum = null) {
  // 1. Smoothly scroll viewport up to the map so user can see the marker
  const mapElem = document.getElementById('itinerary-map');
  if (mapElem) {
    mapElem.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // 2. Pan & zoom map to place coordinates and open popup
  if (mapInstance) {
    mapInstance.invalidateSize();
    mapInstance.flyTo([lat, lon], 15, { duration: 0.9 });

    // Find matching marker and open its popup
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

function toggleVisitedActivity(dayIdx, actIdx, event) {
  if (event) {
    event.stopPropagation();
  }

  if (!currentItineraryData || !currentItineraryData.days) return;
  const day = currentItineraryData.days[dayIdx];
  if (!day || !day.activities || !day.activities[actIdx]) return;

  const act = day.activities[actIdx];
  act.visited = !act.visited;

  renderItinerary(currentItineraryData);

  if (act.visited) {
    showNotificationToast(`Visited: "${act.title}"! Progress updated.`, 'success');
  }
}

function updateVisitedProgress() {
  if (!currentItineraryData || !currentItineraryData.days) return;

  let totalSpots = 0;
  let visitedSpots = 0;

  currentItineraryData.days.forEach(day => {
    (day.activities || []).forEach(act => {
      totalSpots++;
      if (act.visited) {
        visitedSpots++;
      }
    });
  });

  const pct = totalSpots > 0 ? Math.round((visitedSpots / totalSpots) * 100) : 0;

  // Update SVG Circular Progress Bar
  const circleBar = document.getElementById('itinerary-circle-bar');
  if (circleBar) {
    const circumference = 251.2; // 2 * PI * 40
    const offset = circumference - (circumference * pct / 100);
    circleBar.style.strokeDashoffset = offset;
  }

  const pctText = document.getElementById('itinerary-circle-pct');
  if (pctText) {
    pctText.textContent = `${pct}%`;
  }

  const subtitleText = document.getElementById('itinerary-circle-subtitle');
  if (subtitleText) {
    subtitleText.textContent = `${visitedSpots} of ${totalSpots} visiting spots covered`;
  }

  const statusBadge = document.getElementById('itinerary-circle-status');
  if (statusBadge) {
    if (pct === 0) {
      statusBadge.textContent = 'Ready for Departure';
      statusBadge.style.color = 'var(--accent-cyan)';
    } else if (pct < 100) {
      statusBadge.textContent = `In Progress (${pct}%)`;
      statusBadge.style.color = 'var(--accent-amber)';
    } else {
      statusBadge.textContent = 'Trip Completed! 🎉';
      statusBadge.style.color = 'var(--accent-emerald)';
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

  // Auto-sync From Currency based on searched city
  updateFromCurrencyForCity(dest);

  // Update Custom Day dropdown options based on selected days
  const customDaySelect = document.getElementById('custom-spot-day');
  if (customDaySelect) {
    customDaySelect.innerHTML = '';
    for (let d = 1; d <= days; d++) {
      customDaySelect.innerHTML += `<option value="${d}">Day ${d}</option>`;
    }
  }

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<div class="spinner"></div> Synthesizing & Optimizing TSP Route...`;
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

    // Optimize waypoints per day with Nearest-Neighbor / 2-Opt TSP
    (data.days || []).forEach(day => {
      day.activities = optimizeActivitiesTSP(day.activities, data.center_coordinates);
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
  let totalDistanceKm = 0;

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
    statusBadge.textContent = `${data.city || 'Destination'} (Optimal TSP Mapped)`;
  }

  (data.days || []).forEach((day, dayIdx) => {
    let actHtml = '';
    (day.activities || []).forEach((act, actIdx) => {
      globalPointIdx++;
      const pointNum = globalPointIdx;
      const formattedActCost = act.cost_inr > 0 ? formatCostFromINR(act.cost_inr) : "Free";
      const isVisited = !!act.visited;

      if (act.lat && act.lon && mapInstance) {
        // Calculate cumulative route distance
        if (mapCoords.length > 0) {
          const prev = mapCoords[mapCoords.length - 1];
          totalDistanceKm += calculateHaversineDistance(prev[0], prev[1], act.lat, act.lon);
        }
        mapCoords.push([act.lat, act.lon]);

        const pinClass = isVisited ? 'custom-map-pin visited-pin' : 'custom-map-pin';
        const pinContent = isVisited ? `✓` : `${pointNum}`;

        const customPinIcon = L.divIcon({
          className: 'custom-map-pin-container',
          html: `<div class="${pinClass}" title="${act.title}">${pinContent}</div>`,
          iconSize: [32, 32],
          iconAnchor: [16, 16],
          popupAnchor: [0, -18]
        });

        const marker = L.marker([act.lat, act.lon], { icon: customPinIcon })
          .addTo(mapInstance)
          .bindPopup(`
            <div style="font-family:'Outfit',sans-serif; padding:6px; min-width:190px;">
              <strong style="color:#0284c7; font-size:0.95rem;">#${pointNum} Day ${day.day}: ${sanitizeAndConvertEmojis(act.title)}</strong><br/>
              <span style="color:#64748b; font-size:0.82rem;">Time: ${act.time} | Cost: ${formattedActCost}</span><br/>
              <span style="display:inline-block; margin-top:2px; font-size:0.75rem; color:${isVisited ? '#10b981' : '#f59e0b'}; font-weight:700;">
                ${isVisited ? '✓ Completed / Visited' : '⏳ Scheduled to Visit'}
              </span>
              <p style="font-size:0.8rem; margin-top:4px; color:#334155;">${sanitizeAndConvertEmojis(act.desc)}</p>
            </div>
          `);
        mapMarkers.push(marker);
      }

      const escapedTitle = act.title.replace(/'/g, "\\'");
      actHtml += `
        <div class="timeline-item">
          <div class="timeline-dot" style="${isVisited ? 'background:var(--accent-emerald); border-color:rgba(16,185,129,0.5);' : ''}"></div>
          <div class="timeline-card ${isVisited ? 'is-visited' : ''}" onclick="focusMapActivity(${act.lat}, ${act.lon}, '${escapedTitle}', '${formattedActCost}', ${pointNum})" title="Click to view on interactive map">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <span style="font-weight: 700; color: var(--accent-cyan); font-size: 0.85rem; display:flex; align-items:center; gap:0.35rem;">
                <i data-lucide="clock" style="width:14px; height:14px;"></i> ${act.time}
              </span>
              <div style="display:flex; align-items:center; gap:0.5rem;">
                <button type="button" class="visited-toggle-btn ${isVisited ? 'is-visited' : ''}" onclick="toggleVisitedActivity(${dayIdx}, ${actIdx}, event)" title="Toggle visited state">
                  <i data-lucide="${isVisited ? 'check-circle-2' : 'circle'}" style="width:13px; height:13px;"></i>
                  <span>${isVisited ? 'Visited' : 'Mark Visited'}</span>
                </button>
                <span class="activity-badge"><i data-lucide="map-pin" style="width:11px; height:11px; margin-right:3px;"></i> Spot #${pointNum} | ${act.category}</span>
              </div>
            </div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 0.35rem;">${sanitizeAndConvertEmojis(act.title)}</h4>
            <p style="color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 0.5rem;">${sanitizeAndConvertEmojis(act.desc)}</p>
            <div style="display: flex; gap: 1.25rem; font-size: 0.78rem; color: var(--text-muted); align-items:center;">
              <span style="display:flex; align-items:center; gap:0.25rem;"><i data-lucide="hourglass" style="width:12px; height:12px;"></i> ${act.duration}</span>
              <span style="display:flex; align-items:center; gap:0.25rem; color:var(--accent-emerald); font-weight:600;"><i data-lucide="banknote" style="width:12px; height:12px;"></i> ${formattedActCost}</span>
              <button type="button" class="btn btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.65rem; margin-left:auto; color:var(--accent-cyan); display:flex; align-items:center; gap:0.25rem;" onclick="focusMapActivity(${act.lat}, ${act.lon}, '${escapedTitle}', '${formattedActCost}', ${pointNum})">
                <i data-lucide="crosshair" style="width:12px; height:12px;"></i> View on Map
              </button>
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
  const formattedRouteDist = `${Math.round(totalDistanceKm * 10) / 10} km`;

  container.innerHTML = `
    <div class="glass-card" style="margin-bottom: 1.5rem; background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1));">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
          <h2 style="font-size: 1.5rem; font-weight: 800;">${data.destination} - ${data.total_days} Day Masterplan</h2>
          <p style="color: var(--text-secondary); font-size: 0.9rem;">
            Style: ${data.travel_style} | Pace: ${data.pace} | Est. Total: <strong style="color:var(--accent-emerald); font-size:1.05rem;">${formattedTotalTrip}</strong> (${formattedDailyRate}/day)
          </p>
        </div>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
          <span class="brand-badge" style="background:rgba(16,185,129,0.15); color:var(--accent-emerald); border-color:rgba(16,185,129,0.3);">
            <i data-lucide="route" style="width:12px; height:12px; margin-right:4px;"></i> TSP Route: ${formattedRouteDist}
          </span>
          <span class="brand-badge"><i data-lucide="train" style="width:12px; height:12px; margin-right:4px;"></i> ${data.summary.recommended_transit_pass}</span>
        </div>
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

  // Update Circular Exploration Progress
  updateVisitedProgress();
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
      const pills = (d.dietary || []).map(tag => {
        const isNonVeg = tag.toLowerCase().includes('non-veg') || tag.toLowerCase().includes('poultry') || tag.toLowerCase().includes('meat') || tag.toLowerCase().includes('pork') || tag.toLowerCase().includes('seafood');
        const cls = isNonVeg ? 'dish-diet-pill non-veg' : 'dish-diet-pill';
        const icon = isNonVeg ? `<i data-lucide="drumstick" style="width:11px; height:11px; margin-right:3px;"></i>` : '';
        return `<span class="${cls}">${icon}${tag}</span>`;
      }).join(' ');
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
// Smart Packing Checklist with Custom Items & Live Progress
// ---------------------------------------------------------
function initPackingAssistant() {
  const generateBtn = document.getElementById('packing-generate-btn');
  if (!generateBtn) return;

  generateBtn.addEventListener('click', async () => {
    const dest = document.getElementById('packing-dest').value || 'Goa';
    const days = parseInt(document.getElementById('packing-days').value, 10) || 5;
    const season = document.getElementById('packing-season').value;

    // Sync From Currency as well
    updateFromCurrencyForCity(dest);

    generateBtn.disabled = true;
    generateBtn.innerHTML = `<div class="spinner"></div> Generating Checklist...`;

    try {
      const data = await API.generatePacking({
        destination: dest,
        days: days,
        season: season,
        activities: ["Sightseeing", "Dining", "Photography", "Walking"]
      });

      // Store in memory
      activePackingList = (data.checklist || []).map(item => ({
        item: item.item,
        category: item.category,
        essential: !!item.essential,
        checked: false,
        is_custom: false
      }));

      renderPackingChecklist(data.destination, data.season, data.trip_duration_days, data.luggage_advice);
    } catch (err) {
      const container = document.getElementById('packing-checklist-container');
      if (container) {
        container.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Failed to generate checklist.</div>`;
      }
    } finally {
      generateBtn.disabled = false;
      generateBtn.innerHTML = `<i data-lucide="check-square"></i> Generate Packing Checklist`;
      initLucideIcons();
    }
  });
}

function initCustomPackingBuilder() {
  const addBtn = document.getElementById('add-custom-packing-btn');
  const nameInput = document.getElementById('custom-packing-item-name');
  const catSelect = document.getElementById('custom-packing-cat');

  if (!addBtn || !nameInput) return;

  addBtn.addEventListener('click', () => {
    const name = nameInput.value.trim();
    if (!name) {
      nameInput.focus();
      showNotificationToast('Please enter an item name.', 'info');
      return;
    }

    if (activePackingList.length === 0) {
      // Create empty list container if not generated yet
      const dest = document.getElementById('packing-dest').value || 'Trip';
      activePackingList = [];
    }

    const newItem = {
      item: name,
      category: catSelect.value,
      essential: catSelect.value === 'Essentials',
      checked: false,
      is_custom: true
    };

    activePackingList.unshift(newItem);
    nameInput.value = '';

    const dest = document.getElementById('packing-dest').value || 'Trip';
    const season = document.getElementById('packing-season').value || 'Summer';
    const days = document.getElementById('packing-days').value || '5';

    renderPackingChecklist(dest, season, days, "Custom items incorporated into luggage checklist.");
    showNotificationToast(`Added "${name}" to your packing checklist!`, 'success');
  });

  nameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      addBtn.click();
    }
  });
}

function removeCustomPackingItem(index, event) {
  if (event) event.stopPropagation();
  if (index >= 0 && index < activePackingList.length) {
    const removed = activePackingList.splice(index, 1);
    const dest = document.getElementById('packing-dest').value || 'Trip';
    const season = document.getElementById('packing-season').value || 'Summer';
    const days = document.getElementById('packing-days').value || '5';
    renderPackingChecklist(dest, season, days, "Luggage checklist updated.");
    showNotificationToast(`Removed "${removed[0].item}".`, 'info');
  }
}

function renderPackingChecklist(destination = 'Trip', season = 'Summer', days = 5, luggageAdvice = '') {
  const container = document.getElementById('packing-checklist-container');
  if (!container) return;

  let itemsHtml = '';
  activePackingList.forEach((item, idx) => {
    const isChecked = !!item.checked;
    const isCustom = !!item.is_custom;

    itemsHtml += `
      <div class="checklist-item ${isChecked ? 'checked' : ''}" onclick="toggleCheckItem(${idx}, this, event)">
        <input type="checkbox" class="checklist-checkbox" id="chk-${idx}" ${isChecked ? 'checked' : ''} onchange="toggleCheckItem(${idx}, this.closest('.checklist-item'), event)" />
        <div style="flex: 1;">
          <span class="item-title" style="font-size: 0.92rem; color: #fff;">${sanitizeAndConvertEmojis(item.item)}</span>
          <span style="font-size: 0.72rem; color: var(--accent-cyan); margin-left: 0.5rem; text-transform: uppercase;">[${item.category}]</span>
          ${isCustom ? '<span style="font-size: 0.68rem; color: var(--accent-amber); margin-left: 0.35rem;">(Custom)</span>' : ''}
        </div>
        ${item.essential ? '<span class="dish-diet-pill" style="color:var(--accent-rose); border-color:rgba(244,63,94,0.3); background:rgba(244,63,94,0.15);">Essential</span>' : ''}
        ${isCustom ? `<button type="button" class="checklist-delete-btn" onclick="removeCustomPackingItem(${idx}, event)" title="Delete custom item"><i data-lucide="trash-2" style="width:14px; height:14px;"></i></button>` : ''}
      </div>
    `;
  });

  container.innerHTML = `
    <div class="checklist-progress-card">
      <div class="checklist-progress-header">
        <div>
          <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff;">${destination} (${season}) - ${days} Days</h3>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.2rem; display:flex; align-items:center; gap:0.4rem;">
            <i data-lucide="briefcase"></i> ${luggageAdvice || 'Luggage & Outfit Index'}
          </p>
        </div>
        <div style="text-align: right;">
          <span id="checklist-pct-badge" class="checklist-pct-badge">0%</span>
          <div id="checklist-count-badge" style="font-size: 0.75rem; color: var(--text-muted);">0 of ${activePackingList.length} items packed</div>
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
  initLucideIcons();
}

function updateChecklistProgress() {
  const total = activePackingList.length;
  if (total === 0) return;

  let checkedCount = 0;
  activePackingList.forEach(item => {
    if (item.checked) checkedCount++;
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

function toggleCheckItem(idx, el, event) {
  if (event && event.target && event.target.tagName === 'BUTTON') return;
  if (idx >= 0 && idx < activePackingList.length) {
    const cb = el ? el.querySelector('input[type="checkbox"]') : null;
    if (event && event.target === cb) {
      activePackingList[idx].checked = cb.checked;
    } else {
      activePackingList[idx].checked = !activePackingList[idx].checked;
      if (cb) cb.checked = activePackingList[idx].checked;
    }
    if (el) el.classList.toggle('checked', activePackingList[idx].checked);
    updateChecklistProgress();
  }
}

function selectAllChecklist(checkAll = true) {
  activePackingList.forEach(item => {
    item.checked = checkAll;
  });
  const checkboxes = document.querySelectorAll('.checklist-checkbox');
  checkboxes.forEach(cb => {
    cb.checked = checkAll;
    const parent = cb.closest('.checklist-item');
    if (parent) parent.classList.toggle('checked', checkAll);
  });
  updateChecklistProgress();
  initLucideIcons();
}

// ---------------------------------------------------------
// Multilingual Audio Phrasebook & Voice Translation Studio
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

const SPEECH_RECOGNITION_LANG_MAP = {
  English: 'en-US',
  Tamil: 'ta-IN',
  Telugu: 'te-IN',
  Hindi: 'hi-IN',
  French: 'fr-FR',
  Spanish: 'es-ES',
  Japanese: 'ja-JP',
  German: 'de-DE',
  Urdu: 'ur-IN',
  Bengali: 'bn-IN',
  Marathi: 'mr-IN',
  auto: 'en-US'
};

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

function initTranslationStudio() {
  const srcSelect = document.getElementById('translator-source-lang');
  const tgtSelect = document.getElementById('translator-target-lang');
  const swapBtn = document.getElementById('translator-swap-btn');
  const translateBtn = document.getElementById('translate-action-btn');
  const inputTxt = document.getElementById('translator-input-text');
  const resultBox = document.getElementById('translation-result-container');
  const voiceMicBtn = document.getElementById('translator-mic-btn');
  const studioCard = document.getElementById('live-voice-translation-studio');
  const toggleStudioBtn = document.getElementById('btn-toggle-translation-studio');
  const closeStudioBtn = document.getElementById('btn-close-translation-studio');

  // Studio Toggle & Close (Modal/Drawer interaction)
  if (toggleStudioBtn && studioCard) {
    toggleStudioBtn.addEventListener('click', () => {
      const isClosed = studioCard.style.display === 'none' || !studioCard.style.display;
      if (isClosed) {
        studioCard.style.display = 'block';
        toggleStudioBtn.classList.add('active');
        studioCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        initLucideIcons();
      } else {
        studioCard.style.display = 'none';
        toggleStudioBtn.classList.remove('active');
      }
    });
  }

  if (closeStudioBtn && studioCard) {
    closeStudioBtn.addEventListener('click', () => {
      studioCard.style.display = 'none';
      if (toggleStudioBtn) {
        toggleStudioBtn.classList.remove('active');
      }
      const phrasesSection = document.getElementById('phrasebook-content');
      if (phrasesSection) {
        phrasesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  if (!translateBtn || !inputTxt) return;

  // Language Swap
  if (swapBtn) {
    swapBtn.addEventListener('click', () => {
      const srcVal = srcSelect.value === 'auto' ? 'English' : srcSelect.value;
      const tgtVal = tgtSelect.value;
      srcSelect.value = tgtVal;
      tgtSelect.value = srcVal;

      // Swap contents if existing translation
      if (inputTxt.value.trim() && resultBox && resultBox.dataset.translatedText) {
        inputTxt.value = resultBox.dataset.translatedText;
      }
      showNotificationToast(`Swapped: ${tgtVal} → ${srcVal}`, 'info');
    });
  }

  // Preset chips
  document.querySelectorAll('.translation-quick-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const src = chip.getAttribute('data-src');
      const tgt = chip.getAttribute('data-tgt');
      const sample = chip.getAttribute('data-sample');

      if (srcSelect) srcSelect.value = src;
      if (tgtSelect) tgtSelect.value = tgt;
      if (inputTxt) inputTxt.value = sample;

      executeTranslation();
    });
  });

  // Voice speech recognition for translation
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (voiceMicBtn && SpeechRecognition) {
    let recognition = null;
    let isListening = false;

    voiceMicBtn.addEventListener('click', (e) => {
      e.preventDefault();
      if (isListening && recognition) {
        recognition.stop();
        return;
      }

      try {
        const srcLang = srcSelect.value || 'English';
        const recLangCode = SPEECH_RECOGNITION_LANG_MAP[srcLang] || 'en-US';

        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = recLangCode;

        recognition.onstart = () => {
          isListening = true;
          voiceMicBtn.classList.add('recording');
          showNotificationToast(`Listening in ${srcLang} (${recLangCode}). Speak now...`, 'info');
        };

        recognition.onresult = (event) => {
          if (event.results && event.results[0] && event.results[0][0]) {
            const transcript = event.results[0][0].transcript;
            if (transcript) {
              inputTxt.value = transcript;
              showNotificationToast(`Captured: "${transcript}"`, 'success');
              executeTranslation();
            }
          }
        };

        recognition.onerror = (event) => {
          console.warn('Voice translation speech recognition error:', event.error);
          voiceMicBtn.classList.remove('recording');
        };

        recognition.onend = () => {
          isListening = false;
          voiceMicBtn.classList.remove('recording');
        };

        recognition.start();
      } catch (err) {
        console.error('Speech recognition error:', err);
        voiceMicBtn.classList.remove('recording');
      }
    });
  }

  async function executeTranslation() {
    const text = inputTxt.value.trim();
    if (!text) {
      inputTxt.focus();
      showNotificationToast('Please type or speak a phrase to translate.', 'info');
      return;
    }

    const src = srcSelect.value;
    const tgt = tgtSelect.value;

    translateBtn.disabled = true;
    translateBtn.innerHTML = `<div class="spinner"></div> Translating...`;
    resultBox.style.display = 'block';
    resultBox.innerHTML = `<div style="text-align:center; padding: 1.5rem;"><div class="spinner"></div><p style="margin-top:0.5rem; color:var(--text-secondary); font-size:0.85rem;">Translating to ${tgt} with speech synthesis...</p></div>`;

    try {
      const data = await API.translatePhrase(text, src, tgt);
      resultBox.dataset.translatedText = data.translated_text;

      const encNative = encodeURIComponent(data.translated_text);
      const encRomanized = encodeURIComponent(data.romanized || '');
      const langCode = data.speech_lang_code || 'en-US';

      resultBox.innerHTML = `
        <div class="translation-result-card">
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span class="activity-badge" style="background:rgba(6,182,212,0.15); color:var(--accent-cyan); border-color:rgba(6,182,212,0.3);">
                ${data.source_language} → ${data.target_language}
              </span>
              <button type="button" class="btn btn-secondary" style="font-size:0.75rem; padding:0.2rem 0.6rem;" onclick="copyTranslationText('${encNative}')">
                <i data-lucide="copy" style="width:12px; height:12px;"></i> Copy
              </button>
            </div>

            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.25rem;">Original: "${sanitizeAndConvertEmojis(data.original_text)}"</div>
            <h3 style="font-size: 1.5rem; font-weight: 800; color: #fff; line-height: 1.3; margin: 0.35rem 0;">${data.translated_text}</h3>
            
            ${data.romanized && data.romanized !== data.translated_text ? `
              <div style="font-size: 0.95rem; color: var(--accent-cyan); display:flex; align-items:center; gap:0.35rem; margin-top: 0.35rem;">
                <i data-lucide="mic" style="width:14px; height:14px;"></i> Pronunciation: <i>${data.romanized}</i>
              </div>
            ` : ''}
          </div>

          <button type="button" class="audio-play-btn" onclick="playSpeech('${encNative}', '${encRomanized}', '${langCode}', this)" title="Listen to Native Pronunciation" style="margin-top:0.25rem;">
            <i data-lucide="volume-2" style="width:20px; height:20px;"></i>
          </button>
        </div>
      `;
      initLucideIcons();
      showNotificationToast('Translation ready! Click the speaker icon to listen.', 'success');
    } catch (err) {
      resultBox.innerHTML = `<div class="glass-card" style="color: var(--accent-rose);"><i data-lucide="alert-circle"></i> Translation failed. ${err.message}</div>`;
      initLucideIcons();
    } finally {
      translateBtn.disabled = false;
      translateBtn.innerHTML = `<i data-lucide="sparkles"></i> Translate & Listen`;
      initLucideIcons();
    }
  }

  translateBtn.addEventListener('click', executeTranslation);
}

function copyTranslationText(encText) {
  const text = decodeURIComponent(encText || '');
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => {
      showNotificationToast('Translated text copied to clipboard!', 'success');
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
  setupMicButton('global-mic-btn', 'global-city-search', (val) => {
    const searchBtn = document.getElementById('global-search-btn');
    if (searchBtn) searchBtn.click();
  });

  setupMicButton('vision-mic-btn', 'vision-prompt');

  setupMicButton('weather-mic-btn', 'weather-city-input', () => {
    const searchBtn = document.getElementById('weather-search-btn');
    if (searchBtn) searchBtn.click();
  });

  setupMicButton('itinerary-mic-btn', 'itinerary-dest', (val) => {
    updateFromCurrencyForCity(val);
    const genBtn = document.getElementById('itinerary-generate-btn');
    if (genBtn) genBtn.click();
  });

  setupMicButton('custom-spot-mic-btn', 'custom-spot-name');

  setupMicButton('food-mic-btn', 'food-city-input', (val) => {
    updateFromCurrencyForCity(val);
    const searchBtn = document.getElementById('food-search-btn');
    if (searchBtn) searchBtn.click();
  });

  setupMicButton('packing-mic-btn', 'packing-dest', (val) => {
    updateFromCurrencyForCity(val);
    const genBtn = document.getElementById('packing-generate-btn');
    if (genBtn) genBtn.click();
  });

  setupMicButton('custom-packing-mic-btn', 'custom-packing-item-name');

  setupMicButton('budget-mic-btn', 'budget-city', (val) => {
    updateFromCurrencyForCity(val);
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

    // Automatically set From Currency to this city's currency
    updateFromCurrencyForCity(city);

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
    showNotificationToast(`Destination set to ${formattedCity}. Synced across all travel modules with local currency!`, 'success');
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


