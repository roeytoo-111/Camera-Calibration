import os
import cv2

# Calibration setup
CHESSBOARD_SIZE = (9, 6)  # Inner corners (Columns, Rows)
OUTPUT_DIRECTORY = 'calibration_images'

def capture_calibration_images():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        
    # Match the working test.py setup exactly
    CAMERA_ID = 1  
    cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Index 1 failed. Trying Index 0...")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
    if not cap.isOpened():
        print("Error: Could not open the thermal camera stream.")
        return

    # Let the camera use its working native resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print("=========================================")
    print(" Thermal Calibration Stream Active!")
    print(f" Resolution: {width}x{height}")
    print(" Press 'c' to capture a calibration frame.")
    print(" Press 'q' to finish and exit.")
    print("=========================================")

    img_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Make a copy to display overlay details
        display_frame = frame.copy()
        
        # Try to detect the chessboard corners live
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret_chess, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

        if ret_chess:
            # Draw lines connecting the corners if found
            cv2.drawChessboardCorners(display_frame, CHESSBOARD_SIZE, corners, ret_chess)
            cv2.putText(display_frame, "Chessboard Detected!", (30, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(display_frame, "Searching for Chessboard...", (30, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

        # UI overlays
        cv2.putText(display_frame, f"Saved: {img_counter}", (30, height - 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.imshow("Thermal Camera Calibration", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            print("Exiting...")
            break
        elif key == ord('c'):
            # Save the clean frame (without green line drawings) for calibration accuracy
            img_name = os.path.join(OUTPUT_DIRECTORY, f"calibration_{img_counter:02d}.jpg")
            cv2.imwrite(img_name, frame)
            print(f"[{img_counter}] Captured and saved: {img_name}")
            img_counter += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nDone! Saved {img_counter} images to the '{OUTPUT_DIRECTORY}' directory.")

if __name__ == "__main__":
    capture_calibration_images()
