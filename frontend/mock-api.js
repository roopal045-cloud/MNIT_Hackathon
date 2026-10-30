// mock-api.js - fake backend answers, shaped exactly like the API contract.
// ALL facts, numbers and names here are DEMO values.
// NEEDS HUMAN VERIFICATION before any real use.

const MOCK_API = (function () {
  const DELAY_MS = 700; // pretend the server is thinking

  function wait(value) {
    return new Promise(function (resolve) {
      setTimeout(function () { resolve(value); }, DELAY_MS);
    });
  }

  // Words that make the mock treat a question as an emergency.
  const EMERGENCY_WORDS = [
    "आग", "साँप", "सांप", "साप", "दुर्घटना", "अपघात", "खून", "रक्तस्त्राव",
    "प्रसव", "सीने में दर्द", "सांस", "श्वास", "बाढ़", "पूर", "ज़हर", "विष",
    "fire", "snake", "accident", "bleeding", "flood", "poison"
  ];

  const COTTON_WORDS = ["कपास", "कापूस", "cotton", "बारिश", "पाऊस", "rain", "नुकसान", "नुकसानी"];

  function hasAny(text, words) {
    const t = (text || "").toLowerCase();
    return words.some(function (w) { return t.indexOf(w.toLowerCase()) !== -1; });
  }

  const SOURCE_DEMO = {
    doc: "Revised_Operational_Guidelines.pdf (PMFBY)",
    page: "NEEDS HUMAN VERIFICATION",
    snippet: "DEMO snippet: localized claims procedure. NEEDS HUMAN VERIFICATION"
  };

  const COTTON_ANSWER = {
    mr: "डेमो उत्तर: पावसामुळे कापसाचे नुकसान झाले असेल, तर पीक विमा योजनेअंतर्गत नुकसानीची माहिती लवकरात लवकर द्या. तुमच्या गावातील कृषी कार्यालयाशी संपर्क करा. (अचूक मुदत: NEEDS HUMAN VERIFICATION)",
    hi: "डेमो उत्तर: बारिश से कपास को नुकसान हुआ है तो फसल बीमा योजना में नुकसान की सूचना जल्द से जल्द दें। अपने गाँव के कृषि कार्यालय से संपर्क करें। (सही समय-सीमा: NEEDS HUMAN VERIFICATION)"
  };

  const REFUSED_ANSWER = {
    mr: "माफ करा, मला याचे खात्रीशीर उत्तर माहीत नाही. कृपया ग्रामपंचायत कार्यालय, CSC केंद्र किंवा किसान कॉल सेंटरशी संपर्क करा.",
    hi: "माफ़ कीजिए, मुझे इसका पक्का उत्तर नहीं पता। कृपया पंचायत कार्यालय, CSC केंद्र या किसान कॉल सेंटर से संपर्क करें।"
  };

  const FIRE_MESSAGE = {
    mr: "आग लागली आहे. लगेच 101 वर फोन करा.",
    hi: "आग लगी है। तुरंत 101 पर फ़ोन करें।"
  };

  const FIRE_SAFETY = {
    mr: "DEMO सुरक्षा ओळ: सुरक्षित ठिकाणी जा. NEEDS HUMAN VERIFICATION",
    hi: "DEMO सुरक्षा पंक्ति: सुरक्षित जगह पर जाएँ। NEEDS HUMAN VERIFICATION"
  };

  function emergencyResponse(language) {
    const lang = language === "mr" ? "mr" : "hi";
    return {
      type: "fire",
      number: "101", // DEMO - NEEDS HUMAN VERIFICATION
      call_uri: "tel:101",
      message_text: FIRE_MESSAGE[lang],
      audio_url: null,
      safety_line: FIRE_SAFETY[lang],
      hospitals: [
        {
          name: "DEMO Hospital, Nashik (placeholder)",
          distance_km: 2.5,
          maps_url: "https://www.google.com/maps"
        }
      ]
    };
  }

  // POST /ask  (input is a plain object: {text, language, mode, role})
  function ask(input) {
    const language = input.language === "mr" ? "mr" : "hi";
    const text = input.text || "";

    if (hasAny(text, EMERGENCY_WORDS)) {
      const e = emergencyResponse(language);
      return wait({
        transcript: text,
        language: language,
        is_emergency: true,
        answer_text: e.message_text,
        audio_url: null,
        source: null,
        confidence: 1,
        refused: false,
        offer_application: null
      });
    }

    // Voice (no text) or a cotton/rain question -> the hero answer.
    if (!text || hasAny(text, COTTON_WORDS)) {
      return wait({
        transcript: text || (language === "mr"
          ? "माझ्या कापसाचे पावसाने नुकसान झाले आहे"
          : "मेरी कपास की फसल बारिश से खराब हो गई"),
        language: language,
        is_emergency: false,
        answer_text: COTTON_ANSWER[language],
        audio_url: null,
        source: SOURCE_DEMO,
        confidence: 0.82,
        refused: false,
        offer_application: "crop_damage"
      });
    }

    // Anything else -> polite refusal.
    return wait({
      transcript: text,
      language: language,
      is_emergency: false,
      answer_text: REFUSED_ANSWER[language],
      audio_url: null,
      source: null,
      confidence: 0.2,
      refused: true,
      offer_application: null
    });
  }

  // POST /emergency  (input: {language, type, lat, lon})
  function emergency(input) {
    return wait(emergencyResponse(input && input.language));
  }

  // POST /draft  (input: {scheme, language, answers})
  function draft(input) {
    return wait({
      pdf_url: null, // no real PDF in the mock
      checklist: [
        { item: "7/12 उतारा (land record)", status: "have" },
        { item: "Bank passbook copy", status: "missing" },
        { item: "Photos of damaged crop", status: "have" }
      ],
      checklist_audio_url: null,
      missing: ["Bank passbook copy"]
    });
  }

  // POST /sms  (input: {text})
  function sms(input) {
    const t = ((input && input.text) || "").trim().toUpperCase();
    if (t === "EMERGENCY") {
      return wait({ reply_text: "DEMO: Fire 101, Ambulance 108, Police 100. NEEDS HUMAN VERIFICATION" });
    }
    if (t === "FASAL") {
      return wait({ reply_text: "DEMO: 1) Report loss quickly. 2) Keep photos. 3) Visit agriculture office. NEEDS HUMAN VERIFICATION" });
    }
    return wait({ reply_text: "DEMO: Send FASAL or EMERGENCY." });
  }

  // GET /panchayat/stats
  function panchayatStats() {
    return wait({
      topics: [
        { topic: "Crop damage", count: 42 },
        { topic: "Pregnancy benefit", count: 17 },
        { topic: "Health", count: 25 }
      ],
      simulated: true
    });
  }

  return { ask: ask, emergency: emergency, draft: draft, sms: sms, panchayatStats: panchayatStats };
})();