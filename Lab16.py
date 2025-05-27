import json
from datetime import datetime


# --- Завдання 1: Основні компоненти бібліотеки ---
class Author:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Author(name='{self.name}')"


class Book:
    def __init__(self, title: str, author: Author, pages: int):
        self.title = title
        self.author = author
        self.pages = pages
        self.is_checked_out = False  # Статус видачі книги

    def __repr__(self):
        return f"Book(title='{self.title}', author={self.author.name}, pages={self.pages})"


class Library:
    def __init__(self):
        # Список книг у бібліотеці
        self.books = []
        # Словник книг, які видані: book -> (користувач, дата видачі)
        self.checked_out_books = {}
        # Історія видач: кортежі (book, user, checkout_date, return_date)
        self.history = []
        # Час читання: book -> список днів читання
        self.read_times = {}

    # --- Завдання 1: Методи для додавання, видалення, пошуку книг ---

    def add_book(self, book: Book):
        if book not in self.books:
            self.books.append(book)
            print(f"Додано книгу: {book.title}")

    def remove_book(self, book: Book):
        if book in self.books:
            self.books.remove(book)
            # Видаляємо з виданих, якщо там була
            self.checked_out_books.pop(book, None)
            print(f"Видалено книгу: {book.title}")
        else:
            print(f"Книга '{book.title}' не знайдена в бібліотеці.")

    def find_books_by_title(self, title: str):
        found = [book for book in self.books if title.lower() in book.title.lower()]
        print(f"Знайдено {len(found)} книгу(и) за назвою '{title}': {[b.title for b in found]}")
        return found

    def find_books_by_author(self, author_name: str):
        found = [book for book in self.books if author_name.lower() in book.author.name.lower()]
        print(f"Знайдено {len(found)} книгу(и) за автором '{author_name}': {[b.title for b in found]}")
        return found

    # --- Завдання 2: Ведення історії видачі книг, повернення з перевіркою термінів ---

    def checkout_book(self, book: Book, user: str, checkout_date: datetime = None):
        if book not in self.books:
            print("Книга відсутня в бібліотеці.")
            return
        if book.is_checked_out:
            print(f"Книга '{book.title}' вже взята.")
            return
        if checkout_date is None:
            checkout_date = datetime.now()
        book.is_checked_out = True
        self.checked_out_books[book] = (user, checkout_date)
        print(f"Книга '{book.title}' видана користувачу '{user}' дата: {checkout_date.date()}")

    def return_book(self, book: Book, return_date: datetime = None):
        if book not in self.books:
            print("Книга відсутня в бібліотеці.")
            return
        if not book.is_checked_out:
            print(f"Книга '{book.title}' не була видана.")
            return
        if return_date is None:
            return_date = datetime.now()
        user, checkout_date = self.checked_out_books.pop(book)
        book.is_checked_out = False
        self.history.append((book, user, checkout_date, return_date))

        duration = (return_date - checkout_date).days
        if book not in self.read_times:
            self.read_times[book] = []
        self.read_times[book].append(duration)

        allowed_days = 14  # Припустимий термін читання
        if duration > allowed_days:
            print(f"Книга '{book.title}' повернена з запізненням на {duration - allowed_days} днів.")
        else:
            print(f"Книга '{book.title}' повернена вчасно, прочитано за {duration} днів.")

    # --- Завдання 3: Статистика бібліотеки, експортування в JSON ---

    def popularity(self):
        # Підрахунок скільки разів кожна книга була видана
        popularity_count = {}
        for record in self.history:
            book = record[0]
            popularity_count[book] = popularity_count.get(book, 0) + 1
        print("Популярність книг (кількість видач):")
        for book, count in popularity_count.items():
            print(f"  {book.title}: {count}")
        return popularity_count

    def return_rate(self):
        # Відсоток повернення книг
        total_checked_out = len(self.history) + len(self.checked_out_books)
        if total_checked_out == 0:
            rate = 0.0
        else:
            returned = len(self.history)
            rate = (returned / total_checked_out) * 100
        print(f"Відсоток повернутих книг: {rate:.2f}%")
        return rate

    def average_reading_time(self):
        # Середній час читання книг у днях
        avg_times = {}
        for book, times in self.read_times.items():
            avg_times[book] = sum(times) / len(times)
        print("Середній час читання книг (у днях):")
        for book, avg in avg_times.items():
            print(f"  {book.title}: {avg:.2f}")
        return avg_times

    def export_statistics_json(self, filename: str):
        stats = {
            "popularity": {book.title: count for book, count in self.popularity().items()},
            "return_rate_percent": self.return_rate(),
            "average_reading_time_days": {book.title: avg for book, avg in self.average_reading_time().items()}
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=4)
        print(f"Статистика експортувалась у файл '{filename}'.")


# --- Демонстрація (ручне тестування користувачем) ---

if __name__ == "__main__":
    print("--- Створення авторів і книг (завдання 1) ---")
    author1 = Author("Леся Українка")
    author2 = Author("Іван Франко")

    book1 = Book("Лісова пісня", author1, 150)
    book2 = Book("Каменярі", author2, 200)
    book3 = Book("Contra spem spero", author1, 100)

    library = Library()

    print("\n--- Додавання книг (завдання 1) ---")
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    print("\n--- Пошук книг за назвою та автором (завдання 1) ---")
    library.find_books_by_title("лісова")
    library.find_books_by_author("Франко")

    print("\n--- Видача книг (завдання 2) ---")
    library.checkout_book(book1, "Олександр", datetime(2025, 5, 10))
    library.checkout_book(book2, "Марія")

    print("\n--- Повернення книг (завдання 2) ---")
    library.return_book(book1, datetime(2025, 5, 20))  # вчасно
    library.return_book(book2, datetime(2025, 6, 5))   # із запізненням

    print("\n--- Статистика бібліотеки (завдання 3) ---")
    library.popularity()
    library.return_rate()
    library.average_reading_time()

    print("\n--- Експорт статистики у JSON (завдання 3) ---")
    library.export_statistics_json("library_stats.json")
