import cv2
import mediapipe as mp
import pyautogui
from pynput.mouse import Button, Controller
import util

screen_width, screen_height = pyautogui.size()
mouse = Controller()
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)


def find_finger_tip(p):
    if p.multi_hand_landmarks:
        hand_landmarks = processed_frame.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None


def move_mouse(i):
    if i is not None:
        x = int(i.x * screen_width)
        y = int(i.y * screen_height)
        pyautogui.moveTo(x, y)


def is_left_click(landmark_list, thumb_index_dist):
    return (util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 < thumb_index_dist and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90
            )


def is_right_click(landmark_list, thumb_index_dist):
    return (util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 < thumb_index_dist and
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90
            )


def detect_gestures(f, l, p):
    if len(l) >= 21:
        index_finger_tip = find_finger_tip(p)
        thumb_index_dist = util.get_distance([l[4], l[5]])

        if thumb_index_dist < 50 and util.get_angle(l[5], l[6], l[8]) > 90:
            move_mouse(index_finger_tip)

        elif is_left_click(landmark_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)

        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)




cam = cv2.VideoCapture(0)
draw = mp.solutions.drawing_utils
while cam.isOpened:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    processed_frame = hands.process(frameRGB)
    landmark_list = []

    if processed_frame.multi_hand_landmarks:
        hand_landmarks = processed_frame.multi_hand_landmarks[0]
        draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

        for i in hand_landmarks.landmark:
            landmark_list.append((i.x, i.y))
    detect_gestures(frame, landmark_list, processed_frame)

    cv2.imshow("image", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
