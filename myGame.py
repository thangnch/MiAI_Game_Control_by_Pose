import cv2
import pyautogui
from myPose import myPose

class myGame():
    def __init__(self):
        self.pose = myPose()
        self.game_started = False
        self.x_position = 1 # 0: Ray ben trai, 1: Ray giua, 2: Ray ben phai
        self.y_position = 1 # 0: Down, 1: Stand, 2: jump
        self.clap_duration = 0 # So frame ma ng dung vo tay

    def move_LRC(self, LRC):
        if LRC=="L":
            for _ in range(self.x_position):
                pyautogui.press('left')
            self.x_position = 0
        elif LRC=="R":
            for _ in range(2, self.x_position, -1):
                pyautogui.press('right')
            self.x_position = 2
        else:
            if self.x_position ==0:
                pyautogui.press('right')
            elif self.x_position == 2:
                pyautogui.press('left')

            self.x_position = 1
        return

    def move_JSD(self, JSD):
        if (JSD=="J") and (self.y_position == 1):
            pyautogui.press('up')
            self.y_position = 2
        elif (JSD=="D") and (self.y_position ==1):
            pyautogui.press('down')
            self.y_position = 0
        elif (JSD=="S") and (self.y_position !=1):
            self.y_position = 1
        return

    def play(self):

        # Khoi tao camera
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 960)

        while True:
            ret, image = cap.read()
            if ret:

                image = cv2.flip(image, 1)
                image_height, image_width, _ = image.shape
                image, results = self.pose.detectPose(image)

                if results.pose_landmarks:
                    # Kiem tra game da bat dau chua
                    if self.game_started:
                        # Kiem tra trai phai
                        image, LRC = self.pose.checkPose_LRC(image, results)
                        self.move_LRC(LRC)

                        # Kiem tra len xuong
                        image, JSD = self.pose.checkPose_JSD(image, results)
                        self.move_JSD(JSD)
                    else:
                        cv2.putText(image, "Clap your hand to start!", (5, image_height-10), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 3)

                    image, CLAP = self.pose.checkPose_Clap(image, results)
                    if CLAP == "C":
                        self.clap_duration +=1

                        if self.clap_duration == 10: #10 frame
                            if self.game_started:
                                # Reset
                                self.x_position  = 1
                                self.y_position  = 1
                                self.pose.save_shoulder_line_y(image, results)
                                pyautogui.press('space')
                            else:
                                self.game_started  = True
                                self.pose.save_shoulder_line_y(image, results)
                                pyautogui.click(x=720, y = 560, button = "left")

                            self.clap_duration = 0
                    else:
                        self.clap_duration = 0


                cv2.imshow("Game", image)

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


myGame = myGame()
myGame.play()