import os
from dotenv import load_dotenv
from fastapi import FastAPI
from llama_cpp import Llama
from llama_cpp.server.app import create_app

load_dotenv()

model_path = os.getenv("MODEL_PATH")
n_ctx = int(os.getenv("N_CTX", 4096))
n_threads = int(os.getenv("N_THREADS", 16))

llm = Llama(
    model_path=model_path,
    n_ctx=n_ctx,
    n_threads=n_threads,
    n_batch=512,
    chat_format="chatml",  # закомментируйте при ошибке
)

app: FastAPI = create_app(llm)
