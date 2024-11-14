import numpy as np
import time

# Константы, размер файла (количество записей) и возможные значения полей
FILE_SIZE = 10000
RANK = ['Профессор', 'Доцент', 'Без звания']
DEGREE = ['Доктор наук', 'Кандидат наук', 'Без степени']
POSITION = ['Профессор', 'Доцент', 'Старший преподаватель', 'Преподаватель']
SPECIALITY = ['Физика', 'Химия', 'Математика', 'Биология', 'История', 'Психология', 'Филология', 'Политология']
NAME = ['Харитонов', 'Андреев', 'Брещенко', 'Волков', 'Евсиков', 'Ковалев', 'Лаптева', 'Парфенович', 'Попенко', 'Приходько', 'Тарасова', 'Титоренко', 'Тынчиров', 'Царюк', 'Шабунин']

def create_teachers_csv(teachers):
    """
    Создает CSV файл с данными о преподавателях
    
    Аргументы:
        teachers (list): Список кортежей, где каждый кортеж содержит данные о преподавателе
                        (имя, звание, степень, должность, специальность по диплому)
    """
    with open('teachers.csv', 'w', encoding='utf-8') as f:
        for teacher in teachers:
            f.write(f'{teacher[0]},{teacher[1]},{teacher[2]},{teacher[3]},{teacher[4]}\n')

def add_to_dict(dictionary, key, index):
    """
    Добавляет индекс в список значений для заданного ключа в словаре
    
    Аргументы:
        dictionary (dict): Словарь для обновления
        key: Ключ, по которому добавляется значение
        index (int): Индекс для добавления в список значений
    """
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(index)

def write_inverted_list(dictionary, filename):
    """
    Записывает инвертированный список в CSV файл
    
    Аргументы:
        dictionary (dict): Словарь, содержащий инвертированные индексы
        filename (str): Имя выходного CSV файла
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for key, indices in dictionary.items():
            f.write(f'{key},{",".join(map(str, indices))}\n')

def create_inverted_lists():
    """
    Создает инвертированные индексы на основе данных из teachers.csv
    
    Читает данные из файла teachers.csv и создает четыре отдельных файла с 
    инвертированными индексами для каждого поля (звание, степень, должность, специальность).
    Каждый инвертированный индекс сохраняется в отдельный CSV файл.
    """
    # Читаем teachers.csv и создаем инвертированные списки
    with open('teachers.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Инициализируем инвертированные списки как словари
    rank_dict = {}
    degree_dict = {}
    position_dict = {}
    speciality_dict = {} 

    # Обрабатываем каждую строку и строим инвертированные списки
    for i, line in enumerate(lines):
        name, rank, degree, position, speciality = line.strip().split(',')
            
        # Добавляем в словари
        add_to_dict(rank_dict, rank, i)
        add_to_dict(degree_dict, degree, i)
        add_to_dict(position_dict, position, i)
        add_to_dict(speciality_dict, speciality, i)
    
    write_inverted_list(rank_dict, 'ranks_inverted.csv')
    write_inverted_list(degree_dict, 'degrees_inverted.csv') 
    write_inverted_list(position_dict, 'positions_inverted.csv')
    write_inverted_list(speciality_dict, 'specialities_inverted.csv')

def get_matching_indices_for_field(field_value, field_indices):
    """
    Обрабатывает условия поиска ИЛИ для каждого поля и возвращает соответствующие индексы
    
    Аргументы:
        field_value (str): Искомые значения, разделенные '|' для условий ИЛИ
        field_indices (dict): Словарь, содержащий инвертированный индекс для поля
    
    Возвращает:
        set: Множество индексов, соответствующих любому из условий ИЛИ
    """
    if not field_value:
        return None
        
    matches = set()
    for value in field_value.split('|'):
        if value in field_indices:
            matches.update(field_indices[value])
    return matches if matches else set()

def read_inverted_index(filename):
    """
    Читает инвертированный индекс из CSV файла в словарь
    
    Аргументы:
        filename (str): Имя CSV файла для чтения
        
    Возвращает:
        dict: Словарь, сопоставляющий ключи с множествами индексов
    """
    indices = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            key, values = line.strip().split(',', 1)
            indices[key] = set(map(int, values.split(',')))
    return indices

def process_field_matches(field_value, field_indices, matching_indices):
    """
    Обрабатывает совпадения для каждого поля и обновляет соответствующие индексы
    
    Аргументы:
        field_value: Искомое значение для поля
        field_indices: Словарь инвертированного индекса для поля
        matching_indices: Текущее множество совпадающих индексов для обновления
    """
    field_matches = get_matching_indices_for_field(field_value, field_indices)
    if field_matches is not None:
        matching_indices &= field_matches

def search_teachers(rank=None, degree=None, position=None, speciality=None):
    """
    Выполняет поиск преподавателей по заданным критериям
    
    Аргументы:
        rank (str, optional): Строка с званиями, разделенными '|' для условия ИЛИ
        degree (str, optional): Строка со степенями, разделенными '|' для условия ИЛИ
        position (str, optional): Строка с должностями, разделенными '|' для условия ИЛИ
        speciality (str, optional): Строка со специальностями по диплому, разделенными '|' для условия ИЛИ
    
    Возвращает:
        matching_records: Список строк с данными найденных преподавателей
    """
    # Загружаем инвертированные индексы из файлов        
    rank_indices = read_inverted_index('ranks_inverted.csv')
    degree_indices = read_inverted_index('degrees_inverted.csv')
    position_indices = read_inverted_index('positions_inverted.csv')
    speciality_indices = read_inverted_index('specialities_inverted.csv')
    
    # Получаем соответствующие индексы для каждого поля, если оно указано
    matching_indices = set(range(FILE_SIZE))  # Создаём множество в соответствии с размером файла

    # Обрабатываем каждое поле
    process_field_matches(rank, rank_indices, matching_indices)
    process_field_matches(degree, degree_indices, matching_indices)
    process_field_matches(position, position_indices, matching_indices) 
    process_field_matches(speciality, speciality_indices, matching_indices)
    
    # Читаем исходные данные для возврата соответствующих записей
    matching_records = []
    with open('teachers.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in matching_indices:
            record = lines[i].strip().split(',')
            # Форматируем запись для красивого вывода
            formatted_record = f"{record[0]}: {record[1]}, {record[2]}, {record[3]}, {record[4]}"
            matching_records.append(formatted_record)
            
    return matching_records


def main():
    # Генерируем данные
    names = np.random.choice(NAME, size=FILE_SIZE)
    ranks = np.random.choice(RANK, size=FILE_SIZE, p=[0.2,0.4,0.4])
    degrees = np.random.choice(DEGREE, size=FILE_SIZE, p=[0.2,0.3,0.5])
    positions = np.random.choice(POSITION, size=FILE_SIZE, p=[0.2,0.3,0.3,0.2])
    specialities = np.random.choice(SPECIALITY, size=FILE_SIZE, p=[0.1,0.1,0.2,0.1,0.1,0.2,0.1,0.1])
    
    # Создаём список записей с именами
    teachers = list(zip(names, ranks, degrees, positions, specialities))

    # Создаём список преподавателей и инвертированные списки
    create_teachers_csv(teachers)
    create_inverted_lists()
    
    # Пример параметров поиска
    rank = "Профессор|Доцент"
    degree = "Кандидат наук" 
    position = "Доцент"
    speciality = "Математика|Физика"
    
    # Засекаем и выводим время поиска   
    start_time = time.time()
    matching_teachers = search_teachers(rank, degree, position, speciality)
    end_time = time.time()
    print(f"\nПоиск занял {(end_time - start_time)*1000:.2f} миллисекунд")
    
    # Записываем результаты в файл
    if matching_teachers.__len__() > 0:
        print(f"\nНайдено преподавателей: {len(matching_teachers)}")
        print("\nСписок найденных преподавателей сохранён в файл found_teachers.csv.")
        with open('found_teachers.csv', 'w', encoding='utf-8') as f:
            for teacher in matching_teachers:
                f.write(f'{teacher}\n')
    else:
        print("Преподаватели не найдены")

if __name__ == "__main__":
    main()
