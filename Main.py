import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
from llama_cpp import Llama
from llama_cpp.server.app import create_app
import uvicorn

def validate_environment():
    """Проверяет и валидирует переменные окружения"""
    load_dotenv()
    
    model_path = os.getenv("MODEL_PATH")
    if not model_path:
        raise ValueError("MODEL_PATH не установлен в переменных окружения")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Файл модели не найден: {model_path}")
    
    try:
        n_ctx = int(os.getenv("N_CTX", 4096))
        n_threads = int(os.getenv("N_THREADS", 16))
    except ValueError as e:
        raise ValueError(f"Ошибка в параметрах окружения: {e}")
    
    if n_ctx <= 0:
        raise ValueError("N_CTX должен быть положительным числом")
    
    if n_threads <= 0:
        raise ValueError("N_THREADS должен быть положительным числом")
    
    return model_path, n_ctx, n_threads

def create_llama_instance(model_path: str, n_ctx: int, n_threads: int) -> Llama:
    """Создает экземпляр Llama с обработкой ошибок"""
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_batch=512,
            chat_format="chatml",  # закомментируйте при ошибке
            verbose=False  # отключаем подробный вывод
        )
        return llm
    except Exception as e:
        print(f"Ошибка при создании экземпляра Llama: {e}")
        # Попробуем без chat_format если возникла ошибка
        try:
            llm = Llama(
                model_path=model_path,
                n_ctx=n_ctx,
                n_threads=n_threads,
                n_batch=512,
                verbose=False
            )
            print("Модель загружена без chat_format")
            return llm
        except Exception as e2:
            raise RuntimeError(f"Не удалось загрузить модель: {e2}")

def main():
    """Основная функция приложения"""
    try:
        # Валидация окружения
        model_path, n_ctx, n_threads = validate_environment()
        print(f"Загрузка модели: {model_path}")
        print(f"Параметры: n_ctx={n_ctx}, n_threads={n_threads}")
        
        # Создание экземпляра Llama
        llm = create_llama_instance(model_path, n_ctx, n_threads)
        print("Модель успешно загружена")
        
        # Создание FastAPI приложения
        app: FastAPI = create_app(llm)
        print("FastAPI приложение создано")
        
        return app
        
    except Exception as e:
        print(f"Ошибка при инициализации приложения: {e}")
        sys.exit(1)

# Создаем приложение только если модуль запускается напрямую
if __name__ == "__main__":
    app = main()
    # Запуск сервера
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=12000,
        reload=False,
        access_log=True
    )
else:
    # Для импорта из других модулей создаем приложение только при необходимости
    app = None
