import cv2 as cv
import numpy as np
import os

#tutaj kalibracja na podstawie rozmiaru monety
def classify_coin(radius):
    if radius <= 40:
        if radius > 33:
            return '5 zł'
        else:
            return '5 gr'

def detect_coins_and_tray(image_path):
    original = cv.imread(image_path)
    gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9, 9), 2)

    circles = cv.HoughCircles(
        blur,
        cv.HOUGH_GRADIENT,
        dp=1.2,
        minDist=60,
        param1=100,
        param2=40,
        minRadius=10,
        maxRadius=80
    )

    coins = []
    if circles is not None:
        circles = np.uint16(np.around(circles[0]))
        for (x, y, r) in circles:
            coin_type = classify_coin(r)
            coins.append((x, y, r, coin_type))
            color = (0, 255, 255) if coin_type == '5 gr' else (0, 0, 255)
            cv.circle(original, (x, y), r, color, 3)
            label = f"{coin_type} ({r})"
            cv.putText(original, label, (x - 30, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv.circle(original, (x, y), 2, (255, 255, 255), 2)

    edges = cv.Canny(blur, 50, 150, apertureSize=3)
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    tray_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            tray_lines.append(((x1, y1), (x2, y2)))
            cv.line(original, (x1, y1), (x2, y2), (255, 0, 0), 2)

    if tray_lines:
        points = np.array([pt for line in tray_lines for pt in line])
        x, y, w, h = cv.boundingRect(points)
        tray_rect = (x, y, x + w, y + h)
        cv.rectangle(original, (x, y), (x + w, y + h), (0, 255, 255), 2)
    else:
        tray_rect = None

    coins_on_tray = []
    coins_off_tray = []
    for (x, y, r, coin_type) in coins:
        if tray_rect and (tray_rect[0] < x < tray_rect[2] and tray_rect[1] < y < tray_rect[3]):
            coins_on_tray.append((x, y, r, coin_type))
        else:
            coins_off_tray.append((x, y, r, coin_type))

    def count_by_type(coin_list):
        count_5zl = sum(1 for c in coin_list if c[3] == '5 zł')
        count_5gr = sum(1 for c in coin_list if c[3] == '5 gr')
        return count_5gr, count_5zl

    on_5gr, on_5zl = count_by_type(coins_on_tray)
    off_5gr, off_5zl = count_by_type(coins_off_tray)

    print(f"Na tacy: {on_5gr} monet 5gr i {on_5zl} monet 5zł.")
    print(f"Poza tacą: {off_5gr} monet 5gr i {off_5zl} monet 5zł.")
    print('-' * 50)

    cv.imshow("Coins", original)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    image_path = "zdjecia/tray1.jpg"
    detect_coins_and_tray(image_path)