from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout, QPushButton, QScrollArea
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QIcon, QKeyEvent
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import qdarktheme, os , sys


def path_(yol):
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, yol)
    else:
        path = yol
    return path

class VolumeMixerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volume Mixer")
        self.setWindowIcon(QIcon(path_('logo_yeni2.png')))
        self.initUI()
        self.initFooter()  # Alt bölümdeki yazı için yeni metod
        self.startRefreshTimer()
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.showNormal()  # Tam ekran modundan çıkar
        elif event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        else:
            super().keyPressEvent(event)

    def initFooter(self):
        footer_label = QLabel("Copyright © Lightfield - ALGOS – Tüm Hakları Saklıdır.")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Yazıyı ortalayın

        # Ana layout'a etiketi ekleyin
        self.layout.addWidget(footer_label)

    def moveToMonitor(self, monitor_number, width, height):
        screen = QApplication.screens()[monitor_number]
        screen_geometry = screen.geometry()
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

    def initUI(self):
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # Scroll alanını oluşturun
        self.scrollArea = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.layout.addWidget(self.scrollArea)
        self.setCentralWidget(self.widget)

        self.refreshSessions()

    def refreshSessions(self):
        # Scroll alanındaki mevcut widget'ları temizle
        for i in reversed(range(self.scrollLayout.count())):
            self.scrollLayout.itemAt(i).widget().setParent(None)

        # Yeni ses oturumu widget'larını ekle
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                session_layout = QHBoxLayout()

                label = QLabel(f"{session.Process.name()}")
                volume_label = QLabel(f"{int(volume.GetMasterVolume() * 100)}%")
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setMaximum(100)
                slider.setValue(int(volume.GetMasterVolume() * 100))
                slider.valueChanged.connect(lambda value, s=session, vl=volume_label: self.setVolumeAndUpdateLabel(value, s, vl))

                mute_button = QPushButton()
                mute_button.setIcon(QIcon(path_('mute_icon.png')))
                mute_button.setCheckable(True)
                mute_button.toggled.connect(lambda checked, s=session: self.toggleMute(checked, s))

                session_layout.addWidget(label)
                session_layout.addWidget(slider)
                session_layout.addWidget(volume_label)
                session_layout.addWidget(mute_button)

                session_widget = QWidget()
                session_widget.setLayout(session_layout)
                self.scrollLayout.addWidget(session_widget)


    def toggleMute(self, checked, session):
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if checked:
            volume.SetMute(1, None)  # Sessize al
        else:
            volume.SetMute(0, None)  # Sesi aç
        # İkonu güncelle
        sender = self.sender()
        if sender:
            sender.setIcon(QIcon(path_('unmute_icon.png' if checked else 'mute_icon.png')))

    def setVolumeAndUpdateLabel(self, value, session, volume_label):
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(value / 100.0, None)
        volume_label.setText(f"{value}%")

    def setVolume(self, value, session):
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(value / 100.0, None)

    def startRefreshTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshSessions)
        self.timer.start(5000)  # Refresh every 5000 milliseconds (5 seconds)

def main():
    app = QApplication([])
    qdarktheme.enable_hi_dpi()
    qdarktheme.setup_theme()
    window = VolumeMixerWindow()
    window.moveToMonitor(0, 800, 600)
    window.showFullScreen()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
