import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import torch
import nibabel as nib
import json
from skimage.transform import resize
import pandas as pd
import os 
import SimpleITK as sitk
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Interface Principal", initial_sidebar_state = 'auto')

# Função para carregar o volume .nii.gz
def load_volume(volume_path):
    volume = nib.load(volume_path).get_fdata()  # Carregar volume usando nibabel
    volume = np.expand_dims(volume, axis=0)  # Adicionar dimensão do batch
    #volume = torch.tensor(volume, dtype=torch.float32)
    return volume

# Função para exibir uma fatia 2D com redimensionamento -> Alterar para o itk *URGENTE*
def display_slice(volume, slice_index, axis, target_shape=(256, 256)):
    volume = torch.tensor(volume, dtype=torch.float32)
    
    if axis == "Sagital":
        slice_data = volume[0, slice_index, :, :].numpy()
    elif axis == "Coronal":
        slice_data = volume[0, :, slice_index, :].numpy()
    elif axis == "Axial":
        slice_data = volume[0, :, :, slice_index].numpy()

    # Redimensionar a fatia para o target_shape
    slice_data_resized = resize(slice_data, target_shape, anti_aliasing=True)
    
    plt.imshow(slice_data_resized, cmap='gray')
    plt.axis('off')
    st.pyplot(plt)

# Função para carregar o JSON com informações das imagens
def load_data_from_json(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data["Subjects"]

def load_infos_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Função para determinar o caso
def determinar_caso(label_real, label_predicted):
    if label_real == "With Artifact" and label_predicted == "With Artifact":
        return "Verdadeiro Positivo"
    elif label_real == "No Artifact" and label_predicted == "No Artifact":
        return "Verdadeiro Negativo"
    elif label_real == "No Artifact" and label_predicted == "With Artifact":
        return "Falso Positivo"
    elif label_real == "With Artifact" and label_predicted == "No Artifact":
        return "Falso Negativo"

def save_to_csv(data, csv_path):
    df = pd.DataFrame(data)
    if not os.path.isfile(csv_path):
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode='a', header=False, index=False)

# Função para gerar a visualização interativa com Plotly
def create_interactive_plot(volume):
    volume = np.transpose(volume[0], (2, 0, 1))  # [z, y, x]
    
    r, c = volume[0].shape
    nb_frames = volume.shape[0]

    fig = go.Figure(frames=[
        go.Frame(data=go.Surface(
            z=(nb_frames - k) * np.ones((r, c)),  # Posicionar a fatia
            surfacecolor=np.flipud(volume[k]),    # Exibir a fatia correspondente
            cmin=0, cmax=np.max(volume)
        ), name=str(k)) for k in range(nb_frames)
    ])

    fig.add_trace(go.Surface(
        z=nb_frames * np.ones((r, c)),
        surfacecolor=np.flipud(volume[nb_frames - 1]),
        colorscale='Gray',
        cmin=0, cmax=np.max(volume),
        colorbar=dict(thickness=20, ticklen=4)
    ))

    def frame_args(duration):
        return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

    sliders = [
        {
            "pad": {"b": 10, "t": 60},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {
                    "args": [[f.name], frame_args(0)],
                    "label": str(k),
                    "method": "animate",
                }
                for k, f in enumerate(fig.frames)
            ],
        }
    ]

    fig.update_layout(
        title='Visualização Interativa de Fatias',
        width=1200,
        height=800,
        scene=dict(
            zaxis=dict(range=[-0.1, nb_frames], autorange=False),
            aspectratio=dict(x=1, y=1, z=1),
        ),
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, frame_args(50)],
                        "label": "&#9654;",  # símbolo de play
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;",  # símbolo de pause
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
        ],
        sliders=sliders
    )

    return fig

def create_3d_volume_plot(volume):
    # Converter o volume para o formato [x, y, z] necessário para o plot
    volume = np.transpose(volume[0], (2, 1, 0))  # [x, y, z]

    # Normalizar o volume para melhor visualização
    volume_normalized = (volume - np.min(volume)) / (np.max(volume) - np.min(volume))

    fig = go.Figure(data=go.Volume(
        x=np.linspace(0, volume.shape[0] - 1, volume.shape[0]),
        y=np.linspace(0, volume.shape[1] - 1, volume.shape[1]),
        z=np.linspace(0, volume.shape[2] - 1, volume.shape[2]),
        value=volume_normalized.flatten(),  # Flatten volume for visualization
        opacity=0.1,  # Transparência
        surface_count=15,  # Número de superfícies para renderizar
        colorscale='Gray'  # Mapa de cores para volumes médicos
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=10, range=[0, volume.shape[0] - 1], title="X"),
            yaxis=dict(nticks=10, range=[0, volume.shape[1] - 1], title="Y"),
            zaxis=dict(nticks=10, range=[0, volume.shape[2] - 1], title="Z"),
            aspectmode='cube'
        ),
        width=800,
        height=800,
        title='Visualização Volumétrica 3D'
    )

    return fig

data_json_path = "./data.json"
data = load_data_from_json(data_json_path)
infos = load_infos_from_json(data_json_path)

st.title(infos["Name"])
st.subheader("Resumo: ")
st.write(infos["Descript"])

# Carregar os dados do arquivo JSON

# model = st.selectbox("Selecione o Modelo", infos["Models"].keys())

subject_ids = list(data.keys())
selected_subject = st.selectbox("Selecione a imagem do subject:", subject_ids)

# Quando um subject for selecionado
if selected_subject:
    subject_data = data[selected_subject]
    volume_path = subject_data["path"]
    label_real = subject_data["label_real"]
    label_predicted = subject_data["label_predicted"]
    anotador = st.selectbox("Selecione o Anotador", infos["Anotadores"])
        
    # Determinar o caso com base nos rótulos real e predito
    caso = determinar_caso(label_real, label_predicted)

    # Carregar o volume .nii.gz
    volume = load_volume(volume_path)
    # Visualização
    
    slice_view = st.selectbox("Selecione o tipo de visão: ", ["Axial", "Coronal", "Sagital"])
    
    slice_ix = st.slider("Selecione o índice da Fatia", 0, volume.shape[3] - 1, 0)
    display_slice(volume, slice_ix, slice_view)

    # Exibir o label verdadeiro e a predição
    # st.write(f"Label Verdadeiro: {label_real}")
    # st.write(f"Predição: {label_predicted}")
    # st.write(f"Caso: {caso}")

    # Opção para o usuário marcar se a predição foi correta ou não
    possui_artefato = st.radio("O volume possui artefatos?", ("Não", "Sim", "Não consigo definir"))

    # Seleção do tipo de artefato e campo para comentário
    type_artefatos = [""]
    if possui_artefato == "Sim":
        type_artefatos = st.multiselect("Tipo de artefato", infos["Outputs"])

    alcance = st.radio("Olhando o eixo axial, o exame abrange as estruturas da boca e início do troco encefálico ou ele se mantém na altura das narinas?", ("Não", "Sim"))
            
    comentario = st.text_area("Deixe um comentário: ")

    # Botão de envio
    csv_path = "respostas.csv"

    # Botão de envio
    if st.button("Enviar"):
        # Dados a serem salvos
        data_to_save = {
            "Subject": [selected_subject],
            "Label Real": [label_real],
            "Predição": [label_predicted],
            "Caso": [caso],
            #"Predição Correta": [pred_correta],
            "Tipo de Artefato": [type_artefatos],
            "Alcance": [alcance],
            "Comentário": [comentario],
            "Anotador": [anotador]
        }

        # Salvar no CSV
        save_to_csv(data_to_save, csv_path)

        st.success("Resposta Cadastrada!")
        st.balloons()
        # st.write("Comentário Enviado:")
        # st.write(f"Predição Correta: {pred_correta}")
        # st.write(f"Tipo de Artefato: {type_artefatos}")
        # st.write(f"Comentário: {comentario}")