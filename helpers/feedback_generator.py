def full_summary(pitch, tempo, eye_contact, sentiment, emotion):
    return f"""
**🎤 Voice Analysis**
- Pitch: {pitch:.2f} Hz – {voice_pitch_feedback(pitch)}
- Tempo: {tempo:.2f} BPM – {voice_tempo_feedback(tempo)}
- Vocal Energy: {vocal_energy_feedback(pitch, tempo)}

**👁️ Eye Contact**
- Eye Contact Ratio: {eye_contact:.2f}% – {eye_contact_feedback(eye_contact)}

**🧠 Speech Sentiment**
- Overall Sentiment: {sentiment} – {sentiment_feedback(sentiment)}

**😊 Facial Emotion**
- Dominant Emotion: {emotion} – {emotion_feedback(emotion)}

**📌 Personality Insights**
{generate_personality_feedback(pitch, tempo, eye_contact, sentiment, emotion)}

**💡 Recommendations for Improvement**
{generate_recommendations(pitch, tempo, eye_contact, sentiment, emotion)}
"""

# --- Helper Functions ---
def voice_pitch_feedback(pitch):
    if pitch < 140:
        return "Low-pitched voice; try slightly raising pitch for clarity and authority."
    elif pitch > 200:
        return "High-pitched voice; maintain stability for confident delivery."
    elif 140 <= pitch < 160:
        return "Pitch is on the lower side; slightly increase for expressiveness."
    elif 180 < pitch <= 200:
        return "Pitch is on the higher side; control variation for professional tone."
    else:
        return "Pitch is well-balanced and clear."

def voice_tempo_feedback(tempo):
    if tempo < 80:
        return "Speech is slow; increasing pace slightly will improve engagement."
    elif tempo > 120:
        return "Speech is fast; slowing down ensures clarity and comprehension."
    else:
        return "Tempo is optimal for listener understanding."

def vocal_energy_feedback(pitch, tempo):
    if pitch > 180 and 90 <= tempo <= 110:
        return "Strong and energetic voice; commands attention."
    elif pitch < 150 or tempo < 85:
        return "Voice could be more lively; try varying pitch and pace for expression."
    else:
        return "Moderately energetic; slight adjustments can enhance impact."

def eye_contact_feedback(eye_contact):
    if eye_contact >= 80:
        return "Excellent eye engagement; audience feels connected."
    elif 60 <= eye_contact < 80:
        return "Good eye contact; maintain consistency for stronger presence."
    elif 40 <= eye_contact < 60:
        return "Moderate eye contact; consider practicing to improve audience connection."
    else:
        return "Low eye engagement; focus on maintaining gaze for confidence."

def sentiment_feedback(sentiment):
    sentiment = sentiment.lower()
    if sentiment == "positive":
        return "You convey confidence and optimism."
    elif sentiment == "neutral":
        return "Neutral tone; adding slight enthusiasm will engage listeners better."
    elif sentiment == "negative":
        return "Tone may appear pessimistic; practice positivity in expression."
    else:
        return f"Detected sentiment: {sentiment}. Focus on clarity and confidence."

def emotion_feedback(emotion):
    emotion = emotion.lower()
    if emotion in ["happy", "joy", "surprise"]:
        return "Emotionally engaging; audience perceives warmth and energy."
    elif emotion in ["sad", "fear", "anger"]:
        return "Emotion may seem tense or subdued; adjust facial expressions to appear approachable."
    elif emotion in ["neutral"]:
        return "Neutral expressions; consider emphasizing key points with slight facial cues."
    else:
        return f"Detected emotion: {emotion}. Use controlled expressions for clarity."

def generate_personality_feedback(pitch, tempo, eye_contact, sentiment, emotion):
    lines = []

    # Voice presence
    if pitch > 180:
        lines.append("✅ Strong vocal presence; commands attention naturally.")
    elif pitch < 150:
        lines.append("🟡 Consider raising pitch slightly to convey authority.")
    else:
        lines.append("✅ Balanced pitch; voice is clear and pleasant.")

    # Speech tempo
    if 90 <= tempo <= 110:
        lines.append("✅ Speech pace is ideal; listeners can easily follow.")
    elif tempo < 90:
        lines.append("🟡 Slightly slow speech; may lose listener engagement. Practice pacing.")
    else:
        lines.append("🟡 Slightly fast speech; slow down at key points to improve clarity.")

    # Eye contact
    if eye_contact >= 70:
        lines.append("✅ Maintains good eye contact; builds trust and engagement.")
    else:
        lines.append("🟡 Practice consistent eye contact to appear confident and approachable.")

    # Sentiment
    if sentiment.lower() == "positive":
        lines.append("✅ Conveys optimism and confidence.")
    elif sentiment.lower() == "neutral":
        lines.append("🟡 Neutral tone; try adding warmth and enthusiasm for better connection.")
    else:
        lines.append("🟡 Tone may seem negative; focus on positivity to boost listener perception.")

    # Emotion
    lines.append(f"🧠 Dominant emotion detected: {emotion}. Align facial expressions with your message for maximum impact.")

    return "\n".join(lines)

def generate_recommendations(pitch, tempo, eye_contact, sentiment, emotion):
    lines = []

    # General actionable tips
    lines.append("- Practice varying pitch to keep audience engaged.")
    lines.append("- Maintain moderate tempo; pause at key points to emphasize ideas.")
    lines.append("- Record and review your speech to notice patterns in voice and emotion.")
    lines.append("- Ensure eye contact aligns with key messages for stronger connection.")
    lines.append("- Use facial expressions deliberately to match the speech content.")
    lines.append("- Incorporate positive language to reflect confidence and optimism.")

    # Voice-energy specific
    if pitch < 150 or tempo < 85:
        lines.append("- Consider vocal exercises to increase energy and projection.")

    # Eye contact specific
    if eye_contact < 60:
        lines.append("- Practice speaking to a camera or mirror to improve eye engagement.")

    return "\n".join(lines)
