from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QPolygonF
from PyQt6.QtCore import QPointF

class TimelineSlider(QWidget):
    """
    Custom video timeline widget that displays:
    - Background bar for total video duration.
    - Highlighted active selection between In and Out markers.
    - Marker In flag [ ] and Marker Out flag [ ].
    - Current playhead scrubber with smooth dragging and clicking.
    - Dark and light theme support (Light by default).
    """
    positionChanged = pyqtSignal(int)
    markerInChanged = pyqtSignal(int)
    markerOutChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(46)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._duration = 1000  # ms
        self._position = 0     # ms
        self._marker_in = 0    # ms
        self._marker_out = 1000 # ms

        self._dragging_playhead = False
        self._hover_pos = -1
        self._is_dark = False  # Par défaut en mode clair
        self.setMouseTracking(True)

    def setDarkMode(self, is_dark: bool):
        self._is_dark = is_dark
        self.update()

    def setDuration(self, duration_ms):
        self._duration = max(1, duration_ms)
        self._marker_in = 0
        self._marker_out = self._duration
        self._position = min(self._position, self._duration)
        self.update()

    def setPosition(self, pos_ms):
        if not self._dragging_playhead:
            self._position = max(0, min(pos_ms, self._duration))
            self.update()

    def setMarkerIn(self, pos_ms):
        pos_ms = max(0, min(pos_ms, self._duration))
        if pos_ms > self._marker_out:
            self._marker_out = pos_ms
        self._marker_in = pos_ms
        self.markerInChanged.emit(self._marker_in)
        self.update()

    def setMarkerOut(self, pos_ms):
        pos_ms = max(0, min(pos_ms, self._duration))
        if pos_ms < self._marker_in:
            self._marker_in = pos_ms
        self._marker_out = pos_ms
        self.markerOutChanged.emit(self._marker_out)
        self.update()

    def resetMarkers(self):
        self._marker_in = 0
        self._marker_out = self._duration
        self.markerInChanged.emit(self._marker_in)
        self.markerOutChanged.emit(self._marker_out)
        self.update()

    def getMarkerIn(self):
        return self._marker_in

    def getMarkerOut(self):
        return self._marker_out

    def _ms_to_x(self, ms):
        margin = 14
        usable_w = self.width() - 2 * margin
        if self._duration <= 0 or usable_w <= 0:
            return margin
        ratio = max(0.0, min(1.0, ms / self._duration))
        return margin + ratio * usable_w

    def _x_to_ms(self, x):
        margin = 14
        usable_w = self.width() - 2 * margin
        if usable_w <= 0:
            return 0
        clamped_x = max(margin, min(x, self.width() - margin))
        ratio = (clamped_x - margin) / usable_w
        return int(ratio * self._duration)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            ms = self._x_to_ms(event.position().x())
            self._position = ms
            self._dragging_playhead = True
            self.positionChanged.emit(ms)
            self.update()

    def mouseMoveEvent(self, event):
        self._hover_pos = event.position().x()
        if self._dragging_playhead:
            ms = self._x_to_ms(event.position().x())
            self._position = ms
            self.positionChanged.emit(ms)
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging_playhead = False
            self.update()

    def leaveEvent(self, event):
        self._hover_pos = -1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin = 14
        w = self.width()
        h = self.height()
        track_y = 18
        track_h = 10
        usable_w = w - 2 * margin

        # 1. Background full track
        painter.setPen(Qt.PenStyle.NoPen)
        track_color = QColor(45, 52, 64) if self._is_dark else QColor(210, 215, 225)
        painter.setBrush(track_color)
        painter.drawRoundedRect(QRectF(margin, track_y, usable_w, track_h), 5, 5)

        # 2. Highlighted range between Marker In and Marker Out
        in_x = self._ms_to_x(self._marker_in)
        out_x = self._ms_to_x(self._marker_out)
        range_w = max(2.0, out_x - in_x)

        painter.setBrush(QColor(0, 150, 255, 180))
        painter.drawRoundedRect(QRectF(in_x, track_y, range_w, track_h), 4, 4)

        # 3. Draw Marker In bracket/flag
        painter.setPen(QPen(QColor(46, 204, 113), 2))
        painter.drawLine(int(in_x), track_y - 8, int(in_x), track_y + track_h + 8)

        # In triangle flag (pointing right)
        in_flag = QPolygonF([
            QPointF(in_x, track_y - 8),
            QPointF(in_x + 9, track_y - 4),
            QPointF(in_x, track_y)
        ])
        painter.setBrush(QColor(46, 204, 113))
        painter.drawPolygon(in_flag)

        # 4. Draw Marker Out bracket/flag
        painter.setPen(QPen(QColor(231, 76, 60), 2))
        painter.drawLine(int(out_x), track_y - 8, int(out_x), track_y + track_h + 8)

        # Out triangle flag (pointing left)
        out_flag = QPolygonF([
            QPointF(out_x, track_y - 8),
            QPointF(out_x - 9, track_y - 4),
            QPointF(out_x, track_y)
        ])
        painter.setBrush(QColor(231, 76, 60))
        painter.drawPolygon(out_flag)

        # 5. Draw Playhead scrubber (Cursor)
        play_x = self._ms_to_x(self._position)

        # Vertical line for playhead
        play_line_color = QColor(255, 255, 255, 230) if self._is_dark else QColor(30, 41, 59, 230)
        painter.setPen(QPen(play_line_color, 2))
        painter.drawLine(int(play_x), 4, int(play_x), h - 4)

        # Playhead handle (circle)
        handle_pen = QPen(QColor(30, 30, 30), 1.5) if self._is_dark else QPen(QColor(100, 116, 139), 1.5)
        painter.setPen(handle_pen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(QPointF(play_x, track_y + track_h / 2), 7, 7)
