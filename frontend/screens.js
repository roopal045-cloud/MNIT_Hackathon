// screens.js - MOCK screens for the demo video (fixed text, nothing is real).
// 1) application draft + checklist  2) SMS feature-phone (prototype)
// 3) panchayat dashboard (simulated). All numbers here are DEMO values.

(function () {
  var TXT = {
    mr: {
      draftTitle: "अर्जाचा मसुदा", draftTag: "नमुना · काहीही सादर केलेले नाही",
      rows: [["नाव", "सुनीता"], ["जिल्हा", "नाशिक"], ["पीक", "कापूस"], ["क्षेत्र", "2 एकर"],
             ["कारण", "गारपीट / शेतात पूर"], ["तारीख", "(डेमो)"]],
      checkTitle: "कागदपत्रांची यादी", have: "आहे", missing: "कमी आहे",
      items: [["७/१२ उतारा", true], ["नुकसानीचे फोटो", true], ["बँक पासबुक प्रत", false]],
      warn: "एक कागदपत्र कमी आहे: बँक पासबुक प्रत. 72 तासांत नुकसान कळवा.",
      speak: "तुमच्याकडे सात बारा उतारा आणि फोटो आहेत. बँक पासबुकची प्रत कमी आहे. 72 तासांत नुकसान कळवा.",
      listen: "यादी ऐका", back: "मागे",
      smsTitle: "एसएमएस (प्रोटोटाइप)", smsHint: "साधा फोन · इंटरनेट नाही",
      smsFasal: "FASAL", smsEm: "EMERGENCY",
      smsReplyFasal: "1) 72 तासांत नुकसान कळवा 2) फोटो ठेवा 3) कृषी कार्यालयात जा",
      smsReplyEm: "आग 101, रुग्णवाहिका 108, आपत्कालीन 112",
      dashTitle: "पंचायत डॅशबोर्ड", dashTag: "सिम्युलेटेड (डेमो) आकडे",
      topics: [["पीक नुकसान", 42], ["गर्भवती महिला लाभ", 17], ["आरोग्य", 25]],
      homeSms: "एसएमएस (प्रोटोटाइप)", homeDash: "पंचायत डॅशबोर्ड"
    },
    hi: {
      draftTitle: "आवेदन का मसौदा", draftTag: "नमूना · कुछ भी जमा नहीं किया गया",
      rows: [["नाम", "सुनीता"], ["जिला", "नाशिक"], ["फसल", "कपास"], ["क्षेत्र", "2 एकड़"],
             ["कारण", "ओलावृष्टि / खेत में बाढ़"], ["तारीख", "(डेमो)"]],
      checkTitle: "दस्तावेज़ों की सूची", have: "है", missing: "कम है",
      items: [["७/१२ उतारा", true], ["नुकसान की फोटो", true], ["बैंक पासबुक की कॉपी", false]],
      warn: "एक दस्तावेज़ कम है: बैंक पासबुक की कॉपी। 72 घंटे में नुकसान की सूचना दें।",
      speak: "आपके पास सात बारह उतारा और फोटो हैं। बैंक पासबुक की कॉपी कम है। 72 घंटे में नुकसान की सूचना दें।",
      listen: "सूची सुनिए", back: "वापस",
      smsTitle: "एसएमएस (प्रोटोटाइप)", smsHint: "साधा फ़ोन · इंटरनेट नहीं",
      smsFasal: "FASAL", smsEm: "EMERGENCY",
      smsReplyFasal: "1) 72 घंटे में नुकसान बताएँ 2) फोटो रखें 3) कृषि कार्यालय जाएँ",
      smsReplyEm: "आग 101, एम्बुलेंस 108, आपात 112",
      dashTitle: "पंचायत डैशबोर्ड", dashTag: "सिमुलेटेड (डेमो) आँकड़े",
      topics: [["फसल नुकसान", 42], ["गर्भवती महिला लाभ", 17], ["स्वास्थ्य", 25]],
      homeSms: "एसएमएस (प्रोटोटाइप)", homeDash: "पंचायत डैशबोर्ड"
    }
  };

  var CSS = [
    ".mk{padding:24px 16px 120px}",
    ".mk h2{margin:0 0 4px;color:#0b2a5b;font-size:1.4rem}",
    ".mk .tag{display:inline-block;background:#fff3cd;color:#7a5200;border:1px solid #f0c36d;border-radius:999px;padding:4px 12px;font-size:.85rem;margin-bottom:14px}",
    ".mk .box{background:#fff;border-radius:18px;padding:16px;box-shadow:0 2px 8px rgba(11,42,91,.08);margin-bottom:14px}",
    ".mk .row{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid #dde5f0}",
    ".mk .row:last-child{border-bottom:0}",
    ".mk .k{color:#5a6475}.mk .v{font-weight:700;text-align:right}",
    ".mk .ok{color:#138808;font-weight:700}.mk .bad{color:#d32f2f;font-weight:700}",
    ".mk .warn{background:#fdecea;border:2px solid #d32f2f;color:#8a1c1c;border-radius:14px;padding:12px;font-weight:700;margin-bottom:14px}",
    ".phone{width:260px;margin:0 auto 16px;background:#1b1f2a;border-radius:28px;padding:18px 14px 22px}",
    ".phone .scr{background:#cfe8c8;border-radius:8px;min-height:230px;padding:10px;font-family:monospace;font-size:.85rem;color:#173317}",
    ".phone .msg{margin:0 0 8px;white-space:pre-wrap;word-break:break-word}",
    ".phone .me{text-align:right;font-weight:700}",
    ".keys{display:flex;gap:10px;justify-content:center;margin-bottom:14px}",
    ".keys button,.homeextra button{font:inherit}",
    ".bar{display:flex;align-items:center;gap:10px;margin:10px 0}",
    ".bar .name{width:44%;font-size:.95rem}",
    ".bar .fill{height:22px;border-radius:6px;background:linear-gradient(90deg,#f28c1b,#138808)}",
    ".bar .n{font-weight:700}",
    ".homeextra{display:flex;flex-direction:column;gap:10px;margin:18px 0 0}"
  ].join("");

  function $(id) { return document.getElementById(id); }
  function lang() { var s = $("lang-select"); return s && s.value === "mr" ? "mr" : "hi"; }
  function T() { return TXT[lang()]; }

  function speak(text) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = lang() === "mr" ? "mr-IN" : "hi-IN";
    window.speechSynthesis.speak(u);
  }

  function hideAll() {
    document.querySelectorAll(".screen").forEach(function (el) { el.classList.add("hidden"); });
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    window.scrollTo(0, 0);
  }
  function goHome() { hideAll(); $("screen-home").classList.remove("hidden"); }

  function backBtn() {
    var b = document.createElement("button");
    b.className = "big-btn navy";
    b.type = "button";
    b.textContent = T().back;
    b.onclick = goHome;
    return b;
  }

  function mkScreen(id) {
    var el = $(id);
    if (!el) {
      el = document.createElement("section");
      el.id = id;
      el.className = "screen mk hidden";
      document.querySelector(".app").appendChild(el);
    }
    el.innerHTML = "";
    return el;
  }

  function add(parent, tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    parent.appendChild(e);
    return e;
  }

  // ---------- 1) application draft + checklist ----------
  function openDraft() {
    var x = T();
    hideAll();
    var s = mkScreen("screen-draft");
    add(s, "h2", "", x.draftTitle);
    add(s, "div", "tag", x.draftTag);
    var box = add(s, "div", "box");
    x.rows.forEach(function (r) {
      var row = add(box, "div", "row");
      add(row, "span", "k", r[0]);
      add(row, "span", "v", r[1]);
    });
    var cb = add(s, "div", "box");
    add(cb, "div", "k", x.checkTitle);
    x.items.forEach(function (it) {
      var row = add(cb, "div", "row");
      add(row, "span", "", it[0]);
      add(row, "span", it[1] ? "ok" : "bad", it[1] ? "✓ " + x.have : "✗ " + x.missing);
    });
    add(s, "div", "warn", x.warn);
    var l = add(s, "button", "big-btn blue", x.listen);
    l.type = "button";
    l.onclick = function () { speak(x.speak); };
    s.appendChild(backBtn());
    s.classList.remove("hidden");
    speak(x.speak);
  }

  // ---------- 2) SMS feature-phone ----------
  function openSms() {
    var x = T();
    hideAll();
    var s = mkScreen("screen-sms");
    add(s, "h2", "", x.smsTitle);
    add(s, "div", "tag", x.smsHint);
    var phone = add(s, "div", "phone");
    var scr = add(phone, "div", "scr");
    add(scr, "p", "msg", "DHARA SMS");
    var keys = add(s, "div", "keys");
    function send(word, reply) {
      add(scr, "p", "msg me", "> " + word);
      setTimeout(function () { add(scr, "p", "msg", reply); }, 600);
    }
    var a = add(keys, "button", "big-btn green", x.smsFasal);
    a.type = "button"; a.onclick = function () { send("FASAL", x.smsReplyFasal); };
    var b = add(keys, "button", "big-btn blue", x.smsEm);
    b.type = "button"; b.onclick = function () { send("EMERGENCY", x.smsReplyEm); };
    s.appendChild(backBtn());
    s.classList.remove("hidden");
  }

  // ---------- 3) panchayat dashboard ----------
  function openDash() {
    var x = T();
    hideAll();
    var s = mkScreen("screen-dash");
    add(s, "h2", "", x.dashTitle);
    add(s, "div", "tag", x.dashTag);
    var box = add(s, "div", "box");
    x.topics.forEach(function (tp) {
      var bar = add(box, "div", "bar");
      add(bar, "span", "name", tp[0]);
      var f = add(bar, "span", "fill");
      f.style.width = (tp[1] * 3) + "px";
      add(bar, "span", "n", String(tp[1]));
    });
    s.appendChild(backBtn());
    s.classList.remove("hidden");
  }

  // ---------- add the two buttons on the home screen ----------
  function addHomeButtons() {
    var home = $("screen-home");
    if (!home || $("home-extra")) return;
    var wrap = document.createElement("div");
    wrap.id = "home-extra";
    wrap.className = "homeextra";
    var b1 = document.createElement("button");
    b1.className = "big-btn blue"; b1.type = "button"; b1.id = "home-sms";
    b1.onclick = openSms;
    var b2 = document.createElement("button");
    b2.className = "big-btn navy"; b2.type = "button"; b2.id = "home-dash";
    b2.onclick = openDash;
    wrap.appendChild(b1); wrap.appendChild(b2);
    home.appendChild(wrap);
    refreshHomeLabels();
  }
  function refreshHomeLabels() {
    if (!$("home-sms")) return;
    $("home-sms").textContent = T().homeSms;
    $("home-dash").textContent = T().homeDash;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var st = document.createElement("style");
    st.textContent = CSS;
    document.head.appendChild(st);
    addHomeButtons();
    var sel = $("lang-select");
    if (sel) sel.addEventListener("change", refreshHomeLabels);
  });

  // app.js calls this when the green "prepare application" button is tapped
  window.DHARA_openDraft = openDraft;
})();