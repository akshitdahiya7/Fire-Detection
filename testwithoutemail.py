# import cv2
# from ultralytics import YOLO

# # Load your trained model
# model = YOLO(r'C:\Coding\Projects\yolo8\yolocff.pt')  # Path to your best model

# # Initialize video capture
# cap = cv2.VideoCapture(0)  # 0 for the default camera

# while True:
#     # Read a frame from the camera
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break
    
#     # Perform detection
#     results = model(frame)

#     # Render results on the frame
#     frame = results[0].plot()  # Annotate the frame with detections
    
#     # Display the frame
#     cv2.imshow('YOLOv8 Detection', frame)

#     # Break the loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the capture and close windows
# cap.release()
# cv2.destroyAllWindows()
# import cv2
# import time
# from pathlib import Path
# from playsound import playsound
# import threading
# from ultralytics import YOLO

# # Load your YOLO model here
# model = YOLO("best.pt")  # Replace "best.pt" with the path to your trained YOLO model

# # Initialize video capture (use your camera or video file path)
# cap = cv2.VideoCapture(0)

# # Define the alarm sound and initial state
# alarm_sound = "alarm_sound.mp3"  # Update extension if needed
# alarm_triggered = False
# fire_detected = False  # New flag to track fire detection

# # Function to play the alarm sound (play only once per detection)
# def play_alarm():
#     global fire_detected  # Access the global flag
#     if not fire_detected:  # Check if fire is currently detected
#         playsound(alarm_sound)
#         fire_detected = True  # Set flag to prevent repeated playing

# # Thread for playing the alarm sound
# alarm_thread = threading.Thread(target=play_alarm)

# # Time tracking
# last_processed_time = time.time()
# interval = 15  # 15 seconds
# frame_counter = 0

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break

#     current_time = time.time()

#     # Process frame every 15 seconds
#     if current_time - last_processed_time >= interval:
#         # Resize the frame (optional)
#         frame_resized = cv2.resize(frame, (640, 480))

#         # Perform detection with YOLOv8
#         results = model(frame_resized)

#         # Access the detections and check for 'fire' class
#         fire_detected = False  # Reset flag before checking

#         for result in results:
#             labels = result.names  # Class names (e.g., "fire", "person", etc.)
#             scores = result.scores  # Confidence scores (updated attribute name)

#             for label, score in zip(labels, scores):
#                 if label == "fire" and score > 0.5:  # Adjust confidence threshold
#                     fire_detected = True
#                     # Start the alarm sound if not already playing and fire detected
#                     if not alarm_thread.is_alive():
#                         alarm_thread.start()

#         # Visualize results
#         frame = results[0].plot()

#         # Update last processed time
#         last_processed_time = current_time

#     # Display the frame
#     cv2.imshow('YOLOv8 Fire Detection', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Cleanup
# cap.release()
# cv2.destroyAllWindows()
import cv2
from ultralytics import YOLO

# Load a pre-trained YOLOv8 model
model = YOLO("best.pt")  # Use your specific trained YOLO model

# Initialize video capture
cap = cv2.VideoCapture(0)  # 0 for the default camera

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Perform detection
    results = model(frame)

    # Filter detections by confidence threshold
    for result in results[0].boxes.data.tolist():  # Access detections
        x1, y1, x2, y2, confidence, class_id = result
        if confidence > 0.8:  # Check confidence threshold
            # Draw bounding box and label for detections
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"Fire {confidence:.2f}",
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    # Display the frame
    cv2.imshow('YOLOv8 Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

