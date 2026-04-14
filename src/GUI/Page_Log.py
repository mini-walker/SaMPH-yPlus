#-----------------------------------------------------------------------------------------
# Purpouse: The log window
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27  
#----------------------------------------------------------------------------------------- 

import sys
import logging


from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PySide6.QtCore import QDateTime


class QTextEditHandler(logging.Handler):
    """
    Logging handler that outputs messages to a QTextEdit with color formatting.
    """
    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        # Generate timestamp
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        time_color = "gray"      # gray for time box
        # message_color = "#000000"   # black for message

        # HTML formatting
        if record.levelno >= logging.ERROR:
            color = 'red'
            level_str = " ERROR "
            formatted_msg = f'<span style="color:{time_color};">[{timestamp}]</span> ' \
                            f'<span style="color:{color};"> ---{level_str}--- {msg}</span>'

        elif record.levelno >= logging.WARNING:

            color = 'orange'
            level_str = " WARNING "
            formatted_msg = f'<span style="color:{time_color};">[{timestamp}]</span> ' \
                            f'<span style="color:{color};"> ---{level_str}--- {msg}</span>'
            
        elif record.levelno >= logging.INFO:
            color = 'black'
            formatted_msg = f'<span style="color:{time_color};">[{timestamp}]</span> ' \
                            f'<span style="color:{color};">{msg}</span>'
        
        self.text_edit.append(formatted_msg)



class LogWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)  # Correct: No string argument for QWidget

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)           # Remove outer margins, order: left, top, right, bottom
        layout.setSpacing(0)                            # No spacing between widgets

        # Create the log area (QTextEdit)
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)

        self.log_window.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
                font-size: 10pt;
                line-height: 1.5;
                padding: 0px 0px 0px 0px;   /* top right bottom left */
            }
            QTextEdit::viewport {
                padding: 0px;
            }
            /* the vertical scroll bar */
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0.1);
                width: 8px;                    /* the width of the scroll bar */
                margin: 4px 0 4px 0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.4);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                width: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            /* the horizontal scroll bar (optional) */
            QScrollBar:horizontal {
                border: none;
                background: rgba(0, 0, 0, 0.1);
                height: 8px;
                margin: 0 4px 0 4px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(0, 0, 0, 0.4);
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(0, 0, 0, 0.6);
            }
        """)


        layout.addWidget(self.log_window)


        # ====== Logging ======
        self.log_handler = QTextEditHandler(self.log_window)
        formatter = logging.Formatter('%(message)s')  # Only log the message
        self.log_handler.setFormatter(formatter)

        self.logger = logging.getLogger("GUI_Log")
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.DEBUG)


        # Test logging
        self.logger.info("Welcome to yPlus calculator!")
        self.logger.info("Application started successfully.")
        # self.logger.warning("This is a warning message.")
        # self.logger.error("This is an error message.")



    def log_message(self, message, level=logging.INFO):

        self.logger.log(level, message)

    def clear_log(self):
        self.log_window.clear()
