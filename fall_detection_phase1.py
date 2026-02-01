"""
AI-Augmented Smart Safety Helmet - Phase 1: Logic Prototype
Fall Detection System using YOLOv5 on Laptop Webcam

Author: [Your Team Name]
Date: February 2026
Version: 1.0

This script implements the complete Phase 1 functionality:
- FR-01: Video Acquisition (30 FPS webcam)
- FR-02: Object Detection (YOLOv5)
- FR-03: Fall Logic (Vertical Velocity Calculation)
- FR-04: Visual Alert (Red Border + "DANGER" text)
- FR-05: Audio Alert (Beep sound)
"""

import cv2
import torch
import numpy as np
import pygame
import time
from collections import deque

# ============================================================================
# CONFIGURATION PARAMETERS
# ============================================================================

# Fall Detection Thresholds
FALL_VELOCITY_THRESHOLD = 5.0  # pixels per frame (minimum velocity to trigger)
MIN_CONSECUTIVE_FRAMES = 3      # Must detect fall for N consecutive frames
DETECTION_CONFIDENCE = 0.5      # YOLOv5 confidence threshold

# Target Object Classes (COCO dataset class names)
TARGET_CLASSES = ['cup', 'bottle', 'cell phone', 'book', 'scissors']

# Alert Configuration
ALERT_DURATION = 2.0  # seconds
ALERT_COOLDOWN = 1.0  # seconds between alerts

# Camera Configuration
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
TARGET_FPS = 30

# ============================================================================
# AUDIO SYSTEM INITIALIZATION
# ============================================================================

class AudioAlertSystem:
    """Handles audio alerts using pygame mixer"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        self.alert_active = False
        self.generate_beep_sound()
    
    def generate_beep_sound(self):
        """Generate a beep sound programmatically"""
        sample_rate = 22050
        duration = 0.2  # 200ms beep
        frequency = 800  # 800 Hz tone
        
        # Generate sine wave
        n_samples = int(duration * sample_rate)
        buf = np.sin(2 * np.pi * frequency * np.linspace(0, duration, n_samples))
        
        # Convert to 16-bit PCM
        buf = (buf * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo_buf = np.column_stack((buf, buf))
        
        self.beep_sound = pygame.sndarray.make_sound(stereo_buf)
    
    def play_alert(self):
        """Play the alert beep"""
        if not self.alert_active:
            self.beep_sound.play()
            self.alert_active = True
    
    def stop_alert(self):
        """Stop the alert"""
        self.alert_active = False

# ============================================================================
# FALL DETECTION LOGIC
# ============================================================================

class FallDetector:
    """Implements the fall detection algorithm"""
    
    def __init__(self, velocity_threshold=FALL_VELOCITY_THRESHOLD, 
                 min_frames=MIN_CONSECUTIVE_FRAMES):
        self.velocity_threshold = velocity_threshold
        self.min_frames = min_frames
        self.tracked_objects = {}
        self.fall_detected_count = 0
        self.last_alert_time = 0
    
    def calculate_velocity(self, current_y, previous_y):
        """Calculate vertical velocity in pixels/frame"""
        return current_y - previous_y
    
    def update_tracking(self, detections, current_frame_time):
        """
        Update object tracking and detect falls
        
        Args:
            detections: List of (class_name, confidence, x1, y1, x2, y2)
            current_frame_time: Current timestamp
            
        Returns:
            bool: True if fall detected, False otherwise
        """
        current_objects = {}
        fall_detected = False
        
        # Process each detection
        for detection in detections:
            class_name, conf, x1, y1, x2, y2 = detection
            
            # Calculate center point
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            
            # Try to match with existing tracked objects
            matched = False
            for obj_id, obj_data in self.tracked_objects.items():
                prev_center_x, prev_center_y, prev_class = obj_data
                
                # Simple distance-based matching
                distance = np.sqrt((center_x - prev_center_x)**2 + 
                                 (center_y - prev_center_y)**2)
                
                if distance < 100 and class_name == prev_class:  # Same object
                    # Calculate velocity
                    velocity = self.calculate_velocity(center_y, prev_center_y)
                    
                    # Check if falling (moving downward)
                    if velocity > self.velocity_threshold:
                        self.fall_detected_count += 1
                        
                        if self.fall_detected_count >= self.min_frames:
                            # Check cooldown period
                            if (current_frame_time - self.last_alert_time) > ALERT_COOLDOWN:
                                fall_detected = True
                                self.last_alert_time = current_frame_time
                                self.fall_detected_count = 0
                    else:
                        self.fall_detected_count = max(0, self.fall_detected_count - 1)
                    
                    matched = True
                    current_objects[obj_id] = (center_x, center_y, class_name)
                    break
            
            # New object
            if not matched:
                new_id = len(current_objects) + len(self.tracked_objects)
                current_objects[new_id] = (center_x, center_y, class_name)
        
        # Update tracked objects
        self.tracked_objects = current_objects
        
        return fall_detected

# ============================================================================
# VISUAL ALERT RENDERING
# ============================================================================

class VisualAlertRenderer:
    """Handles visual alerts on the screen"""
    
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.alert_start_time = None
    
    def render_alert(self, frame):
        """
        Render visual alert on frame
        
        Args:
            frame: OpenCV frame (numpy array)
            
        Returns:
            Modified frame with alert overlay
        """
        # Create red border (thick rectangle)
        border_thickness = 20
        cv2.rectangle(frame, 
                     (0, 0), 
                     (self.frame_width, self.frame_height),
                     (0, 0, 255), 
                     border_thickness)
        
        # Add semi-transparent red overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.frame_width, self.frame_height),
                     (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Add "DANGER" text
        text = "DANGER!"
        font = cv2.FONT_HERSHEY_BOLD
        font_scale = 3
        thickness = 8
        
        # Get text size for centering
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_x = (self.frame_width - text_width) // 2
        text_y = (self.frame_height + text_height) // 2
        
        # Draw text with outline
        cv2.putText(frame, text, (text_x, text_y), font, font_scale,
                   (0, 0, 0), thickness + 4, cv2.LINE_AA)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale,
                   (255, 255, 255), thickness, cv2.LINE_AA)
        
        return frame
    
    def start_alert(self):
        """Start the visual alert"""
        self.alert_start_time = time.time()
    
    def is_alert_active(self):
        """Check if alert should still be displayed"""
        if self.alert_start_time is None:
            return False
        
        elapsed = time.time() - self.alert_start_time
        if elapsed > ALERT_DURATION:
            self.alert_start_time = None
            return False
        
        return True

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class SmartHelmetPhase1:
    """Main application class"""
    
    def __init__(self):
        print("🎯 Initializing AI-Augmented Smart Safety Helmet - Phase 1")
        print("=" * 70)
        
        # Load YOLOv5 model
        print("📦 Loading YOLOv5 model...")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.conf = DETECTION_CONFIDENCE
        print("✅ Model loaded successfully")
        
        # Initialize components
        self.audio_system = AudioAlertSystem()
        self.fall_detector = FallDetector()
        self.visual_alert = VisualAlertRenderer(FRAME_WIDTH, FRAME_HEIGHT)
        
        # Initialize camera
        print(f"📷 Initializing camera (Index: {CAMERA_INDEX})...")
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
        
        if not self.cap.isOpened():
            raise RuntimeError("❌ Failed to open camera")
        
        print("✅ Camera initialized successfully")
        print("=" * 70)
        print("🚀 System Ready!")
        print(f"📊 Target Objects: {', '.join(TARGET_CLASSES)}")
        print(f"⚡ Fall Threshold: {FALL_VELOCITY_THRESHOLD} pixels/frame")
        print(f"🎯 Min Consecutive Frames: {MIN_CONSECUTIVE_FRAMES}")
        print("=" * 70)
        print("💡 Press 'Q' to quit")
        print()
    
    def process_frame(self, frame):
        """
        Process a single frame
        
        Returns:
            processed_frame, fall_detected
        """
        # Run YOLOv5 detection
        results = self.model(frame)
        
        # Parse detections
        detections = []
        for *box, conf, cls in results.xyxy[0]:
            class_name = self.model.names[int(cls)]
            
            # Filter for target classes
            if class_name.lower() in [c.lower() for c in TARGET_CLASSES]:
                x1, y1, x2, y2 = map(int, box)
                detections.append((class_name, float(conf), x1, y1, x2, y2))
        
        # Update fall detection
        current_time = time.time()
        fall_detected = self.fall_detector.update_tracking(detections, current_time)
        
        # Draw bounding boxes
        for class_name, conf, x1, y1, x2, y2 in detections:
            color = (0, 255, 0)  # Green
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            label = f"{class_name}: {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame, fall_detected
    
    def run(self):
        """Main application loop"""
        fps_time = time.time()
        fps_counter = 0
        fps_display = 0
        
        try:
            while True:
                # Capture frame
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to capture frame")
                    break
                
                # Process frame
                processed_frame, fall_detected = self.process_frame(frame)
                
                # Handle fall detection
                if fall_detected:
                    print("⚠️  FALL DETECTED! Activating alerts...")
                    self.visual_alert.start_alert()
                    self.audio_system.play_alert()
                
                # Render visual alert if active
                if self.visual_alert.is_alert_active():
                    processed_frame = self.visual_alert.render_alert(processed_frame)
                else:
                    self.audio_system.stop_alert()
                
                # Calculate FPS
                fps_counter += 1
                if time.time() - fps_time > 1.0:
                    fps_display = fps_counter
                    fps_counter = 0
                    fps_time = time.time()
                
                # Add FPS and status overlay
                status_text = f"FPS: {fps_display} | Objects: {len(self.fall_detector.tracked_objects)}"
                cv2.putText(processed_frame, status_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Add instructions
                cv2.putText(processed_frame, "Press 'Q' to quit", (10, FRAME_HEIGHT - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Display frame
                cv2.imshow('Smart Safety Helmet - Phase 1', processed_frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\n👋 Shutting down...")
                    break
                
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        finally:
            # Cleanup
            self.cap.release()
            cv2.destroyAllWindows()
            pygame.mixer.quit()
            print("✅ Cleanup complete")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        app = SmartHelmetPhase1()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
