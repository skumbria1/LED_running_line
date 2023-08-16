# Импорт библиотеки tkinter для создания графических приложений и
# библиотеки numpy для числовых операций
import tkinter as tk
import numpy as np

# Множитель размера ячейки сетки
S = 10


class GridApp:
    def __init__(self, root, rows: int, cols: int, led_scale_multiplier: int, font_path: str):
        # Корневое окно Tkinter
        self.root = root

        # Количество строк и столбцов для сетки
        self.rows = rows
        self.cols = cols

        # Загрузка символов и соответствующих им битмапов из указанного файла
        font = np.load(font_path)

        # Создание словаря с символами и соответствующими им битмапами
        self.char_to_bitmap = {char: bitmap for char, bitmap in
                               zip(font['chars'], font['array'])}

        # Инициализация сетки нулями (черный экран)
        self.grid_array = np.zeros((rows, cols), dtype=int)

        # Создание холста Tkinter для рисования
        self.canvas = tk.Canvas(self.root, width=self.cols * led_scale_multiplier, height=self.rows * led_scale_multiplier)
        self.canvas.pack()

        # Создание 2D-массива для хранения объектов-прямоугольников,
        # представляющих ячейки сетки
        self.rects = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Инициализация элементов интерфейса сетки
        self.create_grid(led_scale_multiplier)

        # Создание нижнего фрейма для ввода и кнопки отправки
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # Текст по умолчанию для виджета ввода
        self.default_text = 'Текст по умолчанию ()!@#$%^&*_+'
        self.entry = tk.Entry(self.bottom_frame, width=40)
        self.entry.insert(0, self.default_text)
        self.entry.pack(side=tk.LEFT, padx=10)

        # Создание кнопки вывода и её связывание с методом 'submit'
        self.button = tk.Button(self.bottom_frame, text='Выводить', command=self.submit)
        self.button.pack(side=tk.LEFT)

        # Планирование повторного вызова метода update_grid через 100 мс
        self.root.after(100, self.update_grid)

    def create_text_grid(self, text):
        # Преобразование входного текста в массив битмапов, используя данные
        # загруженного шрифта
        character_bitmaps = [self.char_to_bitmap[char] for char in text]
        text_bitmaps_array = np.concatenate(character_bitmaps, axis=1)

        # Создание начального черного массива и объединение с ним массива текста
        black_array = np.zeros((16, 152), dtype=int)
        final_array = np.concatenate((black_array, text_bitmaps_array), axis=1)

        return final_array

    def create_grid(self, led_scale_multiplier):
        # Создание прямоугольников для каждой ячейки в сетке
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * led_scale_multiplier
                y1 = row * led_scale_multiplier
                x2 = x1 + led_scale_multiplier
                y2 = y1 + led_scale_multiplier

                # Установка начального цвета в зависимости от значения в grid_array
                color = 'green' if self.grid_array[row, col] else 'black'
                self.rects[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                                    fill=color)

    def update_grid(self):
        # Обновление цветов прямоугольников на основе значений в grid_array
        for row in range(self.rows):
            for col in range(self.cols):
                color = 'green' if self.grid_array[row, col] else 'black'
                self.canvas.itemconfig(self.rects[row][col], fill=color)

        # Прокрутка grid_array для имитации анимационного эффекта
        self.grid_array = np.roll(self.grid_array, -1, axis=1)

    # Планирование повторного вызова метода update_grid через задержку 100 мс
        self.root.after(100, self.update_grid)

    def submit(self):
        # Получение текста из виджета ввода
        input_text = self.entry.get()
        print('Введенный текст:', input_text)

        # Создание нового массива сетки с заданным входным текстом
        self.grid_array = self.create_text_grid(input_text)


def main():
    root = tk.Tk()  # Создание корневого окна Tkinter
    app = GridApp(root, rows=16, cols=152, led_scale_multiplier=S, font_path='dosfonts/font.npz')
    root.mainloop()  # Запуск основного цикла событий Tkinter


if __name__ == '__main__':
    main()
