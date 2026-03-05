#!/usr/bin/env python3
"""
Upload new rotating bud videos to Shopify products.
Preserves existing images.
"""

import os
from shopify_api import upload_product_video

# Base directory for extracted videos
BASE_DIR = "rotating_products_temp/New Folder With Items"

# Mapping: filename -> list of product IDs
VIDEO_MAPPING = {
    "Rosin moonstick.mov": [
        "8822549545172", "8822549938388", "8941565411540", "8941562101972", 
        "8901471142100", "8625795760340", "8822549774548", "8822549807316", 
        "8686114963668", "8944913187028", "8822549676244", "8625795268820",
        "8686115258580", "8829780754644", "8152398463188", # Moonsticks
        "8152398233812", "8159396167892"                   # Super Joints
    ],
    "CBD oil 600mg.mov": ["7611810840788"],
    "near death drops.mov": ["8808150434004", "8793345294548"],
    "THC breath mints.mov": ["8995166879956"],
    "Platinum chimera breath rosin.mov": ["8949571911892"],
    "Joint 01.mov": [
        "9029350129876", "9029349900500", "9029349638356", 
        "9029349179604", "9029349015764"
    ],
    "THC distillate.mov": ["8822524215508"],
    "Blue sherbet rosin.mov": ["8949572305108"],
    "1200mg oil.mov": ["7811472326868"],
    "death drops.mov": ["8793346408660", "8793348473044"]
}

def main():
    print("🎥 Starting upload of new rotating bud videos...")
    print("=" * 60)
    
    for filename, product_ids in VIDEO_MAPPING.items():
        video_path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(video_path):
            print(f"⚠️ Video NOT FOUND: {filename}")
            continue
            
        print(f"\n🎬 Video: {filename}")
        for pid in product_ids:
            print(f"   ⬆️ Uploading to Product ID: {pid}...")
            if upload_product_video(pid, video_path):
                print(f"   ✅ Done: {pid}")
            else:
                print(f"   ❌ Failed: {pid}")

    print("\n" + "=" * 60)
    print("🎉 All video uploads processed!")

if __name__ == "__main__":
    main()
