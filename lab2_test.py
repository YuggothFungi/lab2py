import unittest
import os
import numpy as np
from lab2 import (
    create_teachers_csv, 
    create_inverted_lists, 
    search_teachers,
    FILE_SIZE,
    NAME,
    RANK,
    DEGREE,
    POSITION,
    SPECIALITY
)

class TestLab2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создает тестовые данные перед запуском тестов"""
        # Генерируем тестовые данные
        names = np.random.choice(NAME, size=FILE_SIZE)
        ranks = np.random.choice(RANK, size=FILE_SIZE, p=[0.2,0.4,0.4])
        degrees = np.random.choice(DEGREE, size=FILE_SIZE, p=[0.2,0.3,0.5])
        positions = np.random.choice(POSITION, size=FILE_SIZE, p=[0.2,0.3,0.3,0.2])
        specialities = np.random.choice(SPECIALITY, size=FILE_SIZE, p=[0.1,0.1,0.2,0.1,0.1,0.2,0.1,0.1])
        
        cls.teachers = list(zip(names, ranks, degrees, positions, specialities))
        create_teachers_csv(cls.teachers)
        create_inverted_lists()

    def test_file_creation(self):
        """Проверяет создание всех необходимых файлов"""
        required_files = [
            'teachers.csv',
            'ranks_inverted.csv',
            'degrees_inverted.csv',
            'positions_inverted.csv',
            'specialities_inverted.csv'
        ]
        
        for file in required_files:
            self.assertTrue(os.path.exists(file), f"Файл {file} не создан")
            self.assertTrue(os.path.getsize(file) > 0, f"Файл {file} пуст")

    def test_search_single_criterion(self):
        """Проверяет поиск по одному критерию"""
        # Поиск только по званию
        results = search_teachers(rank="Профессор")
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIn("Профессор", result)

    def test_search_multiple_criteria(self):
        """Проверяет поиск по нескольким критериям"""
        results = search_teachers(
            rank="Профессор",
            degree="Доктор наук",
            speciality="Математика"
        )
        
        for result in results:
            self.assertIn("Профессор", result)
            self.assertIn("Доктор наук", result)
            self.assertIn("Математика", result)

    def test_search_or_condition(self):
        """Проверяет поиск с условием ИЛИ"""
        results = search_teachers(rank="Профессор|Доцент")
        
        for result in results:
            self.assertTrue(
                any(rank in result for rank in ["Профессор", "Доцент"]),
                "Результат не содержит ни одного из указанных званий"
            )

    def test_search_no_results(self):
        """Проверяет поиск без результатов"""
        results = search_teachers(
            rank="Профессор",
            degree="Без степени",
            position="Преподаватель",
            speciality="Физика"
        )
        self.assertEqual(len(results), 0)

    def test_search_empty_criteria(self):
        """Проверяет поиск без критериев"""
        results = search_teachers()
        self.assertEqual(len(results), FILE_SIZE)

    @classmethod
    def tearDownClass(cls):
        """Удаляет тестовые файлы после завершения тестов"""
        files_to_remove = [
            'teachers.csv',
            'ranks_inverted.csv',
            'degrees_inverted.csv',
            'positions_inverted.csv',
            'specialities_inverted.csv',
            'found_teachers.csv'
        ]
        
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main() 