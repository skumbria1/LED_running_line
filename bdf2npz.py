# Импорт библиотеки numpy и задание псевдонима 'np'
import numpy as np


def main():
    # Создание трехмерного массива numpy размерами (256, 16, 8) с логическим
    # типом данных, инициализированного значениями False
    array = np.zeros((256, 16, 8), dtype=bool)

    # Создание массива numpy размером 256 для хранения значений символов
    chars = np.zeros(256, dtype=str)

    # Создание numpy-массива, представляющего битовую маску со
    # значениями [128, 64, ..., 1]
    # bit_mask = 1 << np.arange(7, -1, -1)

    # Инициализация переменной array_index для отслеживания текущего индекса в
    # 'array'
    array_index = 0

    # Инициализация переменной current_index для отслеживания текущего
    # индекса во внутренних измерениях 'array'
    current_index = 0

    # Инициализация флага 'reading_bitmap' для отслеживания, читаем ли мы в
    # данный момент данные битмапа
    reading_bitmap = False

    # Открытие указанного файла BDF для чтения
    with open('dosfonts/bdf/keyrus.bdf', 'r') as file:
        # Перебор каждой строки в файле
        for line in file.readlines():
            # Проверка, начинается ли строка со 'STARTCHAR'
            if line.startswith('STARTCHAR'):
                # Извлечение шестнадцатеричного кода символа из строки и
                # преобразование его в символ Юникода
                chars[array_index] = chr(int(line.split(' ')[1][2:], 16))

            # Проверка, если текущая строка 'BITMAP'
            elif line == 'BITMAP\n':
                # Установка флага для указания того, что мы теперь читаем
                # данные битмапа для текущего символа
                reading_bitmap = True

                # Сброс текущего индекса до 0 для начала чтения данных
                # битмапа для нового символа
                current_index = 0

            # Проверка, если текущая строка 'ENDCHAR'
            elif line == 'ENDCHAR\n':
                # Сброс флага для указания того, что мы завершили
                # чтение данных битмапа для текущего символа
                reading_bitmap = False

                # Переход к следующему индексу в 'chars' и 'array'
                array_index += 1

            # Проверка, читаем ли мы в данный момент данные битмапа
            elif reading_bitmap:
                # Преобразование шестнадцатеричной строки в двоичную строку,
                # затем преобразование каждой цифры в логическое значение (0 или 1),
                # и сохранение его в соответствующем месте в 'array'
                array[array_index][current_index] = [
                    elem == '1' for elem in bin(int(line, 16))[2:].zfill(8)
                ]

                # Извлечение шестнадцатеричного значения из строки и выполнение
                # побитового И с bit_mask; если результат не равен нулю,
                # устанавливаем соответствующий элемент массива в True
                # array[array_index][current_index] = (int(line, 16) & bit_mask) != 0

                # Переход к следующему индексу внутри данных битмапа текущего символа
                current_index += 1

    # Сохранение массивов 'array' и 'chars' в сжатый файл numpy формата .npz
    np.savez_compressed('dosfonts/font.npz', array=array, chars=chars)


if __name__ == '__main__':
    main()