# scraper.py
#
# Ferramenta Profissional de Coleta de Inteligência Web
# Versão: 1.0.0
# Autor: Ygor/Bezarel
#
# Descrição:
# Este script é um web scraper modular projetado para extrair dados públicos
# de forma ética e eficiente, tratando de bloqueios comuns e estruturando a
# informação em formatos prontos para análise (CSV ou JSON).

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_ecommerce_page(url: str):
    """
    Raspa informações de produtos (nome e preço) de uma página de categoria
    de um site de e-commerce.

    ATENÇÃO: As classes HTML e a estrutura são exemplos e devem ser
    customizadas para cada site-alvo.

    Args:
        url (str): A URL da página a ser raspada.

    Returns:
        pd.DataFrame: Um DataFrame do Pandas com os dados extraídos, ou None se falhar.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Acessando a URL: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Lança um erro para status HTTP ruins (4xx ou 5xx)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products_data = []
        
        # --- SEÇÃO DE CUSTOMIZAÇÃO PARA O CLIENTE ---
        # A lógica abaixo é um exemplo. Para cada novo site, esta seção
        # deve ser adaptada inspecionando o código HTML da página-alvo.
        
        # Exemplo: Encontra todos os contêineres de produtos
        product_containers = soup.find_all('div', class_='product-container-class')
        
        if not product_containers:
            print("AVISO: Nenhum contêiner de produto encontrado. Verifique as classes HTML no script.")
            return None

        for container in product_containers:
            # Extrai o nome do produto
            name_tag = container.find('h2', class_='product-name-class')
            name = name_tag.text.strip() if name_tag else 'Nome não encontrado'
            
            # Extrai o preço do produto
            price_tag = container.find('span', class_='price-tag-class')
            price = price_tag.text.strip() if price_tag else 'Preço não encontrado'
            
            products_data.append({'Nome do Produto': name, 'Preço': price})

            # Pausa aleatória para simular comportamento humano e evitar bloqueios
            time.sleep(random.uniform(0.5, 1.5))
        # ---------------------------------------------
            
        return pd.DataFrame(products_data)

    except requests.exceptions.RequestException as e:
        print(f"ERRO CRÍTICO: Falha ao acessar a URL. Detalhes: {e}")
        return None

if __name__ == "__main__":
    # --- CONFIGURAÇÃO PARA O CLIENTE ---
    # Substitua com a URL real do site que o cliente deseja monitorar
    TARGET_URL = "https://www.examplestore.com/categoria/laptops" 
    OUTPUT_FILENAME = "dados_coletados.csv"
    # ------------------------------------
    
    print("Iniciando a Operação de Coleta de Inteligência...")
    
    df_results = scrape_ecommerce_page(TARGET_URL)
    
    if df_results is not None and not df_results.empty:
        print(f"\nSUCESSO! {len(df_results)} itens foram extraídos.")
        df_results.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8')
        print(f"Os dados foram salvos com sucesso em '{OUTPUT_FILENAME}'")
    else:
        print("\nFALHA: A operação foi concluída sem extrair dados. "
              "Isso pode ocorrer se a URL estiver incorreta, se o site bloqueou o acesso, "
              "ou se as classes HTML no script precisarem de atualização.")
