"""
Authors: Mateusz Budzyński, Igor Gutowski
dependencies:
    pip install opencv-python
"""

import cv2
import numpy as np

def detect_flags_on_video(video_path):
    # Załadowanie pliku wideo
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Konwersja kolorów z BGR na HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Zakresy kolorów flag
        lower_red_poland = np.array([160, 100, 100])
        upper_red_poland = np.array([180, 255, 255])

        lower_red_russia = np.array([100, 100, 100])
        upper_red_russia = np.array([120, 255, 255])

        lower_yellow_ukraine = np.array([20, 50, 50])
        upper_yellow_ukraine = np.array([40, 255, 255])

        # Stworzenie masek kolorów
        mask_poland = cv2.inRange(hsv_frame, lower_red_poland, upper_red_poland)
        mask_russia = cv2.inRange(hsv_frame, lower_red_russia, upper_red_russia)
        mask_ukraine = cv2.inRange(hsv_frame, lower_yellow_ukraine, upper_yellow_ukraine)

        total_mask = mask_poland + mask_russia + mask_ukraine

        # Usunięcie szumów
        kernel = np.ones((5, 5), np.uint8)
        total_mask = cv2.morphologyEx(total_mask, cv2.MORPH_OPEN, kernel)

        # Znalezienie konturów
        contours, _ = cv2.findContours(total_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Rysowanie prostokątów wokół konturów
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            flag_info = "Flaga: "
            if cv2.contourArea(contour) > 500:  # Filtrowanie małych konturów
                if np.any(mask_ukraine[y:y+h, x:x+w]):
                    flag_info += "Ukraina"
                elif np.any(mask_russia[y:y+h, x:x+w]):
                    flag_info += "Rosja"
                elif np.any(mask_poland[y:y+h, x:x+w]):
                    flag_info += "Polska"

                # Wyświetlenie informacji o flagach
                flag_position = "Pozycja: X={}, Y={}, Szerokosc={}, Wysokosc={}".format(x, y, w, h)
                cv2.putText(frame, flag_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, flag_position, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Detekcja flag', frame)
        if cv2.waitKey(20) & 0xFF == 27:  # Przerwanie po naciśnięciu klawisza Esc
            break

    cap.release()
    cv2.destroyAllWindows()


detect_flags_on_video('flags.mp4')