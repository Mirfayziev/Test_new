@echo off
chcp 65001 > nul
echo.
echo ═══════════════════════════════════════════════════════════════════
echo    🚀 AF IMPERIYA - AVTOMATIK O'RNATISH
echo    Windows uchun
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Check Python
echo [1/6] Python tekshirilmoqda...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python topilmadi!
    echo Python 3.9+ ni https://python.org dan o'rnating
    pause
    exit /b 1
)
echo ✅ Python topildi
echo.

REM Create virtual environment
echo [2/6] Virtual environment yaratilmoqda...
if exist venv (
    echo ⚠️  venv mavjud, o'chirish...
    rmdir /s /q venv
)
python -m venv venv
if errorlevel 1 (
    echo ❌ Virtual environment yaratilmadi!
    pause
    exit /b 1
)
echo ✅ Virtual environment yaratildi
echo.

REM Activate virtual environment
echo [3/6] Virtual environment faollashtirilmoqda...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Activate qilib bo'lmadi!
    pause
    exit /b 1
)
echo ✅ Virtual environment faol
echo.

REM Upgrade pip
echo [4/6] pip yangilanmoqda...
python -m pip install --upgrade pip --quiet
echo ✅ pip yangilandi
echo.

REM Install requirements
echo [5/6] Kutubxonalar o'rnatilmoqda...
echo Bu 2-3 daqiqa davom etishi mumkin...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Kutubxonalar o'rnatilmadi!
    echo.
    echo Qo'lda urinib ko'ring:
    echo pip install Flask Flask-SQLAlchemy Flask-Login Werkzeug openpyxl requests python-dotenv
    pause
    exit /b 1
)
echo ✅ Barcha kutubxonalar o'rnatildi
echo.

REM Create database
echo [6/6] Database yaratilmoqda...
python reset_database.py
if errorlevel 1 (
    echo ❌ Database yaratilmadi!
    pause
    exit /b 1
)
echo ✅ Database yaratildi
echo.

echo ═══════════════════════════════════════════════════════════════════
echo    ✅ O'RNATISH MUVAFFAQIYATLI!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Server'ni ishga tushirish uchun:
echo    1. venv\Scripts\activate
echo    2. python app.py
echo.
echo Yoki:
echo    start.bat ni ikki marta bosing
echo.
pause
