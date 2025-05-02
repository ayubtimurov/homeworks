import sys

from database import Note, session
from PySide6.QtWidgets import (QApplication, QSystemTrayIcon, QTextEdit, QHBoxLayout, 
 QVBoxLayout, QWidget, QPushButton, QMenu)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction

app = QApplication(sys.argv)

active_notewindows = {}

class StickyNotes(QWidget):
    def __init__(self, note=None):
        super().__init__()
        self.app = app
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setStyleSheet("background: yellow; color: black; border: 0; font-size: 12px")
        layout = QVBoxLayout()
        
        buttons = QHBoxLayout()
        self.close_btn = QPushButton("x")
        self.close_btn.setStyleSheet("font-weight: bold; font-size: 25px: width: 25px; height: 25px")
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(self.close)
        buttons.addStretch()
        buttons.addWidget(self.close_btn)
        layout.addLayout(buttons)

        self.text = QTextEdit() 
        layout.addWidget(self.text)
        self.setLayout(layout)

        active_notewindows[id(self)] = self
        
        if note is None:
            self.note = Note()
            self.save
        else:
            self.note = note
            self.load()

    def mousePressEvent(self, e):
        self.previous_pos = e.globalPosition()

    def mouseMoveEvent(self, e):
        delta = e.globalPosition() - self.previous_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.previous_pos = e.globalPosition()

    def mouseReleaseEvent(self, e):
        self.save()

    def load(self):
        self.move(self.note.x, self.note.y)
        self.text.setText(self.note.text)

    def save(self):
        self.note.x = self.x()
        self.note.y = self.y()
        self.note.text = self.text.toPlainText()
        session.add(self.note)
        session.commit()

    def delete(self):
        session.delete(self.note)
        session.commit()
        del active_notewindows[id(self)]
        self.close()    

def create_notewindow():
    note = StickyNotes()
    note.show()

existing_notes = session.query(Note).all()

if existing_notes:
    for note in existing_notes:
        create_notewindow(note)
else:
    create_notewindow()

icon = QIcon("sticky_note2.png")

tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

def handle_tray_clicked(reason):
    if(
        QSystemTrayIcon.ActivationReason(reason) 
        == QSystemTrayIcon.ActivationReason.Trigger
    ):
        create_notewindow()

tray.activated.connect(handle_tray_clicked)

app.setQuitOnLastWindowClosed(False)

menu = QMenu()
add_note_action = QAction("Add note")
add_note_action.triggered.connect(create_notewindow)
menu.addAction(add_note_action)

quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

tray.setContextMenu(menu)

app.exec()
