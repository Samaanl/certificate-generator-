import csv
import os
import argparse
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# ⚙️ CONFIGURATION SETTINGS
# ==========================================

# File paths
CSV_FILE = "data.csv"
TEMPLATE_FILE = "certificate.png"
OUTPUT_DIR = "certificates_output"

# Set this to True to draw red boxes on the image! 
# Use this to test your positioning. Set to False for the final generation.
DEBUG_BOXES = False

FONT_PATH = "arial_narrow_7.ttf" # Change this to the path of your downloaded .ttf font

# Bounding Box for the NAME
# x, y: Top-left corner of the box. 
# width, height: The maximum size of the box. The text will center inside this area and shrink if it's too wide.
NAME_BOX = {
    "x": 975,            # Left position
    "y": 650,            # Top position
    "width": 700,        # Maximum width before it starts shrinking the font
    "height": 100,       # Height of the box
    "color": (255,255, 255),  # Black
    "max_font_size": 80  # It will start at 80, and shrink if needed
}

# Bounding Box for the INSTITUTE
INSTITUTE_BOX = {
    "x": 132,            
    "y": 740,            
    "width": 1200,        
    "height": 80,        
    "color": (255,255, 255), # Dark Gray
    "max_font_size": 40 
}

# ==========================================

def draw_text_in_box(draw, text, font_path, box_settings, debug=False):
    """Draws text centered inside a bounding box, shrinking the font if necessary."""
    if not text:
        return

    box_x = box_settings["x"]
    box_y = box_settings["y"]
    box_w = box_settings["width"]
    box_h = box_settings["height"]
    text_color = box_settings["color"]
    current_font_size = box_settings["max_font_size"]
    
    # 1. Draw bounding box if in debug mode so you can see it
    if debug:
        draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], outline="red", width=3)
        
    # 2. Find the right font size to prevent overflow
    font = ImageFont.truetype(font_path, current_font_size)
    while current_font_size > 10:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        # If it fits within the box, stop shrinking
        if text_w <= box_w and text_h <= box_h:
            break
        
        # Otherwise, shrink the font and try again
        current_font_size -= 2
        font = ImageFont.truetype(font_path, current_font_size)

    # 3. Calculate final position to center it exactly INSIDE the box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    offset_y = bbox[1] # PIL vertical offset adjustment
    
    final_x = box_x + (box_w - text_w) / 2
    final_y = box_y + (box_h - text_h) / 2 - offset_y
    
    # 4. Draw the text
    draw.text((final_x, final_y), text, fill=text_color, font=font)

def main():
    # 1. Set up the CLI arguments
    parser = argparse.ArgumentParser(description="Bulk Certificate Generator")
    parser.add_argument("--limit", type=int, default=None, 
                        help="Limit the number of certificates to generate (for testing)")
    args = parser.parse_args()

    # 2. Check if files exist
    if not os.path.exists(TEMPLATE_FILE):
        print(f"❌ Error: Template image '{TEMPLATE_FILE}' not found.")
        return
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: CSV file '{CSV_FILE}' not found.")
        return
    if not os.path.exists(FONT_PATH):
        print(f"❌ Error: Font file '{FONT_PATH}' not found. Please provide a valid .ttf font.")
        return

    # 3. Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 4. Load the fonts (Just checking if the file exists, sizes are dynamic now)
    try:
        ImageFont.truetype(FONT_PATH, 10)
    except Exception as e:
        print(f"❌ Error loading font: {e}")
        return

    # 5. Open template to get its dimensions
    template = Image.open(TEMPLATE_FILE)
    image_width, image_height = template.size

    # 6. Read CSV and generate certificates
    generated_count = 0
    
    print(f"🚀 Starting generation. Outputting to '{OUTPUT_DIR}' folder...")

    # Using utf-8-sig to handle potential BOM characters at the start of the CSV
    with open(CSV_FILE, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Stop if we hit the user-defined limit
            if args.limit and generated_count >= args.limit:
                break
                
            # Safely get Name and Institute, default to empty string if missing
            name = row.get('Name', '').strip()
            institute = row.get('Institute', '').strip()

            if not name:
                continue # Skip empty rows
                
            # Create a fresh copy of the template for this person
            cert_img = template.copy()
            draw = ImageDraw.Draw(cert_img)
            
            # Draw Name and Institute using the dynamic bounding boxes
            draw_text_in_box(draw, name, FONT_PATH, NAME_BOX, debug=DEBUG_BOXES)
            draw_text_in_box(draw, institute, FONT_PATH, INSTITUTE_BOX, debug=DEBUG_BOXES)
            
            # Save the file as PNG
            # Clean up the name to make it a valid filename (removing slashes etc)
            safe_filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            output_path = os.path.join(OUTPUT_DIR, f"{safe_filename}.png")
            
            cert_img.save(output_path, "PNG")
            generated_count += 1
            print(f"✅ Generated: {safe_filename}.png")

    print(f"🎉 Done! Successfully generated {generated_count} certificates.")

if __name__ == "__main__":
    main()