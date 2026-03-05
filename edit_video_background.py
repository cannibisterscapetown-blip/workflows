from moviepy.editor import *
import os

def process_video(input_path, output_path):
    print(f"Processing: {input_path}")
    
    try:
        # Load the videoclip
        clip = VideoFileClip(input_path)
        
        # Mask out black color
        # thr=20 gives a bit of tolerance for non-perfect blacks (compression artifacts)
        # s=0 disables softening which can look bad on sharp edges, but might need tweaking
        masked_clip = clip.fx(vfx.mask_color, color=[0, 0, 0], thr=20, s=2)
        
        # Create a white background of the same size and duration
        white_bg = ColorClip(size=clip.size, color=[255, 255, 255], duration=clip.duration)
        
        # Composite the masked clip over the white background
        final_clip = CompositeVideoClip([white_bg, masked_clip])
        
        # Write the result to a file
        print(f"Writing output to: {output_path}")
        # using libx264 codec for better compatibility
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        print("Done!")
        
    except Exception as e:
        print(f"Error processing video: {e}")

if __name__ == "__main__":
    input_video = "./rotating_products_temp/New Folder With Items/death drops.mov"
    output_video = "./rotating_products_temp/New Folder With Items/death_drops_white.mp4"
    
    if os.path.exists(input_video):
        process_video(input_video, output_video)
    else:
        print(f"Error: Input file not found at {input_video}")
