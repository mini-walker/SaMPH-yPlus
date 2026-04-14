#-----------------------------------------------------------------------
# Purpouse: The operation controller for the user interface
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27  
#-----------------------------------------------------------------------


import sys  # Import system-specific parameters and functions
import os
import webbrowser
import logging
import subprocess
import time
import json
import pandas as pd

from pathlib import Path
from urllib.parse import quote_plus

#-----------------------------------------------------------------------
# Import PyQt5 widgets for UI elements
from PySide6.QtWidgets import ( 
    QApplication, 
    QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog,
    QLabel, QFileDialog, QAbstractButton, QWidget, QStackedWidget, QTabWidget,    
    QLineEdit, QSplitter, 
    QPushButton, QRadioButton, QButtonGroup, QWidgetAction,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QTreeWidget, QTreeWidgetItem, QCheckBox,
    QFormLayout, QGridLayout, QDialog, QDialogButtonBox, QComboBox,
    QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter, QColor                      # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QObject, Slot, QThread      # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Impot the class from the local python files
from GUI.Utils import utils
from GUI.Virtual_Keyboard import CalculatorKeyboard
from GUI.Page_Log import LogWidget, QTextEditHandler
from GUI.Operation_Mainwindow import Operation_Mainwindow_Controller
#-----------------------------------------------------------------------




#-----------------------------------------------------------------------
class Operation_Setting_Controller(QObject):

    def __init__(self, main_window):
        """
        Controller for applying settings to the main application UI.

        Args:
            main_window (QMainWindow): The main window instance of the application.
        """
        self.main_window = main_window
        self.operation_mainwindow  = Operation_Mainwindow_Controller(self.main_window) 
        

        # Get the QSettings file path
        usr_folder = utils.get_usr_dir()
        self.settings_file_path = usr_folder / "settings.ini"


    #-----------------------------------------------------------------------
    def apply_new_settings(self):
        """
        Apply new settings from settings.ini to the main application.

        This function reads the .ini file and updates:
        - Font (type and size) for text-based widgets only
        - Theme / Appearance
        - Toolbar icon visibility and size
        - Language
        """
        # 1. Load settings
        settings = QSettings(str(self.settings_file_path), QSettings.Format.IniFormat)

        # ---------------- Font Settings ----------------
        font_type = settings.value("Font/type", "Times New Roman")
        font_size = int(settings.value("Font/size", "10"))
        app_font = QFont(font_type, font_size)
        QApplication.instance().setFont(app_font)

        # Apply font only to text-based widgets (avoid toolbar)
        text_widgets = (QTextEdit, QLineEdit, QComboBox, QPushButton, QLabel)
        for cls in text_widgets:
            for widget in self.main_window.findChildren(cls):
                widget.setFont(app_font)

        # ---------------- Appearance / Theme ----------------
        appearance_mode = settings.value("Appearance/theme", "Light")  # Light, Dark, Blue
        
        # Set background color 
        central_widget = self.main_window.centralWidget()
        if appearance_mode.lower() == "dark":
            central_widget.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")
        elif appearance_mode.lower() == "blue":
            central_widget.setStyleSheet("background-color: #DCE6F1; color: #000000;")
        else:
            central_widget.setStyleSheet("background-color: #FFFFFF; color: #000000;")


        # ---------------- Toolbar Icons ----------------
        show_toolbar_icons = settings.value("Appearance/toolbar_icons", True, type=bool)
        if hasattr(self.main_window, "tool_bar"):
            self.main_window.tool_bar.setVisible(show_toolbar_icons)


        # ---------------- Language Settings ----------------
        language_type = settings.value("Language/type", "English")
        new_language = "Chinese" if language_type.startswith("Chinese") else "English"
        self.main_window.language_manager.set_language(new_language)

        # self.setWindowTitle(self.main_window.language_manager.get_text("yPlus Calculator"))
        self.main_window.tool_bar.update_ui_texts()
        self.main_window.menu_page.update_ui_texts()
        self.main_window.update_ui_texts()

        # ---------------- Search Settings ----------------
        use_baidu  = settings.value("Search/Baidu", True, type=bool)
        use_google = settings.value("Search/Google", False, type=bool)

        # Connetc signal from the search button
        try:
            self.main_window.search_requested.disconnect()
        except TypeError:
            # Ignore if the signal is not connected
            pass

        if use_baidu and not use_google:
            search_engine = "Baidu"
            self.main_window.search_requested.connect(self.operation_mainwindow.perform_baidu_search)
        elif use_google and not use_baidu:
            search_engine = "Google"
            self.main_window.search_requested.connect(self.operation_mainwindow.perform_google_search)
        else:
            search_engine = "Baidu"
            self.main_window.search_requested.connect(self.operation_mainwindow.perform_baidu_search)  # default



        # ---------------- Notify / Log ----------------
        if hasattr(self.main_window, "log_widget"):
            self.main_window.log_widget.log_message(f"Applied settings from ini:")
            self.main_window.log_widget.log_message(f"Font={font_type} {font_size}pt", level=logging.WARNING)
            self.main_window.log_widget.log_message(f"Theme={appearance_mode}, Language={language_type}", level=logging.WARNING)
            self.main_window.log_widget.log_message(f"Toolbar icons={'On' if show_toolbar_icons else 'Off'}", level=logging.WARNING)
            self.main_window.log_widget.log_message(f"Search engine={search_engine}", level=logging.WARNING)

    #-----------------------------------------------------------------------

