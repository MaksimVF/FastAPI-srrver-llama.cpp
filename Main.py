import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
from llama_cpp.server.app import create_app
from llama_cpp.server.settings import ModelSettings, ServerSettings
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

def create_model_settings(model_path: str, n_ctx: int, n_threads: int) -> ModelSettings:
    """Создает настройки модели с обработкой ошибок"""
    try:
        # Сначала пробуем с chat_format
        model_settings = ModelSettings(
            model=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_batch=512,
            chat_format="chatml",
            verbose=False
        )
        print("Настройки модели созданы с chat_format=chatml")
        return model_settings
    except Exception as e:
        print(f"Ошибка при создании настроек с chat_format: {e}")
        # Попробуем без chat_format если возникла ошибка
        try:
            model_settings = ModelSettings(
                model=model_path,
                n_ctx=n_ctx,
                n_threads=n_threads,
                n_batch=512,
                verbose=False
            )
            print("Настройки модели созданы без chat_format")
            return model_settings
        except Exception as e2:
            raise RuntimeError(f"Не удалось создать настройки модели: {e2}")

def create_server_settings() -> ServerSettings:
    """Создает настройки сервера"""
    return ServerSettings(
        host="0.0.0.0",
        port=12000,
        interrupt_requests=True,
        disable_ping_events=False
    )

def main():
    """Основная функция приложения"""
    try:
        # Валидация окружения
        model_path, n_ctx, n_threads = validate_environment()
        print(f"Загрузка модели: {model_path}")
        print(f"Параметры: n_ctx={n_ctx}, n_threads={n_threads}")
        
        # Создание настроек модели
        model_settings = create_model_settings(model_path, n_ctx, n_threads)
        print("Настройки модели созданы")
        
        # Создание настроек сервера
        server_settings = create_server_settings()
        print("Настройки сервера созданы")
        
        # Создание FastAPI приложения
        app: FastAPI = create_app(
            server_settings=server_settings,
            model_settings=[model_settings]  # передаем как список
        )
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
