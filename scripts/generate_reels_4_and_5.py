#!/usr/bin/env python3
"""
generate_reels_4_and_5.py
Renders Reel 3 (Ghosted by Web Freelancer) and Reel 4 (KES 15K Express Landing Page)
so all 5 reels have high-resolution 1080x1920 MP4 video animations.
"""

import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont
from generate_buffer_reels import (
    WIDTH, HEIGHT, FPS, FONT_BOLD, FONT_BLACK, FONT_REGULAR,
    get_font, draw_rounded_rect, draw_pill, generate_voiceover, create_base_canvas, draw_header_footer
)

def render_reel_ghost():
    print(">>> Rendering Reel: 3 Signs Your Cheap Web Guy is About to Ghost You...")
    narration = (
        "Three signs your cheap web guy is about to ghost you with your deposit. "
        "Sign 1: He says, 'Kuna issue na server naitatua leo jioni.' "
        "Sign 2: He never gives you domain or cPanel login credentials. "
        "Sign 3: Calls start going straight to voicemail. "
        "You thought you saved money with an 8,000 shilling quote, but you lost seven months of business. "
        "At Xclusive Tech, we operate with transparent written contracts, fixed milestone delivery, "
        "and 100% full ownership of your domain and source code. "
        "Have an abandoned website project? Don't start from scratch alone. "
        "WhatsApp Samuel at 0722 753 819 and we will rescue and launch your site in 7 days."
    )
    os.makedirs("assets/videos", exist_ok=True)
    audio_wav = "assets/videos/reel_ghost_voice.wav"
    audio_dur = generate_voiceover(narration, audio_wav, voice="Daniel", rate=172)
    total_dur = audio_dur + 1.2
    total_frames = int(total_dur * FPS)

    s1_end = int(5.0 * FPS)
    s2_end = int(14.0 * FPS)
    s3_end = int(24.0 * FPS)

    video_raw = "assets/videos/reel_ghost_raw.mp4"
    cmd_ffmpeg = [
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", video_raw
    ]
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    font_title_huge = get_font(FONT_BLACK, 68)
    font_title_med = get_font(FONT_BLACK, 50)
    font_bold_large = get_font(FONT_BOLD, 42)
    font_bold_med = get_font(FONT_BOLD, 36)
    font_reg = get_font(FONT_REGULAR, 32)

    for i in range(total_frames):
        img = create_base_canvas(i, primary_color=(253, 49, 188), secondary_color=(239, 68, 68))
        draw = ImageDraw.Draw(img)
        draw_header_footer(draw, "🚩 KENYAN WEB DESIGN RED FLAGS", (253, 49, 188), i, total_frames)

        if i < s1_end:
            card_box = [100, 360, WIDTH - 100, 1460]
            draw_rounded_rect(draw, card_box, 36, fill=(20, 22, 34), outline=(253, 49, 188), width=3)
            draw.text((WIDTH // 2, 480), "👻", font=get_font(FONT_BOLD, 90), anchor="mm")
            draw.text((WIDTH // 2, 630), "3 SIGNS YOUR", font=font_title_huge, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 730), '"CHEAP WEB GUY"', font=font_title_huge, fill=(253, 49, 188), anchor="mm")
            draw.text((WIDTH // 2, 830), "IS ABOUT TO GHOST YOU 🚩", font=font_title_huge, fill=(251, 181, 0), anchor="mm")
            draw_pill(draw, WIDTH // 2, 1020, "DEPOSIT PAID IN MARCH • SITE STILL ERROR 404", font_bold_med, (38, 20, 30), (253, 49, 188), border_color=(253, 49, 188), padding_x=32, padding_y=16)
            draw.text((WIDTH // 2, 1180), "Ulipana deposit ya website kitambo...", font=font_bold_med, fill=(200, 210, 235), anchor="mm")
            draw.text((WIDTH // 2, 1240), "Na bado hakuna kitu inaonekana?", font=font_bold_med, fill=(255, 255, 255), anchor="mm")
        elif i < s2_end:
            draw.text((WIDTH // 2, 260), "THE 3 CLASSIC RED FLAGS", font=font_title_med, fill=(239, 68, 68), anchor="mm")
            flags = [
                ("🚩 RED FLAG #1", '"Kuna issue na server naitatua jioni..."', "Weeks of vague server maintenance excuses"),
                ("🚩 RED FLAG #2", "No cPanel or Domain Credentials", "He holds your digital assets hostage"),
                ("🚩 RED FLAG #3", "WhatsApp Double Blue Ticks", "Calls start going straight to voicemail")
            ]
            fy = 360
            for title, quote, desc in flags:
                draw_rounded_rect(draw, [100, fy, WIDTH - 100, fy + 240], 24, fill=(26, 18, 24), outline=(239, 68, 68), width=2)
                draw.text((140, fy + 45), title, font=get_font(FONT_BOLD, 28), fill=(253, 49, 188), anchor="lm")
                draw.text((140, fy + 110), quote, font=font_bold_large, fill=(255, 255, 255), anchor="lm")
                draw.text((140, fy + 175), desc, font=font_reg, fill=(200, 190, 195), anchor="lm")
                fy += 280
            draw_rounded_rect(draw, [100, 1220, WIDTH - 100, 1460], 28, fill=(35, 18, 20))
            draw.text((WIDTH // 2, 1310), "YOU DID NOT SAVE MONEY.", font=font_title_med, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 1390), "You lost 7 months of leads and marketing momentum.", font=font_bold_med, fill=(251, 181, 0), anchor="mm")
        elif i < s3_end:
            draw.text((WIDTH // 2, 230), "THE XCLUSIVE TECH DIFFERENCE", font=font_title_med, fill=(32, 217, 161), anchor="mm")
            draw_rounded_rect(draw, [100, 310, WIDTH - 100, 1460], 32, fill=(20, 24, 36), outline=(32, 217, 161), width=3)
            draw.text((WIDTH // 2, 400), "WHY 120+ BUSINESSES TRUST US", font=font_title_med, fill=(255, 255, 255), anchor="mm")
            perks = [
                ("🔒 Written Milestone Contracts", "Clear deliverables, no surprise extra costs"),
                ("⏱️ Guaranteed Launch Timelines", "Express in 3-5 days • Starter Sites in 14 days"),
                ("🔑 100% Asset Ownership", "Full source code, domain & hosting handed over"),
                ("💬 Direct WhatsApp Support", "Talk directly to our lead developer, not a queue"),
                ("🏢 Real Physical Office", "Wood Ave, Kilimani, Nairobi • Visit us anytime")
            ]
            py = 500
            for p_title, p_desc in perks:
                draw_rounded_rect(draw, [140, py, WIDTH - 140, py + 160], 20, fill=(28, 34, 52))
                draw.text((180, py + 50), p_title, font=font_bold_med, fill=(32, 217, 161), anchor="lm")
                draw.text((180, py + 110), p_desc, font=font_reg, fill=(210, 220, 240), anchor="lm")
                py += 190
        else:
            draw.text((WIDTH // 2, 260), "LET US RESCUE YOUR SITE", font=font_title_med, fill=(251, 181, 0), anchor="mm")
            draw_rounded_rect(draw, [100, 360, WIDTH - 100, 800], 28, fill=(22, 25, 38), outline=(253, 49, 188), width=3)
            draw_pill(draw, WIDTH // 2, 420, "STUCK OR ABANDONED PROJECT?", font_reg, (253, 49, 188), (255, 255, 255), padding_x=24, padding_y=10)
            draw.text((WIDTH // 2, 510), "Website Rescue & Launch Package", font=font_bold_large, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 600), "LIVE IN 7 DAYS", font=font_title_huge, fill=(32, 217, 161), anchor="mm")
            draw.text((WIDTH // 2, 680), "We audit, redesign, and launch your site professionally", font=font_reg, fill=(180, 190, 215), anchor="mm")
            draw.text((WIDTH // 2, 740), "Milestone contracts with 100% code ownership", font=font_reg, fill=(251, 181, 0), anchor="mm")

            pulse = math.sin(i / FPS * 5) * 5
            btn_box = [100, 900 - int(pulse), WIDTH - 100, 1080 - int(pulse)]
            draw_rounded_rect(draw, btn_box, 36, fill=(37, 211, 102), outline=(255, 255, 255), width=3)
            draw.text((WIDTH // 2, 960 - int(pulse)), "💬 WHATSAPP SAMUEL TO RESCUE YOUR SITE", font=font_bold_med, fill=(5, 46, 25), anchor="mm")
            draw.text((WIDTH // 2, 1030 - int(pulse)), "+254 722 753 819", font=font_title_huge, fill=(5, 46, 25), anchor="mm")
            draw.text((WIDTH // 2, 1180), "Check Pricing & Packages: www.xclusivetech.co.ke", font=font_bold_large, fill=(56, 189, 248), anchor="mm")
            draw.text((WIDTH // 2, 1260), "120+ Verified Deployments Across Kenya", font=font_reg, fill=(160, 175, 205), anchor="mm")

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    output_final = "assets/videos/reel3_ghosted_web_guy.mp4"
    cmd_mux = ["ffmpeg", "-y", "-i", video_raw, "-i", audio_wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", output_final]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(video_raw):
        os.remove(video_raw)
    if os.path.exists(audio_wav):
        os.remove(audio_wav)
    print(f"✅ Ghost Reel completed: {output_final} ({os.path.getsize(output_final)} bytes)")
    return output_final

def render_reel_express():
    print(">>> Rendering Reel 4: KES 15K Express Landing Page...")
    narration = (
        "Who told you that you need 100,000 shillings or two months to launch a website for your business in Kenya? "
        "When starting out or testing a new product, you don't need 20 pages. "
        "You need one focused, lightning-fast landing page designed to do one job: Convert visitors into paying WhatsApp inquiries. "
        "Our Express Landing Page package is only 15,000 shillings: "
        "Delivered in just 3 to 5 business days, loading in under 1.5 seconds on mobile, with direct WhatsApp lead capture. "
        "And if you upgrade to a full business site within 6 months, we credit 100% of your 15,000 shillings toward the upgrade. "
        "Zero risk, maximum speed. WhatsApp Samuel at 0722 753 819 or visit xclusivetech dot c o dot k e."
    )
    os.makedirs("assets/videos", exist_ok=True)
    audio_wav = "assets/videos/reel4_voice.wav"
    audio_dur = generate_voiceover(narration, audio_wav, voice="Daniel", rate=172)
    total_dur = audio_dur + 1.2
    total_frames = int(total_dur * FPS)

    s1_end = int(5.0 * FPS)
    s2_end = int(12.5 * FPS)
    s3_end = int(23.0 * FPS)

    video_raw = "assets/videos/reel4_raw.mp4"
    cmd_ffmpeg = [
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", video_raw
    ]
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    font_title_huge = get_font(FONT_BLACK, 68)
    font_title_med = get_font(FONT_BLACK, 50)
    font_bold_large = get_font(FONT_BOLD, 42)
    font_bold_med = get_font(FONT_BOLD, 36)
    font_reg = get_font(FONT_REGULAR, 32)

    for i in range(total_frames):
        img = create_base_canvas(i, primary_color=(251, 181, 0), secondary_color=(32, 217, 161))
        draw = ImageDraw.Draw(img)
        draw_header_footer(draw, "⚡ FAST ROI & IRRESISTIBLE OFFER", (251, 181, 0), i, total_frames)

        if i < s1_end:
            card_box = [100, 360, WIDTH - 100, 1460]
            draw_rounded_rect(draw, card_box, 36, fill=(20, 22, 34), outline=(251, 181, 0), width=3)
            draw.text((WIDTH // 2, 480), "🚀", font=get_font(FONT_BOLD, 90), anchor="mm")
            draw.text((WIDTH // 2, 630), "YOU DON'T NEED", font=font_title_huge, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 730), "KES 100,000", font=font_title_huge, fill=(239, 68, 68), anchor="mm")
            draw.text((WIDTH // 2, 830), "TO LAUNCH A WEBSITE ❌", font=font_title_huge, fill=(251, 181, 0), anchor="mm")
            draw_pill(draw, WIDTH // 2, 1020, "THE KES 15,000 EXPRESS SOLUTION", font_bold_med, (38, 32, 20), (251, 181, 0), border_color=(251, 181, 0), padding_x=32, padding_y=16)
            draw.text((WIDTH // 2, 1180), "Why spend months planning when you can", font=font_bold_med, fill=(200, 210, 235), anchor="mm")
            draw.text((WIDTH // 2, 1240), "test and sell in 3 business days?", font=font_bold_med, fill=(56, 189, 248), anchor="mm")
        elif i < s2_end:
            draw.text((WIDTH // 2, 260), "WHAT YOUR BUSINESS ACTUALLY NEEDS", font=font_title_med, fill=(56, 189, 248), anchor="mm")
            draw_rounded_rect(draw, [120, 360, WIDTH - 120, 720], 28, fill=(35, 18, 20), outline=(239, 68, 68), width=2)
            draw.text((WIDTH // 2, 440), "THE 20-PAGE CORPORATE TRAP", font=font_bold_med, fill=(239, 68, 68), anchor="mm")
            draw.text((WIDTH // 2, 530), "KES 100K+ • 2 Months Delay", font=font_title_med, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 610), "Visitors get lost in pages and leave without buying.", font=font_reg, fill=(220, 200, 200), anchor="mm")

            draw_rounded_rect(draw, [120, 780, WIDTH - 120, 1460], 28, fill=(18, 30, 24), outline=(32, 217, 161), width=2)
            draw.text((WIDTH // 2, 860), "THE 1-PAGE EXPRESS ADVANTAGE:", font=font_bold_med, fill=(32, 217, 161), anchor="mm")
            pts = [
                "⚡ Explains your offer in 15 seconds",
                "⚡ Sub-1.5s load time on mobile 4G",
                "⚡ Floating WhatsApp button captures leads",
                "⚡ Direct Google Maps & local SEO setup",
                "⚡ Live and selling in 3 to 5 business days"
            ]
            py = 960
            for pt in pts:
                draw.text((160, py), pt, font=font_bold_med, fill=(240, 255, 245), anchor="lm")
                py += 95
        elif i < s3_end:
            draw.text((WIDTH // 2, 230), "THE EXPRESS OFFER BREAKDOWN", font=font_title_med, fill=(251, 181, 0), anchor="mm")
            draw_rounded_rect(draw, [100, 310, WIDTH - 100, 1460], 32, fill=(20, 24, 36), outline=(251, 181, 0), width=3)
            draw.text((WIDTH // 2, 400), "EXPRESS LANDING PAGE PACKAGE", font=font_bold_large, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 480), "KES 15,000", font=font_title_huge, fill=(32, 217, 161), anchor="mm")
            draw_pill(draw, WIDTH // 2, 560, "ONE-TIME PAYMENT • NO HIDDEN FEES", font_reg, (35, 42, 64), (56, 189, 248), padding_x=24, padding_y=10)

            specs = [
                ("⏱️ 3 to 5 Business Days Delivery", "Fastest turnaround in Kenya guaranteed"),
                ("📱 Mobile-First Responsive Design", "Perfect layout on iPhone, Samsung & tablets"),
                ("💬 WhatsApp Direct Lead Capture", "Floating chat button connects buyers to you"),
                ("🎁 100% Upgrade Credit Guarantee", "Upgrade within 6 months, we credit the full 15k!"),
                ("⚡ Sub-1.5s Speed Optimization", "Never lose a visitor to slow loading pages")
            ]
            sy = 650
            for s_t, s_d in specs:
                draw_rounded_rect(draw, [140, sy, WIDTH - 140, sy + 140], 18, fill=(26, 30, 46))
                draw.text((180, sy + 45), s_t, font=font_bold_med, fill=(251, 181, 0), anchor="lm")
                draw.text((180, sy + 95), s_d, font=font_reg, fill=(200, 210, 230), anchor="lm")
                sy += 160
        else:
            draw.text((WIDTH // 2, 260), "CLAIM YOUR SLOT THIS WEEK", font=font_title_med, fill=(32, 217, 161), anchor="mm")
            draw_rounded_rect(draw, [100, 360, WIDTH - 100, 800], 28, fill=(22, 25, 38), outline=(32, 217, 161), width=3)
            draw_pill(draw, WIDTH // 2, 420, "LIMITED SLOTS PER WEEK", font_reg, (32, 217, 161), (5, 46, 32), padding_x=24, padding_y=10)
            draw.text((WIDTH // 2, 510), "Express Sales Landing Page", font=font_bold_large, fill=(255, 255, 255), anchor="mm")
            draw.text((WIDTH // 2, 600), "KES 15,000", font=font_title_huge, fill=(32, 217, 161), anchor="mm")
            draw.text((WIDTH // 2, 680), "Live on Google in 3-5 Business Days", font=font_reg, fill=(180, 190, 215), anchor="mm")
            draw.text((WIDTH // 2, 740), "100% Upgrade Credit Towards Full Site Included", font=font_reg, fill=(251, 181, 0), anchor="mm")

            pulse = math.sin(i / FPS * 5) * 5
            btn_box = [100, 900 - int(pulse), WIDTH - 100, 1080 - int(pulse)]
            draw_rounded_rect(draw, btn_box, 36, fill=(37, 211, 102), outline=(255, 255, 255), width=3)
            draw.text((WIDTH // 2, 960 - int(pulse)), "💬 WHATSAPP SAMUEL TO GET STARTED", font=font_bold_med, fill=(5, 46, 25), anchor="mm")
            draw.text((WIDTH // 2, 1030 - int(pulse)), "+254 722 753 819", font=font_title_huge, fill=(5, 46, 25), anchor="mm")
            draw.text((WIDTH // 2, 1180), "Visit: www.xclusivetech.co.ke", font=font_bold_large, fill=(56, 189, 248), anchor="mm")
            draw.text((WIDTH // 2, 1260), "120+ Verified Deployments Across Kenya", font=font_reg, fill=(160, 175, 205), anchor="mm")

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    output_final = "assets/videos/reel4_express_landing_page.mp4"
    cmd_mux = ["ffmpeg", "-y", "-i", video_raw, "-i", audio_wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", output_final]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(video_raw):
        os.remove(video_raw)
    if os.path.exists(audio_wav):
        os.remove(audio_wav)
    print(f"✅ Express Reel completed: {output_final} ({os.path.getsize(output_final)} bytes)")
    return output_final

if __name__ == "__main__":
    rg = render_reel_ghost()
    re = render_reel_express()
    print("🎉 ALL REELS COMPLETED!")

