"""
Калькулятор питания - приложение для расчёта дневной нормы калорий и БЖУ
"""

import tkinter as tk
from tkinter import ttk, messagebox


class NutritionCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор питания")
        self.root.geometry("950x750")
        self.root.minsize(800, 650)
        self.root.resizable(True, True)
        
        # Палитра цветов (современная)
        self.bg_color = "#FAFBFC"
        self.card_bg = "#FFFFFF"
        self.accent_color = "#4A90D9"
        self.accent_dark = "#357ABD"
        self.success_color = "#34C759"
        self.text_dark = "#1C1C1E"
        self.text_gray = "#8E8E93"
        self.border_color = "#E5E5EA"
        
        # Настройка стиля
        self.setup_styles()
        
        # Основной контейнер с прокруткой
        self.canvas = tk.Canvas(root, bg=self.bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Привязка колеса мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Заголовок
        self.create_header()
        
        # Создание вкладок
        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Вкладка ввода данных
        self.input_frame = tk.Frame(self.notebook, bg=self.card_bg)
        self.notebook.add(self.input_frame, text="  📋 Данные  ")
        
        # Вкладка результатов
        self.result_frame = tk.Frame(self.notebook, bg=self.card_bg)
        self.notebook.add(self.result_frame, text="  📊 Результаты  ")
        
        # Вкладка рекомендаций
        self.recommend_frame = tk.Frame(self.notebook, bg=self.card_bg)
        self.notebook.add(self.recommend_frame, text="  🍎 Рекомендации  ")
        
        # Создание виджетов
        self.create_input_widgets()
        self.create_result_widgets()
        self.create_recommend_widgets()
        
        # Переменные для хранения результатов
        self.results = {}
        
        # Обновление canvas
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_mousewheel(self, event):
        """Обработка прокрутки колесом мыши"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def setup_styles(self):
        """Настройка стилей интерфейса"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background='#F0F0F5', foreground=self.text_gray, 
                       font=('Segoe UI', 11, 'bold'), padding=(18, 8))
        style.map('TNotebook.Tab', background=[('selected', self.card_bg)], 
                 foreground=[('selected', self.accent_color)])
        
        style.configure('TButton', font=('Segoe UI', 11), padding=(15, 8))
        
        style.configure('TLabel', font=('Segoe UI', 11), background=self.card_bg, 
                       foreground=self.text_dark)
    
    def create_rounded_frame(self, parent, bg_color, radius=15):
        """Создание рамки с закругленными углами (визуальная имитация)"""
        frame = tk.Frame(parent, bg=bg_color, bd=0, highlightthickness=0)
        return frame
        
    def create_header(self):
        """Создание заголовка"""
        # Градиентная полоса сверху
        header_frame = tk.Frame(self.scrollable_frame, bg=self.accent_color, height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Контейнер для центрирования
        title_container = tk.Frame(header_frame, bg=self.accent_color)
        title_container.pack(expand=True)
        
        # Заголовок с иконкой
        title_label = tk.Label(
            title_container,
            text="🥗  Калькулятор питания",
            font=('Segoe UI', 26, 'bold'),
            bg=self.accent_color,
            fg="#FFFFFF"
        )
        title_label.pack()
        
        subtitle = tk.Label(
            title_container,
            text="Рассчитайте свою дневную норму калорий и БЖУ",
            font=('Segoe UI', 13),
            bg=self.accent_color,
            fg="#C8E6FF"
        )
        subtitle.pack(pady=(5, 0))
    
    def create_input_widgets(self):
        """Создание виджетов ввода данных"""
        content_frame = tk.Frame(self.input_frame, bg=self.card_bg)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        # Заголовок секции
        section_label = tk.Label(
            content_frame,
            text="📋  Введите ваши данные",
            font=('Segoe UI', 18, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark
        )
        section_label.pack(pady=(10, 20), anchor='w')
        
        # Карточка с полями ввода
        card = tk.Frame(content_frame, bg=self.card_bg, relief=tk.FLAT, 
                       highlightthickness=1, highlightcolor=self.border_color)
        card.pack(fill=tk.X, pady=5)
        
        inner_card = tk.Frame(card, bg="#FAFAFA", relief=tk.FLAT)
        inner_card.pack(fill=tk.X, pady=20)
        
        # Форма
        form_frame = tk.Frame(inner_card, bg="#FAFAFA")
        form_frame.pack(fill=tk.X)
        
        self.vars = {}
        
        # Поля ввода
        fields = [
            ("Возраст (лет):", "age", "25"),
            ("Рост (см):", "height", "170"),
            ("Вес (кг):", "weight", "70"),
        ]
        
        for i, (label, var_name, default) in enumerate(fields):
            lbl = tk.Label(
                form_frame,
                text=label,
                font=('Segoe UI', 12),
                bg="#FAFAFA",
                fg=self.text_dark,
                width=18,
                anchor='e'
            )
            lbl.grid(row=i, column=0, padx=(0, 15), pady=12, sticky='e')
            
            var = tk.StringVar(value=default)
            entry = tk.Entry(
                form_frame,
                font=('Segoe UI', 12),
                width=20,
                bg="#FFFFFF",
                fg=self.text_dark,
                relief=tk.FLAT,
                highlightthickness=2,
                highlightcolor=self.accent_color,
                highlightbackground=self.border_color,
                textvariable=var,
                bd=0
            )
            entry.grid(row=i, column=1, padx=(0, 0), pady=12, sticky='w')
            
            # Рамка вокруг поля
            entry_frame = tk.Frame(form_frame, bg=self.border_color, height=35)
            entry_frame.grid(row=i, column=1, padx=0, pady=12, sticky='w')
            entry_frame.grid_propagate(False)
            entry_frame.config(width=190)
            entry.lift()
            
            self.vars[var_name] = var
        
        # Пол
        gender_section = tk.LabelFrame(
            content_frame, 
            text="🚻  Пол",
            font=('Segoe UI', 12, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark,
            padx=15,
            pady=12,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=self.border_color
        )
        gender_section.pack(fill=tk.X, pady=15)
        
        self.gender_var = tk.StringVar(value="male")
        
        for value, text in [("male", "👨 Мужской"), ("female", "👩 Женский")]:
            rb = tk.Radiobutton(
                gender_section,
                text=text,
                variable=self.gender_var,
                value=value,
                font=('Segoe UI', 11),
                bg=self.card_bg,
                fg=self.text_dark,
                activebackground=self.card_bg,
                selectcolor="#D4E6F7",
                padx=20,
                cursor='hand2'
            )
            rb.pack(side=tk.LEFT, padx=25)
        
        # Уровень активности
        activity_section = tk.LabelFrame(
            content_frame,
            text="🏃  Уровень активности",
            font=('Segoe UI', 12, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark,
            padx=15,
            pady=12,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=self.border_color
        )
        activity_section.pack(fill=tk.X, pady=12)
        
        self.activity_var = tk.StringVar(value="1.375")
        
        activities = [
            ("1.2", "Минимальный (сидячий)"),
            ("1.375", "Легкий (1-3 тренировки)"),
            ("1.55", "Умеренный (3-5 тренировок)"),
            ("1.725", "Высокий (6-7 тренировок)"),
            ("1.9", "Очень высокий")
        ]
        
        for value, text in activities:
            rb = tk.Radiobutton(
                activity_section,
                text=text,
                variable=self.activity_var,
                value=value,
                font=('Segoe UI', 10),
                bg=self.card_bg,
                fg=self.text_dark,
                activebackground=self.card_bg,
                selectcolor="#D4E6F7",
                cursor='hand2'
            )
            rb.pack(anchor='w', padx=25, pady=3)
        
        # Цель
        goal_section = tk.LabelFrame(
            content_frame,
            text="🎯  Ваша цель",
            font=('Segoe UI', 12, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark,
            padx=15,
            pady=12,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=self.border_color
        )
        goal_section.pack(fill=tk.X, pady=12)
        
        self.goal_var = tk.StringVar(value="maintain")
        
        goals = [
            ("lose", "🔽 Похудение"),
            ("maintain", "➡️ Поддержание"),
            ("gain", "🔼 Набор массы")
        ]
        
        for value, text in goals:
            rb = tk.Radiobutton(
                goal_section,
                text=text,
                variable=self.goal_var,
                value=value,
                font=('Segoe UI', 11),
                bg=self.card_bg,
                fg=self.text_dark,
                activebackground=self.card_bg,
                selectcolor="#D4E6F7",
                padx=20,
                cursor='hand2'
            )
            rb.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Кнопки
        button_frame = tk.Frame(content_frame, bg=self.card_bg)
        button_frame.pack(pady=20)
        
        # Кнопка РАССЧИТАТЬ
        calc_button = tk.Button(
            button_frame,
            text="📊  РАССЧИТАТЬ",
            font=('Segoe UI', 14, 'bold'),
            bg=self.success_color,
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor='hand2',
            command=self.calculate,
            padx=45,
            pady=14,
            borderwidth=0,
            width=16
        )
        calc_button.pack(side=tk.LEFT, padx=10)
        
        # Кнопка СБРОС
        reset_button = tk.Button(
            button_frame,
            text="🔄  СБРОС",
            font=('Segoe UI', 12, 'bold'),
            bg="#AEAEB2",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor='hand2',
            command=self.reset_form,
            padx=30,
            pady=14,
            borderwidth=0,
            width=12
        )
        reset_button.pack(side=tk.LEFT, padx=10)
        
        # Эффекты при наведении
        calc_button.bind("<Enter>", lambda e: calc_button.config(bg="#2DBF4E"))
        calc_button.bind("<Leave>", lambda e: calc_button.config(bg=self.success_color))
        reset_button.bind("<Enter>", lambda e: reset_button.config(bg="#8E8E93"))
        reset_button.bind("<Leave>", lambda e: reset_button.config(bg="#AEAEB2"))
    
    def create_result_widgets(self):
        """Создание виджетов для результатов"""
        content_frame = tk.Frame(self.result_frame, bg=self.card_bg)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        title_label = tk.Label(
            content_frame,
            text="📊  Ваши результаты",
            font=('Segoe UI', 18, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark
        )
        title_label.pack(pady=(10, 20), anchor='w')
        
        self.results_container = tk.Frame(content_frame, bg=self.card_bg)
        self.results_container.pack(fill=tk.BOTH, expand=True)
        
        self.instruction_label = tk.Label(
            self.results_container,
            text="📋  Заполните данные на первой вкладке\nи нажмите 'РАССЧИТАТЬ'",
            font=('Segoe UI', 14),
            bg=self.card_bg,
            fg=self.text_gray,
            justify=tk.CENTER
        )
        self.instruction_label.pack(pady=80)
    
    def create_recommend_widgets(self):
        """Создание виджетов для рекомендаций"""
        content_frame = tk.Frame(self.recommend_frame, bg=self.card_bg)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        title_label = tk.Label(
            content_frame,
            text="🍎  Рекомендации по питанию",
            font=('Segoe UI', 18, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark
        )
        title_label.pack(pady=(10, 20), anchor='w')
        
        self.recommend_container = tk.Frame(content_frame, bg=self.card_bg)
        self.recommend_container.pack(fill=tk.BOTH, expand=True)
        
        self.recommend_instruction = tk.Label(
            self.recommend_container,
            text="📋  Результаты появятся здесь\nпосле расчёта",
            font=('Segoe UI', 14),
            bg=self.card_bg,
            fg=self.text_gray,
            justify=tk.CENTER
        )
        self.recommend_instruction.pack(pady=80)
    
    def reset_form(self):
        """Сброс формы"""
        self.vars["age"].set("25")
        self.vars["height"].set("170")
        self.vars["weight"].set("70")
        self.gender_var.set("male")
        self.activity_var.set("1.375")
        self.goal_var.set("maintain")
        
        # Очистка результатов
        for widget in self.results_container.winfo_children():
            widget.destroy()
        self.results_container.pack(fill=tk.BOTH, expand=True)
        self.instruction_label = tk.Label(
            self.results_container,
            text="📋  Заполните данные на первой вкладке\nи нажмите 'РАССЧИТАТЬ'",
            font=('Segoe UI', 14),
            bg=self.card_bg,
            fg=self.text_gray,
            justify=tk.CENTER
        )
        self.instruction_label.pack(pady=80)
        
        # Очистка рекомендаций
        for widget in self.recommend_container.winfo_children():
            widget.destroy()
        self.recommend_container.pack(fill=tk.BOTH, expand=True)
        self.recommend_instruction = tk.Label(
            self.recommend_container,
            text="📋  Результаты появятся здесь\nпосле расчёта",
            font=('Segoe UI', 14),
            bg=self.card_bg,
            fg=self.text_gray,
            justify=tk.CENTER
        )
        self.recommend_instruction.pack(pady=80)
        
        self.results = {}
        self.notebook.select(0)
    
    def calculate(self):
        """Выполнение расчётов"""
        try:
            age = float(self.vars["age"].get())
            height = float(self.vars["height"].get())
            weight = float(self.vars["weight"].get())
            gender = self.gender_var.get()
            activity = float(self.activity_var.get())
            goal = self.goal_var.get()
            
            # Валидация
            if age < 5 or age > 120:
                messagebox.showerror("Ошибка", "Возраст должен быть от 5 до 120 лет")
                return
            if height < 50 or height > 250:
                messagebox.showerror("Ошибка", "Рост должен быть от 50 до 250 см")
                return
            if weight < 20 or weight > 300:
                messagebox.showerror("Ошибка", "Вес должен быть от 20 до 300 кг")
                return
            
            # Расчёт базового метаболизма (Миффлин-Сан-Жеор)
            if gender == "male":
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
            if bmr < 500:
                messagebox.showerror("Ошибка", "Некорректные данные. Проверьте ввод.")
                return
            
            # Дневная норма калорий
            daily_calories = bmr * activity
            
            # Корректировка по цели
            if goal == "lose":
                daily_calories -= 500
            elif goal == "gain":
                daily_calories += 500
            
            # Минимальная норма калорий
            min_calories = 1500 if gender == "male" else 1200
            if daily_calories < min_calories:
                daily_calories = min_calories
                messagebox.showwarning(
                    "Внимание", 
                    f"Установлена минимальная норма: {min_calories} ккал"
                )
            
            # Расчёт БЖУ
            proteins = (daily_calories * 0.30) / 4
            fats = (daily_calories * 0.25) / 9
            carbs = (daily_calories * 0.45) / 4
            
            self.results = {
                'bmr': round(bmr),
                'calories': round(daily_calories),
                'proteins': round(proteins),
                'fats': round(fats),
                'carbs': round(carbs),
                'goal': goal,
                'weight': weight,
                'activity': activity,
                'gender': gender
            }
            
            self.display_results()
            self.display_recommendations()
            self.notebook.select(1)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
    
    def display_results(self):
        """Отображение результатов"""
        for widget in self.results_container.winfo_children():
            widget.destroy()
        
        # Заголовок
        result_title = tk.Label(
            self.results_container,
            text="✨  Ваши результаты",
            font=('Segoe UI', 20, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark
        )
        result_title.pack(pady=(10, 20))
        
        # Главная карточка калорий
        main_card = tk.Frame(self.results_container, bg=self.accent_color, relief=tk.FLAT)
        main_card.pack(pady=10, fill=tk.X, padx=40)
        
        tk.Label(
            main_card,
            text="🔥 Дневная норма калорий",
            font=('Segoe UI', 14),
            bg=self.accent_color,
            fg="#D4E8FF"
        ).pack(pady=(20, 5))
        
        tk.Label(
            main_card,
            text=f"{self.results['calories']}",
            font=('Segoe UI', 52, 'bold'),
            bg=self.accent_color,
            fg="#FFFFFF"
        ).pack()
        
        tk.Label(
            main_card,
            text="ккал",
            font=('Segoe UI', 16),
            bg=self.accent_color,
            fg="#B8DCFF"
        ).pack(pady=(0, 20))
        
        # Базовый метаболизм
        bmr_card = self.create_result_card(
            self.results_container,
            "⚡ Базовый метаболизм",
            f"{self.results['bmr']}",
            "ккал",
            "#FF9500"
        )
        bmr_card.pack(pady=10, fill=tk.X, padx=40)
        
        # БЖУ
        macros_title = tk.Label(
            self.results_container,
            text="🥗  Белки, Жиры, Углеводы",
            font=('Segoe UI', 15, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark
        )
        macros_title.pack(pady=(20, 10))
        
        macros_frame = tk.Frame(self.results_container, bg=self.card_bg)
        macros_frame.pack(pady=10, fill=tk.X, padx=40)
        
        # Белки
        protein_card = self.create_macro_card(
            macros_frame,
            "🥩 Белки",
            f"{self.results['proteins']}",
            "г",
            "#007AFF",
            "30%"
        )
        protein_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        # Жиры
        fat_card = self.create_macro_card(
            macros_frame,
            "🥑 Жиры",
            f"{self.results['fats']}",
            "г",
            "#34C759",
            "25%"
        )
        fat_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        # Углеводы
        carb_card = self.create_macro_card(
            macros_frame,
            "🍞 Углеводы",
            f"{self.results['carbs']}",
            "г",
            "#AF52DE",
            "45%"
        )
        carb_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        # Цель
        goal_text = {'lose': '🔽 Похудение', 'maintain': '➡️ Поддержание веса', 'gain': '🔼 Набор массы'}
        goal_colors = {'lose': '#FF3B30', 'maintain': '#007AFF', 'gain': '#34C759'}
        
        goal_card = tk.Frame(self.results_container, bg="#F2F2F7", relief=tk.FLAT)
        goal_card.pack(pady=15, fill=tk.X, padx=40)
        
        tk.Label(
            goal_card,
            text=f"🎯  Цель: {goal_text[self.results['goal']]}",
            font=('Segoe UI', 13, 'bold'),
            bg="#F2F2F7",
            fg=goal_colors[self.results['goal']]
        ).pack(pady=15)
        
        # Вода
        water_card = tk.Frame(self.results_container, bg="#E8F8F5", relief=tk.FLAT)
        water_card.pack(pady=10, fill=tk.X, padx=40)
        
        water_intake = int(self.results['weight'] * 35)
        tk.Label(
            water_card,
            text=f"💧  Рекомендуемая вода: {water_intake} мл в день",
            font=('Segoe UI', 12),
            bg="#E8F8F5",
            fg="#00A08A"
        ).pack(pady=15)
    
    def create_result_card(self, parent, title, value, unit, color):
        """Создание карточки результата"""
        card = tk.Frame(parent, bg="#F8F8F8", relief=tk.FLAT, 
                       highlightthickness=1, highlightbackground=self.border_color)
        
        tk.Label(card, text=title, font=('Segoe UI', 12), 
                bg="#F8F8F8", fg=self.text_gray).pack(pady=(15, 5))
        
        value_frame = tk.Frame(card, bg="#F8F8F8")
        value_frame.pack(pady=5)
        
        tk.Label(value_frame, text=value, font=('Segoe UI', 32, 'bold'), 
                bg="#F8F8F8", fg=color).pack(side=tk.LEFT)
        
        tk.Label(value_frame, text=f" {unit}", font=('Segoe UI', 14), 
                bg="#F8F8F8", fg=self.text_gray).pack(side=tk.LEFT, pady=15)
        
        return card
    
    def create_macro_card(self, parent, title, value, unit, color, percentage):
        """Создание карточки макроса"""
        card = tk.Frame(parent, bg="#FAFAFA", relief=tk.FLAT, 
                       highlightthickness=1, highlightbackground=self.border_color)
        
        tk.Label(card, text=title, font=('Segoe UI', 11), 
                bg="#FAFAFA", fg=self.text_gray).pack(pady=(12, 5))
        
        tk.Label(card, text=value, font=('Segoe UI', 24, 'bold'), 
                bg="#FAFAFA", fg=color).pack()
        
        tk.Label(card, text=unit, font=('Segoe UI', 11), 
                bg="#FAFAFA", fg=self.text_gray).pack()
        
        tk.Label(card, text=f"({percentage})", font=('Segoe UI', 10, 'bold'), 
                bg="#FAFAFA", fg=color).pack(pady=(0, 10))
        
        return card
    
    def display_recommendations(self):
        """Отображение рекомендаций"""
        for widget in self.recommend_container.winfo_children():
            widget.destroy()
        
        calories = self.results['calories']
        
        # Распределение калорий
        breakfast = int(calories * 0.25)
        lunch = int(calories * 0.35)
        dinner = int(calories * 0.25)
        snacks = int(calories * 0.15)
        
        # Заголовок
        tk.Label(
            self.recommend_container,
            text="📅  Распределение калорий по приёмам пищи",
            font=('Segoe UI', 15, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark
        ).pack(pady=(10, 15))
        
        meals = [
            ("🌅 Завтрак", breakfast, "#FF9500"),
            ("🌞 Обед", lunch, "#FF3B30"),
            ("🌙 Ужин", dinner, "#AF52DE"),
            ("🍿 Перекусы", snacks, "#34C759")
        ]
        
        meals_frame = tk.Frame(self.recommend_container, bg=self.card_bg)
        meals_frame.pack(pady=10, fill=tk.X, padx=30)
        
        for meal, cals, color in meals:
            card = tk.Frame(meals_frame, bg="#FAFAFA", relief=tk.FLAT, 
                          highlightthickness=1, highlightbackground=self.border_color)
            card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
            
            tk.Label(card, text=meal, font=('Segoe UI', 11), 
                    bg="#FAFAFA", fg=self.text_gray).pack(pady=(12, 5))
            tk.Label(card, text=str(cals), font=('Segoe UI', 20, 'bold'), 
                    bg="#FAFAFA", fg=color).pack()
            tk.Label(card, text="ккал", font=('Segoe UI', 10), 
                    bg="#FAFAFA", fg=self.text_gray).pack(pady=(0, 10))
        
        # Продукты
        tk.Label(
            self.recommend_container,
            text="🥗  Рекомендуемые продукты",
            font=('Segoe UI', 15, 'bold'),
            bg=self.card_bg,
            fg=self.text_dark
        ).pack(pady=(20, 12))
        
        foods = [
            ("🥩 Белки:", "Курица, рыба, яйца, творог, говядина, бобовые"),
            ("🥑 Жиры:", "Оливковое масло, орехи, авокадо, жирная рыба"),
            ("🍞 Углеводы:", "Овсянка, гречка, рис, цельнозерновой хлеб"),
            ("🥦 Овощи:", "Брокколи, шпинат, морковь, помидоры, перец")
        ]
        
        for title, products in foods:
            frame = tk.Frame(self.recommend_container, bg=self.card_bg)
            frame.pack(fill=tk.X, padx=35, pady=3)
            
            tk.Label(frame, text=title, font=('Segoe UI', 10, 'bold'), 
                    bg=self.card_bg, fg=self.accent_color, width=12, anchor='w').pack(side=tk.LEFT)
            tk.Label(frame, text=products, font=('Segoe UI', 10), 
                    bg=self.card_bg, fg=self.text_dark).pack(side=tk.LEFT)
        
        # Ограничения
        limit_card = tk.Frame(self.recommend_container, bg="#FFF9E6", relief=tk.FLAT)
        limit_card.pack(pady=20, fill=tk.X, padx=35)
        
        tk.Label(limit_card, text="⚠️  Ограничения", font=('Segoe UI', 12, 'bold'), 
                bg="#FFF9E6", fg="#FF9500").pack(anchor='w', padx=15, pady=(12, 5))
        
        tk.Label(limit_card, 
                text="• Ограничьте сахар и быстрые углеводы\n"
                     "• Избегайте фастфуда и полуфабрикатов\n"
                     "• Сократите соль и алкоголь",
                font=('Segoe UI', 10), bg="#FFF9E6", fg="#8E8E93", 
                justify=tk.LEFT, anchor='w').pack(padx=15, pady=(0, 15), fill=tk.X)
        
        # Советы
        tips_card = tk.Frame(self.recommend_container, bg="#E8F8F5", relief=tk.FLAT)
        tips_card.pack(pady=15, fill=tk.X, padx=35)
        
        tk.Label(tips_card, text="💡  Полезные советы", font=('Segoe UI', 12, 'bold'), 
                bg="#E8F8F5", fg="#00A08A").pack(anchor='w', padx=15, pady=(12, 5))
        
        tk.Label(tips_card,
                text="• Пейте воду перед каждым приёмом пищи\n"
                     "• Ешьте 4-5 раз в день небольшими порциями\n"
                     "• Последний приём пищи за 3-4 часа до сна",
                font=('Segoe UI', 10), bg="#E8F8F5", fg="#8E8E93", 
                justify=tk.LEFT, anchor='w').pack(padx=15, pady=(0, 15), fill=tk.X)


def main():
    """Запуск приложения"""
    root = tk.Tk()
    
    # Центрирование
    window_width = 950
    window_height = 750
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = NutritionCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

