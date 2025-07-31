from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QIcon, QMovie, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

# Environment variables and paths
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("ASSISTANT_NAME", "Assistant")
current_dir = os.getcwd()
TempDirPath = rf"{current_dir}/Frontend/Files"
GraphicsDirPath = rf"{current_dir}/Frontend/Graphics"

def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(query):
    new_query = query.lower().strip()
    query_wrds = new_query.split()
    question_words = ["what", "who", "where", "when", "why", "how", "whose", "whom", "which", "can you", "will you", "would you", "could you", "please", "tell me", "explain", "describe"]
    if any(word + " " in new_query for word in question_words):
        new_query = new_query.rstrip('.?!') + "?"
    else:
        new_query = new_query.rstrip('.?!') + "."
    return new_query.capitalize()

def set_status(file, value):
    with open(rf"{TempDirPath}/{file}", "w", encoding='utf-8') as f:
        f.write(value)

def get_status(file):
    with open(rf"{TempDirPath}/{file}", "r", encoding='utf-8') as f:
        return f.read()

def temp_path(filename):
    return rf"{TempDirPath}/{filename}"

def graphics_path(filename):
    return rf"{GraphicsDirPath}/{filename}"

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Window sizing
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        # Load Screens
        self.stacked_widget = QStackedWidget()
        self.init_screen = QWidget()
        self.chat_screen = QWidget()
        self.stacked_widget.addWidget(self.init_screen)
        self.stacked_widget.addWidget(self.chat_screen)

        # Top bar
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel(Assistantname.capitalize())
        title.setStyleSheet("color: black; font-size: 18px; background-color:white;")
        top_layout.addWidget(title)

        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        top_layout.addWidget(left_spacer)

        center_widget = QWidget()
        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(10)

        def create_icon_button(name, icon_file, on_click):
            btn = QPushButton(f" {name}")
            btn.setIcon(QIcon(graphics_path(icon_file)))
            btn.setStyleSheet("height: 40px; background-color:white; color:black;")
            btn.clicked.connect(on_click)
            return btn

        home_btn = create_icon_button("Home", "home.png", lambda: self.stacked_widget.setCurrentIndex(0))
        chats_btn = create_icon_button("Chats", "chats.png", lambda: self.stacked_widget.setCurrentIndex(1))
        center_layout.addWidget(home_btn)
        center_layout.addWidget(chats_btn)
        center_widget.setLayout(center_layout)
        top_layout.addWidget(center_widget)

        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        top_layout.addWidget(right_spacer)

        min_btn = QPushButton()
        min_btn.setIcon(QIcon(graphics_path("minimize.png")))
        min_btn.setStyleSheet("background-color:white;")
        min_btn.clicked.connect(self.showMinimized)
        top_layout.addWidget(min_btn)

        self.max_btn = QPushButton()
        self.max_icon = QIcon(graphics_path("Maximize.png"))
        self.restore_icon = QIcon(graphics_path("Minimize.png"))
        self.max_btn.setIcon(self.max_icon)
        self.max_btn.setStyleSheet("background-color:white;")
        self.max_btn.clicked.connect(self.toggle_maximize)
        top_layout.addWidget(self.max_btn)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(graphics_path("Close.png")))
        close_btn.setStyleSheet("background-color:white;")
        close_btn.clicked.connect(self.close)
        top_layout.addWidget(close_btn)

        top_bar.setLayout(top_layout)

        # Initial Screen Layout
        init_layout = QVBoxLayout()

        gif_label = QLabel()
        movie = QMovie(graphics_path("jarvis.gif"))
        screen = QApplication.desktop().screenGeometry()
        movie.setScaledSize(QSize(int(screen.width()*0.7), int(screen.height()*0.6)))
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignHCenter)
        movie.start()

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(60, 60)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.load_icon(graphics_path("mic_on.png"))
        self.icon_label.mousePressEvent = self.toggle_icon

        init_layout.addWidget(gif_label)
        init_layout.addWidget(self.label)
        init_layout.addWidget(self.icon_label)
        self.init_screen.setLayout(init_layout)

        # Chat Screen Layout
        chat_layout = QVBoxLayout()
        self.chat_text = QTextEdit()
        self.chat_text.setReadOnly(True)
        self.chat_text.setStyleSheet("background-color: black; color: white;")
        self.chat_text.setFont(QFont("Arial", 13))

        gif_chat = QLabel()
        movie_chat = QMovie(graphics_path("jarvis.gif"))
        movie_chat.setScaledSize(QSize(480, 270))
        gif_chat.setMovie(movie_chat)
        gif_chat.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        movie_chat.start()

        self.chat_status_label = QLabel("")
        self.chat_status_label.setStyleSheet("color: black; font-size: 16px; margin-right: 195px;")
        self.chat_status_label.setAlignment(Qt.AlignRight)

        chat_layout.addWidget(self.chat_text)
        chat_layout.addWidget(gif_chat)
        chat_layout.addWidget(self.chat_status_label)
        self.chat_screen.setLayout(chat_layout)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_bar)
        main_layout.addWidget(self.stacked_widget)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.old_messages = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(5)

        self.setStyleSheet("background-color: white;")

        self.old_pos = None
        self.dragging = False
        self.toggled = True

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.max_btn.setIcon(self.max_icon)
        else:
            self.showMaximized()
            self.max_btn.setIcon(self.restore_icon)

    def update_status(self):
        status_text = get_status("Status.data")
        self.label.setText(status_text)
        self.chat_status_label.setText(status_text)
        messages = get_status("Responses.data")
        if messages and messages != self.old_messages:
            self.chat_text.append(messages)
            self.old_messages = messages

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def SpeechRecogText(self):
        with open(temp_path('Status.data'), 'r', encoding='utf-8') as f:
            messages = f.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(graphics_path('mic_on.png'), 60, 60)
            set_status("MicStatus.data", "False")
        else:
            self.load_icon(graphics_path('mic_off.png'), 60, 60)
            set_status("MicStatus.data", "True")
        self.toggled = not self.toggled

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
