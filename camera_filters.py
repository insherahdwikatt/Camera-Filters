import cv2
import numpy as np

def quantize_gray(img, levels):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) / 255.0
    quant = np.floor(gray * levels) / (levels - 1)
    return (quant * 255).astype(np.uint8)

def contrast_eq(img):
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

def soft_polish(img):
    return cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

def cartoon(img, levels):
    smooth = soft_polish(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    quant = quantize_gray(img, levels)
    return cv2.bitwise_and(smooth, edges_colored)

def nothing(x):
    pass

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera", 800, 600)

    # أنشئ trackbars بأسماء أكثر وضوحاً
    cv2.createTrackbar("Mode (1–5)", "Camera", 1, 5, nothing)
    cv2.createTrackbar("Gray Lvls (2–32)", "Camera", 8, 32, nothing)

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Stream ended or cannot fetch frame.")
            break

        mode = cv2.getTrackbarPos("Mode (1–5)", "Camera")
        levels = cv2.getTrackbarPos("Gray Lvls (2–32)", "Camera")
        levels = max(levels, 2)

        if mode == 1:
            proc = cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 100, 200)
        elif mode == 2:
            proc = quantize_gray(frame, levels)
        elif mode == 3:
            proc = contrast_eq(frame)
        elif mode == 4:
            proc = soft_polish(frame)
        elif mode == 5:
            proc = cartoon(frame, levels)
        else:
            proc = frame


        display = proc.copy()
        cv2.putText(display, f"Mode: {mode}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(display, f"Gray Lvls: {levels}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

        cv2.imshow("Camera", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
