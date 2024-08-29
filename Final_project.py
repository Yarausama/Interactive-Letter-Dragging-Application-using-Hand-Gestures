import cv2
import mediapipe as mp
import random

# Initialize MediaPipe Hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize OpenCV webcam capture
cap = cv2.VideoCapture(0)

# Get the frame size from the camera
ret, frame = cap.read()
frame_height, frame_width, _ = frame.shape

# Define letters with random initial positions
letters = {
    'A': (random.randint(50, frame_width - 100), random.randint(50, frame_height - 100)),
    'B': (random.randint(50, frame_width - 100), random.randint(50, frame_height - 100)),
    'C': (random.randint(50, frame_width - 100), random.randint(50, frame_height - 100))
}

def is_pinch(landmarks):
    """Check if the index finger and thumb are pinching"""
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    
    # Debugging line to see the distance
    print(f"Pinch Distance: {distance}")
    
    return distance < 0.05  # Adjust threshold as necessary

def draw_letters(frame, letters):
    """Draw letters on the frame"""
    for letter, position in letters.items():
        cv2.putText(frame, letter, position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip the image horizontally for natural interaction
    frame = cv2.flip(frame, 1)

    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and find hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for pinch
            if is_pinch(hand_landmarks.landmark):
                index_finger_pos = hand_landmarks.landmark[8]

                # Convert normalized coordinates to screen coordinates
                x = int(index_finger_pos.x * frame.shape[1])
                y = int(index_finger_pos.y * frame.shape[0])

                # Visual feedback - Draw a circle on the index finger
                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                # Check if any letter is close to the pinch
                for letter, position in letters.items():
                    lx, ly = position
                    if abs(lx - x) < 50 and abs(ly - y) < 50:  # Adjust threshold as necessary
                        letters[letter] = (x, y)

    # Draw the letters on the frame
    draw_letters(frame, letters)

    # Display the resulting frame
    cv2.imshow('Interactive Letter Dragging', frame)

    if cv2.waitKey(1) == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


