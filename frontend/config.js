// config.js - settings shared by all frontend files

const CONFIG = {
  // Where the backend (Person A's FastAPI server) runs.
  // On the Android emulator this will change to http://10.0.2.2:8000 later.
  API_BASE_URL: "http://127.0.0.1:8000",

  // The app opens in Hindi. Users can switch to Marathi.
  DEFAULT_LANGUAGE: "hi",

  // Languages: Tamil is shown disabled ("coming soon").
  LANGUAGES: [
    { code: "hi", label: "हिंदी", enabled: true },
    { code: "mr", label: "मराठी", enabled: true },
    { code: "ta", label: "தமிழ்", enabled: false }
  ],

  // If the backend is not running, use fake answers from mock-api.js.
  FALLBACK_TO_MOCK: true
};