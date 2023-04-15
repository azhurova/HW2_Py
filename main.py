import csv
import re
import os

## Читаем адресную книгу в формате CSV в список contacts_list:
with open("phonebook_raw.csv", encoding="utf8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

## 1. Пункты 1-3 задания.

# Строка поиска телефонного номера
regex_number = r"(8|\+7)[\- ]?\(?(\d{3})\)?[\- ]?([\d\-]{3})[\- ]?([\d\-]{2})[\- ]?([\d\-]{2})"
# Формат телефонного номера
subst_number = "+7(\\2)\\3-\\4-\\5"

# Строка поиска телефонного номера с добавочным номером
regex_additional_number = r"(8|\+7)[\- ]?\(?(\d{3})\)?[\- ]?([\d\-]{3})[\- ]?([\d\-]{2})[\- ]?([\d\-]{2}).*(\d{4}).*"
# Формат телефонного номера с добавочным номером
subst_additional_number = "+7(\\2)\\3-\\4-\\5 доб.\\6"

# Цикл по списку контактов
for row_index, row in enumerate(contacts_list):
    # 1. Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
    # В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.

    # Читаем текущие значения из колонок 1,2,3
    last_name = row[0]
    first_name = row[1]
    sur_name = row[2]

    # Разбираем колонку 2 на Имя,Отчество
    split_list = first_name.split()
    if len(split_list) > 0:
        first_name = split_list[0]
    if len(split_list) > 1:
        sur_name = split_list[1]

    # Разбираем колонку 1 на Фамилию,Имя,Отчество
    split_list = last_name.split()
    if len(split_list) > 0:
        last_name = split_list[0]
    if len(split_list) > 1:
        first_name = split_list[1]
    if len(split_list) > 2:
        sur_name = split_list[2]

    # Записываем значения в колонки 1,2,3
    row[0] = last_name
    row[1] = first_name
    row[2] = sur_name

    # 2. Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер,
    # формат будет такой: +7(999)999-99-99 доб.9999.

    # Колонка phone с номером телефона
    phone_index = 5
    phone_text = row[phone_index]

    phone_sub_text = re.sub(regex_number, subst_number, phone_text, 0)
    phone_sub_text = re.sub(regex_additional_number, subst_additional_number, phone_sub_text, 0)
    contacts_list[row_index][phone_index] = phone_sub_text

# 3. Объединить все дублирующиеся записи о человеке в одну.

contacts_dict = {}
# Цикл по списку контактов
for row in contacts_list:
    # Уникальный ключ Фамилия+Имя
    row_key = (row[0] + row[1]).upper()
    dict_element = contacts_dict.get(row_key)
    if dict_element is None:
        dict_element = row
    else:
        # Цикл по ячейкам строки из списка контактов
        for index, cell_text in enumerate(dict_element):
            if len(cell_text) == 0:
                dict_element[index] = row[index]
    contacts_dict[row_key] = dict_element

contacts_list.clear()
for key, item in contacts_dict.items():
    contacts_list.append(item)

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding="utf8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

os.startfile("phonebook.csv")