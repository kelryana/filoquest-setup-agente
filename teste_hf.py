#!/usr/bin/env python3
import os
from transformers import pipeline
from huggingface_hub import login

# pega o token da variável de ambiente 
token = os.getenv("HF_TOKEN")
if token:
    login(token=token)
    print("login no Hugging Face realizado com sucesso!")
else:
    print("token não encontrado. Use: export HF_TOKEN='seu_token'")

# testa um modelo pequeno (analise de sentimento)? achei legal
classificador = pipeline("sentiment-analysis", 
                         model="distilbert-base-uncased-finetuned-sst-2-english")

resultado = classificador("Estou muito feliz em aprender sobre Hugging Face!")
print(f"resultado: {resultado}")