#!/usr/bin/env python3
"""
Визуальный редактор профилей нагрузки Locust
Для редактирования loadshape_stability.py
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import re
from pathlib import Path
from typing import List, Dict, Any
import copy
import os


class LoadShapeEditor:
    def __init__(self, root, filepath=None):
        self.root = root
        self.root.geometry("1400x900")
        
        # Определяем путь к файлу
        if filepath is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.filepath = os.path.join(script_dir, "loadshape_stability.py")
        else:
            self.filepath = filepath
        
        # Устанавливаем заголовок окна с именем файла
        self.root.title(f"Locust Load Shape Editor - {os.path.basename(self.filepath)}")
        
        # Доступные user classes
        self.available_user_classes = [
            "WebUser_UC01",  # GET / - главная
            "WebUser_UC02",  # GET /contact - страница формы
            "WebUser_UC03",  # GET /about - о нас
            "WebUser_UC04",  # GET /projects - проекты
            "WebUser_UC05",  # POST /contact - отправка формы
            "WebUser_UC05_API",  # POST /api/contact - JSON API
            "WebUser_UC06"  # GET /metrics - метрики Prometheus
        ]
        
        self.stages = []
        self.current_stage_index = None
        
        # Параметры калькулятора нагрузки
        self.avg_requests_per_user = 10  # среднее кол-во запросов на пользователя в минуту
        self.avg_response_time = 0.5  # средняя длительность ответа в секундах
        self.avg_request_size_kb = 5  # средний размер запроса в KB
        self.avg_response_size_kb = 10  # средний размер ответа в KB
        
        # Загрузка существующих данных
        print(f"[DEBUG] Загрузка файла: {self.filepath}")
        self.load_from_file()
        print(f"[DEBUG] Загружено этапов: {len(self.stages)}")
        
        # Создание интерфейса
        self.create_ui()
        
        # Первоначальная отрисовка графика
        self.update_graph()
        
        # Показываем сообщение если файл успешно загружен
        if self.stages:
            print(f"[INFO] Успешно загружено {len(self.stages)} этапов из файла")
        else:
            print(f"[WARNING] Файл пуст или не содержит этапов")
    
    def load_from_file(self):
        """Загрузка stages из существующего файла"""
        self.stages = []  # Очищаем список перед загрузкой
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Поиск определения stages (более гибкий паттерн)
            pattern = r'stages\s*=\s*\[(.*?)\n\s*\]'
            match = re.search(pattern, content, re.DOTALL)
            
            if not match:
                # Попробуем альтернативный паттерн
                pattern = r'stages\s*=\s*\[(.*?)\]'
                match = re.search(pattern, content, re.DOTALL)
            
            if match:
                stages_text = match.group(1)
                
                # Парсинг каждого stage (улучшенный подход для многострочных структур)
                # Разделяем по `},` чтобы получить отдельные словари
                stage_parts = stages_text.split('},')
                
                for stage_part in stage_parts:
                    # Пропускаем пустые части
                    if not stage_part.strip():
                        continue
                    
                    # Добавляем обратно закрывающую скобку если она была удалена
                    stage_str = stage_part.strip()
                    if not stage_str.endswith('}'):
                        stage_str += '}'
                    
                    # Проверяем что это действительно stage (содержит duration)
                    if '"duration"' not in stage_str:
                        continue
                    
                    try:
                        # Извлечение параметров
                        duration_match = re.search(r'"duration":\s*(\d+)', stage_str)
                        users_match = re.search(r'"users":\s*(\d+)', stage_str)
                        spawn_rate_match = re.search(r'"spawn_rate":\s*(\d+)', stage_str)
                        
                        if not (duration_match and users_match and spawn_rate_match):
                            continue
                        
                        duration = int(duration_match.group(1))
                        users = int(users_match.group(1))
                        spawn_rate = int(spawn_rate_match.group(1))
                        
                        # Извлечение user_classes (БЕЗ кавычек - как имена классов Python)
                        # Поддержка многострочных массивов
                        user_classes_match = re.search(r'"user_classes":\s*\[([^\]]+)\]', stage_str, re.DOTALL)
                        user_classes = []
                        
                        if user_classes_match:
                            classes_text = user_classes_match.group(1)
                            # Удаляем пробелы, переносы строк и разделяем по запятой
                            classes_text = classes_text.replace('\n', ' ').replace('\r', '')
                            user_classes = [uc.strip() for uc in classes_text.split(',') if uc.strip()]
                        
                        self.stages.append({
                            "duration": duration,
                            "users": users,
                            "spawn_rate": spawn_rate,
                            "user_classes": user_classes
                        })
                    
                    except Exception as e:
                        print(f"Ошибка парсинга этапа: {e}")
                        continue
                
                if not self.stages:
                    messagebox.showwarning("Предупреждение", 
                        f"Файл не содержит корректных этапов нагрузки.\n"
                        f"Убедитесь, что файл содержит блок 'stages = [...]'")
            else:
                messagebox.showwarning("Предупреждение", 
                    f"В файле не найден блок 'stages'.\n"
                    f"Создайте новый профиль или выберите другой файл.")
        
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл не найден:\n{self.filepath}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}\n\nПодробности: {type(e).__name__}")
            import traceback
            traceback.print_exc()
    
    def create_menu(self):
        """Создание меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        file_menu.add_command(label="Открыть...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_to_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Меню Инструменты
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Инструменты", menu=tools_menu)
        
        tools_menu.add_command(label="Настройки калькулятора", command=self.show_calculator_settings)
        
        # Меню Помощь
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        
        help_menu.add_command(label="Предварительный просмотр кода", command=self.preview_code)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        # Горячие клавиши
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_to_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    def open_file(self):
        """Открытие файла LoadShape"""
        # Диалог выбора файла
        initial_dir = os.path.dirname(self.filepath) if self.filepath else os.getcwd()
        
        filename = filedialog.askopenfilename(
            title="Открыть профиль нагрузки Locust",
            initialdir=initial_dir,
            filetypes=[
                ("Python файлы", "*.py"),
                ("Все файлы", "*.*")
            ]
        )
        
        if filename:
            # Обновляем путь к файлу
            self.filepath = filename
            
            # Очищаем текущие stages
            self.stages = []
            
            # Загружаем новый файл
            self.load_from_file()
            
            # Обновляем интерфейс
            self.refresh_stages_list()
            self.update_graph()
            self.update_file_info()
            self.update_window_title()
            
            messagebox.showinfo("Успех", f"Файл открыт:\n{os.path.basename(filename)}")
    
    def update_file_info(self):
        """Обновление информации о файле"""
        if hasattr(self, 'file_label'):
            self.file_label.config(text=os.path.basename(self.filepath))
    
    def update_window_title(self):
        """Обновление заголовка окна"""
        filename = os.path.basename(self.filepath)
        self.root.title(f"Locust Load Shape Editor - {filename}")
    
    def show_calculator_settings(self):
        """Окно настроек калькулятора нагрузки"""
        try:
            settings_window = tk.Toplevel(self.root)
            settings_window.title("Настройки калькулятора нагрузки")
            settings_window.geometry("550x450")
            settings_window.transient(self.root)
            settings_window.grab_set()
            
            # Заголовок
            title_frame = ttk.Frame(settings_window, padding=10)
            title_frame.pack(fill=tk.X)
            ttk.Label(title_frame, text="Настройте параметры для расчета метрик нагрузки", 
                      font=("Arial", 11, "bold")).pack()
            
            # Фрейм с настройками
            main_frame = ttk.Frame(settings_window, padding=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Поля ввода
            fields = []
            
            # Requests per user per minute
            row1 = ttk.Frame(main_frame)
            row1.pack(fill=tk.X, pady=5)
            ttk.Label(row1, text="Запросов на пользователя в минуту:", width=35).pack(side=tk.LEFT)
            entry1 = ttk.Entry(row1, width=15)
            entry1.insert(0, str(self.avg_requests_per_user))
            entry1.pack(side=tk.LEFT, padx=5)
            ttk.Label(row1, text="req/user/min").pack(side=tk.LEFT)
            fields.append(('avg_requests_per_user', entry1, float))
            
            # Average response time
            row2 = ttk.Frame(main_frame)
            row2.pack(fill=tk.X, pady=5)
            ttk.Label(row2, text="Среднее время ответа:", width=35).pack(side=tk.LEFT)
            entry2 = ttk.Entry(row2, width=15)
            entry2.insert(0, str(self.avg_response_time))
            entry2.pack(side=tk.LEFT, padx=5)
            ttk.Label(row2, text="секунд").pack(side=tk.LEFT)
            fields.append(('avg_response_time', entry2, float))
            
            # Average request size
            row3 = ttk.Frame(main_frame)
            row3.pack(fill=tk.X, pady=5)
            ttk.Label(row3, text="Средний размер запроса:", width=35).pack(side=tk.LEFT)
            entry3 = ttk.Entry(row3, width=15)
            entry3.insert(0, str(self.avg_request_size_kb))
            entry3.pack(side=tk.LEFT, padx=5)
            ttk.Label(row3, text="KB").pack(side=tk.LEFT)
            fields.append(('avg_request_size_kb', entry3, float))
            
            # Average response size
            row4 = ttk.Frame(main_frame)
            row4.pack(fill=tk.X, pady=5)
            ttk.Label(row4, text="Средний размер ответа:", width=35).pack(side=tk.LEFT)
            entry4 = ttk.Entry(row4, width=15)
            entry4.insert(0, str(self.avg_response_size_kb))
            entry4.pack(side=tk.LEFT, padx=5)
            ttk.Label(row4, text="KB").pack(side=tk.LEFT)
            fields.append(('avg_response_size_kb', entry4, float))
            
            # Информация
            info_frame = ttk.Frame(main_frame)
            info_frame.pack(fill=tk.X, pady=10)
            info_text = "Эти параметры используются для расчета:\n"
            info_text += "• Ожидаемого RPS (requests per second)\n"
            info_text += "• Требований к bandwidth\n"
            info_text += "• Concurrent connections"
            ttk.Label(info_frame, text=info_text, justify=tk.LEFT, 
                      foreground="gray", font=("Arial", 8)).pack(anchor=tk.W)
            
            # Разделитель
            ttk.Separator(settings_window, orient='horizontal').pack(fill=tk.X, pady=10)
            
            # Кнопки
            buttons_frame = ttk.Frame(settings_window, padding=15)
            buttons_frame.pack(fill=tk.X)
            
            def save_settings():
                try:
                    for field_name, entry, field_type in fields:
                        value = field_type(entry.get())
                        if value <= 0:
                            raise ValueError(f"{field_name} должен быть положительным числом")
                        setattr(self, field_name, value)
                    
                    # Обновляем расчеты
                    self.calculate_load_metrics()
                    messagebox.showinfo("Успех", "Настройки калькулятора сохранены!")
                    settings_window.destroy()
                except ValueError as e:
                    messagebox.showerror("Ошибка", f"Неверное значение:\n{e}")
            
            def reset_defaults():
                entry1.delete(0, tk.END)
                entry1.insert(0, "10")
                entry2.delete(0, tk.END)
                entry2.insert(0, "0.5")
                entry3.delete(0, tk.END)
                entry3.insert(0, "5")
                entry4.delete(0, tk.END)
                entry4.insert(0, "10")
            
            save_btn = ttk.Button(buttons_frame, text="Сохранить", command=save_settings, width=15)
            save_btn.pack(side=tk.LEFT, padx=5, pady=5)
            
            reset_btn = ttk.Button(buttons_frame, text="По умолчанию", command=reset_defaults, width=15)
            reset_btn.pack(side=tk.LEFT, padx=5, pady=5)
            
            cancel_btn = ttk.Button(buttons_frame, text="Отмена", command=settings_window.destroy, width=15)
            cancel_btn.pack(side=tk.RIGHT, padx=5, pady=5)
            
        except Exception as e:
            import traceback
            error_msg = f"Ошибка при открытии окна настроек:\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Ошибка", f"Не удалось открыть окно настроек:\n{str(e)}")
    
    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
Визуальный редактор профилей нагрузки Locust
Версия 1.0.0

Возможности:
• Визуальный график нагрузки
• Добавление/редактирование этапов
• Выбор User Classes
• Сохранение в файл

Создано для FastAPI Portfolio Load Testing
        """
        messagebox.showinfo("О программе", about_text.strip())
    
    def create_ui(self):
        """Создание интерфейса"""
        # Создание меню
        self.create_menu()
        
        # Главный контейнер с двумя панелями
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Левая панель - список stages и управление
        left_frame = ttk.Frame(main_paned, width=500)
        main_paned.add(left_frame, weight=1)
        
        # Правая панель - график
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        # === ЛЕВАЯ ПАНЕЛЬ ===
        
        # Заголовок
        ttk.Label(left_frame, text="Этапы нагрузки", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Список stages
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.stages_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.stages_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.stages_listbox.yview)
        self.stages_listbox.bind('<<ListboxSelect>>', self.on_stage_select)
        
        # Кнопки управления stages
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="➕ Добавить", command=self.add_stage).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="✏️ Редактировать", command=self.edit_stage).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="❌ Удалить", command=self.delete_stage).pack(side=tk.LEFT, padx=2)
        
        # Статистика
        stats_frame = ttk.LabelFrame(left_frame, text="Статистика", padding=10)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="", font=("Arial", 9))
        self.stats_label.pack()
        
        # Калькулятор нагрузки
        calc_frame = ttk.LabelFrame(left_frame, text="Калькулятор нагрузки", padding=10)
        calc_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.calc_label = ttk.Label(calc_frame, text="", font=("Arial", 9), foreground="darkgreen")
        self.calc_label.pack()
        
        # Информация о файле
        file_info_frame = ttk.LabelFrame(left_frame, text="Файл", padding=10)
        file_info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.file_label = ttk.Label(file_info_frame, text=os.path.basename(self.filepath), 
                              font=("Arial", 9), foreground="blue")
        self.file_label.pack()
        
        # Кнопки сохранения
        save_frame = ttk.Frame(left_frame)
        save_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(save_frame, text="💾 Сохранить в файл", command=self.save_with_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(save_frame, text="👁️ Просмотр кода", command=self.preview_code).pack(fill=tk.X, pady=2)
        
        # === ПРАВАЯ ПАНЕЛЬ - ГРАФИК ===
        
        ttk.Label(right_frame, text="График нагрузки", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Matplotlib график
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figure, right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Интерактивная подсказка при наведении курсора
        self.cursor_annotation = None
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        
        # Обновление списка
        self.refresh_stages_list()
    
    def refresh_stages_list(self):
        """Обновление списка stages"""
        self.stages_listbox.delete(0, tk.END)
        cumulative_time = 0
        
        for i, stage in enumerate(self.stages):
            duration = stage["duration"]
            users = stage["users"]
            spawn_rate = stage["spawn_rate"]
            user_classes = ", ".join(stage["user_classes"])
            
            time_range = f"{cumulative_time:3d}-{duration:3d}s"
            text = f"{i+1}. {time_range} | Users: {users:3d} | Rate: {spawn_rate} | {user_classes[:30]}"
            
            self.stages_listbox.insert(tk.END, text)
            cumulative_time = duration
        
        self.update_stats()
    
    def update_stats(self):
        """Обновление статистики"""
        if not self.stages:
            self.stats_label.config(text="Нет этапов")
            return
        
        total_duration = self.stages[-1]["duration"] if self.stages else 0
        max_users = max([s["users"] for s in self.stages]) if self.stages else 0
        num_stages = len(self.stages)
        
        stats_text = f"Этапов: {num_stages}\n"
        stats_text += f"Общая длительность: {total_duration} сек ({total_duration//60} мин)\n"
        stats_text += f"Максимум пользователей: {max_users}"
        
        self.stats_label.config(text=stats_text)
        self.calculate_load_metrics()
    
    def calculate_load_metrics(self):
        """Расчет метрик нагрузки"""
        # Проверяем, что виджет калькулятора создан
        if not hasattr(self, 'calc_label'):
            return
        
        if not self.stages:
            self.calc_label.config(text="Нет данных для расчета")
            return
        
        # Расчет метрик
        max_users = max([s["users"] for s in self.stages])
        total_duration = self.stages[-1]["duration"] if self.stages else 0
        
        # Ожидаемый RPS на пике
        peak_rps = (max_users * self.avg_requests_per_user) / 60
        
        # Средний RPS (учитываем все этапы с весами по времени)
        weighted_users = 0
        for i, stage in enumerate(self.stages):
            prev_duration = self.stages[i-1]["duration"] if i > 0 else 0
            stage_duration = stage["duration"] - prev_duration
            weighted_users += stage["users"] * stage_duration
        
        avg_users = weighted_users / total_duration if total_duration > 0 else 0
        avg_rps = (avg_users * self.avg_requests_per_user) / 60
        
        # Общий throughput (total requests)
        total_requests = (avg_users * self.avg_requests_per_user * total_duration) / 60
        
        # Оценка требований к ресурсам (concurrent connections)
        concurrent_connections = max_users * self.avg_response_time * peak_rps
        
        # Оценка требований к полосе пропускания
        total_transfer_kb = (self.avg_request_size_kb + self.avg_response_size_kb)
        peak_bandwidth_mbps = (peak_rps * total_transfer_kb * 8) / 1024  # *8 для битов, /1024 для MB
        avg_bandwidth_mbps = (avg_rps * total_transfer_kb * 8) / 1024
        
        # Оценка данных за тест
        total_data_gb = (total_requests * total_transfer_kb) / (1024 * 1024)
        
        # Формирование текста
        calc_text = f"🎯 Пиковая нагрузка: {max_users} польз.\n"
        calc_text += f"📊 Средняя нагрузка: {avg_users:.1f} польз.\n"
        calc_text += f"📈 Пиковый RPS: ~{peak_rps:.1f}\n"
        calc_text += f"📉 Средний RPS: ~{avg_rps:.1f}\n"
        calc_text += f"🔢 Всего запросов: ~{total_requests:.0f}\n"
        calc_text += f"🔗 Max connections: ~{concurrent_connections:.0f}\n"
        calc_text += f"🌐 Пиковый bandwidth: ~{peak_bandwidth_mbps:.2f} Mbps\n"
        calc_text += f"📊 Средний bandwidth: ~{avg_bandwidth_mbps:.2f} Mbps\n"
        calc_text += f"💾 Общий трафик: ~{total_data_gb:.2f} GB\n"
        calc_text += f"\n💡 Параметры:\n"
        calc_text += f"   • {self.avg_requests_per_user} req/user/min\n"
        calc_text += f"   • {self.avg_response_time}s response time\n"
        calc_text += f"   • {self.avg_request_size_kb}KB req + {self.avg_response_size_kb}KB resp"
        
        self.calc_label.config(text=calc_text)
    
    def update_graph(self):
        """Обновление графика нагрузки"""
        self.ax.clear()
        self.cursor_annotation = None  # Сбрасываем аннотацию при перерисовке
        
        if not self.stages:
            self.ax.text(0.5, 0.5, 'Нет данных для отображения', 
                        ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return
        
        # Построение ступенчатого графика
        times = []
        users = []
        
        prev_duration = 0
        for i, stage in enumerate(self.stages):
            current_duration = stage["duration"]
            current_users = stage["users"]
            
            # Добавляем начало ступени (вертикальный переход)
            times.append(prev_duration)
            users.append(current_users)
            
            # Добавляем конец ступени (горизонтальное плато)
            times.append(current_duration)
            users.append(current_users)
            
            prev_duration = current_duration
        
        # Заполнение области под графиком
        self.ax.fill_between(times, users, alpha=0.3, color='blue')
        self.ax.plot(times, users, '-', linewidth=2, color='darkblue')
        
        # Маркеры на границах этапов
        stage_times = [stage["duration"] for stage in self.stages]
        stage_users = [stage["users"] for stage in self.stages]
        self.ax.plot(stage_times, stage_users, 'o', markersize=8, color='darkblue')
        
        # Аннотации для каждого этапа
        for i, stage in enumerate(self.stages):
            time = stage["duration"]
            user_count = stage["users"]
            self.ax.annotate(f'{user_count} users', 
                           xy=(time, user_count), 
                           xytext=(10, 10),
                           textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                           fontsize=8)
        
        self.ax.set_xlabel('Время (секунды)', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('Количество пользователей', fontsize=12, fontweight='bold')
        self.ax.set_title('Профиль нагрузки Locust', fontsize=14, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(bottom=0)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def on_mouse_move(self, event):
        """Отображение времени теста при наведении курсора на график"""
        if not self.stages or event.inaxes != self.ax:
            # Если курсор вне графика или нет данных - скрываем аннотацию
            if self.cursor_annotation:
                self.cursor_annotation.set_visible(False)
                self.canvas.draw_idle()
            return
        
        # Получаем координаты курсора
        x_pos = event.xdata  # время в секундах
        y_pos = event.ydata  # количество пользователей
        
        if x_pos is None or y_pos is None:
            return
        
        # Находим текущее количество пользователей для данного времени
        current_users = 0
        for stage in self.stages:
            if x_pos <= stage["duration"]:
                current_users = stage["users"]
                break
        
        # Форматирование времени
        minutes = int(x_pos // 60)
        seconds = int(x_pos % 60)
        
        # Создаём или обновляем аннотацию
        tooltip_text = f"Время: {minutes}м {seconds}с ({int(x_pos)}с)\nПользователей: {current_users}"
        
        if self.cursor_annotation is None:
            # Создаём аннотацию при первом наведении
            self.cursor_annotation = self.ax.annotate(
                tooltip_text,
                xy=(x_pos, y_pos),
                xytext=(20, 20),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.8', fc='lightyellow', ec='gray', alpha=0.95),
                fontsize=9,
                fontweight='bold',
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='gray', lw=1.5)
            )
        else:
            # Обновляем существующую аннотацию
            self.cursor_annotation.set_text(tooltip_text)
            self.cursor_annotation.xy = (x_pos, y_pos)
            self.cursor_annotation.set_visible(True)
        
        self.canvas.draw_idle()
    
    def on_stage_select(self, event):
        """Обработчик выбора stage"""
        selection = self.stages_listbox.curselection()
        if selection:
            self.current_stage_index = selection[0]
    
    def add_stage(self):
        """Добавление нового stage"""
        dialog = StageDialog(self.root, self.available_user_classes)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            # Вычисление нового duration (кумулятивного)
            last_duration = self.stages[-1]["duration"] if self.stages else 0
            dialog.result["duration"] = last_duration + dialog.result["duration"]
            
            self.stages.append(dialog.result)
            self.refresh_stages_list()
            self.update_graph()
    
    def edit_stage(self):
        """Редактирование существующего stage"""
        if self.current_stage_index is None:
            messagebox.showwarning("Предупреждение", "Выберите этап для редактирования")
            return
        
        stage = copy.deepcopy(self.stages[self.current_stage_index])
        
        # Вычисление относительной длительности
        if self.current_stage_index > 0:
            prev_duration = self.stages[self.current_stage_index - 1]["duration"]
            stage["duration"] = stage["duration"] - prev_duration
        
        dialog = StageDialog(self.root, self.available_user_classes, stage)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            # Пересчёт кумулятивной длительности
            if self.current_stage_index > 0:
                prev_duration = self.stages[self.current_stage_index - 1]["duration"]
                dialog.result["duration"] = prev_duration + dialog.result["duration"]
            
            self.stages[self.current_stage_index] = dialog.result
            
            # Обновление последующих stages
            self.recalculate_durations()
            
            self.refresh_stages_list()
            self.update_graph()
    
    def delete_stage(self):
        """Удаление stage"""
        if self.current_stage_index is None:
            messagebox.showwarning("Предупреждение", "Выберите этап для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный этап?"):
            del self.stages[self.current_stage_index]
            self.recalculate_durations()
            self.current_stage_index = None
            self.refresh_stages_list()
            self.update_graph()
    
    def get_relative_durations(self):
        """Получить список относительных длительностей из кумулятивных"""
        relative_durations = []
        for i, stage in enumerate(self.stages):
            if i == 0:
                relative_durations.append(stage["duration"])
            else:
                relative_durations.append(stage["duration"] - self.stages[i-1]["duration"])
        return relative_durations
    
    def apply_relative_durations(self, relative_durations):
        """Применить относительные длительности, пересчитав кумулятивные"""
        cumulative = 0
        for i, duration in enumerate(relative_durations):
            cumulative += duration
            self.stages[i]["duration"] = cumulative
    
    def recalculate_durations(self):
        """Пересчёт кумулятивных длительностей после изменений"""
        relative_durations = self.get_relative_durations()
        self.apply_relative_durations(relative_durations)
    
    def generate_code(self):
        """Генерация Python кода для LoadShape"""
        if not self.stages:
            return '    stages = []'
        
        code_lines = ['    stages = [']
        
        for i, stage in enumerate(self.stages):
            # Форматирование user_classes
            user_classes_str = ', '.join(stage['user_classes'])
            
            # Комментарий для первого этапа
            comment = "  # Прогрев" if i == 0 else ""
            
            # Формирование строки этапа
            line = f'        {{"duration": {stage["duration"]}, "users": {stage["users"]}, '
            line += f'"spawn_rate": {stage["spawn_rate"]}, "user_classes": [{user_classes_str}]}}'
            
            # Добавляем запятую если это не последний элемент
            if i < len(self.stages) - 1:
                line += ','
            
            # Добавляем комментарий
            line += comment
            
            code_lines.append(line)
        
        code_lines.append('    ]')
        
        return '\n'.join(code_lines)
    
    def preview_code(self):
        """Предварительный просмотр кода"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Предварительный просмотр кода")
        preview_window.geometry("800x600")
        
        text_widget = scrolledtext.ScrolledText(preview_window, wrap=tk.NONE, font=("Courier", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        code = self.generate_code()
        text_widget.insert('1.0', code)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(preview_window, text="Закрыть", command=preview_window.destroy).pack(pady=5)
    
    def save_as_file(self):
        """Сохранение профиля с новым именем"""
        # Диалог сохранения файла
        initial_dir = os.path.dirname(self.filepath) if self.filepath else os.getcwd()
        initial_filename = os.path.basename(self.filepath) if self.filepath else "loadshape_new.py"
        
        filename = filedialog.asksaveasfilename(
            title="Сохранить профиль нагрузки как...",
            initialdir=initial_dir,
            initialfile=initial_filename,
            defaultextension=".py",
            filetypes=[
                ("Python файлы", "*.py"),
                ("Все файлы", "*.*")
            ]
        )
        
        if filename:
            # Временно сохраняем старый путь
            old_filepath = self.filepath
            
            # Обновляем путь к файлу
            self.filepath = filename
            
            try:
                # Если файл новый, создаём базовую структуру
                is_new_file = not os.path.exists(filename)
                
                if is_new_file:
                    # Создаём новый файл с текущим профилем
                    self.create_new_file(filename)
                else:
                    # Обновляем существующий файл
                    self.save_to_file_internal()
                
                # Обновляем интерфейс
                self.update_file_info()
                self.update_window_title()
                
                messagebox.showinfo("Успех", f"Файл сохранён как:\n{os.path.basename(filename)}")
            
            except Exception as e:
                # В случае ошибки возвращаем старый путь
                self.filepath = old_filepath
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
    
    def create_new_file(self, filename):
        """Создание нового файла LoadShape с базовой структурой"""
        # Генерируем код stages из текущего профиля
        stages_code = self.generate_code()
        
        template = f'''"""
Профиль нагрузки Locust
Создано в визуальном редакторе
"""
from locust import LoadTestShape

from locustfile import (
    WebUser_UC01,
    WebUser_UC02,
    WebUser_UC03,
    WebUser_UC04,
    WebUser_UC05,
    WebUser_UC05_API,
    WebUser_UC06
)


class LoadShape(LoadTestShape):
    """Профиль нагрузки"""
{stages_code}

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
'''
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(template)
    
    def save_with_dialog(self):
        """Сохранение с диалогом выбора: перезаписать или сохранить как"""
        # Создаём диалог выбора
        dialog = tk.Toplevel(self.root)
        dialog.title("Сохранить профиль")
        dialog.geometry("400x180")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Центрируем диалог
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        result = {'action': None}
        
        # Заголовок
        ttk.Label(dialog, text="Как сохранить профиль?", 
                 font=("Arial", 12, "bold")).pack(pady=15)
        
        # Информация о файле
        filename = os.path.basename(self.filepath)
        ttk.Label(dialog, text=f"Файл: {filename}", 
                 font=("Arial", 9), foreground="gray").pack(pady=5)
        
        # Кнопки
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=20)
        
        def on_overwrite():
            result['action'] = 'overwrite'
            dialog.destroy()
        
        def on_save_as():
            result['action'] = 'save_as'
            dialog.destroy()
        
        def on_cancel():
            result['action'] = 'cancel'
            dialog.destroy()
        
        ttk.Button(buttons_frame, text="✏️ Перезаписать файл", 
                  command=on_overwrite, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="💾 Сохранить как...", 
                  command=on_save_as, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(dialog, text="❌ Отмена", command=on_cancel).pack(pady=5)
        
        # Ждём закрытия диалога
        self.root.wait_window(dialog)
        
        # Выполняем действие
        if result['action'] == 'overwrite':
            self.save_to_file()
        elif result['action'] == 'save_as':
            self.save_as_file()
    
    def save_to_file(self):
        """Сохранение изменений в текущий файл"""
        try:
            self.save_to_file_internal()
            messagebox.showinfo("Успех", f"Файл успешно сохранён:\n{os.path.basename(self.filepath)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
    
    def save_to_file_internal(self):
        """Внутренняя логика сохранения файла (без messagebox)"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Генерация нового кода stages
        new_stages_code = self.generate_code()
        
        # Улучшенный паттерн для полной замены блока stages
        # Ищем "stages = [" до соответствующей закрывающей "]"
        # Используем многострочный режим и учитываем отступы
        pattern = r'(    stages\s*=\s*\[)(.*?)(\n    \])'
        
        # Проверяем, есть ли блок stages
        if re.search(pattern, content, re.DOTALL):
            # Заменяем только содержимое между [ и ]
            stages_content = '\n' + '\n'.join(new_stages_code.split('\n')[1:-1]) + '\n'
            new_content = re.sub(pattern, r'\g<1>' + stages_content + r'\g<3>', content, flags=re.DOTALL)
        else:
            # Если блока stages нет, ищем класс и добавляем
            class_pattern = r'(class \w+\(LoadTestShape\):.*?""")'
            new_content = re.sub(
                class_pattern, 
                r'\g<1>\n' + new_stages_code + '\n',
                content,
                flags=re.DOTALL
            )
        
        # Сохранение
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)


class StageDialog:
    """Диалог для добавления/редактирования stage"""
    
    def __init__(self, parent, available_user_classes, stage=None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Редактирование этапа" if stage else "Новый этап")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.available_user_classes = available_user_classes
        self.result = None
        
        # Значения по умолчанию
        self.duration_var = tk.IntVar(value=stage["duration"] if stage else 60)
        self.users_var = tk.IntVar(value=stage["users"] if stage else 10)
        self.spawn_rate_var = tk.IntVar(value=stage["spawn_rate"] if stage else 1)
        
        self.create_ui(stage)
    
    def create_ui(self, stage):
        """Создание интерфейса диалога"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Duration
        ttk.Label(main_frame, text="Длительность (секунды):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        duration_frame = ttk.Frame(main_frame)
        duration_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Entry(duration_frame, textvariable=self.duration_var, width=10).pack(side=tk.LEFT)
        ttk.Label(duration_frame, text="секунд", foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # Users
        ttk.Label(main_frame, text="Количество пользователей:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        users_frame = ttk.Frame(main_frame)
        users_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Entry(users_frame, textvariable=self.users_var, width=10).pack(side=tk.LEFT)
        ttk.Label(users_frame, text="пользователей", foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # Spawn rate
        ttk.Label(main_frame, text="Скорость запуска (spawn rate):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        spawn_frame = ttk.Frame(main_frame)
        spawn_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Entry(spawn_frame, textvariable=self.spawn_rate_var, width=10).pack(side=tk.LEFT)
        ttk.Label(spawn_frame, text="пользователей/сек", foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # User classes
        ttk.Label(main_frame, text="User Classes:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Фрейм с чекбоксами
        classes_frame = ttk.Frame(main_frame)
        classes_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Создание чекбоксов для каждого user class
        self.class_vars = {}
        for user_class in self.available_user_classes:
            var = tk.BooleanVar()
            if stage and user_class in stage["user_classes"]:
                var.set(True)
            
            cb = ttk.Checkbutton(classes_frame, text=user_class, variable=var)
            cb.pack(anchor=tk.W, pady=2)
            
            self.class_vars[user_class] = var
        
        # Кнопки
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="✅ Сохранить", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="❌ Отмена", command=self.cancel).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        """Сохранение результата"""
        # Проверка выбранных user classes
        selected_classes = [uc for uc, var in self.class_vars.items() if var.get()]
        
        if not selected_classes:
            messagebox.showwarning("Предупреждение", "Выберите хотя бы один User Class")
            return
        
        try:
            duration = self.duration_var.get()
            users = self.users_var.get()
            spawn_rate = self.spawn_rate_var.get()
            
            if duration <= 0 or users <= 0 or spawn_rate <= 0:
                raise ValueError("Все значения должны быть положительными")
            
            self.result = {
                "duration": duration,
                "users": users,
                "spawn_rate": spawn_rate,
                "user_classes": selected_classes
            }
            
            self.dialog.destroy()
        
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные:\n{e}")
    
    def cancel(self):
        """Отмена"""
        self.dialog.destroy()


def main():
    root = tk.Tk()
    app = LoadShapeEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
