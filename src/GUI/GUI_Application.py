#-----------------------------------------------------------------------------------------
# Purpouse: The main application window 
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27  
#----------------------------------------------------------------------------------------- 

import sys  # Import system-specific parameters and functions
import os
import webbrowser
import logging

from pathlib import Path

#-----------------------------------------------------------------------------------------
# Import PyQt5 widgets for UI elements
from PySide6.QtWidgets import ( 
    QApplication, 
    QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog,
    QLabel, QTextEdit, QFileDialog, QAbstractButton, QWidget, QStackedWidget, QTabWidget,    
    QLineEdit, QSplitter, 
    QPushButton, QRadioButton, QButtonGroup,
    QVBoxLayout, QHBoxLayout, QMdiArea, QMdiSubWindow, QSizePolicy, QCheckBox,
    QFormLayout, QGridLayout, QGroupBox, QComboBox,
    QMessageBox
)
# from PySide6.QtVirtualKeyboard import QVirtualKeyboard
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter                         # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QEvent, QLocale        # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------------------------


# Add the parent directory to the Python path for debugging (independent execution)
if __name__ == "__main__": 

    print("Debug mode!")   # ***Sometimes, the Vscode will load wrong python interpreter, if the code doesn't run, try to change the interpreter.

    # Get project root folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if project_root not in sys.path: sys.path.insert(0, project_root)




#-----------------------------------------------------------------------------------------
# Impot the class from the local python files
from GUI.Utils import utils
from GUI.Bar_Tool import Tool_Bar
from GUI.Page_Menu import Menu_Page
from GUI.Page_Log import LogWidget
from GUI.Virtual_Keyboard import CalculatorKeyboard, ClickableLineEdit
from GUI.Page_Setting import Setting_Window  
from GUI.Operation_Mainwindow import Operation_Mainwindow_Controller
from GUI.Operation_Setting import Operation_Setting_Controller  
from GUI.Language_Manager import Language_Manager
#-----------------------------------------------------------------------------------------



#=========================================================================================
class GUI_Application(QMainWindow):     # Define the login window class, inheriting from QMainWindow

    # Singal from the main window
    compute_requested = Signal()        # Computing singal from the compute button
    reset_requested = Signal()          # reset singal from the reset button
    search_requested = Signal()         # search singal from the seach item

    material_combo_requested = Signal(str)  # material singal from the material combo

    


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Constructor
    def __init__(self, parent=None):

        super().__init__(parent)        # Call the parent class constructor, makesure the parent class is QMainWindow



        # ================================== QSS setting =================================
        # QSS settings, this style sheet affects the entire application
        self.setStyleSheet("""
            /* Main window separator */
            QMainWindow::separator {
            width: 4px;
            height: 5px;
            background: #F0F0F0;   /* Light gray or white */
            }        
            QtoolBar {
                background-color: #F0F0F0;   /* Light gray or white */
            }
            QLineEdit {
                padding: 2px 5px 2px 5px;   /* Space for text, order isb top right bottom left */
                padding-left: 5px;     /* Space for magnifying glass icon */
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: #fff;
                font-size: 14px;
                height: 20px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4; /* VS Code blue highlight */
            }
            QtoolBar::item {
                padding: 3px 15px 3px 15px;             /* Spacing around tool items, padding order: up right down left */
                background: transparent;                /* Keep it transparent when not hovered */
                color: black;                           /* Text color */
                qproperty-alignment: 'AlignCenter';     /* Center the text */
            }
            QtoolBar::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,     /* top white */
                    stop:1 #FFF0F0      /* bottom pale cyan --- #C7ECFF; grey --- #C0C0C0 */
                );
                color: black;           /* text color on selection */
                border-radius: 3px;     /* rounded corners */
            }
            /* Drop-down tools */
            Qtool::item {
                padding: 5px 20px;
                background-color: white;
                color: black;
            }
            /* Hover effect for tool items */
            Qtool::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,     /* top white */
                    stop:1 #C7ECFF      /* bottom pale cyan */
                );
                color: black;           /* text color on selection */
                border-radius: 4px;     /* rounded corners */
            }
            /* Toolbar styling */
            QToolButton {
                icon-size: 24px;
                margin-right: 10px;
                margin: 0px 10px;                           /* Spacing around tool items, padding order: up right down left */
            }
            /* QPushButton styling */              
            QPushButton {
                background-color: rgba(255, 255, 255, 0);   /* transparent */
                color: black;                               /* font color */
                border-radius: 4px;                         /* roundered corner */
                padding: 4px 20px;
                border: 1px solid rgba(0,0,0,0.2);         /* The border */
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 212, 0.2);  /* Windows 11 light bule for hovering */
            }
            QPushButton:pressed {
                background-color: rgba(0, 120, 212, 0.4);  /* Emphasize the pressed state */
            }
        """)
        # ================================================================================












    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Language manager
        self.language_manager = Language_Manager()               # The gobal language manager
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Initialization scheme
        self.init_main_window_ui()      # Initialize the main window

        self.init_tool()                # Initialize the tool bar

        self.init_menu_page()           # Initialize the menu page which can be slidding out from left side

        self.init_setting_window()      # Initialize the toolbar

        # Create the operation
        self.operation_mainwindow = Operation_Mainwindow_Controller(self) 
        self.operation_setting    = Operation_Setting_Controller(self)     

        # Load the settings
        self.load_settings_on_startup()    

        # Connect the signals and slots
        self.connect_signals()
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Load the settings, if exists
    # Otherwise, create default settings
    def load_settings_on_startup(self):
        """
        Check if settings.ini exists; if yes, load it.
        Otherwise, create one with default values.
        """
        usr_folder = utils.get_usr_dir()
        settings_path = usr_folder / "settings.ini"

        # Check if settings.ini exists
        if settings_path.exists():
            print(f"[INFO] Loading settings from: {settings_path}")
            settings = QSettings(str(settings_path), QSettings.Format.IniFormat)
            self.operation_setting.apply_new_settings()  # apply the settings
        else:
            print("[INFO] No settings.ini found. Creating default settings...")

            # The default settings for the initial loading
            settings = QSettings(str(settings_path), QSettings.Format.IniFormat)
            settings.setValue("Font/type", "Times New Roman")
            settings.setValue("Font/size", 10)
            settings.setValue("Appearance/theme", "Light")
            settings.setValue("Appearance/toolbar_icons", True)
            settings.setValue("Language/type", "English")
            settings.setValue("Search/Baidu", True)
            settings.setValue("Search/Google", False)
            settings.sync()

            # use the default settings
            self.operation_setting.apply_new_settings()

        # Save the settings
        self.settings = settings
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Connect the signals from the tool bar
    def connect_signals(self):

        #---------------------------------------------------------------------------------
        # Signal from the tool bar in main window
        self.tool_bar.show_keyboard_requested.connect(self.operation_mainwindow.handle_show_keyboard)
        self.tool_bar.show_log_requested.connect(self.operation_mainwindow.handle_show_log)
        self.tool_bar.about_requested.connect(self.operation_mainwindow.handle_about)
        self.tool_bar.show_setting_requested.connect(self.operation_mainwindow.handle_show_setting)
        self.tool_bar.export_requested.connect(self.operation_mainwindow.handle_export)
        self.tool_bar.show_menu_requested.connect(self.operation_mainwindow.handle_show_menu_page)

        # Signal from  compute and reset buttons, along with the search button in main window
        self.compute_requested.connect(self.operation_mainwindow.handle_compute)
        self.reset_requested.connect(self.operation_mainwindow.handle_reset)


        # Get the QSettings file path
        usr_folder = utils.get_usr_dir()
        settings_file_path = usr_folder / "settings.ini"

        # Check the settings
        settings   = QSettings(str(settings_file_path), QSettings.Format.IniFormat)
        use_baidu  = settings.value("Search/Baidu", True, type=bool)
        use_google = settings.value("Search/Google", False, type=bool)

        # Connetc signal from the search button
        if use_baidu and not use_google:
            self.search_requested.connect(self.operation_mainwindow.perform_baidu_search)
        elif use_google and not use_baidu:
            self.search_requested.connect(self.operation_mainwindow.perform_google_search)
        else:
            self.search_requested.connect(self.operation_mainwindow.perform_baidu_search)  # default

        

        # Signal from the material comboBox in main window
        self.material_combo_requested.connect(self.operation_mainwindow.handle_material_change)
        #---------------------------------------------------------------------------------

        #---------------------------------------------------------------------------------
        # Signal from the setting page
        self.setting_page.settings_page_operation_signal.connect(self.log_widget.log_message)
        self.setting_page.apply_settings_signal.connect(self.operation_setting.apply_new_settings) # Connect apply signal
        #---------------------------------------------------------------------------------

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Initialize the main window    
    def init_main_window_ui(self):

        #---------------------------------------------------------------------------------
        window_ratio = 0.45
        self.aspect_ratio = 9/16                                # Aspect ratio
        total_window_height = window_ratio*1960                 # Total window height for reference
        total_window_with   = window_ratio*1080                 # Total window width for reference

        # Set system title bar (plain text, no HTML or font control)
        main_window_title = utils.convert_sub_and_superscript("SaMPH-yPlus")
        self.setWindowTitle(main_window_title)                          # Set the window title 
        # self.resize(total_window_with, total_window_height)             # Set the initial size of the main window
        self.setFixedSize(total_window_with, total_window_height)       # Set the fixed main window size
        
        # Disable the maximize button, only the minimize and close buttons are available
        self.setWindowFlags(Qt.Window |
                            Qt.WindowMinimizeButtonHint |
                            Qt.WindowCloseButtonHint)

        # Set the window icon (optional)
        window_icon_path = utils.resource_path("images/yPlus-calculator-logo-blue.png")
        pixmap = QPixmap(window_icon_path)
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setWindowIcon(QIcon(pixmap))
        #---------------------------------------------------------------------------------

        #---------------------------------------------------------------------------------
        # Initialize the main window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Model Parameters region in the top-left of the main window
        # create QGroupBox
        model_parameters_group  = QGroupBox("Model Parameters")
        model_parameters_layout = QVBoxLayout() 


        # Material combo
        material_layout = QHBoxLayout()
        self.material_label = QLabel("Material (optional):")
        self.material_label.setFont(QFont("Times New Roman", 10))
        self.material_combo = QComboBox()
        self.material_combo.addItems(["", "Fresh water (20 \u00B0C)", "Sea water (20 \u00B0C)", "Air (20 \u00B0C)"])
        material_layout.addWidget(self.material_label)
        material_layout.addWidget(self.material_combo)

        # Send material combo signal currentTextChanged/currentIndexChanged
        self.material_combo.currentTextChanged.connect(self.material_combo_requested)



        # Variable arrangement combo
        scheme_layout = QHBoxLayout()
        self.scheme_label = QLabel("Spatial discretization scheme:")
        self.scheme_label.setFont(QFont("Times New Roman", 10))
        self.scheme_combo = QComboBox()
        self.scheme_combo.addItems(["Cell-centered", "Vertex-centered"])
        scheme_layout.addWidget(self.scheme_label)
        scheme_layout.addWidget(self.scheme_combo)

        # Skin friction formula combo
        skin_friction_layout = QHBoxLayout()
        self.skin_friction_label = QLabel("Skin friction coefficient formula:")
        self.skin_friction_label.setFont(QFont("Times New Roman", 10))
        self.skin_friction_combo = QComboBox()
        self.skin_friction_combo.addItems([
            "Prandtl-Schlichting (1979)", 
            "Prandtl-Kármán (1932)",
            "ITTC-1957 (ship)"
        ])
        skin_friction_layout.addWidget(self.skin_friction_label)
        skin_friction_layout.addWidget(self.skin_friction_combo)


        # Boundary layer thickness formula  combo
        boundary_layer_layout = QHBoxLayout()
        self.boundary_layer_label = QLabel("Boundary layer thickness formula:")
        self.boundary_layer_label.setFont(QFont("Times New Roman", 10))
        self.boundary_layer_combo = QComboBox()
        self.boundary_layer_combo.addItems([
            "Schlichting (1979)", 
            "White (1991)"
        ])
        boundary_layer_layout.addWidget(self.boundary_layer_label)
        boundary_layer_layout.addWidget(self.boundary_layer_combo)


        # Add the combos to the layout
        model_parameters_layout.addLayout(material_layout)
        model_parameters_layout.addLayout(scheme_layout)
        model_parameters_layout.addLayout(skin_friction_layout)
        model_parameters_layout.addLayout(boundary_layer_layout)
        model_parameters_group.setLayout(model_parameters_layout)

        # Set the style sheet
        model_parameters_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 15px;
                color: #2c3e50;
                border: 1.5px solid gray;
                border-radius: 4px;
                margin-top: 0.5em;          /* Move the group box down */
                padding-top: 5px;
                height: 22px;                         
            }
            QGroupBox::title {
                font-size: 12pt;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 5px;
                color: gray;                /* Win10 gray */
                border-radius: 4px;
            }
        """)
        # For the convenience of reset text, set the object name
        model_parameters_group.setObjectName("model_parameters_group") 

        self.material_label.setObjectName("material_combo_label")
        self.material_combo.setObjectName("material_combo")
        self.scheme_label.setObjectName("scheme_combo_label")
        self.scheme_combo.setObjectName("scheme_combo")
        self.skin_friction_label.setObjectName("skin_friction_combo_label")
        self.skin_friction_combo.setObjectName("skin_friction_combo")
        self.boundary_layer_label.setObjectName("boundary_layer_combo_label")
        self.boundary_layer_combo.setObjectName("boundary_layer_combo")


        # Define the style for the combo boxes
        combo_box_list = [
            self.material_combo,
            self.scheme_combo,
            self.skin_friction_combo,
            self.boundary_layer_combo
        ]
        for combo_box in combo_box_list:

            # Set style for the combobox
            arrow_path = utils.resource_path("images/WIN11-Icons/icons8-expand-arrow-100.png")

            print(f"[DEBUG] Loading arrow from: {arrow_path}")

            arrow_path = arrow_path.replace("\\", "/")
            combo_box.setStyleSheet(f"""
                QComboBox {{
                    border: 1px solid #aaaaaa;
                    border-radius: 4px;
                    font-size: 13px;
                    padding: 4px 28px 4px 8px;
                    background-color: #F0F0F0;   /* Light gray or white */
                    min-width: 6em;
                }}
                QGroupBox::title {{
                    font-size: 12pt;
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    left: 12px;
                    padding: 0 5px;
                    color: gray;                /* Win10 gray */
                    border-radius: 4px;
                }}        
                QComboBox::drop-down {{
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 20px;
                    border: none;
                    background: transparent;
                }}
                QComboBox::down-arrow {{
                    image: url("{arrow_path}");
                    width: 15px;
                    height: 15px;
                }}
                QComboBox::item:hover {{
                    background-color: #F0F0F0;  /* Hover color */
                }}
                QComboBox QAbstractItemView {{
                    border: 1px solid #aaaaaa;
                    border-radius: 6px;
                    selection-background-color: #d0f0c0;
                    background: white;
                    font-size: 18pt;
                }}
                QComboBox QAbstractItemView::item:hover {{
                    background-color: #F0F0F0;      /* Hover color: very light gray */
                    border-radius: 6px;              /* Keep rounded corners */
                    color: black;                   /* Hover text color */
                }}
            """)
        #---------------------------------------------------------------------------------

        #---------------------------------------------------------------------------------
        # Add input data group in the top-right of the main window
        input_group = QGroupBox("Input data")
        self.input_layout = QFormLayout()

        # Define input parameters: (Name, Symbol, Default Unit)
        input_parameters = [
            ("Freestream velocity", "U_\u221E", "m/s"),                     # Freestream velocity, U (m/s)
            ("Freestream density", "\u03C1", "kg/m^3"),                     # Density of water, \rho, (kg/m^3)
            ("Dynamic viscosity", "\u03BC", "Pa\u00B7s"),                   # Dynamic viscosity, \mu (Pa s)
            ("Reference length", "L", "m"),                                 # Reference length, L (m)
            ("Grid stretch ratio (optional)", "", ""),                                 # Grid stretch ratio
            ("Desired y^+", "", "")                                         # y+
        ]

        # Add input objectnames
        input_objectnames = [
            "freestream_velocity", 
            "freestream_density", 
            "dynamic_viscosity", 
            "reference_length",
            "grid_stretch_ratio",
            "desired_yPlus"
        ]

        for idx, (name, symbol, default_unit) in enumerate(input_parameters):

            # Special treatment for 'Grid stretch ratio' and 'Desired y^+'
            if idx == 4 or idx == 5:
                label_text = f"{utils.convert_sub_and_superscript(name)}:"
            else:
                label_text = f"{utils.convert_sub_and_superscript(name)}, <i>{utils.convert_sub_and_superscript(symbol)}</i> ({utils.convert_sub_and_superscript(default_unit)}):"
            
            label = QLabel(label_text)
            label.setTextFormat(Qt.RichText)
            label.setFont(QFont("Times New Roman", 10))
            label.setObjectName(f"{input_objectnames[idx]}")                    # For the convenience of reset text, set the object name

            input_lineditor = ClickableLineEdit()                        # Make sure the virtual keyboard is enabled
            input_lineditor.setClearButtonEnabled(True)                  # Enable the clear button

            # # Add the placeholder text for Grid stretch ratio
            # if idx == 4:
            #     placeholder = "> 1.0 (Grid stretch ratio)"
            #     input_lineditor.setPlaceholderText(placeholder)

            self.input_layout.addRow(label, input_lineditor)

        input_group.setLayout(self.input_layout)    # Add to input_group

        # Set the style sheet
        input_group.setStyleSheet("""
            QGroupBox {
                font-size: 12pt;
                font-weight: bold;
                color: #2c3e50;
                border: 1.5px solid gray;
                border-radius: 4px;
                margin-top: 0.5em;          /* Move the group box down */
                padding-top: 5px;
            }
            QGroupBox::title {
                font-size: 12pt;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 5px;
                color: gray;                /* Win10 gray */
                border-radius: 4px;
            }
        """)

        # For the convenience of reset text, set the object name
        input_group.setObjectName("input_group")
        #---------------------------------------------------------------------------------


        #---------------------------------------------------------------------------------
        # Add the model parameters group to the top-left of the main window
        top_layout=QVBoxLayout()
        # top_layout.addStretch()
        top_layout.addWidget(model_parameters_group)
        # top_layout.addStretch()
        top_layout.addWidget(input_group)
        #---------------------------------------------------------------------------------


        #---------------------------------------------------------------------------------
        # Ouput region in the middle of the main window
        output_group = QGroupBox("Output results")
        self.output_layout = QFormLayout()

        # Define the output results
        output_results = [
            ("Estimated boundary layer thickness", "\u03B4", "m"),      # Estimated boundary layer thickness (m)
            ("First-grid spacing", "\u0394S", "m"),                     # First-grid spacing, (m)
            ("Reynolds number", "Re", ""),                              # Reynolds number
            ("Number of prism layers", "N", ""),                        # Number of prism layers
        ]

        # Add output objectnames
        output_objectnames = [
            "estimated_boundary_layer_thickness", 
            "first_grid_spacing", 
            "reynolds_number", 
            "number_of_prism_layers"
        ]

        for idx, (name, symbol, default_unit) in enumerate(output_results):

            # Special treatment for 'Reynolds number' and 'Number of prism layers'
            if idx == 2 or idx == 3:
                label_text = f"{utils.convert_sub_and_superscript(name)}, <i>{utils.convert_sub_and_superscript(symbol)}</i>:"
            else:
                label_text = f"{utils.convert_sub_and_superscript(name)}, <i>{utils.convert_sub_and_superscript(symbol)}</i> ({utils.convert_sub_and_superscript(default_unit)}):"
            
            label = QLabel(label_text)
            label.setTextFormat(Qt.RichText)
            label.setFont(QFont("Times New Roman", 10))
            label.setObjectName(f"{output_objectnames[idx]}")                     # For the convenience of reset text, set the object name

            output_lineditor = ClickableLineEdit()                        # Make sure the virtual keyboard is enabled
            self.output_layout.addRow(label, output_lineditor)

        # Add the output results to the layout
        output_group.setLayout(self.output_layout)

        # Set the style sheet
        output_group.setStyleSheet("""
            QGroupBox {
                font-size: 12pt;
                font-weight: bold;
                color: #2c3e50;
                border: 1.5px solid gray;
                border-radius: 4px;
                margin-top: 0.5em;          /* Move the group box down */
                padding-top: 5px;
                padding-bottom: 0px;
            }
            QGroupBox::title {
                font-size: 12pt;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 5px;
                color: gray;                /* Win10 gray */
                border-radius: 4px;
            }
        """)

        # For the convenience of reset text, set the object name
        output_group.setObjectName("output_group")
        #---------------------------------------------------------------------------------

        #---------------------------------------------------------------------------------
        # Add the reset and compute button
        self.compute_button = QPushButton(self)
        self.compute_button.setIcon(QIcon(str(utils.resource_path("images/Win11-Icons/icons8-calculate-100.png"))))
        self.compute_button.setFixedSize(60, 30)  # Set button size
        self.compute_button.setIconSize(QSize(24, 24))
        self.compute_button.setStyleSheet("font-size: 12px; font-family: Times New Roman")  # Customize font size
        self.compute_button.setToolTip("Compute")

        # Send the calculate_requested signal
        self.compute_button.clicked.connect(lambda: self.compute_requested.emit())


        self.reset_button = QPushButton(self)
        self.reset_button.setIcon(QIcon(str(utils.resource_path("images/Win11-Icons/icons8-erase-100.png"))))
        self.reset_button.setFixedSize(60, 30)  # Set button size
        self.reset_button.setIconSize(QSize(24, 24))
        self.reset_button.setStyleSheet("font-size: 12px; font-family: Times New Roman")  # Customize font size
        self.reset_button.setToolTip("Reset")

        # Send the reset_requested signal
        self.reset_button.clicked.connect(lambda: self.reset_requested.emit())

        # Add the object name
        self.compute_button.setObjectName("compute_button")
        self.reset_button.setObjectName("reset_button")

        self.compute_button.setStyleSheet("""
        QPushButton:hover {
            background-color: #E6F1FB;  /* hover background */
        }
        QPushButton:pressed {
            background-color: #CDE0F7;  /* pressed background */
        }
        """)
        self.reset_button.setStyleSheet("""
        QPushButton:hover {
            background-color: #E6F1FB;  /* hover background */
        }
        QPushButton:pressed {
            background-color: #CDE0F7;  /* pressed background */
        }
        """)
        #---------------------------------------------------------------------------------


        #---------------------------------------------------------------------------------
        # Add Search input and button
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by Google...")
        self.search_edit.setClearButtonEnabled(True)                  # Enable the clear button
        self.search_edit.setFixedHeight(30)
        self.search_edit.setStyleSheet("""
            QLineEdit {
                padding: 2px 5px 2px 5px;        /* Space for text, order is top right bottom left */
                padding-left: 10px;              /* Space for the left button */
                padding-right: 10px;             /* Space for the right button */
                border: 1.5px solid grey;
                border-radius: 8px;
                font-size: 13px;
                width: 200px;
            }
            QLineEdit:focus {
                border: 1.0px solid #0078D7;    /* #0078D7 --- Microsoft Blue */
            }
        """)

        # Put the search logo at the leading of the search bar
        logo_action = self.search_edit.addAction(
            QIcon(QIcon(str(utils.resource_path("images/Win11-Icons/icons8-google-100.png")))),  # The google label
            QLineEdit.ActionPosition.LeadingPosition
        )
        logo_action.setIconVisibleInMenu(False)

        # Send the reset_requested signal
        self.search_edit.returnPressed.connect(lambda: self.search_requested.emit())
        #---------------------------------------------------------------------------------

        #---------------------------------------------------------------------------------
        # Combine the search, reset and compute buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_edit)
        button_layout.addStretch(1)           # Leave the left side blank 
        button_layout.addWidget(self.reset_button)
        button_layout.addSpacing(10)          # The spacing between two buttons
        button_layout.addWidget(self.compute_button)
        # button_layout.addStretch(1)           # Leave the right side blank 
        #---------------------------------------------------------------------------------




        #---------------------------------------------------------------------------------
        # Log and keyboard region in the bottom of the main window
        log_group = QGroupBox("")
        log_group_layout = QVBoxLayout()
        log_group.setLayout(log_group_layout)
        log_group_layout.setContentsMargins(0, 0, 0, 0)       # GroupBox margins
        log_group_layout.setSpacing(0)                        # Remove internal spacing
        # log_group.setStyleSheet("""
        #     QGroupBox {
        #         padding: 1px 1px 1px 1px;   /* Space for text, order isb top right bottom left */
        #         border: 2px solid #A0A0A0;
        #         border-radius: 6px;
        #         margin-top: 0px;
        #         font-size: 12pt;
        #         font-weight: bold;
        #         color: #003366;
        #         background-repeat: no-repeat;
        #         background-position: center;
        #         background-color: #F7F7F7;  /* fallback color */
        #         height: 100px;
        #     }
        #     QGroupBox::title {
        #         subcontrol-origin: margin;
        #         left: 15px;
        #         padding: 0 5px;
        #     }
        # """)

        # The background image in the log group
        self.bottom_background_label = QLabel()
        self.bottom_background_label.setAlignment(Qt.AlignCenter)
        self.bottom_background_label.setPixmap(QPixmap(utils.resource_path("images/yPlus-calculator-logo-blue.png")))
        self.bottom_background_label.setScaledContents(True)  # Scale the image to fit the label
        self.bottom_background_label.hide()  # Hide the background image in the beginning as it has a tab


        # TabWidget
        self.log_and_keyboard_tab_widget = QTabWidget()
        self.log_and_keyboard_tab_widget.setTabsClosable(True)                       # Tabs can be closed
        self.log_and_keyboard_tab_widget.tabCloseRequested.connect(self.close_tab)   # Close tab

        # === Tab 1: Log ===
        self.log_widget = LogWidget(self)
        self.log_and_keyboard_tab_widget.addTab(self.log_widget, "Log")

        # # === Tab 2: Keyboard ===
        # self.keyboard_widget = CalculatorKeyboard()
        # self.log_and_keyboard_tab_widget.addTab(self.keyboard_widget, "Keyboard")
        # self.log_and_keyboard_tab_widget.setSizePolicy(
        #     QSizePolicy.Expanding,                  # The horizontal size policy
        #     QSizePolicy.Fixed                       # The vertical size policy
        # )

        log_group_layout.addWidget(self.log_and_keyboard_tab_widget)
        log_group_layout.addWidget(self.bottom_background_label)
        #---------------------------------------------------------------------------------



        # ================================ Add to main layout ============================
        # Expand to fill the available space
        model_parameters_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        input_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        output_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        log_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # # main_layout.addStretch()
        # main_layout.addWidget(model_parameters_group, stretch=3)   # stretch factor = 3
        # main_layout.addWidget(input_group, stretch=9)   # stretch factor = 3
        # # main_layout.addStretch()
        # main_layout.addWidget(output_group, stretch=3)
        # # main_layout.addStretch()
        # main_layout.addLayout(button_layout)
        # # main_layout.addStretch()
        # # main_layout.addWidget(log_group)
        # main_layout.addWidget(log_group, stretch=2)

        main_layout.addWidget(model_parameters_group)   # stretch factor = 3
        main_layout.addWidget(input_group)   # stretch factor = 3
        # main_layout.addStretch()
        main_layout.addWidget(output_group)
        # main_layout.addStretch()
        main_layout.addLayout(button_layout)
        # main_layout.addStretch()
        # main_layout.addWidget(log_group)
        main_layout.addWidget(log_group)
        
        # ================================================================================

        #---------------------------------------------------------------------------------


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Intialize the tool bar
    def init_tool(self):

        # Call the function of 'create_tool_bar' in “Bar_tool.py” to create the tool bar
        self.tool_bar = Tool_Bar(self)    # Parameter: send self as parent
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Intialize the menu page
    def init_menu_page(self):

        # Initialize the Menu_Page class in Page_Menu.py” to create the tool bar
        self.menu_page = Menu_Page(self, self.tool_bar)    # Parameter: send self as parent
        
        # Inorder to show the menu page, put it in the central widget for debugging
        # self.setCentralWidget(self.menu_page)
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def close_tab(self, index):

        """
        Close a tab and clear references if it was one of the special pages.
        """

        # if self.log_and_keyboard_tab_widget.tabText(index) not in ["Log"]:

        # Get the name of the tab before it is closed
        name = self.log_and_keyboard_tab_widget.tabText(index)

        # Send warnning message to log window
        self.log_widget.log_message(f"Closed tab: {name}.", level=logging.WARNING)

        # # Test passing message to logger (it works)
        # self.log_widget.log_message(f"Closed tab: {name}.", level=logging.ERROR)
        # self.log_widget.log_message(f"Closed tab: {name}.", level=logging.INFO)
        # self.log_widget.log_message(f"Closed tab: {name}.", level=logging.WARNING)

        self.log_and_keyboard_tab_widget.removeTab(index)

        # If there are no tabs left, hide the tab widget
        if self.log_and_keyboard_tab_widget.count() == 0:
            self.log_and_keyboard_tab_widget.hide()
            self.bottom_background_label.show()

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Intialize the menu page
    def init_setting_window(self):

        # Initialize the Setting_Window class in Page_Setting.py” to create the setting dialog
        self.setting_page = Setting_Window(self)    # Parameter: send self as parent

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Update the UI texts in the central widget
    def update_ui_texts(self, parent_widget=None):
        """
        Update UI texts of all widgets recursively based on the current language.

        This function traverses all widgets inside the given parent widget (or the main window itself),
        and updates the text of labels, buttons, combo boxes, and group boxes according to the
        translation dictionary stored in self.translations.

        Args:
            parent_widget (QWidget, optional): The starting widget for traversal.
                                            Defaults to self.central_widget if not specified.
        """

        # =====================================================================
        # 0. Preparation
        # =====================================================================
        if parent_widget is None:
            parent_widget = self.central_widget

        current_lang = self.language_manager.language  # Get current language

        if current_lang not in self.language_manager.translations:
            print(f"[Warning] No translation found for language: {current_lang}")
            return

        translations = self.language_manager.translations[current_lang]  # Load current language dictionary
        
        # =====================================================================
        # 1. Helper function: recursively traverse and update all widgets
        # =====================================================================
        def traverse_and_update(widget):
            """
            Recursively traverse through all child widgets and update their text
            according to the translation dictionary.
            """

            # --------------------------------------------------------------
            # QLabel
            # --------------------------------------------------------------
            if isinstance(widget, QLabel):
                name = widget.objectName()
                if name in translations:
                    widget.setText(translations[name])

            # --------------------------------------------------------------
            # Update text for QPushButton widgets
            # --------------------------------------------------------------
            elif isinstance(widget, QPushButton):
                name = widget.objectName()  # Get the object name of the button
                if name in translations:
                    translation = translations[name]
                    
                    if isinstance(translation, dict):
                        # If translations[name] is a dictionary, get the "text" field
                        widget.setText(translation.get("text", widget.text()))
                        
                        # Optional: set the tooltip if provided in the dictionary
                        if "tooltip" in translation:
                            widget.setToolTip(translation["tooltip"])
                    else:
                        # If translations[name] is a simple string, set it directly
                        widget.setText(str(translation))

            # --------------------------------------------------------------
            # QGroupBox
            # --------------------------------------------------------------
            elif isinstance(widget, QGroupBox):
                name = widget.objectName()
                if name in translations:
                    widget.setTitle(translations[name])

            # --------------------------------------------------------------
            # QComboBox
            # --------------------------------------------------------------
            elif isinstance(widget, QComboBox):
                name = widget.objectName()
                if name in translations:
                    widget.clear()
                    widget.addItems(translations[name])

            # --------------------------------------------------------------
            # QCheckBox
            # --------------------------------------------------------------
            elif isinstance(widget, QCheckBox):
                name = widget.objectName()
                if name in translations:
                    widget.setText(translations[name])

            # --------------------------------------------------------------
            # QRadioButton
            # --------------------------------------------------------------
            elif isinstance(widget, QRadioButton):
                name = widget.objectName()
                if name in translations:
                    widget.setText(translations[name])

            # --------------------------------------------------------------
            # QTabWidget (update each tab text)
            # --------------------------------------------------------------
            elif isinstance(widget, QTabWidget):
                name = widget.objectName()
                if name in translations:
                    for i in range(widget.count()):
                        tab_name = f"{name}_tab{i}"
                        if tab_name in translations:
                            widget.setTabText(i, translations[tab_name])

            # --------------------------------------------------------------
            # Recursively traverse children
            # --------------------------------------------------------------
            for child in widget.findChildren(QWidget):
                traverse_and_update(child)

        # =====================================================================
        # 2. Start updating from the given parent widget
        # =====================================================================
        traverse_and_update(parent_widget)

        print(f"[Info] UI text updated to language: {current_lang}")

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
















#-----------------------------------------------------------------------------------------
# Main execution block, this is only used for debugging
if __name__ == '__main__':  # Ensure this code runs only when the file is executed directly
    
    app = QApplication(sys.argv)    # Create the application object
    window = GUI_Application()      # Create an instance of the GUI_Application class
    window.show()                   # Display the login window
    sys.exit(app.exec())            # Start the application's event loop
#-----------------------------------------------------------------------------------------





