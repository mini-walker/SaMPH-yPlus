#-----------------------------------------------------------------------------------------
# Purpouse: Create the tool bar
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
    QFormLayout, QGridLayout, 
    QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter                          # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QEvent, QObject         # Import Qt core functionalities such as alignment
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


class Tool_Bar(QObject):

    """
    Helper to create the application's tools and toolbar-related actions.
    Call it from your main window after main window has been created:
    """

    show_menu_requested = Signal()
    export_requested = Signal() 
    show_setting_requested = Signal()
    show_keyboard_requested = Signal()
    show_log_requested = Signal()
    about_requested = Signal()
    
    # --------------------------------------------------------------------------------
    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent     # 
        self.tool_bar = None     # 
        self.language = parent.language_manager

        self.create_tool_bar()
    # --------------------------------------------------------------------------------


    # --------------------------------------------------------------------------------
    def create_tool_bar(self):

        # Create the tool bar
        self.tool_bar = self.parent.addToolBar("MainToolbar")
        self.tool_bar.setMovable(False)
        self.tool_bar.setFixedHeight(32)
        self.tool_bar.setIconSize(QSize(24, 24))
        # self.tool_bar.setMovable(False)                        # The tool bar cannot be moved

        # Create the tool actions, i.e., menu, export, settings, computing buttons.

        self.menu_action = QAction(
            QIcon(str(utils.resource_path("images/WIN11-Icons/icons8-menu-100.png"))), 
            self.language.get_text("Menu"), 
            self
        )
        self.export_action = QAction(
            QIcon(str(utils.resource_path("images/WIN11-Icons/icons8-export-100.png"))), 
            self.language.get_text("Export"), 
            self
        )
        self.setting_action = QAction(
            QIcon(str(utils.resource_path("images/WIN11-Icons/icons8-gear-100-2.png"))), 
            self.language.get_text("Settings"), 
            self
        )
        self.computing_action = QAction(
            QIcon(str(utils.resource_path("images/WIN11-Icons/icons8-calculate-100.png"))), 
            self.language.get_text("Compute"), 
            self
        )
        self.reset_action = QAction(
            QIcon(str(utils.resource_path("images/WIN11-Icons/icons8-calculate-100.png"))),
            self.language.get_text("Reset"),
            self
        )
        self.show_keyboard_action = QAction(
            QIcon(str(utils.resource_path("images/WIN11-Icons/icons8-keyboard-100.png"))),
            self.language.get_text("Show keyboard"),
            self
        )
        self.show_log_action = QAction(
            QIcon(str(utils.resource_path("images/WIN11-Icons/icons8-log-100.png"))),
            self.language.get_text("Show log"),
            self
        )
        self.about_action = QAction(
            QIcon(str(utils.resource_path("images/WIN11-Icons/icons8-about-100.png"))),
            self.language.get_text("About"),
            self
        )

        # Add the actions to the tool bar
        self.tool_bar.addAction(self.menu_action)
        self.tool_bar.addAction(self.export_action)
        self.tool_bar.addAction(self.setting_action)
        self.tool_bar.addAction(self.show_keyboard_action)
        self.tool_bar.addAction(self.show_log_action)
        self.tool_bar.addAction(self.about_action)
        # self.tool_bar.addAction(computing_action)


        #-----------------------------------------------------------------------------
        # Signals
        self.menu_action.triggered.connect(self._on_menu_clicked)
        self.export_action.triggered.connect(self._on_export_clicked)
        self.setting_action.triggered.connect(self._on_setting_clicked)
        self.show_keyboard_action.triggered.connect(self._on_show_keyboard_clicked)
        self.show_log_action.triggered.connect(self._on_show_log)
        self.about_action.triggered.connect(self._on_about_clicked)
        #-----------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    

    
    # --------------------------------------------------------------------------------
    # Slots for signals
    def _on_menu_clicked(self):
        print("Toolbar: emit menu_requested signal")
        self.show_menu_requested.emit()

    def _on_export_clicked(self):
        print("Toolbar: emit export_requested signal")
        self.export_requested.emit()
    
    def _on_setting_clicked(self):
        print("Toolbar: emit show_setting_requested signal")
        self.show_setting_requested.emit()

    def _on_show_keyboard_clicked(self):
        print("Toolbar: emit show_keyboard_requested signal")
        self.show_keyboard_requested.emit()
    
    def _on_show_log(self):
        print("Toolbar: emit show_log_requested signal")
        self.show_log_requested.emit()
    
    def _on_about_clicked(self):
        print("Toolbar: emit about_requested signal")
        self.about_requested.emit()
    #----------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------
    # Show the actions
    def actions(self):
        """Return the QAction list from the internal QToolBar."""
        return self.tool_bar.actions()
    #----------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------
    # Show the tool bar
    def setVisible(self, visible):
        self.tool_bar.setVisible(visible)
    #----------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------
    # Set the icon size
    def setIconSize(self, size: QSize):
        self.tool_bar.setIconSize(size)
    #----------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------
    # Update the UI texts fot the tool bar
    def update_ui_texts(self):
        
        """Update toolbar texts when language changes."""
        
        print("Updating toolbar language...")

        # Go through all the actions and change its name
        for action in self.tool_bar.actions():
            current_action_name = action.text()  # Current action name
            translated = self.language.get_text(current_action_name)
            action.setText(translated)

    #----------------------------------------------------------------------------------
    