#!/usr/bin/env python3
"""
Script to create placeholder audio files for testing the MajorChord audio player.
This creates simple sine wave audio files for demonstration purposes.
"""

import os
import wave
import struct
import math

def create_sine_wave(filename, frequency=440, duration=30, sample_rate=44100):
    """Create a simple sine wave audio file"""
    
    # Calculate number of frames
    num_frames = int(sample_rate * duration)
    
    # Create the audio data
    audio_data = []
    for i in range(num_frames):
        # Generate sine wave
        value = math.sin(2 * math.pi * frequency * i / sample_rate)
        # Convert to 16-bit integer
        audio_data.append(int(value * 32767))
    
    # Create WAV file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters: 1 channel, 2 bytes per sample, sample rate, number of frames
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.setnframes(num_frames)
        
        # Write audio data
        for sample in audio_data:
            wav_file.writeframes(struct.pack('<h', sample))

def create_placeholder_file(filename, content):
    """Create a placeholder text file for MP3 files"""
    with open(filename, 'w') as f:
        f.write(content)

def main():
    """Create sample audio files for the MajorChord app"""
    
    # Ensure audio directory exists
    if not os.path.exists('audio'):
        os.makedirs('audio')
    
    # Define the audio files to create with symptom-based characteristics
    audio_files = [
        # Stress Relief & Relaxation (Low frequencies, longer durations)
        ("weightless.mp3", 220, 480, "Stress relief - Marconi Union's Weightless"),
        ("claire_de_lune.mp3", 330, 300, "Classical relaxation - Debussy"),
        ("river_flows.mp3", 440, 240, "Piano meditation - Yiruma"),
        ("sound_of_silence.mp3", 550, 270, "Contemplative rock - Disturbed"),
        
        # Energy & Motivation (Higher frequencies, upbeat)
        ("eye_of_tiger.mp3", 660, 264, "Energetic rock - Survivor"),
        ("happy.mp3", 440, 233, "Uplifting pop - Pharrell Williams"),
        ("cant_stop_feeling.mp3", 330, 235, "Upbeat pop - Justin Timberlake"),
        ("shake_it_off.mp3", 550, 219, "Cheerful pop - Taylor Swift"),
        
        # Focus & Concentration (Medium frequencies, steady)
        ("lofi_study.mp3", 220, 1800, "Lo-fi study beats"),
        ("classical_study.mp3", 330, 1200, "Classical study music - Mozart"),
        ("white_noise.mp3", 440, 3600, "White noise for focus"),
        ("brain_fm_focus.mp3", 220, 1800, "Brain.fm focus music"),
        
        # Sleep & Rest (Very low frequencies, long durations)
        ("sleep_well.mp3", 110, 3600, "Sleep sounds"),
        ("ocean_waves.mp3", 165, 3600, "Ocean waves for sleep"),
        ("rain_sounds.mp3", 220, 3600, "Rain sounds for relaxation"),
        ("deep_sleep.mp3", 82, 3600, "Deep sleep music"),
        
        # Mood Enhancement (Varied frequencies)
        ("good_vibes.mp3", 440, 240, "Positive energy pop"),
        ("sunshine.mp3", 550, 210, "Happy tunes"),
        ("dance_party.mp3", 660, 180, "Energetic beats"),
        ("chill_vibes.mp3", 330, 300, "Relaxed beats"),
        
        # Additional songs for comprehensive library
        ("moonlight_sonata.mp3", 330, 900, "Beethoven - Moonlight Sonata"),
        ("here_comes_sun.mp3", 440, 185, "The Beatles - Here Comes the Sun"),
        ("walking_sunshine.mp3", 550, 235, "Katrina & The Waves"),
        ("concentration.mp3", 220, 1800, "Brain.fm concentration"),
        ("study_music.mp3", 330, 1200, "Lo-fi study music"),
        ("meditation_sounds.mp3", 165, 3600, "Meditation ambient"),
        ("deep_breathing.mp3", 110, 1800, "Deep breathing guide"),
        ("nature_sounds.mp3", 220, 3600, "Nature ambient"),
        ("calm_melodies.mp3", 330, 600, "Calm piano melodies"),
        ("uplifting_beats.mp3", 440, 240, "Uplifting electronic"),
        ("relaxation_guide.mp3", 165, 1800, "Relaxation guide"),
        ("stress_relief.mp3", 220, 1200, "Stress relief music"),
        ("anxiety_calm.mp3", 165, 1800, "Anxiety calming sounds"),
        ("depression_lift.mp3", 440, 300, "Depression lifting music"),
        ("insomnia_cure.mp3", 110, 3600, "Insomnia relief"),
        ("focus_enhance.mp3", 330, 1800, "Focus enhancement"),
        ("mood_boost.mp3", 550, 240, "Mood boosting music"),
        ("energy_boost.mp3", 660, 180, "Energy boosting music"),
        ("sleep_aid.mp3", 82, 3600, "Sleep aid music"),
        ("calm_anxiety.mp3", 165, 1800, "Anxiety calming"),
        ("uplift_depression.mp3", 440, 300, "Depression uplifting"),
        ("focus_concentration.mp3", 220, 1800, "Concentration focus"),
        ("relax_stress.mp3", 165, 1200, "Stress relaxation"),
        ("sleep_insomnia.mp3", 110, 3600, "Insomnia sleep"),
        ("boost_mood.mp3", 550, 240, "Mood boosting"),
        ("energize_life.mp3", 660, 180, "Life energizing"),
        ("calm_mind.mp3", 220, 1800, "Mind calming"),
        ("heal_anxiety.mp3", 165, 1800, "Anxiety healing"),
        ("lift_spirits.mp3", 440, 300, "Spirit lifting"),
        ("concentrate_focus.mp3", 220, 1800, "Focus concentrating"),
        ("relax_body.mp3", 165, 1200, "Body relaxation"),
        ("sleep_deep.mp3", 82, 3600, "Deep sleep"),
        ("calm_heart.mp3", 165, 1800, "Heart calming"),
        ("uplift_soul.mp3", 440, 300, "Soul uplifting"),
        ("focus_mind.mp3", 220, 1800, "Mind focusing"),
        ("relax_muscles.mp3", 165, 1200, "Muscle relaxation"),
        ("sleep_peace.mp3", 82, 3600, "Peaceful sleep"),
    ]
    
    print("Creating comprehensive sample audio files for MajorChord...")
    
    for filename, frequency, duration, description in audio_files:
        filepath = os.path.join('audio', filename)
        print(f"Creating {filename} - {description}")
        
        # Create placeholder text file (simulating MP3)
        content = f"""Placeholder audio file for {filename}
Description: {description}
Frequency: {frequency}Hz
Duration: {duration} seconds
This is a placeholder file for testing the audio player.
In a real application, this would be an actual MP3 file.
"""
        create_placeholder_file(filepath, content)
    
    print(f"\nCreated {len(audio_files)} sample audio files in the 'audio' directory.")
    print("Note: These are placeholder files. In a real application, you would use actual MP3 files.")

if __name__ == "__main__":
    main() 