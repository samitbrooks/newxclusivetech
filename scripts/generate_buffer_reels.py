#!/usr/bin/env python3
"""
generate_buffer_reels.py
Renders 3 broadcast-grade 1080x1920 (9:16) video reels with synchronized audio voiceover,
kinetic motion typography, device mockups, and Daraja M-Pesa animations.
"""

import os
import sys
import math
import wave
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1920
FPS = 30

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_pill(draw, x, y, text, font, bg_color, text_color, border_color=None, padding_x=28, padding_y=14):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + padding_x * 2
    h = th + padding_y * 2
    r = h // 2
    box = [x - w // 2, y - h // 2, x + w // 2, y + h // 2]
    draw_rounded_rect(draw, box, radius=r, fill=bg_color, outline=border_color, width=2 if border_color else 1)
    draw.text((x - tw // 2, y - th // 2 - 2), text, font=font, fill=text_color)
    return box

def get_audio_duration(wav_path):
    with wave.open(wav_path, 'rb') as w:
        return w.getnframes() / float(w.getframerate())

def generate_voiceover(narration_text, output_wav, voice="Daniel", rate=175):
    aiff_tmp = output_wav.replace(".wav", ".aiff")
    cmd_say = ["say", "-v", voice, "-r", str(rate), "-o", aiff_tmp, narration_text]
    subprocess.run(cmd_say, check=True)
    cmd_conv = [
        "ffmpeg", "-y", "-i", aiff_tmp,
        "-ar", "44100", "-ac", "2",
        output_wav
    ]
    subprocess.run(cmd_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(aiff_tmp):
        os.remove(aiff_tmp)
    return get_audio_duration(output_wav)

def generate_chime_wav(output_wav):
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "sine=frequency=987:duration=0.12",
        "-f", "lavfi", "-i", "sine=frequency=1318:duration=0.25",
        "-filter_complex", "[0:0][1:0]concat=n=2:v=0:a=1[out]",
        "-map", "[out]", "-ar", "44100", "-ac", "2",
        output_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def create_base_canvas(frame_idx, primary_color=(95, 57, 255), secondary_color=(32, 217, 161)):
    # Dark obsidian base
    img = Image.new("RGB", (WIDTH, HEIGHT), (12, 13, 19))
    draw = ImageDraw.Draw(img)

    t = frame_idx / FPS
    # Animated soft glowing lights
    cx1 = int(WIDTH * 0.35 + 100 * math.sin(t * 0.9))
    cy1 = int(HEIGHT * 0.25 + 80 * math.cos(t * 0.8))
    cx2 = int(WIDTH * 0.65 + 110 * math.cos(t * 0.75))
    cy2 = int(HEIGHT * 0.75 + 90 * math.sin(t * 0.85))

    for r in range(350, 40, -45):
        alpha = int(12 * (1 - r / 350))
        c1 = (primary_color[0] * alpha // 15, primary_color[1] * alpha // 15, primary_color[2] * alpha // 15)
        draw.ellipse([cx1 - r, cy1 - r, cx1 + r, cy1 + r], fill=c1)
        c2 = (secondary_color[0] * alpha // 15, secondary_color[1] * alpha // 15, secondary_color[2] * alpha // 15)
        draw.ellipse([cx2 - r, cy2 - r, cx2 + r, cy2 + r], fill=c2)

    # Clean geometric background lines
    for y in range(0, HEIGHT, 160):
        draw.line([(0, y), (WIDTH, y)], fill=(20, 22, 32), width=1)
    for x in range(0, WIDTH, 160):
        draw.line([(x, 0), (x, HEIGHT)], fill=(20, 22, 32), width=1)

    return img

def draw_header_footer(draw, badge_text, badge_color, frame_idx, total_frames):
    font_badge = get_font(FONT_BOLD, 26)
    draw_pill(draw, WIDTH // 2, 90, badge_text, font_badge, (22, 25, 38), badge_color, border_color=(50, 56, 80), padding_x=28, padding_y=12)

    # Bottom Progress Bar
    pct = min(1.0, frame_idx / max(1, total_frames))
    draw.rectangle([0, HEIGHT - 14, WIDTH, HEIGHT], fill=(25, 28, 42))
    draw.rectangle([0, HEIGHT - 14, int(WIDTH * pct), HEIGHT], fill=badge_color)

    # Bottom Branding Banner
    font_footer = get_font(FONT_BOLD, 28)
    draw.text((WIDTH // 2, HEIGHT - 70), "⚡ XCLUSIVE TECH • +254 722 753 819 • xclusivetech.co.ke", font=font_footer, fill=(160, 175, 205), anchor="mm")

# ==============================================================================
# REEL 1 RENDERER
# ==============================================================================
def render_reel_1():
    print(">>> Rendering Reel 1: The 'DM For Price' Trap...")
    narration_text = (
        "Why D M for price is killing 70% of your sales in Kenya. "
        "Your customers are shopping on their phones late at night with money in their M-Pesa. "
        "When you make them wait hours for a D M reply, you lose the sale to your competitors. "
        "With an automated e-commerce store from Xclusive Tech, customers tap buy, enter their number, "
        "and an automated Daraja M-Pesa prompt appears instantly on their screen. "
        "Orders are confirmed and you get paid while you sleep. "
        "Stop losing sales. Get your custom online store from Xclusive Tech today. "
        "WhatsApp Samuel at 0722 753 819 or visit xclusivetech dot c o dot k e."
    )
    
    os.makedirs("assets/videos", exist_ok=True)
    audio_wav = "assets/videos/reel1_voice.wav"
    audio_dur = generate_voiceover(narration_text, audio_wav, voice="Daniel", rate=172)
    # Add 1.0 second buffer at end
    total_dur = audio_dur + 1.2
    total_frames = int(total_dur * FPS)
    print(f"Reel 1 Audio Duration: {audio_dur:.2f}s, Total Frames: {total_frames}")

    # Section breakpoints (in seconds)
    s1_end = int(5.5 * FPS)
    s2_end = int(13.0 * FPS)
    s3_end = int(24.5 * FPS)

    # Prepare ffmpeg video pipe
    video_raw = "assets/videos/reel1_raw.mp4"
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        video_raw
    ]
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    font_title_huge = get_font(FONT_BLACK, 72)
    font_title_med = get_font(FONT_BLACK, 54)
    font_bold_large = get_font(FONT_BOLD, 44)
    font_bold_med = get_font(FONT_BOLD, 36)
    font_reg = get_font(FONT_REGULAR, 32)

    for i in range(total_frames):
        img = create_base_canvas(i, primary_color=(95, 57, 255), secondary_color=(32, 217, 161))
        draw = ImageDraw.Draw(img)
        draw_header_footer(draw, "🔥 E-COMMERCE CONVERSION TIP", (32, 217, 161), i, total_frames)

        # ----------------------------------------------------
        # SCENE 1: HOOK (0 -> 5.5s)
        # ----------------------------------------------------
        if i < s1_end:
            # Kinetic scale in
            scale_t = min(1.0, i / (0.6 * FPS))
            pulse = math.sin(i / FPS * 6) * 4

            # Central Hero Card
            card_box = [100, 360, WIDTH - 100, 1460]
            draw_rounded_rect(draw, card_box, 36, fill=(20, 22, 34), outline=(95, 57, 255), width=3)

            # Warning icon
            draw.text((WIDTH // 2, 480 + pulse), "⚠️", font=get_font(FONT_BOLD, 90), anchor="mm")

            draw.text((WIDTH // 2, 640), 'WHY "DM FOR PRICE"', font=font_title_huge, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 740), 'IS KILLING 70%', font=font_title_huge, fill=(253, 49, 188), anchor="mm")
            draw.text((WIDTH // 2, 840), 'OF YOUR SALES 📉', font=font_title_huge, fill=(32, 217, 161), anchor="mm")

            # Explanation pill
            draw_pill(draw, WIDTH // 2, 1020, "KENYA CONSUMER REALITY CHECK", font_bold_med, (30, 34, 52), (251, 181, 0), border_color=(251, 181, 0), padding_x=32, padding_y=16)

            draw.text((WIDTH // 2, 1180), "What happens when your customers shop", font=font_bold_med, fill=(200, 210, 235), anchor="mm")
            draw.text((WIDTH // 2, 1240), "at 11:30 PM on their phones...", font=font_title_med, fill=(56, 189, 248), anchor="mm")

        # ----------------------------------------------------
        # SCENE 2: THE MIDNIGHT TRAP (5.5s -> 13.0s)
        # ----------------------------------------------------
        elif i < s2_end:
            local_i = i - s1_end

            # Header text
            draw.text((WIDTH // 2, 260), "THE MIDNIGHT CART ABANDONMENT", font=font_title_med, fill=(253, 49, 188), anchor="mm")

            # Phone / Clock container
            draw_rounded_rect(draw, [120, 350, WIDTH - 120, 600], 28, fill=(22, 25, 38), outline=(60, 66, 95), width=2)
            draw.text((WIDTH // 2, 440), "⏰ TIME: 11:45 PM", font=font_title_huge, fill=(251, 181, 0), anchor="mm")
            draw.text((WIDTH // 2, 530), "Customer browsing in bed • M-Pesa loaded 📱", font=font_reg, fill=(200, 210, 235), anchor="mm")

            # Simulated DM Chat
            draw_rounded_rect(draw, [120, 650, WIDTH - 120, 1150], 28, fill=(18, 20, 30), outline=(50, 55, 80), width=2)
            
            # Message 1 (Customer at 11:45 PM)
            draw_rounded_rect(draw, [160, 710, 720, 810], 20, fill=(35, 40, 60))
            draw.text((190, 760), "Hey! How much is this jacket? I want to buy now.", font=font_reg, fill=(255, 255, 255), anchor="lm")
            draw.text((680, 785), "11:45 PM", font=get_font(FONT_REGULAR, 20), fill=(140, 150, 180), anchor="rm")

            # Message 2 (Seller 7 hours later at 7:00 AM)
            draw_rounded_rect(draw, [WIDTH - 720, 850, WIDTH - 160, 950], 20, fill=(95, 57, 255))
            draw.text((WIDTH - 690, 900), "Hello dear, check DM for price 😊", font=font_reg, fill=(255, 255, 255), anchor="lm")
            draw.text((WIDTH - 190, 925), "7:12 AM", font=get_font(FONT_REGULAR, 20), fill=(220, 220, 255), anchor="rm")

            # Stamp animation (Appears after 2 seconds)
            if local_i > 1.2 * FPS:
                stamp_box = [180, 1010, WIDTH - 180, 1110]
                draw_rounded_rect(draw, stamp_box, 16, fill=(220, 38, 38))
                draw.text((WIDTH // 2, 1060), "❌ IMPULSE LOST • BOUGHT ELSEWHERE ❌", font=font_bold_med, fill=(255, 255, 255), anchor="mm")

            # Stat Box
            draw_rounded_rect(draw, [120, 1220, WIDTH - 120, 1500], 28, fill=(28, 16, 26), outline=(220, 38, 38), width=2)
            draw.text((WIDTH // 2, 1310), "73% OF KENYAN SHOPPERS", font=font_title_med, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 1390), "abandon purchase if checkout is not instant.", font=font_bold_med, fill=(253, 49, 188), anchor="mm")

        # ----------------------------------------------------
        # SCENE 3: AUTOMATED DARAJA M-PESA CHECKOUT (13.0s -> 24.5s)
        # ----------------------------------------------------
        elif i < s3_end:
            local_i = i - s2_end

            draw.text((WIDTH // 2, 230), "THE SOLUTION: 24/7 DARAJA STK PUSH", font=font_title_med, fill=(32, 217, 161), anchor="mm")

            # Smartphone Bezel
            phone_box = [160, 310, WIDTH - 160, 1500]
            draw_rounded_rect(draw, phone_box, 44, fill=(15, 17, 26), outline=(60, 68, 98), width=3)
            
            # Notch
            draw_rounded_rect(draw, [WIDTH // 2 - 90, 325, WIDTH // 2 + 90, 360], 16, fill=(0, 0, 0))

            # Store Product Card
            draw_rounded_rect(draw, [210, 410, WIDTH - 210, 830], 24, fill=(24, 28, 42))
            draw.text((WIDTH // 2, 480), "Billan Luxury Silk Collection", font=font_bold_med, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 550), "KES 2,500", font=font_title_huge, fill=(32, 217, 161), anchor="mm")
            draw_pill(draw, WIDTH // 2, 630, "IN STOCK • NAIROBI WAREHOUSE", font_reg, (35, 42, 64), (56, 189, 248), padding_x=20, padding_y=10)

            # Buy Button
            draw_rounded_rect(draw, [250, 710, WIDTH - 250, 800], 24, fill=(32, 217, 161))
            draw.text((WIDTH // 2, 755), "🛒 BUY NOW WITH M-PESA", font=font_bold_med, fill=(5, 46, 32), anchor="mm")

            # Animated Safaricom STK Push Dialog
            if local_i > 0.8 * FPS:
                stk_box = [190, 880, WIDTH - 190, 1420]
                draw_rounded_rect(draw, stk_box, 30, fill=(245, 247, 250), outline=(0, 168, 89), width=4)

                # Safaricom Header
                draw_rounded_rect(draw, [190, 880, WIDTH - 190, 970], 28, fill=(0, 168, 89))
                draw.text((WIDTH // 2, 925), "SAFARICOM M-PESA", font=font_bold_med, fill=(255, 255, 255), anchor="mm")

                draw.text((WIDTH // 2, 1030), "Do you want to pay KES 2,500", font=font_bold_large, fill=(20, 20, 25), anchor="mm")
                draw.text((WIDTH // 2, 1090), "to XCLUSIVE TECH STORE?", font=font_bold_large, fill=(20, 20, 25), anchor="mm")

                # PIN dots animation
                draw_rounded_rect(draw, [300, 1160, WIDTH - 300, 1240], 16, fill=(225, 230, 238))
                pin_dots = "• • • •" if local_i > 2.5 * FPS else "• •"
                draw.text((WIDTH // 2, 1200), f"Enter PIN:  {pin_dots}", font=font_title_med, fill=(30, 40, 55), anchor="mm")

                # Green OK Button
                draw_rounded_rect(draw, [280, 1280, WIDTH - 280, 1370], 20, fill=(0, 168, 89))
                draw.text((WIDTH // 2, 1325), "✅ CONFIRM PAYMENT", font=font_bold_med, fill=(255, 255, 255), anchor="mm")

        # ----------------------------------------------------
        # SCENE 4: OFFER & CTA (24.5s -> END)
        # ----------------------------------------------------
        else:
            draw.text((WIDTH // 2, 260), "BUILD YOUR 24/7 ONLINE STORE", font=font_title_med, fill=(251, 181, 0), anchor="mm")

            # Offer Card 1: Express Landing Page
            draw_rounded_rect(draw, [100, 360, WIDTH - 100, 680], 28, fill=(22, 25, 38), outline=(95, 57, 255), width=2)
            draw_pill(draw, WIDTH // 2, 420, "FASTEST TO LAUNCH", font_reg, (95, 57, 255), (255, 255, 255), padding_x=24, padding_y=10)
            draw.text((WIDTH // 2, 500), "Express Sales Landing Page", font=font_bold_large, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 580), "KES 15,000", font=font_title_huge, fill=(32, 217, 161), anchor="mm")
            draw.text((WIDTH // 2, 640), "Ready in 3 to 5 Days • Sub-1.5s Mobile Speed", font=font_reg, fill=(180, 190, 215), anchor="mm")

            # Offer Card 2: E-Commerce Pro
            draw_rounded_rect(draw, [100, 720, WIDTH - 100, 1080], 28, fill=(22, 25, 38), outline=(32, 217, 161), width=2)
            draw_pill(draw, WIDTH // 2, 780, "FULL AUTOMATED CHECKOUT", font_reg, (32, 217, 161), (5, 46, 32), padding_x=24, padding_y=10)
            draw.text((WIDTH // 2, 860), "Complete M-Pesa E-Commerce Store", font=font_bold_large, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 940), "KES 49,000 - 85,000", font=font_title_huge, fill=(253, 49, 188), anchor="mm")
            draw.text((WIDTH // 2, 1010), "Daraja STK Push • Inventory • Orders Dashboard", font=font_reg, fill=(180, 190, 215), anchor="mm")

            # Giant WhatsApp CTA Pill
            pulse = math.sin(i / FPS * 5) * 5
            btn_box = [100, 1160 - int(pulse), WIDTH - 100, 1340 - int(pulse)]
            draw_rounded_rect(draw, btn_box, 36, fill=(37, 211, 102), outline=(255, 255, 255), width=3)
            draw.text((WIDTH // 2, 1220 - int(pulse)), "💬 WHATSAPP SAMUEL TODAY", font=font_title_med, fill=(5, 46, 25), anchor="mm")
            draw.text((WIDTH // 2, 1290 - int(pulse)), "+254 722 753 819", font=font_title_huge, fill=(5, 46, 25), anchor="mm")

            draw.text((WIDTH // 2, 1420), "Visit: www.xclusivetech.co.ke", font=font_bold_large, fill=(56, 189, 248), anchor="mm")
            draw.text((WIDTH // 2, 1490), "Office: Wood Ave, Kilimani, Nairobi", font=font_reg, fill=(160, 175, 205), anchor="mm")

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Raw video encoded successfully.")

    # Mux audio & video together
    output_final = "assets/videos/reel1_dm_for_price_trap.mp4"
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", video_raw,
        "-i", audio_wav,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_final
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(video_raw):
        os.remove(video_raw)
    print(f"✅ Reel 1 completed: {output_final} ({os.path.getsize(output_final)} bytes)")
    return output_final

# ==============================================================================
# REEL 2 RENDERER
# ==============================================================================
def render_reel_2():
    print(">>> Rendering Reel 2: How to Lose a KES 200,000 Corporate Client...")
    narration_text = (
        "How to lose a 200,000 shilling corporate client in 5 seconds. "
        "A client asks for your website and company profile, and you send a WhatsApp catalog or Instagram handle. "
        "You just lost 50% of your negotiating power. "
        "In Kenya, corporate decision makers and institutions do not award serious contracts over social media. "
        "A professional website from Xclusive Tech positions your brand as an established leader with proven case studies, "
        "custom business email, and sub-1.5 second mobile speed. "
        "Starter business websites from 25,000 shillings, delivered in 14 days. "
        "Stop losing high-paying clients. WhatsApp Samuel at 0722 753 819 or visit xclusivetech dot c o dot k e."
    )
    
    os.makedirs("assets/videos", exist_ok=True)
    audio_wav = "assets/videos/reel2_voice.wav"
    audio_dur = generate_voiceover(narration_text, audio_wav, voice="Daniel", rate=172)
    total_dur = audio_dur + 1.2
    total_frames = int(total_dur * FPS)
    print(f"Reel 2 Audio Duration: {audio_dur:.2f}s, Total Frames: {total_frames}")

    s1_end = int(5.5 * FPS)
    s2_end = int(12.5 * FPS)
    s3_end = int(23.5 * FPS)

    video_raw = "assets/videos/reel2_raw.mp4"
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        video_raw
    ]
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    font_title_huge = get_font(FONT_BLACK, 70)
    font_title_med = get_font(FONT_BLACK, 52)
    font_bold_large = get_font(FONT_BOLD, 42)
    font_bold_med = get_font(FONT_BOLD, 36)
    font_reg = get_font(FONT_REGULAR, 32)

    # Load client preview image if available
    isuzu_path = "assets/images/case-studies/irene-muendo-isuzu.png"
    isuzu_img = Image.open(isuzu_path).convert("RGB") if os.path.exists(isuzu_path) else None

    for i in range(total_frames):
        img = create_base_canvas(i, primary_color=(56, 189, 248), secondary_color=(95, 57, 255))
        draw = ImageDraw.Draw(img)
        draw_header_footer(draw, "💼 B2B AUTHORITY & PRICING POWER", (56, 189, 248), i, total_frames)

        # SCENE 1: HOOK (0 -> 5.5s)
        if i < s1_end:
            card_box = [100, 360, WIDTH - 100, 1460]
            draw_rounded_rect(draw, card_box, 36, fill=(20, 22, 34), outline=(56, 189, 248), width=3)

            draw.text((WIDTH // 2, 480), "🏢", font=get_font(FONT_BOLD, 90), anchor="mm")
            draw.text((WIDTH // 2, 630), "HOW TO LOSE A", font=font_title_huge, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 730), "KES 200,000 CLIENT", font=font_title_huge, fill=(251, 181, 0), anchor="mm")
            draw.text((WIDTH // 2, 830), "IN 5 SECONDS 💀", font=font_title_huge, fill=(253, 49, 188), anchor="mm")

            draw_pill(draw, WIDTH // 2, 1020, "THE BOARDROOM REALITY", font_bold_med, (30, 36, 56), (56, 189, 248), border_color=(56, 189, 248), padding_x=32, padding_y=16)

            draw.text((WIDTH // 2, 1180), '"Do you have an official website or profile', font=font_bold_med, fill=(200, 210, 235), anchor="mm")
            draw.text((WIDTH // 2, 1240), 'that our board can review?"', font=font_bold_med, fill=(255, 255, 255), anchor="mm")

        # SCENE 2: THE COST OF NO WEBSITE (5.5s -> 12.5s)
        elif i < s2_end:
            local_i = i - s1_end

            draw.text((WIDTH // 2, 260), "THE AMATEUR TRAP IN KENYA", font=font_title_med, fill=(253, 49, 188), anchor="mm")

            draw_rounded_rect(draw, [120, 360, WIDTH - 120, 720], 28, fill=(28, 16, 26), outline=(220, 38, 38), width=2)
            draw.text((WIDTH // 2, 440), 'YOUR RESPONSE:', font=font_bold_med, fill=(253, 49, 188), anchor="mm")
            draw.text((WIDTH // 2, 530), '"Check our WhatsApp Catalog', font=font_bold_large, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 600), 'or Instagram profile..."', font=font_bold_large, fill=(255, 255, 255), anchor="mm")

            if local_i > 1.0 * FPS:
                draw_rounded_rect(draw, [160, 640, WIDTH - 160, 700], 12, fill=(220, 38, 38))
                draw.text((WIDTH // 2, 670), "🚩 INSTANT CREDIBILITY RED FLAG", font=font_bold_med, fill=(255, 255, 255), anchor="mm")

            draw_rounded_rect(draw, [120, 780, WIDTH - 120, 1460], 28, fill=(20, 23, 34), outline=(60, 68, 98), width=2)
            draw.text((WIDTH // 2, 870), "WHAT CORPORATE CLIENTS THINK:", font=font_bold_med, fill=(251, 181, 0), anchor="mm")

            bullets = [
                "• 'They are an informal side-hustle with no office.'",
                "• 'High risk of disappearing with our deposit.'",
                "• 'We cannot verify their tax or business legitimacy.'",
                "• 'Bargain their quote down by 50% minimum.'"
            ]
            by = 980
            for b in bullets:
                draw.text((170, by), b, font=font_bold_med, fill=(230, 235, 245), anchor="lm")
                by += 100

        # SCENE 3: THE XCLUSIVE TECH AUTHORITY SITE (12.5s -> 23.5s)
        elif i < s3_end:
            draw.text((WIDTH // 2, 230), "INSTANT CORPORATE AUTHORITY", font=font_title_med, fill=(32, 217, 161), anchor="mm")

            # Safari Browser Mockup
            browser_box = [120, 300, WIDTH - 120, 1020]
            draw_rounded_rect(draw, browser_box, 24, fill=(24, 27, 40), outline=(60, 68, 98), width=2)
            
            # Browser Top Bar
            draw_rounded_rect(draw, [120, 300, WIDTH - 120, 370], 24, fill=(35, 40, 60))
            draw.ellipse([150, 325, 170, 345], fill=(239, 68, 68))
            draw.ellipse([185, 325, 205, 345], fill=(245, 158, 11))
            draw.ellipse([220, 325, 240, 345], fill=(16, 185, 129))

            # URL bar
            draw_rounded_rect(draw, [270, 318, WIDTH - 150, 355], 12, fill=(18, 20, 30))
            draw.text((WIDTH // 2, 336), "🔒 https://www.irenemuendoisuzu.co.ke", font=get_font(FONT_REGULAR, 22), fill=(180, 190, 220), anchor="mm")

            # Inset case study screenshot
            if isuzu_img:
                thumb = isuzu_img.resize((WIDTH - 280, 560))
                img.paste(thumb, (140, 390))
            else:
                draw.rectangle([140, 390, WIDTH - 140, 950], fill=(18, 22, 35))

            # Feature Badges Underneath
            draw_rounded_rect(draw, [120, 1060, WIDTH - 120, 1460], 28, fill=(20, 24, 36), outline=(32, 217, 161), width=2)
            draw.text((WIDTH // 2, 1130), "WHY SERIOUS CLIENTS TRUST YOU:", font=font_bold_med, fill=(32, 217, 161), anchor="mm")

            badges = [
                "✅ Sub-1.5s Speed on Kenyan 4G",
                "✅ Custom Business Email (hello@yourbrand.co.ke)",
                "✅ Verified Physical Location & Google Maps",
                "✅ Client Case Studies & Proof of Delivery"
            ]
            y_b = 1220
            for bg in badges:
                draw.text((180, y_b), bg, font=font_bold_med, fill=(255, 255, 255), anchor="lm")
                y_b += 65

        # SCENE 4: CTA
        else:
            draw.text((WIDTH // 2, 260), "COMMAND HIGHER RATES TODAY", font=font_title_med, fill=(251, 181, 0), anchor="mm")

            draw_rounded_rect(draw, [100, 360, WIDTH - 100, 800], 28, fill=(22, 25, 38), outline=(56, 189, 248), width=3)
            draw_pill(draw, WIDTH // 2, 420, "MOST POPULAR FOR SMES", font_reg, (56, 189, 248), (5, 30, 45), padding_x=24, padding_y=10)
            draw.text((WIDTH // 2, 510), "5-Page Custom Corporate Website", font=font_bold_large, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 600), "KES 25,000", font=font_title_huge, fill=(32, 217, 161), anchor="mm")
            draw.text((WIDTH // 2, 680), "Ready in 14 Days • Mobile-First UX • Basic SEO", font=font_reg, fill=(180, 190, 215), anchor="mm")
            draw.text((WIDTH // 2, 740), "100% Code & Domain Ownership Handed Over", font=font_reg, fill=(251, 181, 0), anchor="mm")

            pulse = math.sin(i / FPS * 5) * 5
            btn_box = [100, 900 - int(pulse), WIDTH - 100, 1080 - int(pulse)]
            draw_rounded_rect(draw, btn_box, 36, fill=(37, 211, 102), outline=(255, 255, 255), width=3)
            draw.text((WIDTH // 2, 960 - int(pulse)), "💬 WHATSAPP SAMUEL TO BUILD YOUR SITE", font=font_bold_med, fill=(5, 46, 25), anchor="mm")
            draw.text((WIDTH // 2, 1030 - int(pulse)), "+254 722 753 819", font=font_title_huge, fill=(5, 46, 25), anchor="mm")

            draw.text((WIDTH // 2, 1180), "Explore Live Portfolio: www.xclusivetech.co.ke", font=font_bold_large, fill=(56, 189, 248), anchor="mm")
            draw.text((WIDTH // 2, 1260), "120+ Verified Deployments Across Kenya", font=font_reg, fill=(160, 175, 205), anchor="mm")

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Raw video encoded successfully.")

    output_final = "assets/videos/reel2_huna_website_corporate.mp4"
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", video_raw,
        "-i", audio_wav,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_final
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(video_raw):
        os.remove(video_raw)
    print(f"✅ Reel 2 completed: {output_final} ({os.path.getsize(output_final)} bytes)")
    return output_final

# ==============================================================================
# REEL 3 RENDERER
# ==============================================================================
def render_reel_3():
    print(">>> Rendering Reel 3: Chama & SACCO Automation...")
    narration_text = (
        "Still running your Chama or SACCO on Excel and WhatsApp? "
        "End of month in Kenya: 35 different M-Pesa screenshots flooding the chat, "
        "manual spreadsheets breaking, and endless arguments over loan interest at the AGM. "
        "One laptop crash or corrupt formula can ruin years of trust. "
        "At Xclusive Tech, we build custom cloud-hosted Chama and SACCO platforms. "
        "Members pay directly via automated M-Pesa STK push, contributions reconcile instantly, "
        "and members check their own statements 24/7. "
        "Bring total transparency to your investment group. "
        "WhatsApp Samuel at 0722 753 819 for a live demo, or visit xclusivetech dot c o dot k e slash solutions."
    )
    
    os.makedirs("assets/videos", exist_ok=True)
    audio_wav = "assets/videos/reel3_voice.wav"
    audio_dur = generate_voiceover(narration_text, audio_wav, voice="Daniel", rate=172)
    total_dur = audio_dur + 1.2
    total_frames = int(total_dur * FPS)
    print(f"Reel 3 Audio Duration: {audio_dur:.2f}s, Total Frames: {total_frames}")

    s1_end = int(5.5 * FPS)
    s2_end = int(13.0 * FPS)
    s3_end = int(24.0 * FPS)

    video_raw = "assets/videos/reel3_raw.mp4"
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        video_raw
    ]
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    font_title_huge = get_font(FONT_BLACK, 68)
    font_title_med = get_font(FONT_BLACK, 50)
    font_bold_large = get_font(FONT_BOLD, 42)
    font_bold_med = get_font(FONT_BOLD, 36)
    font_reg = get_font(FONT_REGULAR, 32)

    for i in range(total_frames):
        img = create_base_canvas(i, primary_color=(16, 185, 129), secondary_color=(56, 189, 248))
        draw = ImageDraw.Draw(img)
        draw_header_footer(draw, "📊 CHAMA & SACCO SAAS PLATFORMS", (16, 185, 129), i, total_frames)

        # SCENE 1: HOOK (0 -> 5.5s)
        if i < s1_end:
            card_box = [100, 360, WIDTH - 100, 1460]
            draw_rounded_rect(draw, card_box, 36, fill=(20, 22, 34), outline=(16, 185, 129), width=3)

            draw.text((WIDTH // 2, 480), "🚩", font=get_font(FONT_BOLD, 90), anchor="mm")
            draw.text((WIDTH // 2, 630), "BADO MNASIMAMIA CHAMA", font=font_title_huge, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 730), "KWA EXCEL NA WHATSAPP?", font=font_title_huge, fill=(251, 181, 0), anchor="mm")
            draw.text((WIDTH // 2, 830), "THE MONTH-END DRAMA 💀", font=font_title_huge, fill=(239, 68, 68), anchor="mm")

            draw_pill(draw, WIDTH // 2, 1020, "INVESTMENT CLUB REALITY", font_bold_med, (26, 38, 30), (16, 185, 129), border_color=(16, 185, 129), padding_x=32, padding_y=16)

            draw.text((WIDTH // 2, 1180), "Why manage millions of shillings", font=font_bold_med, fill=(200, 210, 235), anchor="mm")
            draw.text((WIDTH // 2, 1240), "like a primary school tuckshop?", font=font_bold_med, fill=(255, 255, 255), anchor="mm")

        # SCENE 2: THE SPREADSHEET DISASTER (5.5s -> 13.0s)
        elif i < s2_end:
            draw.text((WIDTH // 2, 260), "THE RISKS OF MANUAL CHAMA ACCOUNTING", font=font_title_med, fill=(239, 68, 68), anchor="mm")

            draw_rounded_rect(draw, [120, 360, WIDTH - 120, 680], 28, fill=(35, 18, 22), outline=(239, 68, 68), width=2)
            draw.text((WIDTH // 2, 440), "⚠️ EXCEL FORMULA CORRUPTION", font=font_bold_med, fill=(239, 68, 68), anchor="mm")
            draw.text((WIDTH // 2, 530), "#REF!  #VALUE!  SUM_ERROR", font=font_title_huge, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 610), "One accidental keypress alters years of records.", font=font_reg, fill=(220, 200, 200), anchor="mm")

            draw_rounded_rect(draw, [120, 740, WIDTH - 120, 1460], 28, fill=(20, 23, 34), outline=(60, 68, 98), width=2)
            draw.text((WIDTH // 2, 830), "END-OF-MONTH CHAMA PAIN POINTS:", font=font_bold_med, fill=(251, 181, 0), anchor="mm")

            issues = [
                "❌ 35 M-Pesa screenshots flooded in WhatsApp",
                "❌ Edited/doctored M-Pesa confirmation slips",
                "❌ Disputed table banking loan calculations",
                "❌ Treasurer spending 6 hours manually reconciling",
                "❌ AGM disputes over missing contribution slips"
            ]
            iy = 940
            for iss in issues:
                draw.text((160, iy), iss, font=font_bold_med, fill=(240, 240, 250), anchor="lm")
                iy += 95

        # SCENE 3: THE CUSTOM SAAS PLATFORM (13.0s -> 24.0s)
        elif i < s3_end:
            draw.text((WIDTH // 2, 230), "CUSTOM CLOUD CHAMA PLATFORM", font=font_title_med, fill=(16, 185, 129), anchor="mm")

            # Dashboard Card Mockup
            dash_box = [120, 310, WIDTH - 120, 980]
            draw_rounded_rect(draw, dash_box, 32, fill=(18, 22, 34), outline=(16, 185, 129), width=3)

            draw.text((WIDTH // 2, 380), "KILIMANI ELITE INVESTMENTS PORTAL", font=font_bold_med, fill=(180, 195, 225), anchor="mm")
            
            # Balance Cards
            draw_rounded_rect(draw, [160, 440, WIDTH // 2 - 20, 620], 20, fill=(28, 34, 52))
            draw.text((WIDTH // 4 + 70, 480), "TOTAL GROUP FUND", font=get_font(FONT_BOLD, 22), fill=(140, 155, 190), anchor="mm")
            draw.text((WIDTH // 4 + 70, 545), "KES 2.45M", font=font_title_med, fill=(16, 185, 129), anchor="mm")

            draw_rounded_rect(draw, [WIDTH // 2 + 20, 440, WIDTH - 160, 620], 20, fill=(28, 34, 52))
            draw.text((3 * WIDTH // 4 - 70, 480), "ACTIVE LOANS", font=get_font(FONT_BOLD, 22), fill=(140, 155, 190), anchor="mm")
            draw.text((3 * WIDTH // 4 - 70, 545), "KES 680K", font=font_title_med, fill=(251, 181, 0), anchor="mm")

            # 1-Tap STK Push Action Button
            draw_rounded_rect(draw, [160, 670, WIDTH - 160, 780], 24, fill=(0, 168, 89))
            draw.text((WIDTH // 2, 725), "📱 CONTRIBUTE VIA M-PESA STK PUSH", font=font_bold_med, fill=(255, 255, 255), anchor="mm")

            # Auto Statement Card
            draw_rounded_rect(draw, [160, 820, WIDTH - 160, 930], 20, fill=(35, 42, 64))
            draw.text((WIDTH // 2, 875), "📄 Instant Member PDF Statement Generator", font=font_bold_med, fill=(56, 189, 248), anchor="mm")

            # Benefits Grid
            draw_rounded_rect(draw, [120, 1030, WIDTH - 120, 1460], 28, fill=(20, 24, 36), outline=(56, 189, 248), width=2)
            draw.text((WIDTH // 2, 1100), "BUILT SPECIFICALLY FOR KENYA:", font=font_bold_med, fill=(56, 189, 248), anchor="mm")

            chama_features = [
                "⚡ Direct Safaricom Daraja STK Push Integration",
                "⚡ 100% Automated Instant Account Reconciliation",
                "⚡ Transparent Member Self-Service Dashboards",
                "⚡ Automated Loan Engine & Due-Date SMS Reminders",
                "⚡ Daily Automated Cloud Backups & Zero Excel Stress"
            ]
            fy = 1180
            for feat in chama_features:
                draw.text((160, fy), feat, font=get_font(FONT_BOLD, 30), fill=(255, 255, 255), anchor="lm")
                fy += 55

        # SCENE 4: CTA
        else:
            draw.text((WIDTH // 2, 260), "UPGRADE YOUR CHAMA TODAY", font=font_title_med, fill=(251, 181, 0), anchor="mm")

            draw_rounded_rect(draw, [100, 360, WIDTH - 100, 800], 28, fill=(22, 25, 38), outline=(16, 185, 129), width=3)
            draw_pill(draw, WIDTH // 2, 420, "CUSTOM KENYAN SOFTWARE", font_reg, (16, 185, 129), (5, 46, 32), padding_x=24, padding_y=10)
            draw.text((WIDTH // 2, 510), "Custom Cloud Chama & SACCO Web App", font=font_bold_large, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 600), "Tailored For Your Group", font=font_title_med, fill=(56, 189, 248), anchor="mm")
            draw.text((WIDTH // 2, 680), "Live STK Push • Automated Statements • Loan Engine", font=font_reg, fill=(180, 190, 215), anchor="mm")
            draw.text((WIDTH // 2, 740), "Engineered and Hosted in Kenya by Xclusive Tech", font=font_reg, fill=(251, 181, 0), anchor="mm")

            pulse = math.sin(i / FPS * 5) * 5
            btn_box = [100, 900 - int(pulse), WIDTH - 100, 1080 - int(pulse)]
            draw_rounded_rect(draw, btn_box, 36, fill=(37, 211, 102), outline=(255, 255, 255), width=3)
            draw.text((WIDTH // 2, 960 - int(pulse)), "💬 BOOK A LIVE DEMO WITH SAMUEL", font=font_bold_med, fill=(5, 46, 25), anchor="mm")
            draw.text((WIDTH // 2, 1030 - int(pulse)), "+254 722 753 819", font=font_title_huge, fill=(5, 46, 25), anchor="mm")

            draw.text((WIDTH // 2, 1180), "Explore Solutions: www.xclusivetech.co.ke/solutions", font=font_bold_large, fill=(56, 189, 248), anchor="mm")
            draw.text((WIDTH // 2, 1260), "100% Transparency & Peace of Mind for Your Group", font=font_reg, fill=(160, 175, 205), anchor="mm")

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Raw video encoded successfully.")

    output_final = "assets/videos/reel3_chama_sacco_automation.mp4"
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", video_raw,
        "-i", audio_wav,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_final
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(video_raw):
        os.remove(video_raw)
    print(f"✅ Reel 3 completed: {output_final} ({os.path.getsize(output_final)} bytes)")
    return output_final

if __name__ == "__main__":
    r1 = render_reel_1()
    r2 = render_reel_2()
    r3 = render_reel_3()
    print("🎉 ALL 3 BUFFER REELS GENERATED SUCCESSFULLY!")
