@echo off
start cmd /k python server2.py
start cmd /k python server1.py
start cmd /k python client.py
pause >nul