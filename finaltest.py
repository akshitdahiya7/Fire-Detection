
import cv2
from ultralytics import YOLO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

# Load YOLOv8 model
model = YOLO("best.pt")

# Initialize video capture
cap = cv2.VideoCapture(0)

# Email configuration
sender_email = "akshitdahiya1621@gmail.com"
receiver_email = "akshitdahiya2116@gmail.com"
password = "emmr qjwn jmgp npow "  # Use app-specific password if needed
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Email cooldown settings
# Email cooldown settings
# last_email_time = 0
# email_cooldown = 30  # Cooldown time in seconds

# def send_email_with_image(image_path):
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = "Fire Detection Alert"

#     # Email body
#     body = "Fire has been detected by the YOLOv8 model. See the attached image."
#     msg.attach(MIMEText(body, 'plain'))

#     # Attach the image
#     with open(image_path, 'rb') as attachment:
#         mime_base = MIMEBase('application', 'octet-stream')
#         mime_base.set_payload(attachment.read())
#         encoders.encode_base64(mime_base)
#         mime_base.add_header(
#             'Content-Disposition',
#             f'attachment; filename=fire_detected.jpg'
#         )
#         msg.attach(mime_base)

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.send_message(msg)
#         print("Email sent successfully with the image")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

# while True:
#     # Read a frame from the camera
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break

#     # Perform detection
#     results = model(frame)

#     # Flag to check if fire is detected
#     fire_detected = False

#     # Filter detections by confidence threshold
#     for result in results:
#         for box in result.boxes:
#             # Extract bounding box and other attributes
#             x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())  # Bounding box coordinates
#             confidence = float(box.conf[0].cpu().numpy())         # Confidence score
#             class_id = int(box.cls[0].cpu().numpy())              # Class ID (optional)

#             if confidence > 0.8:  # Check confidence threshold
#                 fire_detected = True
#                 # Draw bounding box and label for detections
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(
#                     frame,
#                     f"Fire {confidence:.2f}",
#                     (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     (0, 255, 0),
#                     2,
#                 )

#     # Send email if fire is detected and cooldown has passed
#     current_time = time.time()
#     if fire_detected and (current_time - last_email_time > email_cooldown):
#         image_path = "fire_detected.jpg"  # Path to save the image
#         cv2.imwrite(image_path, frame)   # Save the current frame as a JPG
#         send_email_with_image(image_path)
#         last_email_time = current_time

#     # Display the frame
#     cv2.imshow('YOLOv8 Detection', frame)

#     # Break the loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the capture and close windows
# cap.release()
# cv2.destroyAllWindows()


# Email sending function without cooldown
def send_email_with_image(image_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Fire Detection Alert"

    # Email body
    body = "Fire has been detected by the YOLOv8 model. See the attached image."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the image
    with open(image_path, 'rb') as attachment:
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(attachment.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header(
            'Content-Disposition',
            f'attachment; filename=fire_detected.jpg'
        )
        msg.attach(mime_base)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        print("Email sent successfully with the image")
    except Exception as e:
        print(f"Failed to send email: {e}")

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Perform detection
    results = model(frame)

    # Flag to check if fire is detected
    fire_detected = False

    # Filter detections by confidence threshold
    for result in results:
        for box in result.boxes:
            # Extract bounding box and other attributes
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())  # Bounding box coordinates
            confidence = float(box.conf[0].cpu().numpy())         # Confidence score
            class_id = int(box.cls[0].cpu().numpy())              # Class ID (optional)

            if confidence > 0.8:  # Check confidence threshold
                fire_detected = True
                # Draw bounding box and label for detections
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"Fire {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

    # Send email immediately if fire is detected (no cooldown check)
    if fire_detected:
        image_path = "fire_detected.jpg"  # Path to save the image
        cv2.imwrite(image_path, frame)   # Save the current frame as a JPG
        send_email_with_image(image_path)

    # Display the frame
    cv2.imshow('YOLOv8 Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()