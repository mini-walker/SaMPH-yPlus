@echo off
echo =============================================
echo Cleaning old build and dist folders...
echo =============================================

if exist EXE\build rmdir /s /q EXE\build
if exist EXE\dist rmdir /s /q EXE\dist
if exist SaMPH.spec del SaMPH.spec

echo.
echo =============================================
echo Running PyInstaller...
echo =============================================

REM =====================================================
REM PyInstaller Build Configuration
REM =====================================================
REM 
REM IMPORTANT: Resource Handling
REM -----------------------------------------
REM 1. Images: Code expects resources at _MEIPASS/SaMPH/SaMPH_Images
REM    So we map: src/SaMPH_Images -> SaMPH/SaMPH_Images
REM 
REM 2. Entry Point: src/Main.py
REM    This is the main entry point defined in the project
REM 
REM 3. User Data: 
REM    The application expects 'usr' folder next to the EXE.
REM    We do NOT bundle 'usr' inside the EXE strictly, 
REM    but we copy it to the dist folder after build.
REM 
REM =====================================================

pyinstaller ^
  --clean ^
  --onefile ^
  --windowed ^
  --name "SaMPH-yPlus" ^
  --workpath "EXE/build" ^
  --distpath "EXE/dist" ^
  --paths "src" ^
  --add-data "images;images" ^
  --hidden-import "openpyxl" ^
  --exclude-module "tkinter" ^
  --exclude-module "IPython" ^
  --exclude-module "setuptools" ^
  --icon "images/yPlus-calculator-logo-blue.ico" ^
  src/Main.py

echo.
echo =============================================
echo Copying external resources to dist folder...
echo =============================================

REM Copy usr directory (for settings/history)
if not exist "EXE\dist\usr" mkdir "EXE\dist\usr"
xcopy "usr" "EXE\dist\usr" /E /I /Y

REM Copy Examples directory
if not exist "EXE\dist\Examples" mkdir "EXE\dist\Examples"
xcopy "Examples" "EXE\dist\Examples" /E /I /Y

echo.
echo =============================================
echo Build finished.
echo EXE located at: %CD%\EXE\dist\SaMPH-yPlus.exe
echo =============================================

pause
