@echo off
set name=ChangeEnvironmentVariables
set icon=icon.ico
set script=change_env_var.py
pyinstaller -n %name% -w -F --hidden-import=atexit -i %icon% %script%
start dist
pause