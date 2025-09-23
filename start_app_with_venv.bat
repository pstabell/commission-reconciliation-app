@echo off
cd /d "c:\Users\Patri\OneDrive\STABELL DOCUMENTS\STABELL FILES\TECHNOLOGY\PROGRAMMING\SALES COMMISSIONS APP"
echo Activating virtual environment...
call .venv\Scripts\activate
echo Starting Commission Tracker app...
streamlit run commission_app.py
pause