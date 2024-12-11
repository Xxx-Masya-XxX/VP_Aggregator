@echo off
chcp 65001>nul
if not exist ".venv" (
    echo Виртуальное окружение не найдено, создаю...
    python -m venv .venv
)
call ".venv/Scripts/activate"
if exist "requirements.txt" (
    echo Устанавливаю необходимые библиотеки...
    pip install -r requirements.txt
)
pip freeze > requirements.txt
echo Запуск main.py...
python main.py
start http://localhost:3000
node server.js
