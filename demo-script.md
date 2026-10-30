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
| 0:20-0:35 | Sunita asks | Press the big mic, ask in Marathi about rain damage to cotton (2 acres, Nashik) | Meet Sunita, 2 acres of cotton near Nashik. Rain damaged her crop. She just speaks. |
| 0:35-0:50 | Spoken answer with source | Answer card plays audio, shows "Source: document, page" | She hears the answer and sees exactly which official document it came from. |
| 0:50-1:00 | Offer accepted | Tap "Prepare application" | The assistant offers to prepare her application. She says yes. |
| 1:00-1:20 | 3 to 5 questions | Answer village, acres, date by voice | Only a few simple questions. No Aadhaar or ID numbers. |
| 1:20-1:40 | Draft PDF and checklist | Show PDF preview, play spoken checklist, point at the missing-document warning | A draft in her language and a spoken checklist. It warns her one document is missing. Nothing is submitted. |
| 1:40-1:55 | SMS mode (prototype) | Mock feature-phone screen, type FASAL | No smartphone? Same rules engine over SMS. Labelled prototype. |
| 1:55-2:05 | Panchayat dashboard | Dashboard with simulated counts | Panchayat offices see what villagers ask. Counts are simulated. |
| 2:05-2:15 | One crop question | Ask a crop question by voice | Crop advice from official material, with source. |
| 2:15-2:25 | One health question (ASHA role) | Switch to ASHA worker, ask a health question | ASHA workers get short checklist answers. No diagnosis. |
| 2:25-2:35 | One refused question | Ask something outside the documents | When unsure, it refuses and points to the panchayat office, CSC or Kisan Call Centre. |
| 2:35-2:55 | Emergency demo | Say a fire phrase, or tap the red SOS button | Emergency skips the AI. Big number, Call button, nearest hospital, one safety line. |
| 2:55-3:00 | Close | Home screen | Answer first, then help the user act. DHARA. |

## Things to rehearse
- The exact Marathi sentence Sunita says (native speaker to check): NEEDS HUMAN VERIFICATION
- The emergency phrase for the demo (pick one from data/emergency/emergency.json).
- Which beats are real and which are mock on demo day (write it here before Phase 5): TO FILL.

## Numbers and facts to confirm before the demo
- Emergency numbers (101, 108, 112 and others): NEEDS HUMAN VERIFICATION
- PMFBY reporting time limit and benefit text: NEEDS HUMAN VERIFICATION
- Every "Source: document, page" shown on screen: NEEDS HUMAN VERIFICATION