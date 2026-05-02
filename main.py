import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

# Имя файла для хранения истории задач
HISTORY_FILE = 'task_history.json'

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        
        # Предопределённые задачи
        self.tasks = [
            {"task": "Прочитать статью", "type": "учёба"},
            {"task": "Сделать зарядку", "type": "спорт"},
            {"task": "Позвонить другу", "type": "личное"},
            {"task": "Поработать над проектом", "type": "работа"},
            {"task": "Послушать музыку", "type": "отдых"},
        ]
        self.history = []

        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Кнопка генерации
        self.btn_generate = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task)
        self.btn_generate.pack(padx=10, pady=10)

        # Отображение текущей задачи
        self.label_current = tk.Label(self.root, text="", font=("Arial", 14))
        self.label_current.pack(padx=10, pady=5)

        # Фильтр по типу задач
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(padx=10, pady=10, fill='x')
        tk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, sticky='w')
        self.type_filter = ttk.Combobox(filter_frame, values=["Все", "учёба", "спорт", "личное", "работа", "отдых"])
        self.type_filter.current(0)
        self.type_filter.bind("<<ComboboxSelected>>", self.apply_filter)
        self.type_filter.grid(row=0, column=1, padx=5)

        # История сгенерированных задач
        tk.Label(self.root, text="История задач:").pack(padx=10, pady=5)
        self.history_listbox = tk.Listbox(self.root, height=10, width=50)
        self.history_listbox.pack(padx=10, pady=5)

        # Меню для сохранения/загрузки
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Сохранить историю", command=self.save_history)
        filemenu.add_command(label="Загрузить историю", command=self.load_history)
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.root.config(menu=menubar)

    def generate_task(self):
        # Фильтр по типу
        selected_type = self.type_filter.get()
        filtered_tasks = [t for t in self.tasks if t["type"] == selected_type] if selected_type != "Все" else self.tasks
        if not filtered_tasks:
            messagebox.showinfo("Информация", "Нет задач для выбранного фильтра.")
            return
        task = random.choice(filtered_tasks)
        task_text = f"{task['task']} ({task['type']})"
        self.label_current.config(text=task_text)
        # Добавление в историю
        self.history.append(task)
        self.update_history()

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for t in self.history:
            self.history_listbox.insert(tk.END, f"{t['task']} ({t['type']})")

    def apply_filter(self, event=None):
        # Можно реализовать фильтрацию истории, если нужно
        # Но для генерации фильтр применяется к списку задач
        pass

    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Сохранение", "История успешно сохранена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                self.update_history()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
