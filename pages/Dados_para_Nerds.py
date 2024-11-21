# Page Title: Dados para Nerds

import streamlit as st

st.set_page_config(page_title="Dados para Nerds")

st.title("Página Para Nerds")

st.subheader("Ficha Técnica do Modelo de Detecção de Artefatos Metálicos")

st.write("""
### Introdução

A Tomografia Computadorizada (TC) é uma técnica amplamente utilizada na medicina diagnóstica devido à sua capacidade de fornecer imagens detalhadas das estruturas internas do corpo. No entanto, a presença de artefatos metálicos, como aqueles provenientes de implantes dentários ou cirúrgicos, pode comprometer a qualidade das imagens e dificultar a interpretação clínica. Esses artefatos surgem devido à alta densidade dos materiais metálicos, que causam atenuação excessiva dos raios X, resultando em distorções e ruídos nas imagens reconstruídas.

Com o avanço das técnicas de aprendizado de máquina, especialmente no campo da visão computacional, há um crescente interesse em desenvolver modelos capazes de identificar e mitigar esses artefatos.      

### Objetivo

O objetivo principal deste projeto é criar um modelo de aprendizado de máquina utilizando bibliotecas avançadas, como MONAI, para detectar e eventualmente corrigir artefatos metálicos em imagens de tomografia computadorizada de cabeça.



""")

st.write("""
### Descrição do Modelo
Este modelo foi desenvolvido para detectar artefatos metálicos em exames de imagem, utilizando técnicas de aprendizado de máquina. O foco principal é identificar a presença e a localização de artefatos que podem interferir na análise clínica das imagens.

### Arquitetura do Modelo
- **Tipo de Modelo:** DenseNet121;
- **Arquitetura:** O modelo é baseado em uma arquitetura de rede profunda (DenseNet) que foi otimizada para lidar com imagens médicas, garantindo alta precisão na detecção de artefatos.

### Treinamento do Modelo
- **Conjunto de Dados:** 
    - O modelo foi treinado utilizando um conjunto de dados contendo 3792 imagens rotuladas com e sem artefatos metálicos;
    - Os dados são do banco de imagens do Hospital Israelita Albert Einstein (HIAE);
    - **Kernels:** As séries foram processadas utilizando uma variedade de 28 kernels diferentes, sendo o FC21 o mais comum.
    - **Faixa Etária**: A idade dos pacientes varia de 18 a 85 anos, com uma média de 45 anos e um desvio padrão de 18,27.
    - **Distribuição de Artefatos**: Entre as séries, 1975 contêm artefatos metálicos e 1825 não contêm artefato

- **Hiperparâmetros e Configurações de Treinamento:**
    - **Taxa de Aprendizado:** 0.001 (ajustada dinamicamente com um scheduler)
    - **Batch Size:** 2, 1 (Treinamento e validação)
    - **Número de Épocas:** 25
    - **Otimização:** Utilizou-se o otimizador Adam, com uma função de perda baseada em `CrossEntropyLoss` para a tarefa de classificação binária.
    - **Scheduler:** Um `ReduceLROnPlateau` foi utilizado para reduzir a taxa de aprendizado quando a métrica de validação não apresentava melhorias. Patience = 5;

- **Técnicas de Aumento de Dados:** Foram aplicadas técnicas de aumento de dados para melhorar a robustez do modelo, incluindo:
    - Rotação
    - Translação
    - Redimensionamento
    
### Métricas de Avaliação
O desempenho do modelo foi avaliado com as seguintes métricas:
- **Acurácia:** Medida da proporção de previsões corretas em relação ao total de previsões.
- **Precisão:** Proporção de verdadeiros positivos em relação ao total de positivos previstos.
- **Recall:** Proporção de verdadeiros positivos em relação ao total de positivos reais.
- **F1-Score:** Média harmônica da precisão e do recall.

### Ferramentas e Tecnologias Utilizadas
- **Linguagem de Programação:** Python;
- **Framework**: Monai;
- **Bibliotecas Principais:**
    - PyTorch: Para desenvolvimento e treinamento do modelo.
    - NumPy: Para manipulação de dados.
    - SimpleITK: Para processamento de imagens médicas.
    - Streamlit: Para criação da interface de usuário.

### Implementação
O modelo foi implementado seguindo as melhores práticas de programação e com foco em modularidade e reutilização de código. A arquitetura foi projetada para ser facilmente adaptável a novos conjuntos de dados e novas tarefas de detecção.

### **Resultados e Análises**

Utilizando a melhor rede treinada até o momento (DenseNet), as métricas adquiridas no conjunto de validação são: ****

- **Métricas:**
    - Acurácia: 87.93%
    - Precisão: 0.93
    - Sensibilidade (Recall): 0.83
    - F1 Score: 0.87
    - Verdadeiros Positivos (TP): 170
    - Verdadeiros Negativos (TN): 187
    - Falsos Positivos (FP): 13
    - Falsos Negativos (FN): 36

### Conclusão
Este projeto tem demonstrado a viabilidade de utilizar técnicas de aprendizado profundo para a detecção de artefatos metálicos em tomografias computadorizadas. A implementação do modelo DenseNet121 mostrou-se eficaz, com métricas de desempenho promissoras.""")

st.write("### Observações Finais")
st.write("Essa página é voltada para profissionais que desejam entender melhor os aspectos técnicos do modelo e suas implementações.")
