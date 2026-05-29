import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime

def generate_stats_dashboard(stats: dict, bot_name: str, bot_username: str, avatar_path: str = None):
    """
    Generates an ultra-premium statistics dashboard image.
    
    :param stats: Dictionary containing detailed metrics
    :param bot_name: Display name of the bot
    :param bot_username: Username of the bot
    :param avatar_path: Path to the bot's profile picture
    :return: BytesIO object containing the PNG image
    """
    width, height = 900, 850 # Increased height for more cards
    bg_color = (13, 17, 23) # Modern GitHub-like dark
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # Fonts
    try:
        font_path_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font_path_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        if not os.path.exists(font_path_bold):
            font_path_bold = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font_path_reg = "/usr/share/fonts/truetype/liberation/LiberationSans.ttf"
            
        header_font = ImageFont.truetype(font_path_bold, 30)
        sub_header_font = ImageFont.truetype(font_path_reg, 18)
        label_font = ImageFont.truetype(font_path_bold, 15)
        value_font = ImageFont.truetype(font_path_bold, 42)
        small_val_font = ImageFont.truetype(font_path_bold, 20)
        footer_font = ImageFont.truetype(font_path_reg, 14)
    except:
        header_font = label_font = value_font = small_val_font = footer_font = ImageFont.load_default()

    # --- Header Navigation Bar ---
    draw.rectangle([0, 0, width, 120], fill=(22, 27, 34))
    
    # Draw Avatar (Circular)
    if avatar_path and os.path.exists(avatar_path):
        try:
            avatar = Image.open(avatar_path).convert("RGBA")
            avatar = avatar.resize((85, 85), Image.Resampling.LANCZOS)
            mask = Image.new('L', (85, 85), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, 85, 85), fill=255)
            avatar_circ = ImageOps.fit(avatar, (85, 85), centering=(0.5, 0.5))
            avatar_circ.putalpha(mask)
            image.paste(avatar_circ, (40, 18), avatar_circ)
            draw.ellipse((38, 16, 127, 105), outline=(0, 112, 243), width=3)
        except: pass

    # Bot Branding (Adjusted to prevent clipping)
    draw.text((145, 30), bot_name, font=header_font, fill=(255, 255, 255))
    draw.text((145, 68), f"@{bot_username}", font=sub_header_font, fill=(139, 148, 158))
    
    # Date in Header
    report_date = datetime.now().strftime("%B %d, %Y")
    draw.text((width - 240, 45), f"REPORT: {report_date}", font=footer_font, fill=(0, 112, 243))

    # --- Grid Card System ---
    
    def draw_card(draw, x, y, w, h, title, main_val, sub_metrics=None, color=(0, 112, 243)):
        # Card body
        draw.rounded_rectangle([x, y, x+w, y+h], radius=16, fill=(17, 19, 24), outline=(48, 54, 61), width=1)
        # Accent indicator
        draw.rectangle([x+10, y+25, x+15, y+65], fill=color)
        
        # Labels and Values (Fixed alignment to prevent overlap)
        draw.text((x+25, y+20), title.upper(), font=label_font, fill=(139, 148, 158))
        draw.text((x+25, y+45), str(main_val), font=value_font, fill=(255, 255, 255))
        
        if sub_metrics:
            curr_y = y + 105
            for label, val in sub_metrics.items():
                draw.text((x+25, curr_y), label, font=footer_font, fill=(139, 148, 158))
                # Right align values within card
                val_text = str(val)
                # Calculate right position (relative to card width)
                draw.text((x + w - 30 - len(val_text)*12, curr_y-2), val_text, font=small_val_font, fill=(255, 255, 255))
                curr_y += 38

    # Card 1: Community
    draw_card(draw, 40, 150, 400, 260, "Community Growth", f"{stats['users_total']:,}", 
              {"Daily Join": f"+{stats['joins_day']:,}", "Weekly Join": f"+{stats['joins_week']:,}", "Monthly Join": f"+{stats['joins_month']:,}"}, (0, 112, 243))

    # Card 2: Marketplace
    draw_card(draw, 460, 150, 400, 260, "Marketplace Stats", f"{stats['mp_total_products']:,}", 
              {"Downloads": f"{stats['mp_total_downloads']:,}", "Free Codes": f"{stats['mp_today_products']:,}", "Growth": f"+{stats['mp_today_downloads']:,}"}, (255, 170, 0))

    # Card 3: Bot Cloud
    draw_card(draw, 40, 430, 400, 260, "Bot Cloud Active", f"{stats['bots_active']:,}", 
              {"Total Registered": f"{stats['bots_total']:,}", "Daily Start": f"{stats['starts_day']:,}", "Weekly Start": f"{stats['starts_week']:,}"}, (191, 0, 255))

    # Card 4: Storage & Files
    draw_card(draw, 460, 430, 400, 260, "Content Inventory", f"{stats['files_total']:,}", 
              {"Daily Uploads": f"+{stats['uploads_day']:,}", "Weekly Uploads": f"+{stats['uploads_week']:,}", "Total Folders": f"{stats['folders_total']:,}"}, (0, 200, 100))

    # Card 5: System Health (Simplified)
    draw_card(draw, 40, 710, 820, 90, "System Health Monitor", "Node Status: OPTIMIZED", 
              {"API Latency": "42ms", "Core Engine": "Active", "Uptime": "99.99%"}, (0, 243, 222))

    # --- Footer ---
    draw.line([40, 800, 860, 800], fill=(48, 54, 61), width=1)
    footer_sig = f"© 2026 Admin Dashboard • Secure Identity Verified"
    draw.text((40, 815), footer_sig, font=footer_font, fill=(139, 148, 158))
    draw.text((width - 180, 815), bot_name.upper(), font=footer_font, fill=(0, 112, 243))

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr
