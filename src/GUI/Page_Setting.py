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
    QPushButton, QRadioButton, QButtonGroup, QWidgetAction,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QTreeWidget, QTreeWidgetItem, QCheckBox,
    QFormLayout, QGridLayout, QDialog, QDialogButtonBox, QComboBox,
    QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter   # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings   # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Impot the class from the local python files
from GUI.Utils import utils
#-----------------------------------------------------------------------------------------

from PySide6.QtCore import QSettings

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                               QStackedWidget, QDialogButtonBox, QTabWidget, QLineEdit, QLabel,
                               QComboBox, QCheckBox, QMessageBox, QPushButton)

class Setting_Window(QDialog):
    """
    A modal dialog for configuring application preferences, including General, Font, Appearance,
    AI tool, and Advanced settings. Settings are saved to QSettings for persistence and loaded
    when the dialog is opened.
    """

    # Define a custom signal that can send a string message to log window
    # It is used to send string messages to the log window
    settings_page_operation_signal = Signal(str)

    # Signal to notify main application to apply new settings
    apply_settings_signal = Signal()

    def __init__(self, main_window):
        """
        Initialize the PreferenceWindow dialog.

        Args:
            parent: The parent widget (typically the main window). Defaults to None.
        """
    
        super().__init__()

        self.main_window = main_window
        

        self.setWindowTitle("Preferences")  # Set dialog title
        self.resize(480, 300)  # Set dialog size

        #---------------------------------------------------------------------------------
        # Create 'usr' folder if it doesn't exist for saving setting files
        usr_folder = utils.get_usr_dir()
        os.makedirs(usr_folder, exist_ok = True)
        print(f"'usr' folder is ready at: {os.path.abspath(usr_folder)}")

        # Initialize QSettings for persistent storage
        setting_file_path = usr_folder / "settings.ini"
        self.settings = QSettings(str(setting_file_path), QSettings.Format.IniFormat)
        print(f"QSettings file: {self.settings.fileName()}")  # Debug: Print storage path
        #---------------------------------------------------------------------------------


        #---------------------------------------------------------------------------------
        # Main horizontal layout for tree menu and stacked widget
        main_layout = QHBoxLayout()

        # Left side: Tree widget for navigation
        self.preference_tree = QTreeWidget()
        self.preference_tree.setHeaderHidden(True)  # Hide tree header
        main_layout.addWidget(self.preference_tree, 1)  # Allocate 1/4 width

        # Add top-level items to the tree
        font_item = QTreeWidgetItem(["Font"])
        search_item = QTreeWidgetItem(["Search"])
        language_item = QTreeWidgetItem(["Language"])
        appearance_item = QTreeWidgetItem(["Appearance"])
        advanced_item = QTreeWidgetItem(["Advanced"])
        self.preference_tree.addTopLevelItems([font_item, search_item, language_item,  appearance_item, advanced_item])
        #---------------------------------------------------------------------------------


        #---------------------------------------------------------------------------------
        # Right side: Stacked widget for displaying settings pages
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, 3)  # Allocate 3/4 width

        # Dictionary to store references to controls for saving/loading
        self.controls = {
            "Font": {},
            "Search": {},
            "Language": {},
            "Appearance": {},
            "Advanced": {}
        }

        # Create pages in settings
        self.font_page = self.create_font_page_in_setting()
        self.search_page = self.create_search_page_in_setting()
        self.language_page = self.create_language_page_in_setting()
        self.appearance_page = self.create_appearance_page_in_setting()
        self.advanced_page = self.create_advanced_page_in_setting()
        

        # Add pages to stacked widget
        self.stack.addWidget(self.language_page)
        self.stack.addWidget(self.font_page)
        self.stack.addWidget(self.appearance_page)
        self.stack.addWidget(self.search_page)
        self.stack.addWidget(self.advanced_page)
        

        # Connect tree selection changes to page switching
        self.preference_tree.currentItemChanged.connect(self.change_page)
        self.preference_tree.setCurrentItem(search_item)  # Default to General page

        # Bottom buttons: OK and Cancel
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)  # Save settings and close
        buttons.rejected.connect(self.reject)  # Discard changes and close

        # Main vertical layout: Combine main_layout and buttons
        layout = QVBoxLayout(self)
        layout.addLayout(main_layout)
        layout.addWidget(buttons)



    #-------------------------------------------------------------------------------------
    def accept(self):
        """
        Save all settings to QSettings when OK is clicked and close the dialog.

        This function iterates through all pages of the preferences dialog
        and writes the current values of all controls to persistent storage.
        After saving, a confirmation message box is shown to the user, and the
        dialog is closed.
        """

        # -------- Clear all saved preferences from QSettings ---
        self.settings.clear()
        self.settings.sync()

        # ------------------ General Settings ------------------

        # ------------------ Font Settings ------------------
        font = self.controls.get("Font", {})
        if "type" in font:
            value = font["type"].currentText()
            self.settings.setValue("Font/type", value)
            print(f"Saving Font: type={value}")
        if "size" in font:
            value = font["size"].currentText()
            self.settings.setValue("Font/size", value)
            print(f"Saving Font: size={value}")

        # ------------------ Appearance Settings ------------------
        appearance = self.controls.get("Appearance", {})
        if "theme" in appearance:
            value = appearance["theme"].currentText()
            self.settings.setValue("Appearance/theme", value)
            print(f"Saving Appearance: theme={value}")

        if "toolbar_icons" in appearance:
            key = "toolbar_icons"
            value = appearance[key].isChecked()
            self.settings.setValue(f"Appearance/{key}", value)
            print(f"Saving Appearance: {key}={value}")




        # ------------------ Advanced Settings ------------------
        # No input fields in Advanced page now; only a reset button exists,
        # so nothing needs to be saved from this page.

        # ------------------ Search Settings ------------------
        search = self.controls.get("Search", {})
        for key, ctrl in search.items():
            value = ctrl.isChecked()
            self.settings.setValue(f"Search/{key}", value)
            print(f"Saving Search: {key}={value}")

        # ------------------ Language Settings ------------------
        language = self.controls.get("Language", {})
        if "type" in language:
            value = language["type"].currentText()
            self.settings.setValue("Language/type", value)
            print(f"Saving Language: type={value}")

        # Write all settings to disk
        self.settings.sync()

        # ------------------ Emit Signals ------------------
        self.settings_page_operation_signal.emit("Settings saved successfully!")  # For log window
        self.apply_settings_signal.emit()  # Trigger immediate application of new settings

        # ------------------ Inform User ------------------
        QMessageBox.information(self, "Preferences", "Settings saved successfully!")

        # Close the dialog
        super().accept()
    #-------------------------------------------------------------------------------------






    #-------------------------------------------------------------------------------------
    def reject(self):
        """
        Discard changes and close the dialog when Cancel is clicked.
        """
        print("Settings discarded")
        self.settings_page_operation_signal.emit("Settings discarded!")

        super().reject()  # Close dialog with QDialog.Rejected
    #-------------------------------------------------------------------------------------


    #-------------------------------------------------------------------------------------
    def create_language_page_in_setting(self):
        """
        Create the General settings page with notification and startup checkboxes.

        Returns:
            QWidget: The configured General settings page.
        """
         
        print("Language page created")

        page = QWidget()
        layout = QVBoxLayout(page)
        # layout.addWidget(QLabel("General settings:"))

        # Font type selection
        layout.addWidget(QLabel("Language type:"))
        language_combo = QComboBox()
        language_combo.addItems(["English", "Chinese"])
        saved_font = self.settings.value("Language/type", "English")
        language_combo.setCurrentText(saved_font)
        layout.addWidget(language_combo)
        self.controls["Language"]["type"] = language_combo

        layout.addStretch()  # Push content to top

        return page
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    def create_appearance_page_in_setting(self):
        """
        Create the Appearance settings page with a theme selection dropdown and
        a grouped section for additional appearance options (e.g., toolbar icons).

        Structure:
        - Theme mode selection: "Light", "Dark", or "Blue"
        - Group box: contains various appearance-related checkboxes

        Returns:
            QWidget: The configured Appearance settings page.
        """
        from PySide6.QtWidgets import QGroupBox

        # Create page and layout
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Appearance settings:"))

        # -------------------------------------------------------------------------
        # 1. Theme mode selection
        # -------------------------------------------------------------------------
        layout.addWidget(QLabel("Theme mode:"))

        mode_combo = QComboBox()
        mode_combo.addItems(["Light", "Dark", "Blue"])

        # Load saved theme mode, default to "Light"
        saved_mode = self.settings.value("Appearance/theme", "Light")
        if saved_mode not in ["Light", "Dark", "Blue"]:
            saved_mode = "Light"
        mode_combo.setCurrentText(saved_mode)

        layout.addWidget(mode_combo)
        self.controls["Appearance"]["theme"] = mode_combo

        # -------------------------------------------------------------------------
        # 2. Group box for additional appearance options
        # -------------------------------------------------------------------------
        group_box = QGroupBox("Options")
        group_layout = QVBoxLayout(group_box)

        # Checkbox for showing toolbar icons
        toolbar_icons = QCheckBox("Show toolbar icons")
        toolbar_icons.setChecked(self.settings.value("Appearance/toolbar_icons", True, type=bool))
        toolbar_icons.setChecked(True)  # Default active
        group_layout.addWidget(toolbar_icons)
        self.controls["Appearance"]["toolbar_icons"] = toolbar_icons
        

        # Add group box to main layout
        layout.addWidget(group_box)

        # -------------------------------------------------------------------------
        # Final layout adjustments
        # -------------------------------------------------------------------------
        layout.addStretch()  # Push everything to the top

        return page
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    def create_advanced_page_in_setting(self):
        """
        Create the Advanced settings page with a reset button.

        Returns:
            QWidget: The configured Advanced settings page.
        """
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Advanced settings:"))

        # Button to reset all preferences
        reset_button = QPushButton("Reset preferences")
        reset_button.clicked.connect(self.reset_preferences)
        layout.addWidget(reset_button)

        layout.addStretch()
        return page
    #-------------------------------------------------------------------------------------



    #-------------------------------------------------------------------------------------
    def create_search_page_in_setting(self):
        """
        Create the search tool settings page with mutually exclusive options
        for Baidu and Google using QButtonGroup.

        Returns:
            QWidget: The configured search settings page.
        """
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Search engine:"))

        # ----- Create radio buttons -----
        baidu_radio = QRadioButton("Baidu")
        google_radio = QRadioButton("Google")

        # Set initial selection from settings
        baidu_selected = self.settings.value("Search/Baidu", True, type=bool)
        google_selected = self.settings.value("Search/Google", False, type=bool)

        # Ensure only one is selected
        if baidu_selected and not google_selected:
            baidu_radio.setChecked(True)
        elif google_selected and not baidu_selected:
            google_radio.setChecked(True)
        else:
            baidu_radio.setChecked(True)  # Default fallback

        # ----- Add radio buttons to a button group for mutual exclusivity -----
        button_group = QButtonGroup(page)
        button_group.addButton(baidu_radio)
        button_group.addButton(google_radio)
        button_group.setExclusive(True)  # Ensure only one can be checked

        # ----- Add widgets to layout -----
        layout.addWidget(baidu_radio)
        layout.addWidget(google_radio)

        # Store controls for later access
        self.controls["Search"]["Baidu"] = baidu_radio
        self.controls["Search"]["Google"] = google_radio

        layout.addStretch()  # Push content to top

        print("Search page created")

        return page
    #-------------------------------------------------------------------------------------


    #-------------------------------------------------------------------------------------
    def create_font_page_in_setting(self):
        """
        Create the Font settings page with font type and size selection.

        Returns:
            QWidget: The configured Font settings page.
        """
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Font settings:"))

        # Font type selection
        layout.addWidget(QLabel("Font type:"))
        font_combo = QComboBox()
        font_combo.addItems(["Arial", "Calibri", "Times New Roman", "Courier New", "STFangsong", "SimSun", "Songti SC", "KaiTi"])
        saved_font = self.settings.value("Font/type", "Times New Roman")
        font_combo.setCurrentText(saved_font)
        layout.addWidget(font_combo)
        self.controls["Font"]["type"] = font_combo

        # Font size selection
        layout.addWidget(QLabel("Font size:"))
        size_combo = QComboBox()
        size_combo.addItems([str(s) for s in range(8, 25)])
        saved_size = self.settings.value("Font/size", "10")
        size_combo.setCurrentText(saved_size)
        layout.addWidget(size_combo)
        self.controls["Font"]["size"] = size_combo

        layout.addStretch()
        return page
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Reset the settings
    def reset_preferences(self):
        """
        Reset all application preferences to their default values.

        This function:
        1. Clears all saved settings from QSettings.
        2. Restores UI controls to default states.
        3. Displays an informational message box.
        4. Emits signals to notify the main window about the reset.
        """
        # ---------------------------------------------------------------------------------
        # Step 1: Clear all saved preferences
        # ---------------------------------------------------------------------------------
        self.settings.clear()
        self.settings.sync()

        # ---------------------------------------------------------------------------------
        # Step 2: Reset Font settings
        # ---------------------------------------------------------------------------------
        font_controls = self.controls.get("Font", {})
        if "type" in font_controls:
            font_controls["type"].setCurrentText("Times New Roman")
        if "size" in font_controls:
            font_controls["size"].setCurrentText("10")

        # ---------------------------------------------------------------------------------
        # Step 3: Reset Appearance settings
        # ---------------------------------------------------------------------------------
        appearance_controls = self.controls.get("Appearance", {})
        if "theme" in appearance_controls:
            appearance_controls["theme"].setCurrentText("Light")
        if "toolbar_icons" in appearance_controls:
            appearance_controls["toolbar_icons"].setChecked(True)

        # ---------------------------------------------------------------------------------
        # Step 4: Reset Language settings
        # ---------------------------------------------------------------------------------
        language_controls = self.controls.get("Language", {})
        if "type" in language_controls:
            language_controls["type"].setCurrentText("English")

        # ---------------------------------------------------------------------------------
        # Step 5: Reset Search engine preferences
        # ---------------------------------------------------------------------------------
        search_controls = self.controls.get("Search", {})
        if "Baidu" in search_controls:
            search_controls["Baidu"].setChecked(True)
        if "Google" in search_controls:
            search_controls["Google"].setChecked(False)

        # ---------------------------------------------------------------------------------
        # Step 6: Save reset values to disk
        # ---------------------------------------------------------------------------------
        self.settings.sync()

        # ---------------------------------------------------------------------------------
        # Step 7: Emit signals for UI update / log
        # ---------------------------------------------------------------------------------
        self.apply_settings_signal.emit()          # Apply new settings immediately
        self.settings_page_operation_signal.emit("Reset preferences!")

        # ---------------------------------------------------------------------------------
        # Step 8: Notify user
        # ---------------------------------------------------------------------------------
        QMessageBox.information(
            self,
            "Preferences Reset",
            "All settings have been reset to default values."
        )
    # -------------------------------------------------------------------------------------



    #-------------------------------------------------------------------------------------
    def change_page(self, current, previous):
        """
        Switch the displayed page in the stacked widget based on the selected tree item.

        Args:
            current: The currently selected QTreeWidgetItem.
            previous: The previously selected QTreeWidgetItem.
        """
        if not current:
            return
        text = current.text(0)

        page_map = {
            "Font": self.font_page,
            "Search": self.search_page,
            "Language": self.language_page,
            "Appearance": self.appearance_page,
            "Advanced": self.advanced_page
        }

        if text in page_map:
            self.stack.setCurrentWidget(page_map[text])
    #-------------------------------------------------------------------------------------


    #-------------------------------------------------------------------------------------
    # Update the UI texts (each page has its own method)
    def update_ui_texts(self):
        self.about_action.setText(self.lang.get_text("About"))
    #-------------------------------------------------------------------------------------
