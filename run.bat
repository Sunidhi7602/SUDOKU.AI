@echo off
echo Starting AI Sudoku Solver...
echo.
echo Backend (port 5000)...
start "Backend" cmd /k "cd backend && py -m pip install flask flask-cors && py app.py"
timeout /t 3 /nobreak >nul
echo.
echo Frontend (port 4200)... 
start "Frontend" cmd /k "cd frontend && npm install && ng serve"
echo.
echo Open: http://localhost:4200
echo Backend: http://localhost:5000
pause

