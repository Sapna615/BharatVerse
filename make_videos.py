import imageio
import numpy as np
from PIL import Image
import os

images = [
    ('/Users/sapnarai/.gemini/antigravity-ide/brain/52831b9f-8158-4504-a9ce-2da4813aa59e/taj_mahal_1791472732183.jpg', 'static/videos/video1.mp4'),
    ('/Users/sapnarai/.gemini/antigravity-ide/brain/52831b9f-8158-4504-a9ce-2da4813aa59e/hampi_1791472757322.jpg', 'static/videos/video2.mp4'),
    ('/Users/sapnarai/.gemini/antigravity-ide/brain/52831b9f-8158-4504-a9ce-2da4813aa59e/hawa_mahal_1791472781004.jpg', 'static/videos/video3.mp4')
]

FPS = 30
DURATION = 5  # seconds
TOTAL_FRAMES = FPS * DURATION
TARGET_WIDTH = 1280
TARGET_HEIGHT = 720

def make_video(img_path, out_path):
    print(f"Processing {img_path} -> {out_path}")
    img = Image.open(img_path).convert('RGB')
    
    # Calculate crop logic for zoom
    # We will zoom in by 10% over the duration
    orig_w, orig_h = img.size
    
    writer = imageio.get_writer(out_path, fps=FPS, codec='libx264', quality=8)
    
    for i in range(TOTAL_FRAMES):
        progress = i / float(TOTAL_FRAMES)
        zoom_factor = 1.0 + (0.1 * progress) # zoom from 1x to 1.1x
        
        # calculate crop box
        crop_w = orig_w / zoom_factor
        crop_h = orig_h / zoom_factor
        
        # center crop
        left = (orig_w - crop_w) / 2
        top = (orig_h - crop_h) / 2
        right = left + crop_w
        bottom = top + crop_h
        
        cropped = img.crop((left, top, right, bottom))
        resized = cropped.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        
        frame = np.array(resized)
        writer.append_data(frame)
        
    writer.close()
    print(f"Done {out_path}")

for img, out in images:
    if os.path.exists(img):
        make_video(img, out)
    else:
        print(f"Missing {img}")
