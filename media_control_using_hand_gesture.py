import time
import pyautogui as p
import cv2
import mediapipe as mp

def count_fingers(lst):
    cnt = 0
    
    # thresh value which we calculate by subtracting 0 with 9
    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt += 1

    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 5:
        cnt += 1

    return cnt

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)

start_init = False

prev = -1
pTime = 0

while True:
    end_time = time.time()
    ret, frame = cap.read()
    frame = cv2.resize(frame, (700, 550))
    frame = cv2.flip(frame, 1)

    CTime = time.time()
    fps = 1 / (CTime-pTime)
    pTime = CTime

    frame = cv2.rectangle(frame, (5, 5), (685, 40), (89, 126, 255), -1)
    frame = cv2.putText(frame, "1:forward, 2:backward, 3:vl up, 4:vl down, 5:play/pause", (20, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2, cv2.LINE_AA)
    frame = cv2.rectangle(frame, (5, 45), (190, 80), (255, 222, 125), -1)
    frame = cv2.putText(frame, "your input :", (20, 70), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 0, 255), 2, cv2.LINE_AA)
    frame = cv2.rectangle(frame, (5, 85), (130, 120), (73, 217, 249), -1)
    frame = cv2.putText(frame, f'FPS : {int(fps)}', (20, 110), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2, cv2.LINE_AA)

    res = hand_obj.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:

        hand_keyPoints = res.multi_hand_landmarks[0]
        frame = cv2.putText(frame, " : " + str(count_fingers(hand_keyPoints)), (140, 70), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255, 0, 255), 2, cv2.LINE_AA)

        print(count_fingers(hand_keyPoints))
        cnt = count_fingers(hand_keyPoints)

        if (cnt == 1):
            frame = cv2.rectangle(
                frame, (540, 470), (660, 510), (73, 217, 249), -1)
            frame = cv2.putText(frame, "backward", (548, 495), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2, cv2.LINE_AA)

        elif (cnt == 2):
            frame = cv2.rectangle(
                frame, (540, 470), (640, 510), (73, 217, 249), -1)
            frame = cv2.putText(frame, "forward", (548, 495), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2, cv2.LINE_AA)

        elif (cnt == 3):
            frame = cv2.rectangle(
                frame, (540, 470), (670, 510), (73, 217, 249), -1)
            frame = cv2.putText(frame, "volume up", (548, 495), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2, cv2.LINE_AA)

        elif (cnt == 4):
            frame = cv2.rectangle(
                frame, (540, 470), (695, 510), (73, 217, 249), -1)
            frame = cv2.putText(frame, "volume down", (548, 495), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2, cv2.LINE_AA)

        elif (cnt == 5):
            frame = cv2.rectangle(
                frame, (540, 470), (680, 510), (73, 217, 249), -1)
            frame = cv2.putText(frame, "play/pause", (548, 495), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2, cv2.LINE_AA)

     


        if not (prev == cnt):

            if not (start_init):

                
                start_time = time.time()
                start_init = True

            elif (end_time - start_time) > 0.4:

                if (cnt == 1):
                    p.press("j")
              

                elif (cnt == 2):
                    p.press("l")
                     

                elif (cnt == 3):
                    p.press("up")
                 

                elif (cnt == 4):
                    p.press("down")
                    

                elif (cnt == 5):
                    p.press("space")
               

                prev = cnt
                start_init = False

        drawing.draw_landmarks(
            frame, res.multi_hand_landmarks[0], hands.HAND_CONNECTIONS)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0XFF == 27:

        break



cv2.destroyAllWindows()
cap.release()
