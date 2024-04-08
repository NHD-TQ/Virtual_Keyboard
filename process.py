from cvzone.HandTrackingModule import HandDetector
from time import sleep
from button import *

def virtual_keyboard():
    cap = cv2.VideoCapture(0)
    cap.set(3, 2080)
    cap.set(4, 720)
    finalText = ""
    Type = "Typing..."
    detector = HandDetector(detectionCon=0.8)

    list_char = [["1", "2", "3", "4", "RESET"],
                 ["5", "6", "7", "8", "G"],
                 ["Z", "X", "C", "V", "B"]]

    buttonList = []

    # Draw button.
    def drawALL(img, buttonList):
        for button in buttonList:
            if button.text == "RESET":
                x, y = button.pos
                w, h = button.size
                cv2.rectangle(img, button.pos, (x + w + 100, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 25, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)
            else:
                x, y = button.pos
                w, h = button.size
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 25, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 4)

        return img

    # Draw a button on the screen.
    for i in range(len(list_char)):
        for x, key in enumerate(list_char[i]):
            buttonList.append(Button([100 * x + 50, 100 * i + 50], key))

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)

        img = drawALL(img, buttonList)

        if hands:
            hand1 = hands[0]
            lmList = hand1["lmList"]
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                # Check if your finger is within the coordinates of the button?
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    # Get the distance between 2 fingers
                    d, _, _ = detector.findDistance(lmList[8], lmList[12], img)
                    # The distance between 2 fingers is considered as 1 press.
                    if d < 22:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        if button.text == "RESET":
                            finalText = ""
                            Type = "Typing..."
                        sleep(0.4)

            cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
            cv2.putText(img, finalText, (60, 425),
                        cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 2)
        # Check.
        if len(finalText) == 5:
            if finalText == '16XCV':
                Type = "CORRECT !"
            else:
                Type = "INCORRECT !!"


        if Type == "CORRECT !":
            cv2.rectangle(img, (1100, 50), (800, 200), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, Type, (800, 150),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 128, 0), 4)

        elif Type == "INCORRECT !!":
            cv2.rectangle(img, (1100, 50), (800, 200), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, Type, (800, 150),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
        else:
            cv2.rectangle(img, (1100, 50), (800, 200), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, Type, (800, 150),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
