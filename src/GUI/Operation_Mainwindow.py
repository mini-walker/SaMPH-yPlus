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
import difflib

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
from GUI.Virtual_Keyboard import CalculatorKeyboard
from GUI.Page_Log import LogWidget, QTextEditHandler
from GUI.Operation_Computing import Compute_Thread
#-----------------------------------------------------------------------




#-----------------------------------------------------------------------
class Operation_Mainwindow_Controller(QObject):

    def __init__(self, main_window):

        super().__init__(main_window)

        self.main_window = main_window

        self.keyboard_widget = None

        self.log_widget = None
        self.log_stream = None

        # Get the language manager from the main window
        self.lang_manager = getattr(self.main_window, "language_manager", None) 


    # ----------------------- Signal Handlers ------------------------
    # ----------------------------------------------------------------
    def handle_show_keyboard(self):

        print("Toolbar: Show keyboard")

        # Send message to log window
        self.main_window.log_widget.log_message(f"Create tab: Keyboard.", level=logging.INFO)

        # Check if the tab widget exists firstly
        if not hasattr(self.main_window, "log_and_keyboard_tab_widget"):
            return
        else:
            print("TabWidget is exists.")

        tab_widget = self.main_window.log_and_keyboard_tab_widget
        bottom_background = self.main_window.bottom_background_label

        # Hide the tab widget and show the bottom background， as the background is active in the close tab function
        bottom_background.hide()
        tab_widget.show()

        # Check if the keyboard tab already exists
        for i in range(tab_widget.count()):
            if tab_widget.tabText(i) == "Keyboard":
                tab_widget.setCurrentIndex(i)
                print("Keyboard tab already exists → just show it")
                self.main_window.log_widget.log_message(f"Show tab: Keyboard.", level=logging.INFO)
                return

        # Create a new keyboard tab
        self.keyboard_widget = CalculatorKeyboard()   # KeyboardWidget(self) is in the Virtual_Keyboard.py
        tab_widget.addTab(self.keyboard_widget, "Keyboard")
        tab_widget.setCurrentWidget(self.keyboard_widget)
        print("New Keyboard tab created")
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    def handle_show_log(self):

        print("Toolbar: Show log")

        # Check if the tab widget exists firstly
        if not hasattr(self.main_window, "log_and_keyboard_tab_widget"):
            return
        else:
            print("TabWidget is exists.")

        tab_widget = self.main_window.log_and_keyboard_tab_widget
        bottom_background = self.main_window.bottom_background_label

        # Hide the tab widget and show the bottom background， as the background is active in the close tab function
        bottom_background.hide()
        tab_widget.show()

        # Check if the keyboard tab already exists
        for i in range(tab_widget.count()):
            if tab_widget.tabText(i) == "Log":
                tab_widget.setCurrentIndex(i)
                print("Log tab already exists → just show it")
                self.main_window.log_widget.log_message(f"Show tab: Log.", level=logging.INFO)
                return

        # Create a new keyboard tab
        self.log_widget = LogWidget(self.main_window)       # LogWidget(self) is in the Page_Log.py
        tab_widget.addTab(self.log_widget, "Log")
        tab_widget.setCurrentWidget(self.log_widget)

        # Send message to log window
        self.main_window.log_widget.log_message(f"Create tab: Log.", level=logging.INFO)

        print("New Log tab created")
    # ----------------------------------------------------------------


    # ----------------------------------------------------------------
    # Show the perference setting dialog
    def handle_show_setting(self):

        print("Toolbar: Show setting")

        # Send message to log window
        self.main_window.log_widget.log_message(f"Display the 'Setting' dialog", level=logging.INFO)

        # Show the setting dialog
        self.main_window.setting_page.show()

    # ----------------------------------------------------------------



    # ----------------------------------------------------------------
    #  Show the "about" dialog
    def handle_about(self):
        """
        Display the "About" dialog.
        Display different language content based on self.language ('zh' or 'en').
        """

        # Send message to log window
        self.main_window.log_widget.log_message(f"Display the 'About' dialog", level=logging.INFO)

        #----------------------------------------------------------------
        # Get current language from main_window
        # You can define self.language = 'zh' or 'en' in main_window
        #----------------------------------------------------------------
        # lang = getattr(self.main_window, "language", "en")  # The default language is "en".
        lang = getattr(self.lang_manager, "language", "Enlish")

        #===================== 中文内容 =====================#
        if lang == "Chinese":
            title = "关于软件"
            html_content = """
            <div align="justify" style="font-size: 13px; line-height: 1.6; text-align: justify;">
                <p style="font-family: 'STFangsong', 'SimSun', 'Songti SC'; font-size: 13px;">
                    <b>软件用途：</b><br>
                    本软件用于湍流计算中边界层厚度和第一层网格高度的估算。
                </p>

                <p style="font-family: 'STFangsong', 'SimSun', 'Songti SC'; font-size: 13px;">
                    <b>参考文献：</b><br>
                    1. White, Frank M. 2011. Fluid Mechanics. 7th ed. New York: McGraw-Hill Science, Engineering & Mathematics.<br>
                    2. Spurk, H.J. and Aksel, N., 2008. Fluid mechanics. Berlin, Heidelberg: Springer Berlin Heidelberg.<br>
                    3. Jin, S., Zha, R., Peng, H., Qiu, W. and McTaggart, K., 2024. Determination of Maneuvering Force Coefficients for a Destroyer Model with OpenFOAM. Journal of Ship Research, 68(02), pp.39-65.<br>
                    4. Jin, S., Zha, R., Peng, H., Qiu, W. and Gospodnetic, S., 2020, September. 2D CFD studies on effects of leading-edge propeller manufacturing defects on cavitation performance. In SNAME Maritime Convention (p. D033S015R003). SNAME.<br>
                    5. Jin, S., Peng, H. and Qiu, W., 2024. Numerical study on effects of leading-edge manufacturing defects on cavitation performance of a full-scale propeller. I. Simulation for the model-and full-scale propellers without defect. Physics of Fluids, 36(10).<br>
                </p>

                <p style="font-family: 'STFangsong', 'SimSun', 'Songti SC'; font-size: 13px;">
                    <b>版本：</b>1.0.0 (2025.10)
                </p>

                <p style="font-family: 'STFangsong', 'SimSun', 'Songti SC'; font-size: 13px;">
                    <b>所有权：</b><br>
                    © 2025 高性能水动力学软件开发组。保留所有权利。
                </p>
            </div>
            """
            ok_text = "确定"

        #===================== English content =====================#
        else:
            title = "About"
            html_content = """
            <div align="justify" style="font-size: 13px; style="font-family: 'Times New Roman'; line-height: 1.6; text-align: justify;">
                <p style="font-family: 'Times New Roman'; font-size: 13px;">
                    <b>Software purpose:</b><br>
                    This software is used to estimate boundary layer thickness and the first-layer grid height in simulations with turbulent flow.
                </p>

                <p style="font-family: 'Times New Roman'; font-size: 13px;">
                    <b>References:</b><br>
                    1. White, Frank M. 2011. Fluid Mechanics. 7th ed. New York: McGraw-Hill Science, Engineering & Mathematics.<br>
                    2. Spurk, H.J. and Aksel, N., 2008. Fluid mechanics. Berlin, Heidelberg: Springer Berlin Heidelberg.<br>
                    3. Jin, S., Zha, R., Peng, H., Qiu, W. and McTaggart, K., 2024. Determination of Maneuvering Force Coefficients for a Destroyer Model with OpenFOAM. Journal of Ship Research, 68(02), pp.39-65.<br>
                    4. Jin, S., Zha, R., Peng, H., Qiu, W. and Gospodnetic, S., 2020, September. 2D CFD studies on effects of leading-edge propeller manufacturing defects on cavitation performance. In SNAME Maritime Convention (p. D033S015R003). SNAME.<br>
                    5. Jin, S., Peng, H. and Qiu, W., 2024. Numerical study on effects of leading-edge manufacturing defects on cavitation performance of a full-scale propeller. I. Simulation for the model-and full-scale propellers without defect. Physics of Fluids, 36(10).<br>
                </p>

                <p style="font-family: 'Times New Roman'; font-size: 13px;">
                    <b>Version:</b> 1.0.0 (2025.10)
                </p>

                <p style="font-family: 'Times New Roman'; font-size: 13px;">
                    <b>Ownership:</b><br>
                    © 2025 Shanqin Jin. All rights reserved.<br>
                    This software and its source code are protected under applicable intellectual property laws.
                </p>
            </div>
            """
            ok_text = "OK"

        #===================== 构建对话框 =====================#
        about_dialog = QDialog(self.main_window)
        about_dialog.setWindowTitle(title)
        about_dialog.setMinimumWidth(350)
        about_dialog.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()
        layout.setSpacing(10)

        lbl = QLabel()
        lbl.setTextFormat(Qt.RichText)
        lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        lbl.setWordWrap(True)
        lbl.setText(html_content)
        lbl.setAlignment(Qt.AlignJustify)
        layout.addWidget(lbl)

        # button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        # button_box.button(QDialogButtonBox.Ok).setText(ok_text)
        # button_box.accepted.connect(about_dialog.accept)
        # layout.addWidget(button_box, alignment=Qt.AlignCenter)

        about_dialog.setLayout(layout)
        about_dialog.resize(350, 500)
        about_dialog.exec()
    # ----------------------------------------------------------------


    # ----------------------------------------------------------------
    # The function to perform Baidu search
    def perform_baidu_search(self):
            
        query = self.main_window.search_edit.text().strip()
        if query:
            encoded_query = quote_plus(query)
            url = f"https://www.baidu.com/s?wd={encoded_query}"
        else:
            url = "https://www.baidu.com"

        webbrowser.open(url)

        # Send message to log window
        self.main_window.log_widget.log_message(f"Baidu search: {query}.", level=logging.INFO)

        # self.main_window.close()  # Close dialog after search
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # The function to perform google search
    def perform_google_search(self):
        query = self.main_window.search_edit.text().strip()
        if query:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        else:
            url = "https://www.google.com"

        webbrowser.open(url)

        # Send message to log window
        self.main_window.log_widget.log_message(f"Google search: {query}.", level=logging.INFO)

        # Close the window after search
        # self.main_window.close()
    # ----------------------------------------------------------------



    # ----------------------------------------------------------------
    # The function to handle computing
    def handle_compute(self):

        # Check if the validation of the input data is successful
        main_window  = self.main_window
        input_layout = self.main_window.input_layout

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Collect input data from QFormLayout
        input_data = {}

        for i in range(input_layout.rowCount()):

            # Get label and field widgets
            label_item = input_layout.itemAt(i, QFormLayout.LabelRole)
            field_item = input_layout.itemAt(i, QFormLayout.FieldRole)
            label_widget = label_item.widget() if label_item else None
            field_widget = field_item.widget() if field_item else None

            if label_widget and field_widget:

                # Use objectName for stable reference, fallback to "Row_i"
                input_object_name = label_widget.objectName() or f"Row_{i}"
                label_display_name = input_object_name.replace("_", " ")  # For messages
                text = field_widget.text().strip() # Get the line edit text

                # Skip validation if optional field is empty
                if input_object_name == "grid_stretch_ratio":
                    
                    print(f"Check the value of {label_display_name}.")

                    # allow empty value
                    if not text:
                        # Empty: just skip validation and don't save
                        continue

                    # Check if the field is QLineEdit and validate
                    try:
                        val = float(text)
                        if abs(val - 1.0) <= 1.0E-8:
                            QMessageBox.warning(
                                main_window, "Input Error",
                                f"The value of {label_display_name} should be greater than 1.0"
                            )
                            return
                    except ValueError:
                        QMessageBox.warning(
                            main_window, "Input Error",
                            f"The value of {label_display_name} must be a number"
                        )
                        return
                        
                # ------------------------------------------------------------
                # Save only non-empty fields
                # ------------------------------------------------------------
                if text:
                    input_data[input_object_name] = text


                # Check if the field is QLineEdit and validate
                if isinstance(field_widget, QLineEdit):
                    text = field_widget.text().strip()
                    if not text:
                        QMessageBox.warning(main_window, "Input Error", f"{label_display_name} cannot be empty")
                        return
                    try:
                        val = float(text)
                    except ValueError:
                        QMessageBox.warning(main_window, "Input Error", f"{label_display_name} must be a number")
                        return

                    # Store the text value, not the widget
                    input_data[input_object_name] = text

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Collect data from combo boxes
        combo_controls = {
            "spatial_discretization_scheme": self.main_window.scheme_combo,
            "skin_friction_formula": self.main_window.skin_friction_combo,
            "boundary_layer_formula": self.main_window.boundary_layer_combo
        }

        for key, widget in combo_controls.items():
            input_data[key] = widget.currentText()

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Save input data as JSON
        usr_dir = utils.get_usr_dir()
        file_path = usr_dir / "input_data.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(input_data, f, indent=4, ensure_ascii=False)
            self.main_window.log_widget.log_message(
                f"All input data are saved to {file_path}.", level=logging.INFO
            )


        # Send message to log window
        self.main_window.log_widget.log_message(f"Start computing ...", level=logging.INFO)


        # Create the compute thread in the main window
        self.main_window.compute_thread = Compute_Thread(self.main_window)


        # Connect signal to the finish function
        # As the finished_signal is a signal, not bool, it cannot be used directly
        self.main_window.compute_thread.finished_signal.connect(self.on_compute_finished)
        self.main_window.compute_thread.progress_signal.connect(self.main_window.log_widget.log_message)

        self.main_window.compute_thread.start()  # Start the thread and run with the subthread

    # ----------------------------------------------------------------





    # ----------------------------------------------------------------
    # # Load the calculation results when the computing was finished
    def on_compute_finished(self):

        """
        Read results.json and display values in the output QFormLayout.
        Uses widget objectName to match the JSON keys.
        """
        print("Load the calculation results and display them!")

        output_layout = self.main_window.output_layout

        # Open the result file
        usr_dir   = utils.get_usr_dir()
        results_file = usr_dir / "results.json"
        
        # Check the result file exist
        if not results_file.exists():
            print(f"No results file found: {results_file}.")
            return

        # Open the result file
        try:

            with open(results_file, "r", encoding="utf-8") as f:
                result_data = json.load(f)
        except Exception as e:
            print(f"Results JSON loading failed: {e}")
            return


        # ------------------------------------------------------------
        def find_best_match(key, candidates, cutoff=0.7):
            """
            Find the best match for 'key' from a list of 'candidates' based on similarity.
            Returns the best candidate if similarity > cutoff, else None.
            """
            matches = difflib.get_close_matches(key, candidates, n=1, cutoff=cutoff)
            return matches[0] if matches else None
        # ------------------------------------------------------------


        # Show the results on GUI
        for j in range(output_layout.rowCount()):

            # Get the label and field item
            label_item = output_layout.itemAt(j, QFormLayout.LabelRole)
            field_item = output_layout.itemAt(j, QFormLayout.FieldRole)
            
            if not label_item or not field_item:
                continue

            label_widget = label_item.widget()
            field_widget = field_item.widget()

            if not (label_widget and field_widget):
                continue


            # Normalize the object name: replace underscores with spaces
            obj_name = label_widget.objectName().replace("_", " ")

            # Find the best match in JSON keys
            best_match = find_best_match(obj_name, result_data.keys(), cutoff=0.6)
            if best_match:
                field_widget.setText(str(result_data[best_match]))
            else:
                field_widget.setText("")
    # ----------------------------------------------------------------


    # ----------------------------------------------------------------
    # The function to handle reset
    def handle_reset(self):

        # Send message to log window
        self.main_window.log_widget.log_message(f"Clear the input data and results.", level=logging.WARNING)

        # Get the main window, input layout and output layout
        main_window   = self.main_window
        input_layout  = self.main_window.input_layout
        output_layout = self.main_window.output_layout

        # Clear the input data
        for i in range(input_layout.rowCount()):
            input_layout.itemAt(i, QFormLayout.FieldRole).widget().setText("")

        # Clear the output data
        for i in range(output_layout.rowCount()):
            output_layout.itemAt(i, QFormLayout.FieldRole).widget().setText("")

        # Clear the log window
        self.main_window.log_widget.clear_log()
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # The function to handle material library
    def handle_material_change(self, text: str):

        # Send message to log window
        if text == "": 
            self.main_window.log_widget.log_message(f"Please enter the material properties manually.", level=logging.WARNING)
        else:
            self.main_window.log_widget.log_message(f"Change material to: {text}", level=logging.INFO)

        # Get the main window, input layout and output layout
        main_window   = self.main_window
        input_layout  = self.main_window.input_layout
        
        if "Fresh water" in text or "淡水" in text: 
            input_layout.itemAt(1, QFormLayout.FieldRole).widget().setText("998.2")
            input_layout.itemAt(2, QFormLayout.FieldRole).widget().setText("0.00100160")

        elif "Sea water" in text or "海水" in text: 
            input_layout.itemAt(1, QFormLayout.FieldRole).widget().setText("1025.0")
            input_layout.itemAt(2, QFormLayout.FieldRole).widget().setText("0.00109000")

        elif "Air" in text or "空气" in text:  
            input_layout.itemAt(1, QFormLayout.FieldRole).widget().setText("1.204")
            input_layout.itemAt(2, QFormLayout.FieldRole).widget().setText("0.00001825")
    # ----------------------------------------------------------------


    # ----------------------------------------------------------------
    # Export the data from the output region to an Excel or CSV file
    # ----------------------------------------------------------------
    def handle_export(self):
        """
        Export all results displayed in the output_layout to a user-selected
        Excel (.xlsx) or CSV file.  HTML tags that are used for rich-text
        display in the GUI are stripped before writing.
        """

        # Get the main window, input layout and output layout
        main_window   = self.main_window
        input_layout  = self.main_window.input_layout
        output_layout = self.main_window.output_layout


        # 1. Save-file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            main_window,
            "Export Results",
            "yPlus_results.xlsx",
            "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return

        # 2. Gather data from the QFormLayout
        data = {}
        for row in range(output_layout.rowCount()):
            label_item = output_layout.itemAt(row, QFormLayout.LabelRole)
            field_item = output_layout.itemAt(row, QFormLayout.FieldRole)
            if not label_item or not field_item:
                continue

            label_widget = label_item.widget()
            field_widget = field_item.widget()
            if not label_widget or not field_widget:
                continue

            # ----  Clean the label text  ----
            raw_label = label_widget.text()                # e.g. "Estimated boundary layer thickness, <i>δ</i> (m):"
            clean_label = self._strip_html(raw_label)      # → "Estimated boundary layer thickness, δ (m)"
            clean_label = clean_label.rstrip(":").strip()  # remove trailing colon

            value = field_widget.text()
            data[clean_label] = value

        if not data:
            QMessageBox.warning(main_window, "No Data", "No results to export.")
            return

        # 3. Write file
        try:
            df = pd.DataFrame(list(data.items()), columns=["Item", "Result"])

            if file_path.lower().endswith('.csv'):
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
            else:
                df.to_excel(file_path, index=False, engine='openpyxl')

            QMessageBox.information(main_window, "Export Successful",
                                    f"Results saved to:\n{file_path}")
            self.main_window.log_widget.log_message(f"Results exported to {file_path}")
        except Exception as e:
            QMessageBox.critical(main_window, "Export Failed",
                                f"Could not save file:\n{str(e)}")
            self.main_window.log_widget.log_message(
                f"Export failed: {e}", level=logging.ERROR)

    # ----------------------------------------------------------------
    # Helper: strip simple HTML tags (<i>, <b>, <font …>)
    # ----------------------------------------------------------------
    @staticmethod
    def _strip_html(text: str) -> str:
        """Remove <i>, <b>, <font …> tags and keep the content."""
        import re
        # Replace <i>…</i>, <b>…</b>, etc. with the inner text
        return re.sub(r'</?(i|b|font|span)[^>]*>', '', text)
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # Show menu page
    def handle_show_menu_page(self):

        # Get the main window and menu page
        main_window = self.main_window
        menu_page   = self.main_window.menu_page

        # Show the menu page from left side with sliding anmimation
        if menu_page.isVisible():

            menu_page.slide_out()
            self.main_window.log_widget.log_message(f"Show menu page.", level=logging.INFO)

        else:
            menu_page.slide_in()
            self.main_window.log_widget.log_message(f"Hide menu page.", level=logging.INFO)
