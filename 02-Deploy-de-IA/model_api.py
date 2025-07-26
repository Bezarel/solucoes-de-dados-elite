# model_api.py
#
# Ferramenta Profissional de Deploy de Modelos de IA
# Versão: 1.0.0
# Autor: Ygor/Bezarel
#
# Descrição:
# Este script cria uma API RESTful de alta performance para servir um
# modelo de Machine Learning pré-treinado, tornando-o acessível para
# integração em outras aplicações de forma escalável e segura.

from fastapi import FastAPI, HTTPException
from pantic import BaseModel
import joblib
import pandas as pd
from typing import List

# --- CONFIGURAÇÃO ---
# O cliente deve colocar o arquivo do modelo treinado (.joblib ou .pkl)
# nesta mesma pasta e atualizar o nome do arquivo aqui.
MODEL_FILENAME = "modelo_de_classificacao.joblib"
# --------------------

# Carrega o modelo de forma global quando a aplicação inicia.
try:
    model = joblib.load(MODEL_FILENAME)
    print(f"Modelo '{MODEL_FILENAME}' carregado com sucesso na inicialização.")
except FileNotFoundError:
    model = None
    print(f"AVISO: Arquivo de modelo '{MODEL_FILENAME}' não encontrado. O endpoint /predict retornará um erro.")
except Exception as e:
    model = None
    print(f"ERRO CRÍTICO ao carregar o modelo: {e}")


# Define a estrutura dos dados de entrada para uma única predição.
# As chaves (ex: 'feature1') devem ser exatamente iguais às que o modelo espera.
class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    feature3: str
    feature4: int
    # Exemplo: feature1=10.5, feature2=2.1, feature3='categoria_A', feature4=5

# Inicializa o aplicativo FastAPI com metadados profissionais.
app = FastAPI(
    title="API de Deploy de Modelo de IA",
    description="Serve um modelo de classificação pré-treinado para predições em tempo real.",
    version="1.0.0",
)

@app.post("/predict", summary="Realiza uma única predição")
def predict(data: PredictionInput):
    """
    Recebe os dados de uma única entrada, faz a predição usando o modelo
    carregado e retorna o resultado.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo de IA não está operacional. Verifique a configuração do servidor.")

    try:
        # Converte os dados de entrada Pydantic para um DataFrame do Pandas,
        # que é o formato esperado pela maioria dos modelos Scikit-learn.
        input_df = pd.DataFrame([data.dict()])
        
        # Faz a predição
        prediction_result = model.predict(input_df)
        
        # Retorna o resultado da predição em um formato JSON claro.
        # Usamos int() ou float() para garantir que o tipo de dado seja compatível com JSON.
        return {
            "input_data": data.dict(),
            "prediction": prediction_result[0].item() 
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar a predição: {e}")

@app.get("/", summary="Verifica o status da API")
def read_root():
    """
    Endpoint de verificação de saúde. Se retornar 'status': 'operacional',
    a API está funcionando, mas não garante que o modelo de IA foi carregado.
    """
    model_status = "Carregado e Pronto" if model is not None else "ERRO: Modelo não encontrado"
    return {
        "service": "API de Deploy de Modelo de IA",
        "version": "1.0.0",
        "status": "operacional",
        "model_status": model_status
    }

# Para rodar a API: uvicorn model_api:app --reload
