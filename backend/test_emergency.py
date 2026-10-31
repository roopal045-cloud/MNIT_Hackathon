from app.services.emergency import ENTRIES, detect_emergency, get_emergency_reply

print("entries loaded:", len(ENTRIES))

for phrase in ["मेरे घर में आग लग गई है", "सांप ने काट लिया", "मला साप चावला", "मेरी कपास की फसल खराब हो गई"]:
    print(detect_emergency(phrase))

reply = get_emergency_reply("snakebite", "hi")
print(reply["type"], reply["number"], reply["call_uri"])