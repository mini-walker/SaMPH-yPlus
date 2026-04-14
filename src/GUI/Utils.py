#***********************************************************************
# Very important: you need to use usr_dir when you want to save data
# utils.resource_path only used for reading static files
#***********************************************************************

import sys
import re


from pathlib import Path


class utils:

    #-----------------------------------------------------------------------------------------
    # For static file
    @staticmethod
    def resource_path(relative_path):
        
        """
        Return an absolute resource path that works both during development
        and when bundled by PyInstaller (uses sys._MEIPASS).
        """

        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            # base path is the project folder, yPlus_Calculator
            base_path = Path(__file__).parent.parent.parent.resolve()  # the login file is in src folder
        
        # Join with relative path and return as string
        return str(base_path / relative_path)
    #-----------------------------------------------------------------------------------------



    #-----------------------------------------------------------------------------------------
    # For dynamic file, such as input/output result file
    @staticmethod
    def get_usr_dir():
        if getattr(sys, 'frozen', False):
            
            # The pyinstaller model
            base_dir = Path(sys.executable).parent
        else:
            # debug mode
            base_dir = Path(__file__).resolve().parent.parent.parent  

        usr_dir = base_dir / "usr"
        usr_dir.mkdir(exist_ok=True)
        return usr_dir
    #-----------------------------------------------------------------------------------------



    #-----------------------------------------------------------------------------------------
    @staticmethod
    def convert_sub_and_superscript(text):
        """
        Convert unit text with ^ (superscript) and _ (subscript) to HTML format.

        Args:
            unit_text (str): The unit text (e.g., "m^2" or "m_3").

        Returns:
            str: HTML-formatted unit (e.g., "m<sup>2</sup>" or "m<sub>3</sub>").
        """

        # Transfer the unicode
        def replace_unicode(match):
            code = match.group(1)
            return chr(int(code, 16))
        
        text = re.sub(r'\\u([0-9A-Fa-f]{4})', replace_unicode, text)


        text = re.sub(r'_([^_}]+)', r'<sub>\1</sub>', text)
        text = re.sub(r'\^([^_^}]+)', r'<sup>\1</sup>', text)
        
        return text
    #-----------------------------------------------------------------------------------------
