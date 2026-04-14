@echo off
echo =============================================
echo Cleaning old build and dist folders...
echo =============================================

if exist EXE\build rmdir /s /q EXE\build
if exist EXE\dist rmdir /s /q EXE\dist
if exist SaMPH.spec del SaMPH.spec

echo.
echo =============================================
echo Running PyInstaller (ONEDIR - Faster mode)...
echo =============================================

REM =====================================================
REM ONEDIR Build configuration
REM =====================================================

pyinstaller ^
  --clean ^
  --onedir ^
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
echo Build finished (ONEDIR mode)
echo Main EXE: %CD%\EXE\dist\SaMPH-yPlus.exe
echo Distribute the entire folder: %CD%\EXE\dist\
echo =============================================
echo.
echo Benefits of ONEDIR:
echo - Much faster startup (3-5x)
echo - Smaller overall size
echo - Only ~30-50 MB total
echo =============================================

pause
