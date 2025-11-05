import cv2
import json
import os

ROI_FILE = "searched.json"

def save_roi(roi):
    """Сохраняет ROI (x, y, w, h) в JSON-файл"""
    with open(ROI_FILE, "w") as f:
        json.dump({"roi": roi}, f)
    print(f"💾 ROI сохранён в файл: {ROI_FILE}")

def load_roi():
    if os.path.exists(ROI_FILE):
        with open(ROI_FILE, "r") as f:
            data = json.load(f)
            return tuple(data["roi"])
    return None

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Не удалось открыть камеру.")
        return

    tracker = cv2.legacy.TrackerKCF_create()

    roi = load_roi()
    if roi:
        print("📂 Загружен сохранённый ROI:", roi)
        ret, frame = cap.read()
        if not ret:
            print("❌ Ошибка чтения кадра.")
            return
        tracker.init(frame, roi)
    else:
        ret, frame = cap.read()
        if not ret:
            print("❌ Ошибка чтения кадра.")
            return

        print("🟩 Выделите объект для отслеживания и нажмите ENTER или SPACE.")
        roi = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        tracker.init(frame, roi)

        save_roi(roi)

    print("🚀 Трекинг запущен. Нажмите 'q' для выхода.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        success, box = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Lost!", (50, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow("KCF Object Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()