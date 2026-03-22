# 🚀 Установка и запуск визуального редактора

## Быстрая установка

### Шаг 1: Установка зависимостей

```bash
pip install -r requirements-editor.txt
```

Или вручную:

```bash
pip install matplotlib
```

### Шаг 2: Проверка установки

```bash
python3 -c "import matplotlib; import tkinter; print('✅ Всё установлено!')"
```

### Шаг 3: Запуск редактора

```bash
./run_editor.sh
```

Или напрямую:

```bash
python3 loadshape_editor.py
```

## Устранение проблем

### Проблема 1: ModuleNotFoundError: No module named 'matplotlib'

**Решение:**

```bash
pip install matplotlib
```

Если не помогло:

```bash
pip3 install matplotlib
# или
python3 -m pip install matplotlib
```

### Проблема 2: ModuleNotFoundError: No module named '_tkinter'

**Решение для Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Решение для Fedora/RHEL:**

```bash
sudo dnf install python3-tkinter
```

**Решение для Arch Linux:**

```bash
sudo pacman -S tk
```

**Решение для macOS:**

```bash
brew install python-tk
```

### Проблема 3: Permission denied при запуске ./run_editor.sh

**Решение:**

```bash
chmod +x run_editor.sh
./run_editor.sh
```

### Проблема 4: Редактор запускается, но график не отображается

**Решение:**

```bash
# Установите правильный backend для matplotlib
export MPLBACKEND=TkAgg
python3 loadshape_editor.py
```

Или добавьте в начало `loadshape_editor.py`:

```python
import matplotlib
matplotlib.use('TkAgg')
```

### Проблема 5: Не сохраняются изменения в файл

**Проверьте права:**

```bash
ls -la loadshape_stability.py
```

**Дайте права на запись:**

```bash
chmod u+w loadshape_stability.py
```

## Системные требования

- **Python**: 3.7 или выше
- **matplotlib**: 3.5.0 или выше
- **tkinter**: обычно входит в состав Python
- **ОС**: Linux, macOS, Windows

## Проверка версий

```bash
# Проверка версии Python
python3 --version

# Проверка версии matplotlib
python3 -c "import matplotlib; print(matplotlib.__version__)"

# Проверка наличия tkinter
python3 -c "import tkinter; print('tkinter OK')"
```

## Альтернативные методы установки

### Использование виртуального окружения (рекомендуется)

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements-editor.txt

# Запуск редактора
python3 loadshape_editor.py
```

### Установка в пользовательскую директорию

```bash
pip install --user matplotlib
```

### Установка конкретной версии

```bash
pip install matplotlib==3.5.0
```

## Первый запуск

После успешной установки:

1. Запустите редактор:
   ```bash
   ./run_editor.sh
   ```

2. Вы увидите окно редактора с:
   - Списком существующих этапов из `loadshape_stability.py`
   - Графиком текущего профиля нагрузки
   - Кнопками управления

3. Попробуйте:
   - Выбрать этап в списке
   - Нажать "✏️ Редактировать"
   - Изменить параметры
   - Нажать "✅ Сохранить"
   - Посмотреть обновлённый график

4. Для сохранения изменений:
   - Нажмите "💾 Сохранить в файл"
   - Подтвердите сохранение

## Дополнительная помощь

Если проблема не решена:

1. Проверьте логи:
   ```bash
   python3 loadshape_editor.py 2>&1 | tee editor.log
   ```

2. Проверьте зависимости:
   ```bash
   pip list | grep matplotlib
   ```

3. Попробуйте переустановить:
   ```bash
   pip uninstall matplotlib
   pip install matplotlib
   ```

## Документация

- Полное руководство: [EDITOR_GUIDE.md](EDITOR_GUIDE.md)
- Шаблоны профилей: [loadshape_templates.py](loadshape_templates.py)
- Общая документация: [README.md](README.md)

---

**Если всё работает - приятного использования! 🎉**
