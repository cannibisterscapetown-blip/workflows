#!/usr/bin/env python3
import os
from rembg import remove
from PIL import Image
import io

IMAGE_FILES = [
    "high club lemon skittelz .jpg",
    "high cclub lemon skittelz front.jpg",
    "high club lemon skittelz side .jpg",
    "high club permenant marker.jpg",
    "high club permenant marker front.jpg",
    "high club permemnant marker side.jpg"
]

BASE_PATH = "/Users/norton/Desktop/Cannibisters Agent"

def process_image(filename):
    input_path = os.path.join(BASE_PATH, filename)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name.strip()}_white.jpg" # saving as jpg needs white background, png can be transparent
    output_path = os.path.join(BASE_PATH, output_filename)

    if not os.path.exists(input_path):
        print(f"❌ File not found: {filename}")
        return

    print(f"Processing {filename}...")
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            
        # Remove background
        subject = remove(input_data)
        
        # Convert to PIL Image
        img = Image.open(io.BytesIO(subject))
        
        # Create white background
        white_bg = Image.new("RGB", img.size, (255, 255, 255))
        
        # Paste subject onto white background using alpha channel as mask
        if img.mode == 'RGBA':
            white_bg.paste(img, (0, 0), img)
            final_img = white_bg
        else:
            final_img = img # Fallback if no alpha channel returned (unlikely with rembg)

        # Save
        final_img.save(output_path, "JPEG")
        print(f"✅ Saved to {output_filename}")
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")

def main():
    print("🚀 Starting background removal...")
    for img in IMAGE_FILES:
        process_image(img)
    print("🎉 Done!")

if __name__ == "__main__":
    main()
