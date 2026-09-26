import os
import cv2
from PyQt6.QtCore import QThread, pyqtSignal

class FrameExtractorThread(QThread):
    """
    Worker thread to extract video frames in background without freezing the GUI.
    """
    # Signals
    # progress: (current_frame_extracted, total_frames_to_extract, percent, fps_processing)
    progress = pyqtSignal(int, int, int, float)
    finished = pyqtSignal(int, str)  # (total_extracted, output_directory)
    error = pyqtSignal(str)

    def __init__(self, video_path, output_dir, start_ms, end_ms,
                 image_format="jpg", quality=95, step=1, prefix="frame"):
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir
        self.start_ms = start_ms
        self.end_ms = end_ms
        self.image_format = image_format.lower().replace(".", "")
        self.quality = quality
        self.step = max(1, step)
        self.prefix = prefix or "frame"
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        try:
            if not os.path.exists(self.video_path):
                self.error.emit(f"Le fichier vidéo n'existe pas : {self.video_path}")
                return

            os.makedirs(self.output_dir, exist_ok=True)

            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                self.error.emit("Impossible d'ouvrir la vidéo avec OpenCV.")
                return

            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps <= 0:
                fps = 25.0  # Valeur de secours standard

            total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Calcul des index de frames de début et de fin
            start_frame = int(round((self.start_ms / 1000.0) * fps))
            end_frame = int(round((self.end_ms / 1000.0) * fps))

            start_frame = max(0, min(start_frame, total_video_frames - 1))
            end_frame = max(start_frame, min(end_frame, total_video_frames - 1))

            frames_in_range = (end_frame - start_frame) + 1
            total_to_extract = (frames_in_range + self.step - 1) // self.step

            # Déplacement vers la frame de départ
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            # Paramètres de compression selon le format
            ext = f".{self.image_format}"
            encode_params = []
            if self.image_format in ["jpg", "jpeg"]:
                encode_params = [cv2.IMWRITE_JPEG_QUALITY, int(self.quality)]
            elif self.image_format == "png":
                # Compression PNG de 0 à 9 (3 = bon compromis vitesse/taille)
                encode_params = [cv2.IMWRITE_PNG_COMPRESSION, 3]
            elif self.image_format == "webp":
                encode_params = [cv2.IMWRITE_WEBP_QUALITY, int(self.quality)]

            extracted_count = 0
            current_frame_idx = start_frame

            import time
            start_time = time.time()
            last_signal_time = 0

            # Déterminer la largeur pour le formatage des numéros (ex: 00001)
            digits = max(5, len(str(end_frame + 1)))

            while current_frame_idx <= end_frame and not self._is_cancelled:
                ret, frame = cap.read()
                if not ret:
                    break

                # Sauvegarde selon le step
                if (current_frame_idx - start_frame) % self.step == 0:
                    filename = f"{self.prefix}_{current_frame_idx + 1:0{digits}d}{ext}"
                    filepath = os.path.join(self.output_dir, filename)

                    # Utiliser cv2.imencode + open pour supporter tous les caractères et chemins Windows
                    success, buffer = cv2.imencode(ext, frame, encode_params)
                    if success:
                        with open(filepath, "wb") as f:
                            f.write(buffer)
                        extracted_count += 1
                    else:
                        # Fallback standard
                        cv2.imwrite(filepath, frame, encode_params)
                        extracted_count += 1

                current_frame_idx += 1

                # Notifier périodiquement pour ne pas saturer l'UI
                now = time.time()
                if now - last_signal_time >= 0.05 or current_frame_idx > end_frame:
                    elapsed = now - start_time
                    current_fps = extracted_count / elapsed if elapsed > 0 else 0
                    percent = int((extracted_count / total_to_extract) * 100) if total_to_extract > 0 else 0
                    percent = min(100, percent)
                    self.progress.emit(extracted_count, total_to_extract, percent, current_fps)
                    last_signal_time = now

                # Saut de frames si step > 1
                if self.step > 1 and ((current_frame_idx - start_frame) % self.step != 0):
                    # Trouver la prochaine frame souhaitée
                    next_target = start_frame + (((current_frame_idx - start_frame) // self.step) + 1) * self.step
                    if next_target <= end_frame:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, next_target)
                        current_frame_idx = next_target

            cap.release()

            if self._is_cancelled:
                self.finished.emit(extracted_count, self.output_dir)
            else:
                self.progress.emit(total_to_extract, total_to_extract, 100, 0.0)
                self.finished.emit(extracted_count, self.output_dir)

        except Exception as e:
            self.error.emit(f"Une erreur est survenue lors de l'extraction : {str(e)}")
