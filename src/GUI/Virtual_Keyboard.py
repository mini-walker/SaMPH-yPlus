# =============================================================================
#  Calculator Virtual Keyboard for QTabWidget
#  Features:
#   - Only digits 0-9, decimal point (.), and Backspace
#   - 3-row layout with 0, ., and Backspace in the same column
#   - Click-to-focus detection using mousePressEvent (not focusInEvent)
#   - Global variable tracks the last clicked QLineEdit
#   - Prevents duplicate decimal points
#   - Modern, clean, responsive button styles
#   - Programmer: Shanqin Jin
#   - Email: sjin@mun.ca
#   - Date: 2025-10-27  
# =============================================================================

import sys  # Import system-specific parameters and functions
import os
import webbrowser

from pathlib import Path

# -----------------------------------------------------------------------------
# Import PyQt5 widgets for UI elements
from PySide6.QtWidgets import ( 
    QApplication, 
    QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog,
    QLabel, QTextEdit, QFileDialog, QAbstractButton, QWidget, QStackedWidget, QTabWidget,    
    QLineEdit, QSplitter, 
    QPushButton, QRadioButton, QButtonGroup,
    QVBoxLayout, QHBoxLayout, QMdiArea, QMdiSubWindow,
    QFormLayout, QGridLayout, QGroupBox, QComboBox,
    QMessageBox
)
# from PySide6.QtVirtualKeyboard import QVirtualKeyboard
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter              # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QEvent                         # Import Qt core functionalities such as alignment
# -----------------------------------------------------------------------------


# Add the parent directory to the Python path for debugging (independent execution)
if __name__ == "__main__": 

    print("Debug mode!")   # ***Sometimes, the Vscode will load wrong python interpreter, if the code doesn't run, try to change the interpreter.

    # Get project root folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if project_root not in sys.path: sys.path.insert(0, project_root)








# =============================================================================
#  GLOBAL STATE: Tracks the most recently clicked QLineEdit
#  This allows the keyboard to insert text even when the input field
#  loses focus after switching tabs.
# =============================================================================
LAST_FOCUSED_EDIT = None


def record_focus(edit: QLineEdit):
    """
    Record the QLineEdit that was just clicked.
    This function is called from mousePressEvent to capture user intent.

    Args:
        edit: The QLineEdit instance that received the click.
    """
    global LAST_FOCUSED_EDIT
    LAST_FOCUSED_EDIT = edit


# =============================================================================
#  Custom QLineEdit subclass to detect mouse clicks
#  Standard focusInEvent() does NOT trigger on mouse click in many cases,
#  so we override mousePressEvent() to reliably capture user selection.
# =============================================================================
class ClickableLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Enable mouse tracking (optional, but helps with hover effects if needed)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        """
        Override: Called when the user clicks on the QLineEdit.
        We record this widget as the target for keyboard input.
        """
        record_focus(self)                    # <-- Record this input field
        super().mousePressEvent(event)        # <-- Let Qt handle normal behavior


# =============================================================================
#  CalculatorKeyboard Widget
#  A compact 3×4 virtual keypad embedded in a QTabWidget page.
# =============================================================================
class CalculatorKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(self.get_style())  # Apply visual styling
        self.init_ui()                        # Build the button grid

    # -------------------------------------------------------------------------
    #  Styling: Modern, clean, and responsive button design
    # -------------------------------------------------------------------------
    def get_style(self):
        """
        Returns a Qt stylesheet string for consistent, beautiful buttons.
        - Gradient backgrounds for depth
        - Rounded corners (14px)
        - Hover and pressed states
        - Special colors for Backspace, 0, and .
        """
        return """
        QWidget { background: transparent; }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #f1f5f9, stop:1 #e2e8f0);
            border: 1px solid #cbd5e1;
            border-radius: 14px;
            font: bold 19px 'Segoe UI', Arial;
            color: #1e293b;
            margin: 4px;
            padding: 0;
            min-height: 50px;
        }
        QPushButton:hover {
            background: #dbeafe;
            border: 1px solid #3b82f6;
            color: #1e40af;
        }
        QPushButton:pressed {
            background: #93c5fd;
        }
        QPushButton#delete {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #fca5a5, stop:1 #f87171);
            color: white;
            font-weight: bold;
        }
        QPushButton#delete:hover {
            background: #ef4444;
        }
        QPushButton#zero, QPushButton#dot {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #e0e7ff, stop:1 #c7d2fe);
            color: #1e40af;
            font-weight: bold;
        }
        QPushButton#zero:hover, QPushButton#dot:hover {
            background: #a5b4fc;
            color: white;
        }
        """

    # -------------------------------------------------------------------------
    #  UI Construction: Build the 3-row keypad using QGridLayout
    # -------------------------------------------------------------------------
    def init_ui(self):
        """
        Constructs the keypad layout:
        Row 0:  7  8  9  Backspace
        Row 1:  4  5  6  0
        Row 2:  1  2  3  .
        """
        grid = QGridLayout(self)
        grid.setSpacing(8)                    # Space between buttons
        grid.setContentsMargins(12, 12, 12, 12)  # Padding around the keypad

        # Define button positions: (row, col, rowspan, colspan, label, objectName)
        layout_map = [
            (0, 0, 1, 1, "7", None),
            (0, 1, 1, 1, "8", None),
            (0, 2, 1, 1, "9", None),
            (0, 3, 1, 1, "Backspace", "delete"),   # Backspace button

            (1, 0, 1, 1, "4", None),
            (1, 1, 1, 1, "5", None),
            (1, 2, 1, 1, "6", None),
            (1, 3, 1, 1, "0", "zero"),             # 0 in same column as Backspace

            (2, 0, 1, 1, "1", None),
            (2, 1, 1, 1, "2", None),
            (2, 2, 1, 1, "3", None),
            (2, 3, 1, 1, ".", "dot"),              # Decimal point
        ]

        # Create and place each button
        for row, col, rowspan, colspan, key, obj_id in layout_map:
            btn = QPushButton(key)
            btn.setFixedHeight(56)             # Uniform button height

            # Set width and object name for special buttons
            if obj_id:
                btn.setObjectName(obj_id)
                if obj_id == "delete":
                    btn.setFixedWidth(120)     # Wider Backspace
                elif obj_id in ["zero", "dot"]:
                    btn.setFixedWidth(120)     # 0 and . are also wider

            # Default width for number buttons
            else:
                btn.setFixedWidth(60)

            # Add to grid with span
            grid.addWidget(btn, row, col, rowspan, colspan)

            # Connect click → insert character into the last focused QLineEdit
            btn.clicked.connect(lambda _, k=key: self.input_key(k))

    # -------------------------------------------------------------------------
    #  Input Logic: Insert character into the recorded QLineEdit
    # -------------------------------------------------------------------------
    def input_key(self, key: str):
        """
        Handles button press:
        - Digits: insert at cursor
        - '.': insert only if not already present
        - 'Backspace': delete previous character
        """
        global LAST_FOCUSED_EDIT
        if not LAST_FOCUSED_EDIT:
            return  # Safety: no input field selected

        cursor = LAST_FOCUSED_EDIT.cursorPosition()
        text = LAST_FOCUSED_EDIT.text()

        if key == "Backspace":
            # Delete character before cursor
            if cursor > 0:
                new_text = text[:cursor-1] + text[cursor:]
                LAST_FOCUSED_EDIT.setText(new_text)
                LAST_FOCUSED_EDIT.setCursorPosition(cursor - 1)

        elif key == ".":
            # Prevent multiple decimal points
            if "." not in text:
                new_text = text[:cursor] + "." + text[cursor:]
                LAST_FOCUSED_EDIT.setText(new_text)
                LAST_FOCUSED_EDIT.setCursorPosition(cursor + 1)

        else:
            # Insert digit at cursor position
            new_text = text[:cursor] + key + text[cursor:]
            LAST_FOCUSED_EDIT.setText(new_text)
            LAST_FOCUSED_EDIT.setCursorPosition(cursor + 1)
