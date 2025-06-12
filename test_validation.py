#!/usr/bin/env python3
"""
Тестовый скрипт для проверки валидации без загрузки модели
"""

import os
import tempfile
from Main import validate_environment

def test_validation():
    """Тестирует функцию валидации"""
    
    # Создаем временный файл для имитации модели
    with tempfile.NamedTemporaryFile(suffix='.gguf', delete=False) as temp_file:
        temp_model_path = temp_file.name
        temp_file.write(b"fake model data")
    
    try:
        # Сохраняем оригинальные переменные окружения
        original_env = {
            'MODEL_PATH': os.environ.get('MODEL_PATH'),
            'N_CTX': os.environ.get('N_CTX'),
            'N_THREADS': os.environ.get('N_THREADS')
        }
        
        # Тест 1: Корректные параметры
        print("Тест 1: Корректные параметры")
        os.environ['MODEL_PATH'] = temp_model_path
        os.environ['N_CTX'] = '2048'
        os.environ['N_THREADS'] = '8'
        
        try:
            model_path, n_ctx, n_threads = validate_environment()
            print(f"✅ Успешно: model_path={model_path}, n_ctx={n_ctx}, n_threads={n_threads}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        
        # Тест 2: Отсутствует MODEL_PATH
        print("\nТест 2: Отсутствует MODEL_PATH")
        if 'MODEL_PATH' in os.environ:
            del os.environ['MODEL_PATH']
        
        # Временно переименуем .env файл чтобы он не загружался
        env_file = '.env'
        temp_env_file = '.env.backup'
        if os.path.exists(env_file):
            os.rename(env_file, temp_env_file)
        
        try:
            validate_environment()
            print("❌ Ошибка: должна была возникнуть ошибка")
        except ValueError as e:
            print(f"✅ Ожидаемая ошибка: {e}")
        finally:
            # Восстанавливаем .env файл
            if os.path.exists(temp_env_file):
                os.rename(temp_env_file, env_file)
        
        # Тест 3: Несуществующий файл модели
        print("\nТест 3: Несуществующий файл модели")
        os.environ['MODEL_PATH'] = './nonexistent_model.gguf'
        
        try:
            validate_environment()
            print("❌ Ошибка: должна была возникнуть ошибка")
        except FileNotFoundError as e:
            print(f"✅ Ожидаемая ошибка: {e}")
        
        # Тест 4: Некорректные числовые параметры
        print("\nТест 4: Некорректные числовые параметры")
        os.environ['MODEL_PATH'] = temp_model_path
        os.environ['N_CTX'] = 'invalid'
        
        try:
            validate_environment()
            print("❌ Ошибка: должна была возникнуть ошибка")
        except ValueError as e:
            print(f"✅ Ожидаемая ошибка: {e}")
        
        # Восстанавливаем оригинальные переменные окружения
        for key, value in original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]
        
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_model_path):
            os.unlink(temp_model_path)
    
    print("\n✅ Все тесты валидации завершены")

if __name__ == "__main__":
    test_validation()