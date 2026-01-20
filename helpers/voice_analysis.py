import librosa
import numpy as np

def analyze_audio(file_path, return_array=False):
    y, sr = librosa.load(file_path, sr=None)
    
    # Compute frame-wise tempo (per 0.5 sec window)
    hop_length = int(sr * 0.5)  # 0.5 second window
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    
    # Pitch using YIN
    f0 = librosa.yin(y, fmin=75, fmax=300, sr=sr)
    
    if return_array:
        # Split pitch array into frame chunks matching video frames (approx)
        num_frames = int(librosa.get_duration(y=y, sr=sr) * 30)  # assuming 30 FPS video
        pitch_array = np.interp(np.linspace(0, len(f0), num_frames), np.arange(len(f0)), f0)
        tempo_array = np.full(num_frames, tempo[0])  # tempo constant
        return pitch_array, tempo_array
    else:
        pitch = np.mean(f0)
        return pitch, tempo[0]
