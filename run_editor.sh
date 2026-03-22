#!/bin/bash
# Скрипт для запуска визуального редактора профилей нагрузки Locust

echo "🎨 Запуск визуального редактора профилей нагрузки Locust..."
echo ""

# Проверка установки matplotlib
if ! python3 -c "import matplotlib" 2>/dev/null; then
    echo "⚠️  matplotlib не установлен!"
    echo ""
    echo "Установка зависимостей..."
    pip install -r requirements-editor.txt
    echo ""
fi

# Запуск редактора
echo "✅ Запуск редактора..."
python3 loadshape_editor.py

echo ""
echo "👋 Редактор закрыт."
