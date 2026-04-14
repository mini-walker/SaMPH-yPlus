import sys  # Import system-specific parameters and functions
import os
import webbrowser
import logging
import subprocess
import time
import json

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
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter                              # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QObject, Slot, QThread      # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Impot the class from the local python files
from GUI.Utils import utils
from Algorithm.Calculate_yPlus import calculate_yPlus
#-----------------------------------------------------------------------





#-----------------------------------------------------------------------
# Class: Compute thread
class Compute_Thread(QThread):
    """
    Background computation thread.
    Launches a Fortran or Python calculation subprocess,
    monitors its progress file, and allows early termination via stop flag.
    """

    progress_signal = Signal(str)
    finished_signal = Signal(bool)

    def __init__(self, main_window):

        super().__init__(main_window)

        self.main_window = main_window

        # For input and output data
        self.usr_dir = utils.get_usr_dir()

        self.input_data_file_path  = self.usr_dir / "input_data.json"
        self.output_data_file_path = self.usr_dir / "output_data.json"
        self.calc_script    = Path(utils.resource_path("src/Algorithm/Calculate_yPlus.py")).resolve()
        self.base_dir       = Path(utils.resource_path("")).resolve()
        self.progress_path  = Path(utils.resource_path("usr/progress.txt")).resolve()
        self.stop_flag_path = Path(utils.resource_path("usr/stop.flag")).resolve()


    def run(self):

        """
        Run the external calculation process and emit progress updates.
        """

        # Determine calc file (Python or Fortran executable)
        calc_path = self.calc_script
        print(f'Calculation program path: {calc_path}')  # For debugging

        # self.progress_signal.emit(f"Checking calculation program: {calc_path}")
        # self.progress_signal.emit(f"Exists: {os.path.exists(calc_path)}")

        if not os.path.exists(calc_path):
            self.progress_signal.emit("Error: calculation program not found!")
            return
        
        # Send the message to log window that the file exists
        self.progress_signal.emit(f"Program exists: {os.path.exists(calc_path)}")

        # Start subprocess safely
        try:

            # Run the calculation program
            calculate_yPlus(
                progress_callback=lambda msg, **kwargs: self.progress_signal.emit(msg)
            )
            self.finished_signal.emit(True)
        
        except Exception as e:
            self.finished_signal.emit(False)      
            self.progress_signal.emit(f"Computing Error: {str(e)}")                              
            return

        self.finished_signal.emit(True)                   # Send the finished signal to the main window
        self.progress_signal.emit("Computing Finished.")
#-----------------------------------------------------------------------
