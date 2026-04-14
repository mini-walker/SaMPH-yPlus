#-----------------------------------------------------------------------------------------
# Purpouse: Create the page menu
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27  
#----------------------------------------------------------------------------------------- 

import sys  # Import system-specific parameters and functions
import os
import webbrowser

from pathlib import Path

#-----------------------------------------------------------------------------------------
# Import PyQt5 widgets for UI elements
from PySide6.QtWidgets import ( 
    QApplication, 
    QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog,
    QLabel, QTextEdit, QFileDialog, QAbstractButton, QWidget, QStackedWidget, QTabWidget,    
    QLineEdit, QSplitter, 
    QPushButton, QRadioButton, QButtonGroup,
    QVBoxLayout, QHBoxLayout, QMdiArea, QMdiSubWindow,
    QFormLayout, QGridLayout, QFrame,
    QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter              # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QEvent, QPropertyAnimation, QEasingCurve,  QPoint   # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------------------------


# Add the parent directory to the Python path for debugging (independent execution)
if __name__ == "__main__": 

    # Get project root folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if project_root not in sys.path: sys.path.insert(0, project_root)


#-----------------------------------------------------------------------------------------
# Impot the class from the local python files
from GUI.Utils import utils
#-----------------------------------------------------------------------------------------


class Menu_Page(QWidget):
    """
    Sliding menu page attached to the main window.
    Features:
    - Fixed width menu slides in/out from the left, below the toolbar.
    - Semi-transparent background.
    - Close button at top-right.
    - Buttons correspond to QAction items from the toolbar.
    - Clicking a button triggers its QAction and closes the menu.
    """

    menu_action_triggered = Signal(QAction)

    def __init__(self, parent=None, tool_bar=None):

        super().__init__(parent)
        
        self.tool_bar = tool_bar
        self.main_window = parent

        self.menu_buttons = []  # save (action, button) in menu

        # Set as frameless window but still a child of main window
        # This makes it draw independently and opaque
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, False)


        # Get the height of the toolbar
        if self.tool_bar and hasattr(self.tool_bar, 'tool_bar'):
            toolbar_height = self.tool_bar.tool_bar.height()
        else:
            toolbar_height = 0


        # Calculate menu height starting from toolbar bottom
        self.setFixedWidth(300)
        # self.setFixedHeight((parent.height() if parent else 600) - toolbar_height)
        self.setFixedHeight(500)


        # Initial position: outside left, below toolbar
        toolbar_height = self.tool_bar.tool_bar.height() if self.tool_bar and hasattr(self.tool_bar, 'tool_bar') else 0
        self.move(-self.width(), toolbar_height)
        self.hide()

        self._anim = None
        self.is_visible = False

        self.init_menu_ui()

    # ------------------------------------------------------------------
    def init_menu_ui(self):
        """Initialize menu layout and buttons."""

        # === Container frame with white background ===
        container = QFrame(self)
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #CCCCCC;
            }
        """)

        # === Main layout inside the white container ===
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignTop)

        # --- Top row: title + close button ---
        top_row = QHBoxLayout()
        title = QLabel("Menu")
        title.setStyleSheet("font-size:14px; font-weight:bold; margin:5px;")
        btn_close = QPushButton(self)
        btn_close.setIcon(QIcon(str(utils.resource_path("images/Win11-Icons/icons8-close-100.png"))))
        btn_close.setFixedSize(24, 24)
        btn_close.clicked.connect(self.slide_out)

        top_row.addWidget(title)
        top_row.addStretch()
        top_row.addWidget(btn_close)
        layout.addLayout(top_row)

        # --- Separator ---
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addWidget(sep)


        # --- Menu buttons from toolbar actions ---
        if self.tool_bar:
            for action in self.tool_bar.actions():
                if not action.text() or action.text() == "Menu":
                    continue
                
                btn = QPushButton(self.main_window.language_manager.get_text(action.text()))
                btn.setIcon(action.icon())
                btn.setIconSize(QSize(20, 20))
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding-left: 10px;   
                        padding-right: 10px;
                        padding-top: 5px;
                        padding-bottom: 5px;
                        border: none;
                        font-size: 14px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #E6F1FB;     /* Light blue hover */
                    }
                """)
                btn.clicked.connect(lambda checked=False, a=action: self._on_button_clicked(a))
                layout.addWidget(btn)
                self.menu_buttons.append((action, btn))

        layout.addStretch()

        # === Add container into the main layout of this widget ===
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)
        self.setLayout(main_layout)
    # ------------------------------------------------------------------


    # ------------------------------------------------------------------
    def _on_button_clicked(self, action):
        """Trigger QAction and hide menu."""
        action.trigger()
        self.menu_action_triggered.emit(action)
        self.slide_out()

    # ------------------------------------------------------------------
    def slide_in(self, duration_ms=300):
        """Slide menu in from the left below the toolbar."""
        if self.is_visible:
            return
        self.show()
        self.raise_()

        # Get the height of the toolbar
        if self.tool_bar and hasattr(self.tool_bar, 'tool_bar'):
            toolbar_height = self.tool_bar.tool_bar.height()
        else:
            toolbar_height = 0


        self._anim = QPropertyAnimation(self, b"pos", self)
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(QPoint(-self.width(), toolbar_height))
        self._anim.setEndValue(QPoint(0, toolbar_height))
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.start()
        self.is_visible = True

    def slide_out(self, duration_ms=300):
        """Slide menu out to the left."""
        if not self.is_visible:
            return

        # Get the height of the toolbar
        if self.tool_bar and hasattr(self.tool_bar, 'tool_bar'):
            toolbar_height = self.tool_bar.tool_bar.height()
        else:
            toolbar_height = 0


        self._anim = QPropertyAnimation(self, b"pos", self)
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(self.pos())
        self._anim.setEndValue(QPoint(-self.width(), toolbar_height))
        self._anim.setEasingCurve(QEasingCurve.InCubic)
        self._anim.finished.connect(self.hide)
        self._anim.start()
        self.is_visible = False

    # ------------------------------------------------------------------
    # Update the UI texts fot the tool bar
    def update_ui_texts(self):
        """Update menu texts when language changes."""
        print("Updating menu language...")

        # Update the title
        for child in self.findChildren(QLabel):
            if child.text() == "Menu":  # Original text
                child.setText(self.main_window.language_manager.get_text("Menu"))

        # Update the buttons
        for action, btn in self.menu_buttons:
            key = action.text()  # Current action name
            translated = self.main_window.language_manager.get_text(key)
            btn.setText(translated)
    # ------------------------------------------------------------------
