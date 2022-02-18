import mediapipe as mp
import cv2
import math


class myPose():
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.shoudler_line_y = 0  # Luu lai cai vi tri 2 vai cua nguoi dung khi vo tay bat dau game

    def detectPose(self, image):
        # Chuyển RGB
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Lay ket qua dau ra qua model
        results = self.pose.process(imageRGB)

        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image, landmark_list=results.pose_landmarks,
                                           connections=self.mp_pose.POSE_CONNECTIONS,
                                           landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 225, 255),
                                                                                             thickness=3,
                                                                                             circle_radius=3),
                                           connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 0, 255),
                                                                                               thickness=2))

        return image, results

    def checkPose_LRC(self, image, results):

        # Lay kich thuoc anh dau vao
        image_height, image_width, _ = image.shape
        image_mid_width = image_width // 2

        leftShoulder_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width)
        rightShoulder_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width)

        if (leftShoulder_x < image_mid_width) and (rightShoulder_x < image_mid_width):
            LRC = "L"
        elif (leftShoulder_x > image_mid_width) and (rightShoulder_x > image_mid_width):
            LRC = "R"
        else:
            LRC = "C"

        cv2.putText(image, LRC, (5, image_height - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.line(image, (image_mid_width, 0), (image_mid_width, image_height), (255, 255, 255), 2)

        return image, LRC

    def checkPose_JSD(self, image, results):
        image_height, image_width, _ = image.shape

        leftShoulder_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height)
        rightShoulder_y = int(
            results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height)

        centerShoulder_y = abs(leftShoulder_y + rightShoulder_y) // 2

        jump_threshold = 30
        down_threshold = 15

        if (centerShoulder_y < self.shoudler_line_y - jump_threshold):
            JSD = "J"
        elif (centerShoulder_y > self.shoudler_line_y + down_threshold):
            JSD = "D"
        else:
            JSD = "S"

        cv2.putText(image, JSD, (5, image_height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.line(image, (0, self.shoudler_line_y), (image_width, self.shoudler_line_y), (0, 255, 255), 2)

        return image, JSD

    def checkPose_Clap(self, image, results):

        image_height, image_width, _ = image.shape

        left_hand = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].x * image_width,
                     results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y * image_height)

        right_hand = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width,
                      results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height)

        distance = int(math.hypot(left_hand[0] - right_hand[0], left_hand[1] - right_hand[1]))

        clap_threshold = 100
        if distance < clap_threshold:
            CLAP = "C"
        else:
            CLAP = "N"

        cv2.putText(image, CLAP, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)

        return image, CLAP

    def save_shoulder_line_y(self, image, results):
        image_height, image_width, _ = image.shape

        leftShoulder_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height)
        rightShoulder_y = int(
            results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height)

        self.shoudler_line_y = abs(leftShoulder_y + rightShoulder_y) // 2
        return
