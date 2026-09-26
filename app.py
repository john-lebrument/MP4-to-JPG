import sys
import os
import cv2

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QComboBox, QSlider, QSpinBox,
    QProgressBar, QGroupBox, QLineEdit, QMessageBox, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt, QUrl, QTime, pyqtSignal, QSettings
from PyQt6.QtGui import QIcon, QFont, QKeySequence, QShortcut, QDragEnterEvent, QDropEvent, QPainter, QColor, QPen
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

from timeline_slider import TimelineSlider
from extractor import FrameExtractorThread


DARK_STYLE = """
    QMainWindow {
        background-color: #1a1b1e;
    }
    QWidget {
        color: #e4e7eb;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
    }
    QGroupBox {
        border: 1px solid #2e3440;
        border-radius: 8px;
        margin-top: 10px;
        padding: 12px;
        font-weight: bold;
        background-color: #202227;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 5px;
        color: #5dade2;
    }
    QPushButton {
        background-color: #2e3440;
        border: 1px solid #3b4252;
        border-radius: 6px;
        padding: 7px 14px;
        font-weight: 500;
        color: #e4e7eb;
    }
    QPushButton:hover {
        background-color: #3b4252;
        border-color: #4c566a;
    }
    QPushButton:pressed {
        background-color: #434c5e;
    }
    QPushButton#primaryBtn {
        background-color: #0078d4;
        border-color: #0063b1;
        font-size: 14px;
        font-weight: bold;
        color: #ffffff;
        padding: 10px 20px;
    }
    QPushButton#primaryBtn:hover {
        background-color: #1084d9;
    }
    QPushButton#primaryBtn:disabled {
        background-color: #2a3b4c;
        color: #6c7d8f;
        border-color: #2a3b4c;
    }
    QPushButton#inBtn {
        background-color: #1b4332;
        border-color: #2d6a4f;
        color: #74c69d;
        font-weight: bold;
    }
    QPushButton#inBtn:hover {
        background-color: #2d6a4f;
        color: #d8f3dc;
    }
    QPushButton#outBtn {
        background-color: #49111c;
        border-color: #800f2f;
        color: #ff758f;
        font-weight: bold;
    }
    QPushButton#outBtn:hover {
        background-color: #800f2f;
        color: #ffccd5;
    }
    QPushButton#themeBtn {
        background-color: #2e3440;
        border: 1px solid #4c566a;
        font-weight: bold;
        color: #f1c40f;
    }
    QPushButton#themeBtn:hover {
        background-color: #3b4252;
    }
    QPushButton#closeVideoBtn {
        background-color: #3b2024;
        border: 1px solid #5c2c33;
        color: #fca5a5;
        font-weight: 500;
    }
    QPushButton#closeVideoBtn:hover {
        background-color: #5c2c33;
        color: #fee2e2;
    }
    QPushButton#closeVideoBtn:disabled {
        background-color: #252830;
        border-color: #323642;
        color: #555b6e;
    }
    QLineEdit, QComboBox, QSpinBox {
        background-color: #16181d;
        border: 1px solid #3b4252;
        border-radius: 5px;
        padding: 5px 8px;
        color: #eceff4;
    }
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
        border-color: #0078d4;
    }
    QProgressBar {
        border: 1px solid #2e3440;
        border-radius: 6px;
        background-color: #16181d;
        text-align: center;
        color: #ffffff;
        font-weight: bold;
        height: 22px;
    }
    QProgressBar::chunk {
        background-color: #0078d4;
        border-radius: 5px;
    }
    QMessageBox {
        background-color: #202227;
    }
    QMessageBox QLabel {
        color: #e4e7eb;
        background-color: transparent;
        font-size: 13px;
    }
    QMessageBox QPushButton {
        background-color: #2e3440;
        border: 1px solid #3b4252;
        border-radius: 6px;
        padding: 7px 16px;
        color: #e4e7eb;
        font-weight: bold;
    }
    QMessageBox QPushButton:hover {
        background-color: #3b4252;
    }
"""

LIGHT_STYLE = """
    QMainWindow {
        background-color: #f1f5f9;
    }
    QWidget {
        color: #1e293b;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
    }
    QGroupBox {
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        margin-top: 10px;
        padding: 12px;
        font-weight: bold;
        background-color: #ffffff;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 5px;
        color: #0284c7;
    }
    QPushButton {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 7px 14px;
        font-weight: 500;
        color: #1e293b;
    }
    QPushButton:hover {
        background-color: #e2e8f0;
        border-color: #94a3b8;
    }
    QPushButton:pressed {
        background-color: #cbd5e1;
    }
    QPushButton#primaryBtn {
        background-color: #0284c7;
        border-color: #0369a1;
        font-size: 14px;
        font-weight: bold;
        color: #ffffff;
        padding: 10px 20px;
    }
    QPushButton#primaryBtn:hover {
        background-color: #0369a1;
    }
    QPushButton#primaryBtn:disabled {
        background-color: #94a3b8;
        color: #f1f5f9;
        border-color: #94a3b8;
    }
    QPushButton#inBtn {
        background-color: #dcfce7;
        border-color: #86efac;
        color: #15803d;
        font-weight: bold;
    }
    QPushButton#inBtn:hover {
        background-color: #bbf7d0;
    }
    QPushButton#outBtn {
        background-color: #ffe4e6;
        border-color: #fca5a5;
        color: #b91c1c;
        font-weight: bold;
    }
    QPushButton#outBtn:hover {
        background-color: #fecdd3;
    }
    QPushButton#themeBtn {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        font-weight: bold;
        color: #334155;
    }
    QPushButton#themeBtn:hover {
        background-color: #e2e8f0;
    }
    QPushButton#closeVideoBtn {
        background-color: #fee2e2;
        border: 1px solid #fca5a5;
        color: #991b1b;
        font-weight: 500;
    }
    QPushButton#closeVideoBtn:hover {
        background-color: #fecdd3;
    }
    QPushButton#closeVideoBtn:disabled {
        background-color: #f1f5f9;
        border-color: #e2e8f0;
        color: #94a3b8;
    }
    QLineEdit, QComboBox, QSpinBox {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 5px;
        padding: 5px 8px;
        color: #0f172a;
    }
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
        border-color: #0284c7;
    }
    QProgressBar {
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        background-color: #e2e8f0;
        text-align: center;
        color: #0f172a;
        font-weight: bold;
        height: 22px;
    }
    QProgressBar::chunk {
        background-color: #0284c7;
        border-radius: 5px;
    }
    QMessageBox {
        background-color: #ffffff;
    }
    QMessageBox QLabel {
        color: #0f172a;
        background-color: transparent;
        font-size: 13px;
    }
    QMessageBox QPushButton {
        background-color: #0284c7;
        border: 1px solid #0369a1;
        border-radius: 6px;
        padding: 7px 16px;
        color: #ffffff;
        font-weight: bold;
    }
    QMessageBox QPushButton:hover {
        background-color: #0369a1;
    }
"""


class DropPlaceholderWidget(QFrame):
    """Zone d'accueil visuelle cliquable et supportant le Drag & Drop"""
    clicked = pyqtSignal()
    fileDropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._is_dark = False
        self._is_hovered = False

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        self.icon_label = QLabel("🎬")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 52px;")
        layout.addWidget(self.icon_label)

        self.title_label = QLabel("Glissez-déposez votre vidéo ici")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 17px; font-weight: bold;")
        layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("ou cliquez pour parcourir (MP4, MKV, MOV, AVI, WEBM...)")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.subtitle_label)

    def update_theme(self, is_dark: bool):
        self._is_dark = is_dark
        if self._is_hovered:
            self.setStyleSheet("border: 2px dashed #0078d4; background-color: rgba(0, 120, 212, 0.15); border-radius: 10px;")
        elif is_dark:
            self.setStyleSheet("border: 2px dashed #3b4252; background-color: #181a1f; border-radius: 10px;")
            self.title_label.setStyleSheet("font-size: 17px; font-weight: bold; color: #e4e7eb;")
            self.subtitle_label.setStyleSheet("font-size: 13px; color: #8892b0;")
        else:
            self.setStyleSheet("border: 2px dashed #94a3b8; background-color: #ffffff; border-radius: 10px;")
            self.title_label.setStyleSheet("font-size: 17px; font-weight: bold; color: #1e293b;")
            self.subtitle_label.setStyleSheet("font-size: 13px; color: #64748b;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                ext = os.path.splitext(url.toLocalFile())[1].lower()
                if ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"]:
                    event.acceptProposedAction()
                    self._is_hovered = True
                    self.update_theme(self._is_dark)
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self._is_hovered = False
        self.update_theme(self._is_dark)

    def dropEvent(self, event: QDropEvent):
        self._is_hovered = False
        self.update_theme(self._is_dark)
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path and os.path.isfile(path):
                ext = os.path.splitext(path)[1].lower()
                if ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"]:
                    self.fileDropped.emit(path)
                    event.acceptProposedAction()
                    return


class VideoOverlay(QWidget):
    """
    Couche transparente placée au-dessus du QVideoWidget pour intercepter de manière 100% fiable
    les événements Drag & Drop sous Windows (qui sont sinon interceptés par la fenêtre native DirectShow/MediaFoundation)
    """
    fileDropped = pyqtSignal(str)
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._is_dragging = False

    def paintEvent(self, event):
        if self._is_dragging:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor(0, 150, 255), 4, Qt.PenStyle.DashLine))
            painter.setBrush(QColor(0, 150, 255, 45))
            painter.drawRoundedRect(6, 6, self.width() - 12, self.height() - 12, 10, 10)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                ext = os.path.splitext(url.toLocalFile())[1].lower()
                if ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"]:
                    event.acceptProposedAction()
                    self._is_dragging = True
                    self.update()
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._is_dragging = False
        self.update()

    def dropEvent(self, event: QDropEvent):
        self._is_dragging = False
        self.update()
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path and os.path.isfile(path):
                ext = os.path.splitext(path)[1].lower()
                if ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"]:
                    self.fileDropped.emit(path)
                    event.acceptProposedAction()
                    return
        event.ignore()


class VideoPlayerContainer(QWidget):
    """Conteneur combinant le QVideoWidget et la couche de capture de Drag & Drop"""
    fileDropped = pyqtSignal(str)
    videoClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.video_widget = QVideoWidget(self)
        self.video_widget.setStyleSheet("background-color: #000000; border-radius: 8px;")

        self.overlay = VideoOverlay(self)
        self.overlay.fileDropped.connect(self.fileDropped)
        self.overlay.clicked.connect(self.videoClicked)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.video_widget.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setGeometry(0, 0, self.width(), self.height())


def resource_path(relative_path: str) -> str:
    """Obtient le chemin absolu des ressources, compatible avec le mode script et le mode .exe (PyInstaller)"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def format_ms(ms: int) -> str:
    """Format milliseconds into HH:MM:SS.mmm"""
    if ms < 0:
        ms = 0
    total_seconds = ms // 1000
    milliseconds = ms % 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


class VideoExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP4 to Images Studio - Découpe & Extraction")
        self.resize(1100, 850)
        self.setMinimumSize(850, 680)
        self.setAcceptDrops(True)

        self.current_video_path = ""
        self.video_fps = 30.0
        self.video_total_frames = 0
        self.video_width = 0
        self.video_height = 0
        self.video_duration_ms = 0
        
        # 1. Thème par défaut en CLAIR (False = Light, True = Dark)
        self.is_dark_mode = False

        # 2. Gestion et persistance du dossier de sortie choisi par l'utilisateur
        self.settings = QSettings("MP4toImagesStudio", "Settings")
        self.base_output_dir = self.settings.value("base_output_dir", "")

        self.extractor_thread = None

        # Configuration de l'icône de l'application
        self.icon_path = resource_path("icon.png")
        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path))

        self._init_player()
        self._init_ui()
        self._setup_shortcuts()
        self._apply_theme()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self._apply_theme()

    def _apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(DARK_STYLE)
            self.btn_theme.setText("☀️ Mode Clair")
            self.btn_theme.setToolTip("Basculer vers le mode clair")
            self.lbl_timecode.setStyleSheet("font-family: Consolas, monospace; font-size: 14px; font-weight: bold; color: #61afef;")
            self.lbl_sequence_info.setStyleSheet("color: #98c379; font-weight: 500; padding: 3px 0;")
            self.lbl_dimensions.setStyleSheet("color: #a0aec0; font-weight: 500;")
            if not self.current_video_path:
                self.lbl_file_info.setStyleSheet("color: #8892b0; font-style: italic;")
            else:
                self.lbl_file_info.setStyleSheet("color: #e4e7eb; font-weight: bold;")
        else:
            self.setStyleSheet(LIGHT_STYLE)
            self.btn_theme.setText("🌙 Mode Sombre")
            self.btn_theme.setToolTip("Basculer vers le mode sombre")
            self.lbl_timecode.setStyleSheet("font-family: Consolas, monospace; font-size: 14px; font-weight: bold; color: #0284c7;")
            self.lbl_sequence_info.setStyleSheet("color: #15803d; font-weight: 500; padding: 3px 0;")
            self.lbl_dimensions.setStyleSheet("color: #475569; font-weight: 500;")
            if not self.current_video_path:
                self.lbl_file_info.setStyleSheet("color: #64748b; font-style: italic;")
            else:
                self.lbl_file_info.setStyleSheet("color: #1e293b; font-weight: bold;")

        self.timeline.setDarkMode(self.is_dark_mode)
        self.drop_placeholder.update_theme(self.is_dark_mode)

    def _init_player(self):
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        self.player.positionChanged.connect(self._on_player_position_changed)
        self.player.durationChanged.connect(self._on_player_duration_changed)
        self.player.playbackStateChanged.connect(self._on_playback_state_changed)

    def _init_ui(self):
        central_widget = QWidget(self)
        central_widget.setAcceptDrops(True)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        # 1. Top Bar: Open button + Unload button + File info + Theme switch
        top_bar = QHBoxLayout()
        self.btn_open = QPushButton("📂 Ouvrir une vidéo...")
        self.btn_open.clicked.connect(self.choose_video_file)
        top_bar.addWidget(self.btn_open)

        self.btn_close_video = QPushButton("❌ Décharger la vidéo")
        self.btn_close_video.setObjectName("closeVideoBtn")
        self.btn_close_video.setToolTip("Décharger la vidéo actuelle et libérer le fichier pour pouvoir le supprimer ou le déplacer")
        self.btn_close_video.setEnabled(False)
        self.btn_close_video.clicked.connect(self.unload_video)
        top_bar.addWidget(self.btn_close_video)

        self.lbl_file_info = QLabel("Aucun fichier sélectionné (Glissez-déposez une vidéo ici)")
        top_bar.addWidget(self.lbl_file_info, stretch=1)

        self.lbl_dimensions = QLabel("")
        top_bar.addWidget(self.lbl_dimensions)

        self.btn_theme = QPushButton("🌙 Mode Sombre")
        self.btn_theme.setObjectName("themeBtn")
        self.btn_theme.setFixedWidth(120)
        self.btn_theme.clicked.connect(self.toggle_theme)
        top_bar.addWidget(self.btn_theme)

        main_layout.addLayout(top_bar)

        # 2. Video Preview Area (Stack with Placeholder & VideoContainer)
        self.video_stack = QStackedWidget(self)
        self.video_stack.setMinimumHeight(320)

        self.drop_placeholder = DropPlaceholderWidget(self)
        self.drop_placeholder.clicked.connect(self.choose_video_file)
        self.drop_placeholder.fileDropped.connect(self.load_video)
        self.video_stack.addWidget(self.drop_placeholder)

        self.video_container = VideoPlayerContainer(self)
        self.video_container.fileDropped.connect(self.load_video)
        self.video_container.videoClicked.connect(self.toggle_play_pause)
        self.player.setVideoOutput(self.video_container.video_widget)
        self.video_stack.addWidget(self.video_container)

        self.video_stack.setCurrentIndex(0)
        main_layout.addWidget(self.video_stack, stretch=1)

        # 3. Interactive Timeline Bar
        self.timeline = TimelineSlider(self)
        self.timeline.positionChanged.connect(self._on_timeline_seek)
        self.timeline.markerInChanged.connect(self._on_marker_in_changed)
        self.timeline.markerOutChanged.connect(self._on_marker_out_changed)
        main_layout.addWidget(self.timeline)

        # 4. Player Controls & Marker Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        self.btn_prev_frame = QPushButton("⏮ -1 trame")
        self.btn_prev_frame.setToolTip("Reculer d'une trame (Touche Gauche)")
        self.btn_prev_frame.clicked.connect(self.step_frame_backward)
        controls_layout.addWidget(self.btn_prev_frame)

        self.btn_play_pause = QPushButton("▶ Lecture")
        self.btn_play_pause.setToolTip("Lire / Mettre en pause (Espace ou clic vidéo)")
        self.btn_play_pause.clicked.connect(self.toggle_play_pause)
        self.btn_play_pause.setFixedWidth(110)
        controls_layout.addWidget(self.btn_play_pause)

        self.btn_next_frame = QPushButton("⏭ +1 trame")
        self.btn_next_frame.setToolTip("Avancer d'une trame (Touche Droite)")
        self.btn_next_frame.clicked.connect(self.step_frame_forward)
        controls_layout.addWidget(self.btn_next_frame)

        # Separator line
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Sunken)
        v_line.setStyleSheet("color: #3b4252;")
        controls_layout.addWidget(v_line)

        # Marker In / Out Buttons
        self.btn_set_in = QPushButton("📍 Début [In] (I)")
        self.btn_set_in.setObjectName("inBtn")
        self.btn_set_in.setToolTip("Définir le début de la séquence à extraire")
        self.btn_set_in.clicked.connect(self.set_current_as_in)
        controls_layout.addWidget(self.btn_set_in)

        self.btn_set_out = QPushButton("🏁 Fin [Out] (O)")
        self.btn_set_out.setObjectName("outBtn")
        self.btn_set_out.setToolTip("Définir la fin de la séquence à extraire")
        self.btn_set_out.clicked.connect(self.set_current_as_out)
        controls_layout.addWidget(self.btn_set_out)

        self.btn_reset_selection = QPushButton("🔄 Toute la vidéo")
        self.btn_reset_selection.setToolTip("Réinitialiser les marqueurs pour extraire toute la vidéo")
        self.btn_reset_selection.clicked.connect(self.reset_markers)
        controls_layout.addWidget(self.btn_reset_selection)

        controls_layout.addStretch(1)

        # Timecode display
        self.lbl_timecode = QLabel("00:00:00.000 / 00:00:00.000")
        self.lbl_timecode.setStyleSheet("font-family: Consolas, monospace; font-size: 14px; font-weight: bold; color: #0284c7;")
        controls_layout.addWidget(self.lbl_timecode)

        main_layout.addLayout(controls_layout)

        # Sequence info summary banner
        self.lbl_sequence_info = QLabel("Séquence sélectionnée : Du début à la fin (0 image)")
        self.lbl_sequence_info.setStyleSheet("color: #15803d; font-weight: 500; padding: 3px 0;")
        main_layout.addWidget(self.lbl_sequence_info)

        # 5. Export Settings Box
        export_box = QGroupBox("Options d'extraction")
        export_layout = QVBoxLayout(export_box)

        # Row 1: Output directory
        dir_row = QHBoxLayout()
        dir_row.addWidget(QLabel("Dossier de sortie :"))
        self.txt_output_dir = QLineEdit()
        self.txt_output_dir.setPlaceholderText("Sélectionnez le dossier où enregistrer les images...")
        dir_row.addWidget(self.txt_output_dir, stretch=1)

        self.btn_browse_dir = QPushButton("Parcourir...")
        self.btn_browse_dir.clicked.connect(self.choose_output_dir)
        dir_row.addWidget(self.btn_browse_dir)

        self.btn_open_output_dir = QPushButton("📂 Ouvrir dossier")
        self.btn_open_output_dir.setToolTip("Ouvrir le dossier dans l'Explorateur Windows")
        self.btn_open_output_dir.clicked.connect(self.open_output_folder)
        dir_row.addWidget(self.btn_open_output_dir)
        export_layout.addLayout(dir_row)

        # Row 2: Format, Quality, Step, Prefix
        opts_row = QHBoxLayout()
        opts_row.setSpacing(14)

        # Image format
        opts_row.addWidget(QLabel("Format d'image :"))
        self.combo_format = QComboBox()
        self.combo_format.addItems(["JPG (.jpg)", "PNG (.png)", "WEBP (.webp)", "BMP (.bmp)"])
        self.combo_format.currentIndexChanged.connect(self._on_format_changed)
        opts_row.addWidget(self.combo_format)

        # Quality slider (for JPG/WEBP)
        self.lbl_quality = QLabel("Qualité (95%) :")
        opts_row.addWidget(self.lbl_quality)
        self.slider_quality = QSlider(Qt.Orientation.Horizontal)
        self.slider_quality.setRange(10, 100)
        self.slider_quality.setValue(95)
        self.slider_quality.setFixedWidth(110)
        self.slider_quality.valueChanged.connect(self._on_quality_changed)
        opts_row.addWidget(self.slider_quality)

        # Step / Frequency
        opts_row.addWidget(QLabel("Cadence :"))
        self.combo_step = QComboBox()
        self.combo_step.addItem("Toutes les images (100%)", 1)
        self.combo_step.addItem("1 image sur 2", 2)
        self.combo_step.addItem("1 image sur 5", 5)
        self.combo_step.addItem("1 image sur 10", 10)
        self.combo_step.addItem("1 image par seconde", "1s")
        self.combo_step.currentIndexChanged.connect(self._update_sequence_info)
        opts_row.addWidget(self.combo_step)

        # Prefix
        opts_row.addWidget(QLabel("Préfixe nom :"))
        self.txt_prefix = QLineEdit("frame")
        self.txt_prefix.setFixedWidth(90)
        opts_row.addWidget(self.txt_prefix)

        opts_row.addStretch(1)
        export_layout.addLayout(opts_row)

        main_layout.addWidget(export_box)

        # 6. Extraction Action & Progress Bar
        action_layout = QHBoxLayout()
        self.btn_extract = QPushButton("🚀 Extraire les images")
        self.btn_extract.setObjectName("primaryBtn")
        self.btn_extract.clicked.connect(self.start_extraction)
        action_layout.addWidget(self.btn_extract)

        self.btn_cancel = QPushButton("⏹ Annuler")
        self.btn_cancel.setStyleSheet("background-color: #800f2f; color: white;")
        self.btn_cancel.setVisible(False)
        self.btn_cancel.clicked.connect(self.cancel_extraction)
        action_layout.addWidget(self.btn_cancel)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        action_layout.addWidget(self.progress_bar, stretch=1)

        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("color: #e5c07b; font-weight: 500;")
        action_layout.addWidget(self.lbl_status)

        main_layout.addLayout(action_layout)

    def _setup_shortcuts(self):
        # Space: Play/Pause
        shortcut_space = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        shortcut_space.activated.connect(self.toggle_play_pause)

        # Left / Right: step frames
        shortcut_left = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        shortcut_left.activated.connect(self.step_frame_backward)

        shortcut_right = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        shortcut_right.activated.connect(self.step_frame_forward)

        # I: Marker In
        shortcut_in = QShortcut(QKeySequence(Qt.Key.Key_I), self)
        shortcut_in.activated.connect(self.set_current_as_in)

        # O: Marker Out
        shortcut_out = QShortcut(QKeySequence(Qt.Key.Key_O), self)
        shortcut_out.activated.connect(self.set_current_as_out)

    # Drag and Drop support on main window
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                ext = os.path.splitext(url.toLocalFile())[1].lower()
                if ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"]:
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path and os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"]:
                    self.load_video(file_path)
                    event.acceptProposedAction()
                    return
        event.ignore()

    def choose_video_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une vidéo",
            "",
            "Vidéos (*.mp4 *.mov *.avi *.mkv *.wmv *.webm *.m4v);;Tous les fichiers (*.*)"
        )
        if file_path:
            self.load_video(file_path)

    def update_output_path(self):
        """Met à jour le champ de dossier de sortie en créant automatiquement un sous-dossier au nom de la vidéo"""
        if not self.current_video_path:
            return

        filename = os.path.basename(self.current_video_path)
        base_name = os.path.splitext(filename)[0]

        # Utiliser le dossier de base choisi par l'utilisateur s'il existe, sinon le dossier de la vidéo
        if self.base_output_dir and os.path.isdir(self.base_output_dir):
            parent_dir = self.base_output_dir
        else:
            parent_dir = os.path.dirname(self.current_video_path)

        # Chaque vidéo a son propre sous-dossier dédié
        target_dir = os.path.join(parent_dir, f"{base_name}_images")
        self.txt_output_dir.setText(target_dir)

    def choose_output_dir(self):
        """Permet à l'utilisateur d'indiquer un dossier parent de sortie, et le conserve pour tous les traitements"""
        start_dir = self.base_output_dir if (self.base_output_dir and os.path.isdir(self.base_output_dir)) else ""
        if not start_dir and self.current_video_path:
            start_dir = os.path.dirname(self.current_video_path)

        chosen_dir = QFileDialog.getExistingDirectory(self, "Choisir le dossier racine de sortie", start_dir)
        if chosen_dir:
            self.base_output_dir = chosen_dir
            self.settings.setValue("base_output_dir", self.base_output_dir)
            self.update_output_path()

    def load_video(self, file_path: str):
        if not os.path.isfile(file_path):
            QMessageBox.critical(self, "Erreur", f"Le fichier est introuvable : {file_path}")
            return

        # 1. Déverrouiller et libérer immédiatement l'ancienne vidéo
        if self.player:
            self.player.stop()
            self.player.setSource(QUrl())

        self.current_video_path = file_path
        filename = os.path.basename(file_path)
        self.lbl_file_info.setText(f"{filename}")
        if self.is_dark_mode:
            self.lbl_file_info.setStyleSheet("color: #e4e7eb; font-weight: bold;")
        else:
            self.lbl_file_info.setStyleSheet("color: #1e293b; font-weight: bold;")

        # Afficher le lecteur vidéo dans le stack
        self.video_stack.setCurrentIndex(1)
        self.btn_close_video.setEnabled(True)

        # Read metadata via OpenCV
        cap = cv2.VideoCapture(file_path)
        if cap.isOpened():
            self.video_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            self.video_total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()

            self.lbl_dimensions.setText(
                f"📐 {self.video_width}x{self.video_height} | 🎞️ {self.video_fps:.2f} fps | {self.video_total_frames} images"
            )
        else:
            self.video_fps = 25.0
            self.lbl_dimensions.setText("")

        # Mise à jour automatique du dossier de sortie avec le nom de la vidéo
        self.update_output_path()

        # Set media in player
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.player.pause()

    def unload_video(self):
        """Décharge la vidéo en cours, libère complètement le fichier sous Windows et réinitialise l'application"""
        if self.player:
            self.player.stop()
            self.player.setSource(QUrl())

        self.current_video_path = ""
        self.video_duration_ms = 0
        self.video_fps = 25.0
        self.video_total_frames = 0
        self.video_width = 0
        self.video_height = 0

        self.timeline.setDuration(1000)
        self.timeline.resetMarkers()

        self.lbl_dimensions.setText("")
        self.lbl_timecode.setText("00:00:00.000 / 00:00:00.000")
        self.lbl_sequence_info.setText("Séquence sélectionnée : Du début à la fin (0 image)")
        self.lbl_file_info.setText("Aucun fichier sélectionné (Glissez-déposez une vidéo ici)")
        if self.is_dark_mode:
            self.lbl_file_info.setStyleSheet("color: #8892b0; font-style: italic;")
        else:
            self.lbl_file_info.setStyleSheet("color: #64748b; font-style: italic;")

        self.btn_close_video.setEnabled(False)
        self.btn_play_pause.setText("▶ Lecture")
        self.progress_bar.setVisible(False)
        self.lbl_status.setText("")

        # Revenir à la vue initiale avec la zone de glisser-déposer
        self.video_stack.setCurrentIndex(0)

    def _on_player_duration_changed(self, duration_ms: int):
        self.video_duration_ms = duration_ms
        self.timeline.setDuration(duration_ms)
        self._update_timecode_display()
        self._update_sequence_info()

    def _on_player_position_changed(self, position_ms: int):
        self.timeline.setPosition(position_ms)
        self._update_timecode_display()

    def _on_playback_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.btn_play_pause.setText("⏸ Pause")
        else:
            self.btn_play_pause.setText("▶ Lecture")

    def toggle_play_pause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def _on_timeline_seek(self, position_ms: int):
        self.player.setPosition(position_ms)

    def step_frame_forward(self):
        if self.video_fps <= 0:
            return
        frame_duration = 1000.0 / self.video_fps
        new_pos = int(self.player.position() + frame_duration)
        self.player.pause()
        self.player.setPosition(min(self.video_duration_ms, new_pos))

    def step_frame_backward(self):
        if self.video_fps <= 0:
            return
        frame_duration = 1000.0 / self.video_fps
        new_pos = int(self.player.position() - frame_duration)
        self.player.pause()
        self.player.setPosition(max(0, new_pos))

    def set_current_as_in(self):
        curr = self.player.position()
        self.timeline.setMarkerIn(curr)

    def set_current_as_out(self):
        curr = self.player.position()
        self.timeline.setMarkerOut(curr)

    def reset_markers(self):
        self.timeline.resetMarkers()

    def _on_marker_in_changed(self, in_ms: int):
        self._update_sequence_info()

    def _on_marker_out_changed(self, out_ms: int):
        self._update_sequence_info()

    def _get_step_value(self) -> int:
        data = self.combo_step.currentData()
        if data == "1s":
            return max(1, int(round(self.video_fps)))
        return int(data) if data else 1

    def _update_sequence_info(self):
        in_ms = self.timeline.getMarkerIn()
        out_ms = self.timeline.getMarkerOut()
        diff_ms = max(0, out_ms - in_ms)
        diff_sec = diff_ms / 1000.0

        step = self._get_step_value()
        fps = self.video_fps if self.video_fps > 0 else 25.0

        start_frame = int(round((in_ms / 1000.0) * fps))
        end_frame = int(round((out_ms / 1000.0) * fps))
        total_frames_in_range = max(0, (end_frame - start_frame) + 1)
        frames_to_extract = (total_frames_in_range + step - 1) // step if step > 0 else total_frames_in_range

        self.lbl_sequence_info.setText(
            f"📍 Début : {format_ms(in_ms)}  |  🏁 Fin : {format_ms(out_ms)}  |  "
            f"⏱ Durée : {diff_sec:.2f}s  (~{frames_to_extract} images à extraire)"
        )

    def _update_timecode_display(self):
        curr = self.player.position()
        total = self.video_duration_ms
        self.lbl_timecode.setText(f"{format_ms(curr)} / {format_ms(total)}")

    def _on_format_changed(self, index: int):
        text = self.combo_format.currentText()
        is_lossy = "JPG" in text or "WEBP" in text
        self.lbl_quality.setVisible(is_lossy)
        self.slider_quality.setVisible(is_lossy)

    def _on_quality_changed(self, val: int):
        self.lbl_quality.setText(f"Qualité ({val}%) :")

    def open_output_folder(self):
        out_dir = self.txt_output_dir.text().strip()
        if os.path.exists(out_dir):
            os.startfile(out_dir)
        else:
            QMessageBox.information(self, "Dossier introuvable", "Le dossier n'existe pas encore. Il sera créé lors de l'extraction.")

    def start_extraction(self):
        if not self.current_video_path or not os.path.exists(self.current_video_path):
            QMessageBox.warning(self, "Attention", "Veuillez charger une vidéo valide avant de lancer l'extraction.")
            return

        out_dir = self.txt_output_dir.text().strip()
        if not out_dir:
            QMessageBox.warning(self, "Attention", "Veuillez spécifier un dossier de sortie.")
            return

        # Si le dossier de destination existe déjà et contient déjà des fichiers, créer un sous-dossier incrémenté pour ne pas mélanger
        if os.path.exists(out_dir) and os.path.isdir(out_dir):
            existing_files = [f for f in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, f))]
            if existing_files:
                counter = 2
                base_target = out_dir
                while os.path.exists(f"{base_target}_{counter}") and os.listdir(f"{base_target}_{counter}"):
                    counter += 1
                out_dir = f"{base_target}_{counter}"
                self.txt_output_dir.setText(out_dir)

        in_ms = self.timeline.getMarkerIn()
        out_ms = self.timeline.getMarkerOut()
        if out_ms <= in_ms:
            QMessageBox.warning(self, "Attention", "Le marqueur de fin doit être supérieur au marqueur de début.")
            return

        fmt_text = self.combo_format.currentText()
        if "JPG" in fmt_text:
            img_format = "jpg"
        elif "PNG" in fmt_text:
            img_format = "png"
        elif "WEBP" in fmt_text:
            img_format = "webp"
        else:
            img_format = "bmp"

        quality = self.slider_quality.value()
        step = self._get_step_value()
        prefix = self.txt_prefix.text().strip() or "frame"

        # UI state during extraction
        self.btn_extract.setEnabled(False)
        self.btn_cancel.setVisible(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.lbl_status.setText("Démarrage de l'extraction...")

        # Pause player
        self.player.pause()

        # Launch Thread
        self.extractor_thread = FrameExtractorThread(
            video_path=self.current_video_path,
            output_dir=out_dir,
            start_ms=in_ms,
            end_ms=out_ms,
            image_format=img_format,
            quality=quality,
            step=step,
            prefix=prefix
        )
        self.extractor_thread.progress.connect(self._on_extraction_progress)
        self.extractor_thread.finished.connect(self._on_extraction_finished)
        self.extractor_thread.error.connect(self._on_extraction_error)
        self.extractor_thread.start()

    def cancel_extraction(self):
        if self.extractor_thread and self.extractor_thread.isRunning():
            self.lbl_status.setText("Annulation en cours...")
            self.extractor_thread.cancel()

    def _on_extraction_progress(self, current: int, total: int, percent: int, fps: float):
        self.progress_bar.setValue(percent)
        speed_str = f" ({fps:.1f} img/s)" if fps > 0 else ""
        self.lbl_status.setText(f"{current} / {total} images extraites{speed_str}")

    def _on_extraction_finished(self, total_extracted: int, out_dir: str):
        self.btn_extract.setEnabled(True)
        self.btn_cancel.setVisible(False)
        self.lbl_status.setText(f"Terminé : {total_extracted} images enregistrées !")

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Extraction terminée")
        msg_box.setStyleSheet(self.styleSheet())

        # Couleurs à contraste garanti quel que soit le thème Windows
        if self.is_dark_mode:
            title_col = "#ffffff"
            succ_col = "#74c69d"
            path_col = "#61afef"
        else:
            title_col = "#0f172a"
            succ_col = "#15803d"
            path_col = "#0369a1"

        msg_box.setText(
            f"<div style='color: {title_col}; font-size: 15px; font-weight: bold; margin-bottom: 4px;'>Extraction terminée !</div>"
            f"<div style='color: {succ_col}; font-size: 13px; font-weight: 600;'>{total_extracted} images ont été extraites avec succès.</div>"
        )
        msg_box.setInformativeText(
            f"<div style='color: {path_col}; font-size: 12px; margin-top: 8px;'><b>Dossier :</b> {out_dir}</div>"
        )

        btn_open = msg_box.addButton("Ouvrir le dossier", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton("Fermer", QMessageBox.ButtonRole.RejectRole)
        msg_box.exec()

        if msg_box.clickedButton() == btn_open:
            if os.path.exists(out_dir):
                os.startfile(out_dir)

    def _on_extraction_error(self, err_msg: str):
        self.btn_extract.setEnabled(True)
        self.btn_cancel.setVisible(False)
        self.lbl_status.setText("Erreur lors de l'extraction.")
        QMessageBox.critical(self, "Erreur", err_msg)

    def closeEvent(self, event):
        """Gestion propre de la fermeture : libération des verrous de fichiers et arrêt des threads"""
        # 1. Arrêter le thread d'extraction si actif
        if self.extractor_thread and self.extractor_thread.isRunning():
            self.extractor_thread.cancel()
            self.extractor_thread.wait(1500)

        # 2. Déverrouiller impérativement le fichier vidéo Windows
        if hasattr(self, 'player') and self.player is not None:
            self.player.stop()
            self.player.setSource(QUrl())
            self.player.deleteLater()

        if hasattr(self, 'audio_output') and self.audio_output is not None:
            self.audio_output.deleteLater()

        event.accept()
        QApplication.quit()


def main():
    import ctypes
    try:
        myappid = 'mp4toimages.studio.app.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setApplicationName("MP4toImages")
    app.setQuitOnLastWindowClosed(True)
    
    icon_path = resource_path("icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        
    window = VideoExtractorApp()
    window.show()
    exit_code = app.exec()
    
    # Terminaison stricte et immédiate du processus (garantit zéro processus résiduel)
    os._exit(exit_code)


if __name__ == "__main__":
    main()
