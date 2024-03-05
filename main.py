'''
pip install pycaw
'''

import cv2
from hand_tracking_module import HandTracking
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
detector = HandTracking()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]
vol = -30

while True:
    _, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=False)

    # new code
    if lm_list is not None:
        finger_statu = detector.which_finger_up(img)
        if finger_statu == [0, 1, 0, 0, 0]:
            if lm_list[8][1] >= lm_list[5][1]:
                vol += 1
            elif lm_list[8][1] < lm_list[5][1]:
                vol -= 1
    if vol > max_vol:
        vol = 0
    elif vol < min_vol:
        vol = -65

    volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    ########################################################
    # old code
    # if lm_list is not None:
    # x1, y1 = lm_list[4][1], lm_list[4][2]
    # x2, y2 = lm_list[8][1], lm_list[8][2]
    # cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    #
    # cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
    # cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
    # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    # cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    #
    # length = math.hypot(x2 - x1, y2 - y1)
    #
    # vol = np.interp(length, [20, 130], [min_vol, max_vol])
    # if length > 130 or length < 20:
    #     cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)
    # volume.SetMasterVolumeLevel(vol, None)
    ########################################################
