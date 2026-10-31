# DHARA demo script (3 minutes)

Rule for the demo: say "prototype" for SMS and dashboard. All counts are
simulated and labelled. Never claim a number is verified unless it is.

## Setup before we start
- Backend running, frontend open on the laptop (phone-shaped, centred).
- App language set to Marathi, role Farmer, low-data OFF.
- Phone on the same Wi-Fi as a backup screen.
- Backup plan: if the backend fails, the app uses the mock answers. Say nothing, continue.

## Timed beats

| Time | Beat | Who / what we show | What to say (one line) |
|------|------|--------------------|------------------------|
| 0:00-0:20 | The problem | Slide or home screen | Schemes, crop and health info are in English or formal Hindi. Rural users cannot use them. DHARA answers by voice in their language. |
| 0:20-0:35 | Sunita asks | Press the big mic, ask in Marathi: her cotton field was flooded or hit by hail (2 acres, Nashik) | Meet Sunita, 2 acres of cotton near Nashik. Her field was flooded or hit by hail. She just speaks. |
| 0:35-0:50 | Spoken answer with source | Answer card plays audio, shows "Source: document, page" | She hears the answer and sees exactly which official document it came from. |
| 0:50-1:00 | Offer accepted | Tap "Prepare application" | The assistant offers to prepare her application. She says yes. |
| 1:00-1:20 | 3 to 5 questions | Answer village, acres, date by voice | Only a few simple questions. No Aadhaar or ID numbers. |
| 1:20-1:40 | Draft PDF and checklist | Show PDF preview, play spoken checklist, point at the missing-document warning | A draft in her language and a spoken checklist. It warns her one document is missing. Nothing is submitted. |
| 1:40-1:55 | SMS mode (prototype) | Mock feature-phone screen, type FASAL | No smartphone? Same rules engine over SMS. Labelled prototype. |
| 1:55-2:05 | Panchayat dashboard | Dashboard with simulated counts | Panchayat offices see what villagers ask. Counts are simulated. |
| 2:05-2:15 | One crop question | Ask a crop question by voice | Crop advice from official material, with source. |
| 2:15-2:25 | One health question (ASHA role) | Switch to ASHA worker, ask a health question | ASHA workers get short checklist answers. No diagnosis. |
| 2:25-2:35 | One refused question | Ask something outside the documents | When unsure, it refuses and points to the panchayat office, CSC or Kisan Call Centre. |
| 2:35-2:55 | Emergency demo | Say a fire phrase, or tap the red SOS button | Emergency skips the AI. Big number, Call button, one safety line. Hospital shown only if a verified one exists. |
| 2:55-3:00 | Close | Home screen | Answer first, then help the user act. DHARA. |

## Which beats are real and which are mock
- REAL (live backend): the Marathi question, the spoken answer with its source,
  the refused question, the health question, and the SOS screen.
- MOCK (built-in sample data, not connected to the backend): the application
  draft and checklist, the SMS screen (prototype), the dashboard counts (simulated).
- Say "prototype" for SMS and "simulated" for the dashboard counts, every time.
- If the backend is off, the app falls back to mock answers for everything.

## Things to rehearse
- The exact Marathi sentence Sunita says (flooded or hit by hail): NEEDS HUMAN
  VERIFICATION by a native Marathi speaker.
- The emergency phrase for the demo (pick one from data/emergency/emergency.json).
- Hospital block on the SOS screen: it is hidden when the hospital is missing or
  its name says PLACEHOLDER or DEMO. Do not show a placeholder hospital on camera.

## Numbers and facts to confirm before the demo
- Emergency numbers (101, 108, 112 and others): NEEDS HUMAN VERIFICATION.
  data/emergency/VERIFICATION.md has not confirmed them. Do not say "verified".
- PMFBY reporting time limit and benefit text: NEEDS HUMAN VERIFICATION
- Every "Source: document, page" shown on screen: NEEDS HUMAN VERIFICATION
- Sunita's cause of loss (flooded or hit by hail): plain "rain" is not a covered
  cause, so keep this wording.
  ## Sunita's sentence (Marathi) and what a native speaker must confirm

Sentence Sunita says (spoken and sent by the Crops card): NEEDS HUMAN VERIFICATION
- Marathi: माझ्या कापसाच्या पिकाचे पुरामुळे किंवा गारपिटीमुळे नुकसान झाले आहे
- Meaning: "My cotton crop has been damaged by flood or hail."
- Hindi version: मेरी कपास की फसल बाढ़ या ओलावृष्टि से खराब हो गई (NEEDS HUMAN VERIFICATION)

A native Marathi speaker must confirm:
1. The sentence sounds natural for a Nashik farmer (not too formal or bookish).
2. The word for hail (गारपीट) and flood (पूर) are the words villagers use in Nashik.
3. She can say it clearly in one breath, so the speech recognition hears it right.
4. The first two lines of the spoken answer: grammar, tone, and that nothing is
   promised (no "you will get money").
5. The refusal text points to the panchayat office, CSC or Kisan Call Centre in
   natural Marathi.
6. The Marathi labels on screen (mic, play, SOS, call, back) read naturally.
7. The Marathi spoken text sounds right on the gTTS voice; if a word is
   mispronounced, note it and reword.

First lines of the answer shown on screen: TO FILL after the real answer is
checked (see below).
Status: NEEDS HUMAN VERIFICATION until a native speaker signs off.