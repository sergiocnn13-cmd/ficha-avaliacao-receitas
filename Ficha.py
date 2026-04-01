import streamlit as st
from fpdf import FPDF
import datetime
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ficha Sensorial Reedukar", layout="wide")

st.title("📝 FICHA DE ANÁLISE SENSORIAL")

# --- 1. INFORMAÇÕES GERAIS ---
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a:
        responsavel = st.text_input("Nome do Avaliador:", value="Sérgio Ramos")
    with col_b:
        data_teste = st.date_input("Data:", datetime.date.today())

# --- 2. ESCALA HEDÔNICA (TABELA) ---
st.divider()
opcoes_escala = [
    "Gostei extremamente", "Gostei muito", "Gostei moderadamente", 
    "Gostei ligeiramente", "Indiferente", "Desgostei ligeiramente", 
    "Desgostei moderadamente", "Desgostei muito", "Desgostei extremamente"
]
atributos = ["COR", "SABOR", "AROMA", "TEXTURA", "ACEITAÇÃO"]
selecoes = {}

st.markdown("### 1. Marque sua avaliação:")
cols = st.columns(5)
for i, attr in enumerate(atributos):
    with cols[i]:
        selecoes[attr] = st.radio(f"**{attr}**", opcoes_escala, key=f"sel_{attr}")

# --- 3. REAÇÃO ---
st.divider()
st.markdown("### 2. Escolha sua reação ao produto:")
reacoes_map = {
    "😡 Detestei": "detestei.png",
    "😟 Não Gostei": "nao_gostei.png",
    "😐 Indiferente": "indiferente.png",
    "🙂 Gostei": "gostei.png",
    "🤩 Adorei": "adorei.png"
}
escolha_reacao = st.radio("Selecione sua reação:", list(reacoes_map.keys()), horizontal=True, label_visibility="collapsed")
imagem_reacao = reacoes_map[escolha_reacao]

# --- 4. INTENÇÃO DE COMPRA ---
st.divider()
intencao_opcoes = [
    "Certamente compraria", "Provavelmente compraria", 
    "Talvez comprasse / talvez não", "Provavelmente não compraria", 
    "Certamente não compraria"
]
intencao_escolha = st.radio("🛒 3. Intenção de compra:", intencao_opcoes, horizontal=True)

sugestoes = st.text_area("✍️ 4. Opiniões e sugestões:")

# --- 5. FUNÇÃO PDF ---
def gerar_pdf_final(responsavel, data_teste, imagem_reacao, selecoes, atributos, opcoes_escala, intencao_escolha, intencao_opcoes, sugestoes):
    pdf = FPDF()
    pdf.add_page()
    
    # Logo
    try:
        pdf.image("logo_reedukar.png", x=80, y=10, w=50)
        pdf.ln(30)
    except:
        pdf.ln(10)

    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "FICHA DE ANÁLISE SENSORIAL", ln=True, align="C")
    pdf.ln(5)

    # Dados
    pdf.set_font("helvetica", "", 10)
    pdf.cell(90, 8, f"Avaliador: {responsavel}", ln=0)
    pdf.cell(0, 8, f"Data: {data_teste}", ln=1)
    
    # Inserir Emoji como IMAGEM
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(15, 10, "Reação: ", ln=0)
    try:
        # Tenta colocar a imagem da carinha
        pdf.image(imagem_reacao, x=pdf.get_x() + 2, y=pdf.get_y() - 2, w=8)
    except:
        pdf.cell(0, 10, "[Imagem não encontrada]", ln=1)
    pdf.ln(10)

    # Tabela Centralizada
    pdf.set_font("helvetica", "B", 8)
    col_escala = 45
    col_attr = 29
    pdf.cell(col_escala, 10, "ESCALA", border=1, align="C")
    for attr in atributos:
        pdf.cell(col_attr, 10, attr, border=1, align="C")
    pdf.ln()

    pdf.set_font("helvetica", "", 8)
    for opcao in opcoes_escala:
        pdf.cell(col_escala, 8, opcao, border=1)
        for attr in atributos:
            if selecoes[attr] == opcao:
                pdf.set_fill_color(200, 255, 200)
                pdf.cell(col_attr, 8, "X", border=1, align="C", fill=True)
            else:
                pdf.cell(col_attr, 8, "", border=1, align="C")
        pdf.ln()

    # Intenção de Compra
    pdf.ln(8)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 10, "INTENÇÃO DE COMPRA:", ln=True)
    pdf.set_font("helvetica", "", 10)
    for opt in intencao_opcoes:
        check = "[ X ]" if intencao_escolha == opt else "[   ]"
        pdf.cell(0, 7, f"{check} {opt}", ln=True)

    # Sugestões
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 10, "OPINIÕES E SUGESTÕES:", ln=True)
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 7, sugestoes if sugestoes else "Nenhuma observação.")

    return pdf.output()

# --- 6. BOTÃO ---
st.divider()
if st.button("🚀 GERAR RELATÓRIO FINAL"):
    if responsavel:
        pdf_out = gerar_pdf_final(
            responsavel, data_teste, imagem_reacao, selecoes, 
            atributos, opcoes_escala, intencao_escolha, intencao_opcoes, sugestoes
        )
        st.download_button(
            label="📥 Baixar PDF",
            data=bytes(pdf_out),
            file_name=f"Ficha_Reedukar_{data_teste}.pdf",
            mime="application/pdf"
        )