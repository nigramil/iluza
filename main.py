import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'trainings.json'

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        
        self.trainings = []

        # Создаем интерфейс
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля для ввода
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10, fill='x')

        tk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky='w')
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, sticky='w')
        self.type_entry = tk.Entry(input_frame)
        self.type_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, sticky='w')
        self.duration_entry = tk.Entry(input_frame)
        self.duration_entry.grid(row=0, column=5, padx=5)

        add_button = tk.Button(input_frame, text="Добавить тренировку", command=self.add_training)
        add_button.grid(row=0, column=6, padx=10)

        # Фильтры
    filter_frame = tk.Frame(self.root)
        filter_frame.pack(padx=10, pady=10, fill='x')

        tk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, sticky='w')
        self.type_filter = ttk.Combobox(filter_frame, values=["Все"])
        self.type_filter.current(0)
        self.type_filter.bind("<<ComboboxSelected>>", self.apply_filters)
        self.type_filter.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Фильтр по дате (YYYY-MM-DD):").grid(row=0, column=2, sticky='w')
        self.date_filter = tk.Entry(filter_frame)
        self.date_filter.bind("<KeyRelease>", lambda e: self.apply_filters())
        self.date_filter.grid(row=0, column=3, padx=5)

        reset_button = tk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters)
        reset_button.grid(row=0, column=4, padx=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Тип", "Длительность"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип тренировки")
        self.tree.heading("Длительность", text="Длительность (мин)")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Меню для сохранения/загрузки
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Сохранить", command=self.save_data)
        filemenu.add_command(label="Загрузить", command=self.load_data)
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.root.config(menu=menubar)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def add_training(self):
        date = self.date_entry.get().strip()
        t_type = self.type_entry.get().strip()
        duration = self.duration_entry.get().strip()

        # Валидация
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте YYYY-MM-DD.")
            return
        if not t_type:
            messagebox.showerror("Ошибка", "Введите тип тренировки.")
            return
        try:
            duration_int = int(duration)
            if duration_int <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        # Добавление записи
        training = {"date": date, "type": t_type, "duration": duration_int}
        self.trainings.append(training)
        self.update_tree()
        self.clear_entries()

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def update_tree(self, filtered_list=None):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Вывод данных
        data_to_show = filtered_list if filtered_list is not None else self.trainings
        for t in data_to_show:
            self.tree.insert('', tk.END, values=(t["date"], t["type"], t["duration"]))

        # Обновление фильтров типа
        types = set(t["type"] for t in self.trainings)
        types_list = ["Все"] + sorted(types)
        self.type_filter['values'] = types_list
        self.type_filter.current(0)

    def apply_filters(self, event=None):
        filtered = self.trainings
        selected_type = self.type_filter.get()
        date_filter_value = self.date_filter.get().strip()

        if selected_type != "Все":
            filtered = [t for t in filtered if t["type"] == selected_type]
        if date_filter_value:
            try:
                datetime.strptime(date_filter_value, '%Y-%m-%d')
                filtered = [t for t in filtered if t["date"] == date_filter_value]
            except ValueError:
                # Некорректный формат фильтра — игнорируем
                pass

        self.update_tree(filtered)

    def reset_filters(self):
        self.type_filter.current(0)
        self.date_filter.delete(0, tk.END)
        self.update_tree()

    def save_data(self):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.trainings = json.load(f)
                self.update_tree()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
