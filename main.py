import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "books.json"


class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker — Трекер прочитанных книг")
        self.root.geometry("900x580")
        self.root.resizable(False, False)

        self.books = []
        self.load_books()

        self.create_widgets()
        self.update_table()
        self.update_stats()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Book Tracker — Трекер прочитанных книг",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        form_frame = tk.LabelFrame(self.root, text="Добавление книги", padx=10, pady=10)
        form_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(form_frame, text="Название книги:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = tk.Entry(form_frame, width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Автор:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.author_entry = tk.Entry(form_frame, width=25)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.genre_entry = tk.Entry(form_frame, width=25)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Количество страниц:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.pages_entry = tk.Entry(form_frame, width=25)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(
            form_frame,
            text="Добавить книгу",
            width=20,
            command=self.add_book
        ).grid(row=0, column=4, rowspan=2, padx=15)

        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(filter_frame, text="Жанр содержит:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=22)
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Страниц больше:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_pages_entry = tk.Entry(filter_frame, width=15)
        self.filter_pages_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(
            filter_frame,
            text="Применить фильтр",
            command=self.apply_filter
        ).grid(row=0, column=4, padx=5)

        tk.Button(
            filter_frame,
            text="Сбросить фильтр",
            command=self.reset_filter
        ).grid(row=0, column=5, padx=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(padx=15, pady=10, fill="both", expand=True)

        columns = ("title", "author", "genre", "pages")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=13)

        self.table.heading("title", text="Название")
        self.table.heading("author", text="Автор")
        self.table.heading("genre", text="Жанр")
        self.table.heading("pages", text="Страниц")

        self.table.column("title", width=260)
        self.table.column("author", width=210)
        self.table.column("genre", width=160)
        self.table.column("pages", width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=5)

        tk.Button(
            buttons_frame,
            text="Удалить выбранную книгу",
            width=22,
            command=self.delete_selected
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            buttons_frame,
            text="Сохранить в JSON",
            width=18,
            command=self.save_books
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            buttons_frame,
            text="Загрузить из JSON",
            width=18,
            command=self.load_books_button
        ).grid(row=0, column=2, padx=5)

        self.stats_label = tk.Label(self.root, text="", font=("Arial", 11, "bold"))
        self.stats_label.pack(pady=5)

    def validate_book(self, title, author, genre, pages):
        if not title:
            raise ValueError("Название книги не должно быть пустым.")
        if not author:
            raise ValueError("Автор не должен быть пустым.")
        if not genre:
            raise ValueError("Жанр не должен быть пустым.")
        if not pages:
            raise ValueError("Количество страниц не должно быть пустым.")

        try:
            pages_value = int(pages)
        except ValueError:
            raise ValueError("Количество страниц должно быть числом.")

        if pages_value <= 0:
            raise ValueError("Количество страниц должно быть положительным числом.")

        return pages_value

    def add_book(self):
        try:
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            genre = self.genre_entry.get().strip()
            pages_text = self.pages_entry.get().strip()

            pages = self.validate_book(title, author, genre, pages_text)

            book = {
                "title": title,
                "author": author,
                "genre": genre,
                "pages": pages
            }

            self.books.append(book)
            self.save_books(show_message=False)
            self.update_table()
            self.update_stats()
            self.clear_inputs()

            messagebox.showinfo("Успех", "Книга успешно добавлена.")

        except ValueError as error:
            messagebox.showerror("Ошибка ввода", str(error))

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def update_table(self, books_to_show=None):
        for item in self.table.get_children():
            self.table.delete(item)

        books = books_to_show if books_to_show is not None else self.books

        for book in books:
            self.table.insert(
                "",
                tk.END,
                values=(
                    book.get("title", ""),
                    book.get("author", ""),
                    book.get("genre", ""),
                    book.get("pages", "")
                )
            )

    def apply_filter(self):
        genre_filter = self.filter_genre_entry.get().strip().lower()
        pages_filter = self.filter_pages_entry.get().strip()

        try:
            pages_min = None
            if pages_filter:
                pages_min = int(pages_filter)
                if pages_min < 0:
                    raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Фильтр по страницам должен быть неотрицательным числом.")
            return

        filtered = []
        for book in self.books:
            genre_match = True
            pages_match = True

            if genre_filter:
                genre_match = genre_filter in book.get("genre", "").lower()

            if pages_min is not None:
                pages_match = int(book.get("pages", 0)) > pages_min

            if genre_match and pages_match:
                filtered.append(book)

        self.update_table(filtered)
        self.stats_label.config(
            text=f"Показано книг: {len(filtered)} из {len(self.books)}"
        )

    def reset_filter(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_pages_entry.delete(0, tk.END)
        self.update_table()
        self.update_stats()

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления.")
            return

        values = self.table.item(selected[0], "values")
        title, author, genre, pages = values

        for book in self.books:
            if (
                book.get("title") == title and
                book.get("author") == author and
                book.get("genre") == genre and
                str(book.get("pages")) == str(pages)
            ):
                self.books.remove(book)
                break

        self.save_books(show_message=False)
        self.update_table()
        self.update_stats()
        messagebox.showinfo("Удаление", "Книга удалена.")

    def save_books(self, show_message=True):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.books, file, ensure_ascii=False, indent=2)

        if show_message:
            messagebox.showinfo("Сохранение", "Данные сохранены в books.json.")

    def load_books(self):
        if not os.path.exists(DATA_FILE):
            self.books = []
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                self.books = json.load(file)
        except (json.JSONDecodeError, OSError):
            self.books = []

    def load_books_button(self):
        self.load_books()
        self.update_table()
        self.update_stats()
        messagebox.showinfo("Загрузка", "Данные загружены из books.json.")

    def update_stats(self):
        total_books = len(self.books)
        total_pages = sum(int(book.get("pages", 0)) for book in self.books)
        self.stats_label.config(
            text=f"Всего книг: {total_books} | Всего страниц: {total_pages}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
