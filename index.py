# app.py

from flask import Flask, render_template, Response, request, redirect
import cv2 as cv
import threading

# from drowsiness_detection.detector import DrowsinessDetectionApp

import os
import mediapipe as mp
from scipy.spatial import distance as dis
import pygame

app = Flask(__name__)

# Lock to synchronize access to the camera
camera_lock = threading.Lock()


# @app.route("/")
# def home():
#     return render_template("index.html")

# Function to check for custom ringtones
def get_ringtone_paths():
    if os.path.exists(CUSTOM_SLEEP_RINGTONE_PATH):
        sleep_ringtone = CUSTOM_SLEEP_RINGTONE_PATH
    else:
        sleep_ringtone = DEFAULT_SLEEP_RINGTONE

    if os.path.exists(CUSTOM_TIRED_RINGTONE_PATH):
        tired_ringtone = CUSTOM_TIRED_RINGTONE_PATH
    else:
        tired_ringtone = DEFAULT_TIRED_RINGTONE

    return sleep_ringtone, tired_ringtone

@app.route("/upload_custom_ringtone", methods=["POST"])
def upload_custom_ringtone():
    if "custom_sleep_ringtone" in request.files:
        custom_sleep_ringtone = request.files["custom_sleep_ringtone"]
        if custom_sleep_ringtone.filename != "":
            custom_sleep_ringtone.save(CUSTOM_SLEEP_RINGTONE_PATH)

    if "custom_tired_ringtone" in request.files:
        custom_tired_ringtone = request.files["custom_tired_ringtone"]
        if custom_tired_ringtone.filename != "":
            custom_tired_ringtone.save(CUSTOM_TIRED_RINGTONE_PATH)

        # Automatically use the custom ringtone when it's uploaded
        return redirect("/")

    return redirect("/")

@app.route("/")
def home():
    # Automatically set custom ringtones if available
    sleep_ringtone, tired_ringtone = get_ringtone_paths()
    
    return render_template("index.html", sleep_ringtone=sleep_ringtone, tired_ringtone=tired_ringtone)



# def __init__(self):
pygame.init()
sleep_ringtone_path = (
    "Sleep.wav"  # Provide the correct path to sleep.wav
)

tired_ringtone_path = (
    "Tired.wav"  # Provide the correct path to tired.wav
)
# Define paths for default ringtones
DEFAULT_SLEEP_RINGTONE = "static/sleep.wav"
DEFAULT_TIRED_RINGTONE = "static/tired.wav"

# Define paths for custom ringtones
CUSTOM_SLEEP_RINGTONE_PATH = "custom_ringtones/sleep/sleep_custom.wav"
CUSTOM_TIRED_RINGTONE_PATH = "custom_ringtones/tired/tired_custom.wav"


def drowsiness_detection():
    # Initialize the video capture
    # Placeholder for the actual detection logic
    print(
        "Drowsiness detection started using sleep ringtone:",
        sleep_ringtone_path,
    )
    print("and tired ringtone:", tired_ringtone_path)

    def draw_landmarks(image, outputs, land_mark, color):
        height, width = image.shape[:2]
        for face in land_mark:
            point = outputs.multi_face_landmarks[0].landmark[face]
            point_scale = ((int)(point.x * width), (int)(point.y * height))
            cv.circle(image, point_scale, 2, color, 1)

    def euclidean_distance(image, top, bottom):
        height, width = image.shape[0:2]
        point1 = int(top.x * width), int(top.y * height)
        point2 = int(bottom.x * width), int(bottom.y * height)
        distance = dis.euclidean(point1, point2)
        return distance

    def get_aspect_ratio(image, outputs, top_bottom, left_right):
        landmark = outputs.multi_face_landmarks[0]
        top = landmark.landmark[top_bottom[0]]
        bottom = landmark.landmark[top_bottom[1]]
        top_bottom_dis = euclidean_distance(image, top, bottom)
        left = landmark.landmark[left_right[0]]
        right = landmark.landmark[left_right[1]]
        left_right_dis = euclidean_distance(image, left, right)
        aspect_ratio = left_right_dis / top_bottom_dis
        return aspect_ratio

    face_mesh = mp.solutions.face_mesh
    STATIC_IMAGE = False
    MAX_NO_FACES = 2
    DETECTION_CONFIDENCE = 0.6
    TRACKING_CONFIDENCE = 0.5
    COLOR_RED = (0, 0, 255)
    COLOR_BLUE = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    LIPS = [
        61,
        146,
        91,
        181,
        84,
        17,
        314,
        405,
        321,
        375,
        291,
        308,
        324,
        318,
        402,
        317,
        14,
        87,
        178,
        88,
        95,
        185,
        40,
        39,
        37,
        0,
        267,
        269,
        270,
        409,
        415,
        310,
        311,
        312,
        13,
        82,
        81,
        42,
        183,
        78,
    ]
    RIGHT_EYE = [
        33,
        7,
        163,
        144,
        145,
        153,
        154,
        155,
        133,
        173,
        157,
        158,
        159,
        160,
        161,
        246,
    ]
    LEFT_EYE = [
        362,
        382,
        381,
        380,
        374,
        373,
        390,
        249,
        263,
        466,
        388,
        387,
        386,
        385,
        384,
        398,
    ]
    LEFT_EYE_TOP_BOTTOM = [386, 374]
    LEFT_EYE_LEFT_RIGHT = [263, 362]
    RIGHT_EYE_TOP_BOTTOM = [159, 145]
    RIGHT_EYE_LEFT_RIGHT = [133, 33]
    UPPER_LOWER_LIPS = [13, 14]
    LEFT_RIGHT_LIPS = [78, 308]
    FACE = [
        10,
        338,
        297,
        332,
        284,
        251,
        389,
        356,
        454,
        323,
        361,
        288,
        397,
        365,
        379,
        378,
        400,
        377,
        152,
        148,
        176,
        149,
        150,
        136,
        172,
        58,
        132,
        93,
        234,
        127,
        162,
        21,
        54,
        103,
        67,
        109,
    ]
    face_model = face_mesh.FaceMesh(
        static_image_mode=STATIC_IMAGE,
        max_num_faces=MAX_NO_FACES,
        min_detection_confidence=DETECTION_CONFIDENCE,
        min_tracking_confidence=TRACKING_CONFIDENCE,
    )
    capture = cv.VideoCapture(0)
    frame_count = 0
    min_frame = 6
    min_tolerance = 5.0
    # capture = cv2.VideoCapture(0)

    while True:
        # with camera_lock:
        # ret, frame = capture.read()

        # if not ret:
        # break

        # Perform drowsiness detection on the frame using drowsiness_app
        # frame = drowsiness_app.start_detection()

        # Display the frame with any overlay or annotations

        # Convert the frame to JPEG format

        result, image = capture.read()
        image = cv.flip(image, 1)
        if result:
            image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            outputs = face_model.process(image_rgb)
            if outputs.multi_face_landmarks:
                draw_landmarks(image, outputs, FACE, COLOR_GREEN)
                draw_landmarks(image, outputs, LEFT_EYE_TOP_BOTTOM, COLOR_RED)
                draw_landmarks(image, outputs, LEFT_EYE_LEFT_RIGHT, COLOR_RED)
                ratio_left = get_aspect_ratio(
                    image, outputs, LEFT_EYE_TOP_BOTTOM, LEFT_EYE_LEFT_RIGHT
                )
                draw_landmarks(image, outputs, RIGHT_EYE_TOP_BOTTOM, COLOR_RED)
                draw_landmarks(image, outputs, RIGHT_EYE_LEFT_RIGHT, COLOR_RED)
                ratio_right = get_aspect_ratio(
                    image, outputs, RIGHT_EYE_TOP_BOTTOM, RIGHT_EYE_LEFT_RIGHT
                )
                ratio = (ratio_left + ratio_right) / 2.0
                if ratio > min_tolerance:
                    frame_count += 1
                else:
                    frame_count = 0
                if frame_count > min_frame:
                    pygame.mixer.music.load(sleep_ringtone_path)
                    print("Sleep")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        continue
                draw_landmarks(image, outputs, UPPER_LOWER_LIPS, COLOR_BLUE)
                draw_landmarks(image, outputs, LEFT_RIGHT_LIPS, COLOR_BLUE)
                ratio_lips = get_aspect_ratio(
                    image, outputs, UPPER_LOWER_LIPS, LEFT_RIGHT_LIPS
                )
                if ratio_lips < 1.8:
                    pygame.mixer.music.load(tired_ringtone_path)
                    print("Tired")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        continue
            # cv.imshow("FACE MESH", image)
            if cv.waitKey(1) & 255 == 27:
                break

        buffer = cv.imencode(".jpg", image)[1]
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

    # Release resources when done
    with camera_lock:
        capture.release()


@app.route("/video")
def video():
    # Initialize the Drowsiness Detection App
    # drowsiness_app = DrowsinessDetectionApp()

    return Response(
        drowsiness_detection(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(debug=True)
