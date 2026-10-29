#!/usr/bin/env python3
"""
render_all_premium_reels.py
Complete rendering orchestrator for all 5 broadcast-grade video reels.
Renders Google Chrome HTML5 slides (Google Fonts, glassmorphism, 3D graphics)
and generates smooth Ken-Burns 3D motion videos with sound design.
"""

import os
import shutil
import subprocess
import numpy as np
import wave
from PIL import Image

WIDTH = 1080
HEIGHT = 1920
FPS = 30
SCENE_DUR = 4.5  # seconds per scene
FADE_DUR = 0.5   # seconds crossfade

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")

def generate_soundtrack(output_wav, total_sec=22.5):
    print(">>> Generating 124 BPM tech soundtrack with transition SFX...")
    sr = 44100
    bpm = 124
    beat_sec = 60.0 / bpm
    n_samples = int(total_sec * sr)
    t = np.linspace(0, total_sec, n_samples, False)
    audio = np.zeros(n_samples, dtype=np.float32)

    # Kick drum on every beat
    for b in range(int(total_sec / beat_sec)):
        k_start = int(b * beat_sec * sr)
        k_len = int(0.22 * sr)
        if k_start + k_len < n_samples:
            kt = np.linspace(0, 0.22, k_len, False)
            freq = 150.0 * np.exp(-kt * 22)
            kick = np.sin(2 * np.pi * freq * kt) * np.exp(-kt * 16)
            audio[k_start:k_start+k_len] += kick * 0.55

    # Hi-hat on every half beat
    for h in range(int(total_sec / (beat_sec / 2))):
        h_start = int(h * (beat_sec / 2) * sr)
        h_len = int(0.045 * sr)
        if h_start + h_len < n_samples:
            noise = np.random.uniform(-1, 1, h_len) * np.exp(-np.linspace(0, 0.045, h_len) * 90)
            audio[h_start:h_start+h_len] += noise * 0.12

    # Synth pad chord progression
    f_chord = 0.10 * np.sin(2 * np.pi * 174.61 * t) + 0.08 * np.sin(2 * np.pi * 220.0 * t) + 0.07 * np.sin(2 * np.pi * 261.63 * t)
    audio += f_chord * (0.85 + 0.15 * np.sin(2 * np.pi * 0.4 * t))

    audio = np.clip(audio, -0.95, 0.95)
    audio_i16 = (audio * 32767).astype(np.int16)

    raw_beat = "/tmp/raw_beat.wav"
    with wave.open(raw_beat, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_i16.tobytes())

    # Mix with SFX at scene transition offsets
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", raw_beat,
        "-i", "/System/Library/Sounds/Pop.aiff",
        "-i", "/System/Library/Sounds/Ping.aiff",
        "-i", "/System/Library/Sounds/Hero.aiff",
        "-filter_complex",
        "[1:a]adelay=100|100[s0]; "
        "[1:a]adelay=4200|4200[s1]; "
        "[2:a]adelay=8500|8500[s2]; "
        "[1:a]adelay=12800|12800[s3]; "
        "[3:a]adelay=17000|17000[s4]; "
        "[0:a][s0][s1][s2][s3][s4]amix=inputs=6:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]",
        "-ar", "44100",
        "-ac", "2",
        output_wav
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(raw_beat):
        os.remove(raw_beat)

def render_html_slides(html_path, output_dir, count=5):
    os.makedirs(output_dir, exist_ok=True)
    png_paths = []
    abs_html = os.path.abspath(html_path)

    for i in range(1, count + 1):
        out_png = os.path.join(output_dir, f"scene_{i}.png")
        url = f"file://{abs_html}?scene={i}"
        cmd = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--screenshot={out_png}",
            "--window-size=1080,1920",
            url
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        png_paths.append(out_png)
    return png_paths

def build_video_from_slides(slide_pngs, audio_wav, output_mp4):
    scenes = [Image.open(p).convert("RGB") for p in slide_pngs]
    scene_frames = int(SCENE_DUR * FPS)
    fade_frames = int(FADE_DUR * FPS)

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_wav,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def get_zoomed(img, progress):
        scale = 1.0 + 0.08 * progress
        w = int(WIDTH / scale)
        h = int(HEIGHT / scale)
        x = (WIDTH - w) // 2
        y = (HEIGHT - h) // 2
        return img.crop((x, y, x + w, y + h)).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

    for s_idx in range(len(scenes)):
        cur_img = scenes[s_idx]
        next_img = scenes[s_idx + 1] if s_idx + 1 < len(scenes) else None

        for f in range(scene_frames):
            p = f / scene_frames
            frame_a = get_zoomed(cur_img, p)

            if next_img and f >= (scene_frames - fade_frames):
                fade_p = (f - (scene_frames - fade_frames)) / fade_frames
                frame_b = get_zoomed(next_img, 0.0)
                final_frame = Image.blend(frame_a, frame_b, fade_p)
            else:
                final_frame = frame_a

            proc.stdin.write(final_frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ Generated video: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")

def main():
    soundtrack_wav = "/tmp/reel_soundtrack.wav"
    generate_soundtrack(soundtrack_wav, total_sec=22.5)

    reels_config = [
        {
            "num": 1,
            "template": "scripts/templates/reel1_slides.html",
            "asset_file": "assets/videos/reel1_dm_for_price_trap.mp4",
            "dl_file": "01_Reel_DM_For_Price_Trap.mp4",
            "title": "Why 'DM For Price' is Killing 70% of Sales"
        },
        {
            "num": 2,
            "template": "scripts/templates/reel2_slides.html",
            "asset_file": "assets/videos/reel2_huna_website_corporate.mp4",
            "dl_file": "02_Reel_Huna_Website_Corporate.mp4",
            "title": "How to Lose a KES 200,000 Corporate Client"
        },
        {
            "num": 3,
            "template": "scripts/templates/reel3_slides.html",
            "asset_file": "assets/videos/reel3_ghosted_web_guy.mp4",
            "dl_file": "03_Reel_Ghosted_By_Cheap_Web_Guy.mp4",
            "title": "3 Signs Your Cheap Web Guy is About to Ghost You"
        },
        {
            "num": 4,
            "template": "scripts/templates/reel4_slides.html",
            "asset_file": "assets/videos/reel4_express_landing_page.mp4",
            "dl_file": "04_Reel_KES_15K_Express_Landing_Page.mp4",
            "title": "KES 15K Express Landing Page Secret"
        },
        {
            "num": 5,
            "template": "scripts/templates/reel5_slides.html",
            "asset_file": "assets/videos/reel3_chama_sacco_automation.mp4",
            "dl_file": "05_Reel_Chama_SACCO_Automation.mp4",
            "title": "Bado Mnasimamia Chama kwa Excel na WhatsApp?"
        }
    ]

    os.makedirs("assets/videos", exist_ok=True)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    for item in reels_config:
        print(f"\n=======================================================")
        print(f"🎬 Processing Reel #{item['num']}: {item['title']}")
        print(f"=======================================================")
        slide_dir = f"/tmp/reel_{item['num']}_slides"
        slides = render_html_slides(item["template"], slide_dir, count=5)
        build_video_from_slides(slides, soundtrack_wav, item["asset_file"])

        # Copy to Downloads with official numbered name
        dl_dest = os.path.join(DOWNLOADS_DIR, item["dl_file"])
        shutil.copyfile(item["asset_file"], dl_dest)
        print(f"📁 Copied to Downloads: {dl_dest}")

    print("\n🎉 ALL 5 BROADCAST-GRADE REELS RENDERED & COPIED TO DOWNLOADS!")

if __name__ == "__main__":
    main()
