from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy ,QLabel, QFrame
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("ASSISTANT_NAME")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}/Frontend/Files"
GraphicsDirPath = rf"{current_dir}/Frontend/Graphics"

def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(query):
    new_query = query.lower().strip()
    query_wrds = new_query.split()
    question_words = ["what", "who", "where", "when", "why", "how" , "whose" , "whom", "which" , "can you" , "will you" , "would you" , "could you" , "please" , "tell me" , "explain" , "describe"]
    
    if any(word + " " in new_query for word in question_words):
        if(query_wrds[-1][-1] in ['.' , '?' , '!']):
            new_query = new_query[:-1] + "?"
        else:
            new_query += '?'
    else:
        if(query_wrds[-1][-1] in ['.' , '?' , '!']):
            new_query = new_query[:-1] + "."
        else:
            new_query += '.'
    return new_query.capitalize()

def SetMicStatus(command):
    with open(rf"{TempDirPath}/MicStatus.data", "w" ,encoding ='utf-8') as file:
        file.write(command)
        
def getMicStatus():
    with open(rf"{TempDirPath}/MicStatus.data", "r" ,encoding ='utf-8') as file:
        status = file.read()
    return status

def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w" ,encoding ='utf-8') as file:
        file.write(Status)
def getAssistantStatus():
    with open(rf"{TempDirPath}/Status.data", "r" ,encoding ='utf-8') as file:
        status = file.read()
    return status    

def MicButtonInitialized():
    SetMicStatus("False")

def MicButtonClosed():
    SetMicStatus("True")

def GraphicsPath(filename):
    Path = rf'{GraphicsDirPath}/{filename}'
    return Path

def TempDIRPath(filename):
    Path = rf'{TempDirPath}/{filename}'
    return Path

def text_display(text):
    with open(rf'{TempDirPath}/Responses.data', 'w', encoding='utf-8') as file:
        file.write(text)
        
class ChatSelection(QWidget):
    
    def __init__(self):
        super(ChatSelection,self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10 , 40 , 40 ,100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QTextEdit.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1,1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))        
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)

        # Display GIF
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsPath('jarvis.gif'))
        max_gif_size_W = 480
        max_gif_size_H = 270
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()

        layout.addWidget(self.gif_label)

        # Display accompanying text
        self.label = QLabel("")
        self.label.setStyleSheet(
            "color: white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px;"
        )
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)

        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
                            QScrollBar:vertical {
                               border: none;
                               background: black;
                               width: 10px;
                               margin: 0px 0px 0px 0px;
                               }
                            QScrollBar::handle:vertical {
                                    background: white;
                                    min-height: 20px;
                                }

                            QScrollBar::add-line:vertical {
                                background: black;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                                height: 10px;
                            }

                            QScrollBar::sub-line:vertical {
                                background: black;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                                height: 10px;
                            }      
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: none;
                                background: none;
                                color: none;
                            }
                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                            """)
    def loadMessages(self):
        global old_chat_message
        with open(TempDIRPath('Responses.data') , 'r' , encoding='utf-8') as f:
            messages = f.read()
            if None == messages:
                pass
            elif len(messages) <= 1:
                pass
            elif str(old_chat_message) == str(messages):
                pass
            else:
                self.addMessage(message = messages , color = 'White')
                old_chat_message = messages
        
    def SpeechRecogText(self):
        with open(TempDIRPath('Status.data') , 'r' , encoding='utf-8') as f:
            messages = f.read()
            self.label.setText(messages)
            
    def load_icon(self , path , width=60 , height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width , height , Qt.KeepAspectRatio)
        self.icon_label.setPixmap(new_pixmap)
    
    def toggle_icon(self , event = None):
        if self.toggled:
            self.load_icon(GraphicsDirPath('voice.png') , 60 ,60 )
            MicButtonInitialized()
        else:
            self.load_icon(GraphicsDirPath('mic.png') , 60 ,60 )
            MicButtonClosed()
        self.toggled = not self.toggled
    
    def addMessage(self , message , color ):
        cursor = self.chat_text_edit.textCursor()

        # char_format = QTextCharFormat()
        # block_format = QTextBlockFormat()
        # block_format.setTopMargin(10)
        # block_format.setLeftMargin(10)
        # char_format.setForeground(QColor(color))
        # cursor.setCharFormat(char_format)
        # cursor.setBlockFormat(block_format)
        # cursor.insertText(message + "\n")
        # self.chat_text_edit.setTextCursor(cursor)
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)
        
class InitialScreen(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        gif_label = QLabel()
        movie = QMovie(GraphicsPath('jarvis.gif'))
        gif_label.setMovie(movie)
        max_gif_size_H = int(screen_width / 16*9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_H))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsPath('mic_on.png'))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px ; margin-bottom:0;")

        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)

        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        with open(TempDIRPath('Status.data') , 'r' , encoding='utf-8') as f:
            messages = f.read()
            self.label.setText(messages)
    
    def load_icon(self , path , width = 60 , height = 60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width , height)
        self.icon_label.setPixmap(new_pixmap)
    
    def toggle_icon(self , event = None):
        if self.toggled:
            self.load_icon(GraphicsPath('mic_on.png') , 60 ,60 )
            MicButtonInitialized()
        else:
            self.load_icon(GraphicsPath('mic_off.png') , 60 ,60 )
            MicButtonClosed()
        self.toggled = not self.toggled
            
class MessageScreen(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_w = desktop.screenGeometry().width()
        screen_h = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        label = QLabel()
        layout.addWidget(label)
        chat_selection = ChatSelection()
        layout.addWidget(chat_selection)
        self.setLayout(layout)
        self.setFixedHeight(screen_h)
        self.setFixedWidth(screen_w)
        self.setStyleSheet("background-color: black;")
class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget  
        self.initUI()
        self.current_screen = None
        
    def initUI(self):
        # top_bar = QWidget()
        self.setFixedHeight(50)
        top_layout = QHBoxLayout(self)
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
            btn.setIcon(QIcon(GraphicsPath(icon_file)))
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
        min_btn.setIcon(QIcon(GraphicsPath("minimize.png")))
        min_btn.setStyleSheet("background-color:white;")
        min_btn.clicked.connect(self.minimizeWindow)
        top_layout.addWidget(min_btn)

        self.max_btn = QPushButton()
        self.max_icon = QIcon(GraphicsPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicsPath("Minimize.png"))
        self.max_btn.setIcon(self.max_icon)
        self.max_btn.setStyleSheet("background-color:white;")
        self.max_btn.clicked.connect(self.maximizeWindow)
        top_layout.addWidget(self.max_btn)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(GraphicsPath("Close.png")))
        close_btn.setStyleSheet("background-color:white;")
        close_btn.clicked.connect(self.closeWindow)
        top_layout.addWidget(close_btn)

        # top_bar.setLayout(top_layout)
        self.darggable = True
        self.offset = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)
    
    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.max_btn.setIcon(self.max_icon)
        else:
            self.parent().showMaximized()
            self.max_btn.setIcon(self.restore_icon)
        
    def closeWindow(self):
        self.parent().close()
    
    def mousePressEvent(self, event):
        if self.darggable:
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.darggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)
    
    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        message_screen = MessageScreen(self)
        self.current_screen = message_screen
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        
    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        initial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screen_w = desktop.screenGeometry().width()
        screen_h = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screen_w, screen_h)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)   


def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()
    
