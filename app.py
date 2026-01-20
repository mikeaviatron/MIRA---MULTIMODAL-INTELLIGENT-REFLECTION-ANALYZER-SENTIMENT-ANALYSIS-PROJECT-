import streamlit as st
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from helpers.voice_analysis import analyze_audio
from helpers.speech_recognition import speech_to_text
from helpers.speech_sentiment import analyze_sentiment
from helpers.video_analysis import analyze_video
from helpers.face_emotion import detect_emotion
from helpers.feedback_generator import full_summary

# --- Page Config ---
st.set_page_config(
    page_title="Project MIRA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>

.centered-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.15);
    margin-bottom: 25px;
}
.metric-title {font-weight: 600; font-size: 18px;}
.metric-value {font-size: 24px; font-weight: bold;}
.badge {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 12px;
    font-weight: bold;
    color: white;
    font-size: 14px;
}
.positive {background-color: #4CAF50;}
.neutral {background-color: #FFC107;}
.negative {background-color: #F44336;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="centered-title">🧠 Project MIRA</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align:center;">Multimodal Intelligent Reflection Analyzer</h4>', unsafe_allow_html=True)
st.divider()

# --- Video Uploader ---
uploaded_video = st.file_uploader("📤 Upload your speaking video (MP4)", type=["mp4"])

# Register Unicode font for emojis in PDF
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

def generate_pdf_report_with_charts(pitch, tempo, eye_contact, sentiment, emotion, feedback, chart_path):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>🧠 Project MIRA - Personality Analysis Report</b>", styles['Title']))
    story.append(Spacer(1, 12))

    # Metrics
    story.append(Paragraph(f"🎤 <b>Average Pitch:</b> {pitch:.1f} Hz", styles['Normal']))
    story.append(Paragraph(f"⏱ <b>Average Tempo:</b> {tempo:.1f} BPM", styles['Normal']))
    story.append(Paragraph(f"👁 <b>Eye Contact:</b> {eye_contact:.1f}%", styles['Normal']))
    story.append(Paragraph(f"🧠 <b>Sentiment:</b> {sentiment}", styles['Normal']))
    story.append(Paragraph(f"😊 <b>Emotion:</b> {emotion}", styles['Normal']))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>📈 Performance Trends:</b>", styles['Heading2']))
    story.append(Image(chart_path, width=400, height=300))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>📊 Detailed Feedback:</b>", styles['Heading2']))
    feedback_lines = feedback.strip().split("\n")
    for line in feedback_lines:
        story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 6))

    doc.build(story)
    return temp_file.name

if uploaded_video:
    with st.spinner("⏳ Processing video..."):
        os.makedirs("uploads", exist_ok=True)
        video_path = os.path.join("uploads", "input.mp4")
        audio_path = os.path.join("uploads", "audio.wav")

        # Save video
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())

        # Extract audio using ffmpeg
        subprocess.call([
            'ffmpeg', '-y', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', audio_path
        ])

        # --- Analysis ---
        pitch_array, tempo_array = analyze_audio(audio_path, return_array=True)
        eye_contact_array = analyze_video(video_path, return_array=True)

        # Synchronize lengths
        min_len = min(len(pitch_array), len(tempo_array), len(eye_contact_array))
        pitch_array = pitch_array[:min_len]
        tempo_array = tempo_array[:min_len]
        eye_contact_array = eye_contact_array[:min_len]
        frames = np.arange(min_len)

        # Averages
        pitch = np.mean(pitch_array)
        tempo = np.mean(tempo_array)
        eye_contact = np.mean(eye_contact_array) * 100

        text = speech_to_text(audio_path)
        sentiment = analyze_sentiment(text)
        emotion = detect_emotion(video_path)
        feedback = full_summary(pitch, tempo, eye_contact, sentiment, emotion)

    st.success("✅ Analysis complete!")

    # --- Dashboard ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="card"><h4 class="metric-title">🎤 Average Pitch</h4>'
                    f'<p class="metric-value">{pitch:.1f} Hz</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card"><h4 class="metric-title">⏱ Average Tempo</h4>'
                    f'<p class="metric-value">{tempo:.1f} BPM</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="card"><h4 class="metric-title">👁 Eye Contact</h4>'
                    f'<p class="metric-value">{eye_contact:.1f}%</p></div>', unsafe_allow_html=True)

    # --- Trend Chart ---
    st.markdown('<div class="card"><h4>📈 Performance Trends</h4></div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    ax[0].plot(frames, pitch_array, color='#4B7BEC', label='Pitch (Hz)')
    ax[0].legend(); ax[0].grid()

    ax[1].plot(frames, tempo_array, color='#FF9800', label='Tempo (BPM)')
    ax[1].legend(); ax[1].grid()

    ax[2].plot(frames, eye_contact_array*100, color='#4CAF50', label='Eye Contact (%)')
    ax[2].legend(); ax[2].grid()
    ax[2].set_xlabel('Frame Number')

    chart_path = os.path.join("uploads", "trend_chart.png")
    plt.savefig(chart_path)
    st.pyplot(fig)

    # --- Sentiment & Emotion ---
    st.markdown('<div class="card"><h4>🧠 Speech Sentiment & Emotion</h4></div>', unsafe_allow_html=True)
    sentiment_class = "positive" if sentiment=="Positive" else "neutral" if sentiment=="Neutral" else "negative"
    emotion_class = "positive" if emotion in ["happy","surprise"] else "neutral" if emotion=="neutral" else "negative"
    st.markdown(f"""
        <span class="badge {sentiment_class}">Sentiment: {sentiment}</span>
        &nbsp;&nbsp;
        <span class="badge {emotion_class}">Emotion: {emotion}</span>
    """, unsafe_allow_html=True)

    # --- Feedback ---
    st.markdown('<div class="card"><h4>📊 Detailed Personality & Performance Insights</h4></div>', unsafe_allow_html=True)
    feedback_lines = feedback.strip().split("\n")
    formatted_feedback = "".join([f"<p>{line}</p>" for line in feedback_lines])
    st.markdown(f'<div class="card">{formatted_feedback}</div>', unsafe_allow_html=True)

    # --- Download PDF Button ---
    pdf_file = generate_pdf_report_with_charts(pitch, tempo, eye_contact, sentiment, emotion, feedback, chart_path)
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📥 Download Full Report (PDF)",
            data=f,
            file_name="MIRA_Report.pdf",
            mime="application/pdf"
        )
