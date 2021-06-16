#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # удаляем проблемы в начале и конце строчки
    line = line.strip()

    # разбиваем каждую по символу таба
    # чтобы получить ключ и значение (число вхождений)
    word, count = line.split(' ', 1)

    # пытаемся перевести строку в число (число вхождений)
    try:
        count = int(count)
    except ValueError:
        # если перевести не получилось
        # то просто игнорируем эту строку и
        continue  # продолжаем выполнение

    # Следующий блок отработает только потому,
    # что хадуп  сначала отсортирует значения по ключу
    #  а только потом пошлёт их нашему редуктору
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # записывает результат в стандартный поток вывода
            # опять же разделяя значения табом.
            print(current_word, current_count)
        current_count = count
        current_word = word

# не забудем напечатать и последнее слово (если оно есть)
if current_word == word:
    print(current_word, current_count)