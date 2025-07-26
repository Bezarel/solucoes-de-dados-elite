# Ferramenta de Higienização e Pré-Processamento de Dados v1.0.0

## 1. Visão Geral

Esta ferramenta é uma solução em Python projetada para automatizar o processo de limpeza de datasets em formato CSV. Ela recebe um arquivo de dados "sujo" e gera uma versão limpa, consistente e pronta para ser utilizada em análises de negócios, dashboards ou no treinamento de modelos de Inteligência Artificial.

## 2. Funcionalidades Principais

O script aplica as seguintes técnicas de limpeza de forma sequencial:

* **Remoção de Colunas Vazias:** Descarta colunas que possuem mais de 90% de valores ausentes.
* **Preenchimento Inteligente:** Preenche os valores nulos restantes, usando a **mediana** para colunas numéricas (para resistir a valores extremos) e a **moda** (valor mais comum) para colunas de texto.
* **Correção de Tipos:** Converte automaticamente colunas que deveriam ser numéricas, mas estão formatadas como texto.
* **Padronização de Texto:** Remove espaços em branco desnecessários no início e no fim das células de texto.
* **Remoção de Duplicatas:** Elimina linhas que são cópias exatas de outras, garantindo a integridade do dataset.

## 3. Instruções de Uso (Setup Rápido)

Siga estes três passos para rodar a ferramenta.

### Passo 1: Preparar o Ambiente

É necessário ter o Python 3 instalado no seu sistema. Em seguida, abra um terminal (Prompt de Comando ou PowerShell no Windows, Terminal no macOS/Linux) e instale a única dependência necessária com o seguinte comando:

```bash
pip install -r requirements.txt
```

### Passo 2: Preparar o Arquivo de Dados

1.  Pegue o seu arquivo CSV que precisa de limpeza.
2.  Renomeie este arquivo para `dados_brutos_cliente.csv`.
3.  Coloque este arquivo na **mesma pasta** onde você salvou o script `data_sanitizer.py`.

### Passo 3: Executar o Script

Com o terminal aberto na pasta correta, execute o seguinte comando:

```bash
python data_sanitizer.py
```

O script irá processar o arquivo e, ao final, criará um novo arquivo chamado `dados_limpos_e_prontos.csv` nesta mesma pasta. Este novo arquivo contém seus dados higienizados e prontos para uso.

## 4. Suporte e Customização

Este script foi projetado para ser robusto, mas cada dataset é único. Caso encontre algum erro ou precise de customizações específicas (ex: regras de limpeza diferentes, processamento de outros formatos de arquivo), por favor, entre em contato.

---
*Solução desenvolvida por [Seu Nome/Ygor S. Silva]*
