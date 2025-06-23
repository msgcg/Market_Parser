#!/bin/bash

LOG_FILE="/home/vnc/Pyenv/Market_Parser/logs/cron.log"
APP_DIR="/home/vnc/Pyenv/Market_Parser/app"
VENV_DIR="/home/vnc/Pyenv/Market_Parser/.venv"

# Логируем начало работы
echo "=== $(TZ='Europe/Moscow' date) Начало скрипта ===" >> "$LOG_FILE"

# Проверка наличия виртуального окружения
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "❌ Виртуальное окружение не найдено" >> "$LOG_FILE"
    exit 1
fi

# Активация окружения
source "$VENV_DIR/bin/activate"
echo "✅ Окружение активировано" >> "$LOG_FILE"

# Переход в папку с приложением
cd "$APP_DIR" || {
    echo "❌ Папка с приложением не найдена" >> "$LOG_FILE"
    exit 1
}

# Запуск скриптов
scripts=("Shedule1.py" "Shedule2.py")

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "🚀 Запуск скрипта: $script" >> "$LOG_FILE"
        "$VENV_DIR/bin/python" "$script" >> "$LOG_FILE" 2>&1
        echo "✅ Завершено: $script" >> "$LOG_FILE"
    else
        echo "⚠️ Скрипт не найден: $script" >> "$LOG_FILE"
    fi
done

# Деактивация окружения
deactivate
echo "🎯 Скрипт завершён" >> "$LOG_FILE"
