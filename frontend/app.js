// app.js - main logic of the DHARA front end.

(function () {
  // ---------- Texts in Hindi and Marathi ----------
  const STR = {
    hi: {
      title: "बोलकर पूछिए", mic: "दबाकर बोलिए", micStop: "रोकने के लिए दबाइए",
      listening: "सुन रहा हूँ...", thinking: "सोच रहा हूँ...", speaking: "बोल रहा हूँ...",
      play: "सुनिए", offer: "आवेदन तैयार करें", back: "वापस", sos: "आपातकाल",
      call: "फ़ोन करें", maps: "नक्शे में खोलें",
      roleFarmer: "किसान", roleAsha: "आशा कार्यकर्ता",
      lowOff: "कम डेटा: बंद", lowOn: "कम डेटा: चालू",
      crops: "फसल", schemes: "योजनाएँ", health: "स्वास्थ्य",
      source: "स्रोत", page: "पृष्ठ", km: "किमी",
      noMic: "माइक नहीं मिला। डेमो उत्तर दिखा रहा हूँ।",
      offerSoon: "आवेदन की सुविधा बाद के चरण में जुड़ेगी।",
      cottonQ: "मेरी कपास की फसल बारिश से खराब हो गई"
    },
    mr: {
      title: "बोलून विचारा", mic: "दाबून बोला", micStop: "थांबवण्यासाठी दाबा",
      listening: "ऐकत आहे...", thinking: "विचार करत आहे...", speaking: "बोलत आहे...",
      play: "ऐका", offer: "अर्ज तयार करा", back: "मागे", sos: "आणीबाणी",
      call: "फोन करा", maps: "नकाशात उघडा",
      roleFarmer: "शेतकरी", roleAsha: "आशा कार्यकर्ती",
      lowOff: "कमी डेटा: बंद", lowOn: "कमी डेटा: चालू",
      crops: "पीक", schemes: "योजना", health: "आरोग्य",
      source: "स्रोत", page: "पान", km: "किमी",
      noMic: "माइक सापडला नाही. डेमो उत्तर दाखवत आहे.",
      offerSoon: "अर्जाची सुविधा नंतरच्या टप्प्यात जोडली जाईल.",
      cottonQ: "माझ्या कापसाचे पावसाने नुकसान झाले आहे"
    }
  };

  // ---------- App state ----------
  const state = {
    language: CONFIG.DEFAULT_LANGUAGE,
    role: "farmer",        // "farmer" or "asha"
    mode: "normal",        // "normal" or "low_data"
    recorder: null,
    chunks: [],
    listening: false,
    lastAnswer: null,
    audioEl: null
  };

  // ---------- Small helpers ----------
  function $(id) { return document.getElementById(id); }
  function t() { return STR[state.language]; }

  function showScreen(name) {
    ["home", "answer", "emergency"].forEach(function (s) {
      $("screen-" + s).classList.toggle("hidden", s !== name);
    });
    window.scrollTo(0, 0);
  }

  function setMicState(name) { // "", "listening", "thinking", "speaking"
    const btn = $("mic-btn");
    btn.classList.remove("listening", "thinking", "speaking");
    if (name) btn.classList.add(name);
    const labels = {
      "": t().mic, listening: t().micStop, thinking: t().thinking, speaking: t().speaking
    };
    $("mic-label").textContent = labels[name];
    $("status").textContent = name ? t()[name] : "";
  }

  function speechLang() { return state.language === "mr" ? "mr-IN" : "hi-IN"; }

  function stopSpeaking() {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    if (state.audioEl) { state.audioEl.pause(); state.audioEl = null; }
  }

  // Play the server audio if there is one, else the browser's own voice.
  function speak(text, audioUrl) {
    stopSpeaking();
    if (audioUrl) {
      const url = /^https?:/.test(audioUrl) ? audioUrl : CONFIG.API_BASE_URL + audioUrl;
      state.audioEl = new Audio(url);
      state.audioEl.play().catch(function () {});
      return;
    }
    if (window.speechSynthesis && text) {
      const u = new SpeechSynthesisUtterance(text);
      u.lang = speechLang();
      window.speechSynthesis.speak(u);
    }
  }

  // ---------- Talking to the backend (or the mock) ----------
  async function postWithTimeout(path, options) {
    const ctrl = new AbortController();
    const timer = setTimeout(function () { ctrl.abort(); }, 5000);
    try {
      const res = await fetch(CONFIG.API_BASE_URL + path, Object.assign({ signal: ctrl.signal }, options));
      if (!res.ok) throw new Error("HTTP " + res.status);
      return await res.json();
    } finally {
      clearTimeout(timer);
    }
  }

  async function callAsk(audioBlob, text) {
    try {
      const form = new FormData();
      form.append("language", state.language);
      form.append("mode", state.mode);
      form.append("role", state.role);
      if (audioBlob) form.append("audio", audioBlob, "question.webm");
      if (text) form.append("text", text);
      return await postWithTimeout("/ask", { method: "POST", body: form });
    } catch (err) {
      if (!CONFIG.FALLBACK_TO_MOCK) throw err;
      console.warn("Backend not reachable, using mock:", err);
      return MOCK_API.ask({ text: text || "", language: state.language, mode: state.mode, role: state.role });
    }
  }

  async function callEmergency() {
    try {
      return await postWithTimeout("/emergency", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language: state.language })
      });
    } catch (err) {
      if (!CONFIG.FALLBACK_TO_MOCK) throw err;
      console.warn("Backend not reachable, using mock:", err);
      return MOCK_API.emergency({ language: state.language });
    }
  }

  // ---------- Showing results ----------
  function showAnswer(data) {
    state.lastAnswer = data;
    $("answer-transcript").textContent = data.transcript ? "“" + data.transcript + "”" : "";
    $("answer-text").textContent = data.answer_text || "";

    const refused = $("answer-refused");
    const source = $("answer-source");
    if (data.refused) {
      refused.textContent = data.answer_text;
      refused.classList.remove("hidden");
      $("answer-text").classList.add("hidden");
      source.textContent = "";
    } else {
      refused.classList.add("hidden");
      $("answer-text").classList.remove("hidden");
      source.textContent = data.source
        ? t().source + ": " + data.source.doc + ", " + t().page + " " + data.source.page
        : "";
    }

    $("offer-btn").classList.toggle("hidden", !data.offer_application);
    showScreen("answer");
    setMicState("");
    speak(data.answer_text, data.audio_url);
  }

  function showEmergency(e) {
    $("em-message").textContent = e.message_text || "";
    $("em-number").textContent = e.number || "";
    $("em-call").setAttribute("href", e.call_uri || "tel:112");

    const hospital = (e.hospitals && e.hospitals[0]) || null;
    document.querySelector(".em-hospital").classList.toggle("hidden", !hospital);
    if (hospital) {
      $("em-hospital-name").textContent = hospital.name;
      $("em-hospital-dist").textContent = hospital.distance_km + " " + t().km;
      $("em-maps").setAttribute("href", hospital.maps_url || "#");
    }
    $("em-safety").textContent = e.safety_line || "";
    showScreen("emergency");
    setMicState("");
    speak(e.message_text, e.audio_url);
  }

  async function handleResult(data) {
    if (data.is_emergency) {
      showEmergency(await callEmergency());
    } else {
      showAnswer(data);
    }
  }

  async function sendQuestion(audioBlob, text) {
    setMicState("thinking");
    try {
      await handleResult(await callAsk(audioBlob, text));
    } catch (err) {
      console.error(err);
      setMicState("");
      $("status").textContent = "⚠️ " + err.message;
    }
  }

  // ---------- Mic recording (tap to start, tap to stop) ----------
  async function toggleMic() {
    stopSpeaking();
    if (state.listening) { state.recorder.stop(); return; }

    if (!navigator.mediaDevices || !window.MediaRecorder) {
      $("status").textContent = t().noMic;
      sendQuestion(null, "");
      return;
    }

    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch (err) {
      $("status").textContent = t().noMic;
      sendQuestion(null, "");
      return;
    }

    state.chunks = [];
    state.recorder = new MediaRecorder(stream);
    state.recorder.ondataavailable = function (ev) { if (ev.data.size > 0) state.chunks.push(ev.data); };
    state.recorder.onstop = function () {
      state.listening = false;
      stream.getTracks().forEach(function (tr) { tr.stop(); });
      sendQuestion(new Blob(state.chunks, { type: "audio/webm" }), "");
    };
    state.recorder.start();
    state.listening = true;
    setMicState("listening");
  }

  // ---------- Language, role, low-data ----------
  function renderLanguageButtons() {
    const box = $("lang-switch");
    box.innerHTML = "";
    CONFIG.LANGUAGES.forEach(function (lang) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "lang-btn" + (lang.code === state.language ? " active" : "");
      b.textContent = lang.enabled ? lang.label : lang.label + " (जल्द)";
      b.disabled = !lang.enabled;
      b.addEventListener("click", function () { state.language = lang.code; applyLanguage(); });
      box.appendChild(b);
    });
  }

  function applyLanguage() {
    const s = t();
    document.documentElement.lang = state.language;
    $("home-title").textContent = s.title;
    $("play-label").textContent = s.play;
    $("offer-label").textContent = s.offer;
    $("back-label").textContent = s.back;
    $("em-back-label").textContent = s.back;
    $("em-call-label").textContent = s.call;
    $("em-maps-label").textContent = s.maps;
    $("sos-label").textContent = s.sos;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      el.textContent = s[el.getAttribute("data-i18n")];
    });
    $("role-label").textContent = state.role === "farmer" ? s.roleFarmer : s.roleAsha;
    $("lowdata-label").textContent = state.mode === "low_data" ? s.lowOn : s.lowOff;
    renderLanguageButtons();
    setMicState(state.listening ? "listening" : "");
  }

  // ---------- Wire up the buttons ----------
  function init() {
    $("mic-btn").addEventListener("click", toggleMic);

    $("role-btn").addEventListener("click", function () {
      state.role = state.role === "farmer" ? "asha" : "farmer";
      applyLanguage();
    });

    $("lowdata-btn").addEventListener("click", function () {
      state.mode = state.mode === "normal" ? "low_data" : "normal";
      $("lowdata-btn").classList.toggle("on", state.mode === "low_data");
      applyLanguage();
    });

    document.querySelectorAll(".topic").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const topic = btn.getAttribute("data-topic");
        // "crops" asks the hero cotton question; others send the topic word.
        const question = topic === "crops" ? t().cottonQ : t()[topic];
        sendQuestion(null, question);
      });
    });

    $("play-btn").addEventListener("click", function () {
      if (state.lastAnswer) speak(state.lastAnswer.answer_text, state.lastAnswer.audio_url);
    });

    $("offer-btn").addEventListener("click", function () { alert(t().offerSoon); });

    function goHome() { stopSpeaking(); showScreen("home"); setMicState(""); }
    $("back-btn").addEventListener("click", goHome);
    $("em-back").addEventListener("click", goHome);

    $("sos-btn").addEventListener("click", async function () {
      stopSpeaking();
      showEmergency(await callEmergency());
    });

    applyLanguage();
    showScreen("home");
  }

  document.addEventListener("DOMContentLoaded", init);
})();