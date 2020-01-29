@ECHO OFF
echo --- STARTED PYTHON TO EXE CONVERSION ---

pyinstaller.exe --clean --onedir --noconsole --icon=D:\Privat\Compiling_Room\Python\DnD\pyambientmixer\ambient-mixer-data\mixer.ico --specpath=.\_generated\spec --distpath=.\_generated\dist --workpath=.\_generated\build %1



Set filename=%1
For %%A in ("%filename%") do (
    REM Set Folder=%%~dpA
    REM Set Name=%%~nxA
	Set NameOnly=%%~nA
)
REM echo.Folder is: %Folder%
REM echo.Name is: %Name%
REM echo.NameOnly is: %NameOnly%

copy mixer.ico _generated\dist\%NameOnly%

cd _generated
cd dist
cd %NameOnly%
del mkl_*.dll

mkdir .presets
cd..
cd..
cd..
copy presets\silence.xml _generated\dist\%NameOnly%\.presets

echo ---------- END OF CONVERSION -----------
pause