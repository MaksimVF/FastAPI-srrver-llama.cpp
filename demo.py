#!/usr/bin/env python3
"""
Демонстрационный скрипт для показа работы исправленного кода
"""

import os
import tempfile
from Main import validate_environment, create_model_settings

def demo_with_fake_model():
    """Демонстрация работы с фиктивной моделью"""
    
    # Создаем временный файл для имитации модели
    with tempfile.NamedTemporaryFile(suffix='.gguf', delete=False) as temp_file:
        temp_model_path = temp_file.name
        # Записываем минимальные данные для имитации модели
        temp_file.write(b"fake model data" * 1000)  # Делаем файл больше
    
    try:
        # Сохраняем оригинальные переменные окружения
        original_model_path = os.environ.get('MODEL_PATH')
        
        # Устанавливаем путь к фиктивной модели
        os.environ['MODEL_PATH'] = temp_model_path
        
        print("🔍 Демонстрация исправленного кода:")
        print("=" * 50)
        
        # Тест валидации
        print("1. Тестирование валидации окружения...")
        try:
            model_path, n_ctx, n_threads = validate_environment()
            print(f"✅ Валидация прошла успешно:")
            print(f"   - Путь к модели: {model_path}")
            print(f"   - Размер контекста: {n_ctx}")
            print(f"   - Количество потоков: {n_threads}")
        except Exception as e:
            print(f"❌ Ошибка валидации: {e}")
            return
        
        # Тест создания настроек модели
        print("\n2. Тестирование создания настроек модели...")
        try:
            model_settings = create_model_settings(model_path, n_ctx, n_threads)
            print("✅ Настройки модели созданы успешно")
            print(f"   - Модель: {model_settings.model}")
            print(f"   - Контекст: {model_settings.n_ctx}")
            print(f"   - Потоки: {model_settings.n_threads}")
        except Exception as e:
            print(f"❌ Ошибка создания настроек: {e}")
        
        print("\n3. Резюме исправлений:")
        print("✅ Исправлена ошибка с create_app() - теперь используются правильные настройки")
        print("✅ Добавлена проверка существования файла модели")
        print("✅ Добавлена валидация переменных окружения") 
        print("✅ Добавлена обработка ошибок при создании настроек")
        print("✅ Добавлен fallback для chat_format")
        print("✅ Улучшена структура кода")
        print("✅ Добавлены информативные сообщения об ошибках")
        print("✅ Настроены CORS для веб-доступа")
        
        # Восстанавливаем оригинальные переменные окружения
        if original_model_path is not None:
            os.environ['MODEL_PATH'] = original_model_path
        elif 'MODEL_PATH' in os.environ:
            del os.environ['MODEL_PATH']
        
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_model_path):
            os.unlink(temp_model_path)

def show_usage_instructions():
    """Показывает инструкции по использованию"""
    print("\n" + "=" * 50)
    print("📋 ИНСТРУКЦИИ ПО ИСПОЛЬЗОВАНИЮ:")
    print("=" * 50)
    print("1. Скачайте модель в формате GGUF, например:")
    print("   - Llama 2 7B Chat: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF")
    print("   - CodeLlama: https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF")
    print()
    print("2. Обновите файл .env:")
    print("   MODEL_PATH=/path/to/your/model.gguf")
    print()
    print("3. Запустите сервер:")
    print("   python Main.py")
    print()
    print("4. Откройте в браузере:")
    print("   http://localhost:12000/docs")

if __name__ == "__main__":
    demo_with_fake_model()
    show_usage_instructions()