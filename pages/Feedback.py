import streamlit as st

st.set_page_config(page_title="Feedback")

st.title("Feedback sobre a Detecção de Artefatos Metálicos")

st.subheader("Por favor, responda as seguintes perguntas:")

# Perguntas
st.write("1. De forma geral, ao ver o resultado do algoritmo, você concorda com a classificação como 'sem artefato' ou 'com artefato'?")
resposta1 = st.slider("Selecione um valor de 1 a 5", 1, 5, 3, key="as1")

st.write("2. Sua interpretação pessoal foi influenciada pelo resultado do algoritmo?")
resposta2 = st.radio("", ("Sim", "Não"))

st.write("3. Qual seria a sua avaliação para o grau de dificuldade na interpretação dos exames, de modo geral?")
grau_dificuldade = st.slider("Selecione um valor de 1 a 5", 1, 5, 3, key="as2")

st.write("4. Você gostaria de deixar um comentário adicional sobre sua experiência?")
comentario_adicional = st.text_area("Comentário:")

# Botão de envio
submitted = st.button("Enviar Feedback")

if submitted:
    feedback_data = {
        "Classificacao": resposta1,
        "Influenciado pelo Algoritmo": resposta2,
        "Grau de Dificuldade": grau_dificuldade,
        "Comentario": comentario_adicional
    }
    
    # Aqui você pode salvar os dados ou processá-los como desejar
    st.success("Obrigado pelo seu feedback!")