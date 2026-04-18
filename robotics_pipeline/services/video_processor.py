import cv2
import numpy as np
from typing import List

class VideoProcessor:
    def __init__(self, sample_rate: int = 30):
        self.sample_rate = sample_rate

    def process_video(self, video_path: str) -> List[np.ndarray]:
        """
        Simulates extracting frames from a video.
        If video_path is 'dummy', returns mock frame data.
        """
        frames = []
        if video_path == "dummy":
            # Return dummy blank frames
            for _ in range(5):
                frames.append(np.zeros((224, 224, 3), dtype=np.uint8))
            return frames
            
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_count % self.sample_rate == 0:
                    # In a real scenario, we'd preprocess the frame here
                    frames.append(frame)
                frame_count += 1
            cap.release()
        except Exception as e:
            print(f"Error processing video: {e}")
            
        return frames

video_processor = VideoProcessor()
