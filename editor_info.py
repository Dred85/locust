#!/usr/bin/env python3
"""
Информация о визуальном редакторе профилей нагрузки Locust
"""
import sys
import os


def print_banner():
    """Вывод баннера"""
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   🎨 ВИЗУАЛЬНЫЙ РЕДАКТОР ПРОФИЛЕЙ НАГРУЗКИ LOCUST 🎨                 ║
║                                                                      ║
║   Графический инструмент для создания и редактирования               ║
║   профилей нагрузки (LoadShape) в Locust                            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """Проверка зависимостей"""
    print("\n📦 Проверка зависимостей:\n")
    
    dependencies = {
        "Python": None,
        "matplotlib": None,
        "tkinter": None
    }
    
    # Проверка Python
    try:
        version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        dependencies["Python"] = version
        print(f"  ✅ Python {version}")
    except Exception as e:
        print(f"  ❌ Python: {e}")
    
    # Проверка matplotlib
    try:
        import matplotlib
        dependencies["matplotlib"] = matplotlib.__version__
        print(f"  ✅ matplotlib {matplotlib.__version__}")
    except ImportError:
        print(f"  ❌ matplotlib не установлен")
        print(f"     Установите: pip install matplotlib")
    
    # Проверка tkinter
    try:
        import tkinter
        dependencies["tkinter"] = "OK"
        print(f"  ✅ tkinter установлен")
    except ImportError:
        print(f"  ❌ tkinter не установлен")
        print(f"     Установите: sudo apt-get install python3-tk")
    
    return all(v is not None for v in dependencies.values())


def print_features():
    """Вывод возможностей"""
    print("\n✨ Возможности редактора:\n")
    
    features = [
        "Визуальный график нагрузки в реальном времени",
        "Добавление новых этапов нагрузки",
        "Редактирование существующих этапов",
        "Удаление ненужных этапов",
        "Перемещение этапов (изменение порядка)",
        "Выбор User Classes для каждого этапа",
        "Статистика профиля (длительность, пользователи)",
        "Предварительный просмотр сгенерированного кода",
        "Автоматическое сохранение в loadshape_stability.py",
        "Управление кумулятивными duration"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"  {i:2d}. ✅ {feature}")


def print_quick_start():
    """Вывод инструкций по быстрому старту"""
    print("\n🚀 Быстрый старт:\n")
    
    print("  1. Установите зависимости:")
    print("     $ pip install -r requirements-editor.txt")
    print()
    print("  2. Запустите редактор:")
    print("     $ ./run_editor.sh")
    print("     или")
    print("     $ python3 loadshape_editor.py")
    print()
    print("  3. Используйте интерфейс:")
    print("     - Добавляйте/редактируйте этапы")
    print("     - Смотрите график в реальном времени")
    print("     - Сохраняйте изменения в файл")


def print_files():
    """Вывод списка файлов"""
    print("\n📁 Файлы проекта:\n")
    
    files = {
        "loadshape_editor.py": "Главный файл редактора",
        "run_editor.sh": "Скрипт быстрого запуска",
        "requirements-editor.txt": "Зависимости",
        "EDITOR_GUIDE.md": "Полное руководство",
        "INSTALL.md": "Инструкции по установке",
        "loadshape_templates.py": "Шаблоны профилей",
        "editor_info.py": "Этот скрипт (информация)"
    }
    
    for filename, description in files.items():
        exists = "✅" if os.path.exists(filename) else "❌"
        print(f"  {exists} {filename:30s} - {description}")


def print_templates():
    """Вывод информации о шаблонах"""
    print("\n📊 Доступные шаблоны профилей:\n")
    
    try:
        from loadshape_templates import TEMPLATE_DESCRIPTIONS
        
        for i, (template_name, info) in enumerate(TEMPLATE_DESCRIPTIONS.items(), 1):
            print(f"  {i:2d}. {info['name']}")
            print(f"      Длительность: {info['duration']}")
            print(f"      Макс. пользователей: {info['max_users']}")
            print(f"      Применение: {info['use_case']}")
            print()
    except ImportError:
        print("  ⚠️  Файл loadshape_templates.py не найден")


def print_documentation():
    """Вывод ссылок на документацию"""
    print("\n📚 Документация:\n")
    
    docs = {
        "EDITOR_GUIDE.md": "Полное руководство по использованию",
        "INSTALL.md": "Инструкции по установке и устранению проблем",
        "README.md": "Общая документация проекта",
        "../EDITOR_README.md": "Краткая инструкция (в корне проекта)"
    }
    
    for filename, description in docs.items():
        exists = "✅" if os.path.exists(filename) else "❌"
        print(f"  {exists} {filename:30s} - {description}")


def print_footer():
    """Вывод футера"""
    print("\n" + "═" * 72)
    print("  Для запуска редактора выполните: ./run_editor.sh")
    print("  Для просмотра шаблонов: python3 loadshape_templates.py")
    print("═" * 72)
    print()


def main():
    """Главная функция"""
    print_banner()
    
    all_ok = check_dependencies()
    
    print_features()
    print_quick_start()
    print_files()
    print_templates()
    print_documentation()
    print_footer()
    
    if not all_ok:
        print("⚠️  Внимание: Не все зависимости установлены!")
        print("   Выполните: pip install -r requirements-editor.txt\n")
        return 1
    else:
        print("✅ Всё готово к работе!\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
