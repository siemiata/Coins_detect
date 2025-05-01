# Coins_detect

1. Kalibracja monet przez promień:
   - def classify_coin(radius):
    - if radius <= 40:
    -    if radius > 33:
    -       return '5 zł'
     -   else:
      -      return '5 gr'
  
2. Wczytanie obrazu i wstępna obróbka:
   - original = cv.imread(image_path)
   - gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
   - blur = cv.GaussianBlur(gray, (9, 9), 2)
  
3. Wykrywanie monet przy użyciu HoughCircles:
   - circles = cv.HoughCircles(..., minRadius=10, maxRadius=80)

4. Wykrywanie tacki przy użyciu HoughLines:
   - edges = cv.Canny(...)
   - lines = cv.HoughLinesP(...)

5. Podział monet – na tacy vs poza tacką:
   - if tray_rect and (tray_rect[0] < x < tray_rect[2] and tray_rect[1] < y < tray_rect[3]):
  
6. Zliczanie i wypisywanie wyników:
   - print(f"Na tacy: {on_5gr} monet 5gr i {on_5zl} monet 5zł.")
  
7. Wyświetlenie wyniku:
   - cv.imshow("Coins", original)
