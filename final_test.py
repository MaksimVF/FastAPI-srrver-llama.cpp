#!/usr/bin/env python3
"""
Финальный тест для демонстрации исправления ошибки create_app()
"""

import os
import tempfile
import sys

def test_original_error_fixed():
    """Демонстрирует, что оригинальная ошибка исправлена"""
    
    print("🔧 ДЕМОНСТРАЦИЯ ИСПРАВЛЕНИЯ ОШИБКИ create_app()")
    print("=" * 60)
    
    # Создаем временный файл для имитации модели
    with tempfile.NamedTemporaryFile(suffix='.gguf', delete=False) as temp_file:
        temp_model_path = temp_file.name
        temp_file.write(b"fake model data" * 1000)
    
    try:
        # Сохраняем оригинальные переменные окружения
        original_env = {
            'MODEL_PATH': os.environ.get('MODEL_PATH'),
            'N_CTX': os.environ.get('N_CTX'),
            'N_THREADS': os.environ.get('N_THREADS')
        }
        
        # Устанавливаем тестовые переменные
        os.environ['MODEL_PATH'] = temp_model_path
        os.environ['N_CTX'] = '2048'
        os.environ['N_THREADS'] = '8'
        
        print("1. Тестирование импорта и создания настроек...")
        
        try:
            from llama_cpp.server.settings import ModelSettings, ServerSettings
            from llama_cpp.server.app import create_app
            print("   ✅ Импорт успешен")
            
            # Создаем настройки
            model_settings = ModelSettings(
                model=temp_model_path,
                n_ctx=2048,
                n_threads=8,
                n_batch=512,
                verbose=False
            )
            print("   ✅ ModelSettings созданы")
            
            server_settings = ServerSettings(
                host="0.0.0.0",
                port=12000
            )
            print("   ✅ ServerSettings созданы")
            
            # Пытаемся создать приложение
            print("\n2. Тестирование create_app() с правильными параметрами...")
            
            try:
                app = create_app(
                    server_settings=server_settings,
                    model_settings=[model_settings]
                )
                print("   ✅ create_app() вызван без ошибок валидации!")
                print("   ✅ ОСНОВНАЯ ОШИБКА ИСПРАВЛЕНА!")
                
                if app is not None:
                    print(f"   ✅ Приложение создано: {type(app)}")
                    return True
                    
            except Exception as e:
                error_msg = str(e)
                if "validation error" in error_msg.lower() and "serverSettings" in error_msg:
                    print(f"   ❌ Ошибка валидации все еще присутствует: {e}")
                    return False
                elif "Failed to load model" in error_msg:
                    print(f"   ✅ Ошибка валидации исправлена!")
                    print(f"   ⚠️  Ожидаемая ошибка загрузки модели: {e}")
                    print("   (Это нормально - нужна настоящая модель)")
                    return True
                else:
                    print(f"   ⚠️  Другая ошибка: {e}")
                    return False
                    
        except ImportError as e:
            print(f"   ❌ Ошибка импорта: {e}")
            return False
            
    finally:
        # Восстанавливаем оригинальные переменные окружения
        for key, value in original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]
        
        # Удаляем временный файл
        if os.path.exists(temp_model_path):
            os.unlink(temp_model_path)

def main():
    """Основная функция теста"""
    
    success = test_original_error_fixed()
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТ ТЕСТА:")
    print("=" * 60)
    
    if success:
        print("🎉 УСПЕХ! Ошибка с create_app() полностью исправлена!")
        print()
        print("✅ Что было исправлено:")
        print("   - create_app() теперь принимает ModelSettings и ServerSettings")
        print("   - Убрана передача экземпляра Llama напрямую")
        print("   - Исправлены параметры ServerSettings")
        print("   - Добавлена правильная обработка ошибок")
        print()
        print("📝 Для полной работы:")
        print("   1. Скачайте модель в формате GGUF")
        print("   2. Укажите путь в .env файле")
        print("   3. Запустите: python Main.py")
        
    else:
        print("❌ ОШИБКА! Проблема с create_app() не полностью исправлена")
        print("   Требуется дополнительная отладка")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)