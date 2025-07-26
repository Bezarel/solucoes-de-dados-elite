# data_sanitizer.py
#
# Ferramenta Profissional de Limpeza e Pré-Processamento de Dados
# Versão: 1.0.0
# Autor: Ygor/Bezarel
#
# Descrição:
# Este script automatiza o processo de limpeza de datasets em formato CSV,
# aplicando uma série de tratamentos para garantir a qualidade e a consistência
# dos dados, preparando-os para análise e uso em modelos de Machine Learning.

import pandas as pd
from typing import Union

def sanitize_dataframe(df: pd.DataFrame, missing_value_threshold: float = 0.9) -> pd.DataFrame:
    """
    Aplica uma série de técnicas de limpeza robustas em um DataFrame do Pandas.

    Args:
        df (pd.DataFrame): O DataFrame sujo a ser processado.
        missing_value_threshold (float): A porcentagem de valores nulos (entre 0 e 1)
                                         para que uma coluna seja descartada. Padrão é 0.9 (90%).

    Returns:
        pd.DataFrame: Um novo DataFrame com os dados limpos e processados.
    """
    sanitized_df = df.copy()
    initial_rows, initial_cols = sanitized_df.shape
    print(f"Iniciando higienização... Dataset original com {initial_rows} linhas e {initial_cols} colunas.")

    # 1. Remover colunas com uma alta porcentagem de valores ausentes
    col_threshold = int(initial_rows * missing_value_threshold)
    sanitized_df.dropna(axis=1, thresh=col_threshold, inplace=True)
    if initial_cols > sanitized_df.shape[1]:
        print(f" -> {initial_cols - sanitized_df.shape[1]} colunas removidas por excesso de valores nulos.")

    # 2. Preencher valores ausentes restantes com base no tipo da coluna
    for col in sanitized_df.columns:
        if sanitized_df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(sanitized_df[col]):
                # Para números, preenche com a mediana (mais robusta a outliers)
                median_val = sanitized_df[col].median()
                sanitized_df[col].fillna(median_val, inplace=True)
            else:
                # Para texto/categóricos, preenche com o valor mais comum (moda)
                mode_val = sanitized_df[col].mode()[0]
                sanitized_df[col].fillna(mode_val, inplace=True)
    print(" -> Valores ausentes restantes foram preenchidos com a mediana (para números) ou moda (para texto).")

    # 3. Tentar converter colunas de texto que contêm números
    for col in sanitized_df.select_dtypes(include=['object']).columns:
        # Tenta a conversão, ignorando colunas que claramente não são numéricas
        sanitized_df[col] = pd.to_numeric(sanitized_df[col], errors='ignore')
    
    # 4. Remover espaços em branco no início e fim de todas as colunas de texto
    for col in sanitized_df.select_dtypes(include=['object']).columns:
        sanitized_df[col] = sanitized_df[col].str.strip()
    print(" -> Espaços em branco desnecessários removidos das colunas de texto.")

    # 5. Remover linhas completamente duplicadas
    sanitized_df.drop_duplicates(inplace=True)
    if initial_rows > sanitized_df.shape[0]:
        print(f" -> {initial_rows - sanitized_df.shape[0]} linhas duplicadas foram removidas.")

    final_rows, final_cols = sanitized_df.shape
    print(f"Higienização concluída. Dataset final com {final_rows} linhas e {final_cols} colunas.")
    return sanitized_df

def main(input_file: str, output_file: str):
    """
    Função principal que orquestra a leitura, limpeza e salvamento do arquivo.
    """
    try:
        # Tenta ler o arquivo com diferentes codificações para maior compatibilidade
        try:
            dirty_df = pd.read_csv(input_file, encoding='utf-8')
        except UnicodeDecodeError:
            print("AVISO: Falha ao ler com UTF-8. Tentando com 'latin-1'.")
            dirty_df = pd.read_csv(input_file, encoding='latin-1')
        
        # Chama a função de limpeza
        clean_df = sanitize_dataframe(dirty_df)
        
        # Salva o resultado
        clean_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print("\nSUCESSO! O arquivo limpo foi salvo em:", output_file)
        
    except FileNotFoundError:
        print(f"\nERRO CRÍTICO: O arquivo de entrada '{input_file}' não foi encontrado.")
        print("Por favor, verifique se o nome do arquivo e o caminho estão corretos.")
    except Exception as e:
        print(f"\nERRO INESPERADO: Um erro ocorreu durante o processamento.")
        print(f"Detalhes do Erro: {e}")

if __name__ == "__main__":
    # Esta seção permite que o script seja executado diretamente do terminal.
    # O cliente só precisa colocar o arquivo sujo na mesma pasta e rodar o script.
    
    # --- CONFIGURAÇÃO PARA O CLIENTE ---
    INPUT_FILENAME = "dados_brutos_cliente.csv"  # O nome do arquivo que o cliente fornecer
    OUTPUT_FILENAME = "dados_limpos_e_prontos.csv" # O nome do arquivo que será gerado
    # ------------------------------------

    main(input_file=INPUT_FILENAME, output_file=OUTPUT_FILENAME)
