import streamlit as st
from fpdf import FPDF
from PIL import Image
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Avaliação Técnica", page_icon="📝", layout="wide")

st.title("📝 Ficha de Avaliação de Receita")

# --- 1. INFORMAÇÕES GERAIS ---
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a:
        nome_receita = st.text_input("Nome da receita:")
        responsavel = st.text_input("Responsável:")
    with col_b:
        data_teste = st.date_input("Data do teste:", datetime.date.today())
        versao = st.text_input("Versão:", placeholder="Ex: Teste 1")
    
    foto = st.file_uploader("📸 Subir foto da receita", type=["jpg", "jpeg", "png"])

if foto:
    st.image(foto, caption="Foto da Degustação", width=300)

# --- 2. AVALIAÇÃO COM NOTAS E OBSERVAÇÕES ---
st.divider()
st.subheader("👅 Avaliação Sensorial e Técnica")

# Criamos as colunas para os sliders
c1, c2 = st.columns(2)

# Dicionário para armazenar os dados
avaliacoes = {}

# Itens da avaliação
itens_col1 = ["Sabor", "Aroma", "Temperos"]
itens_col2 = ["Textura", "Aparência", "Consistência"]

with c1:
    for item in itens_col1:
        nota = st.select_slider(f"Nota para **{item}**", options=list(range(11)), value=5, key=f"nota_{item}")
        obs = st.text_input(f"Observações sobre {item.lower()}:", key=f"obs_{item}")
        avaliacoes[item] = {"nota": nota, "obs": obs}
        st.write("---")

with c2:
    for item in itens_col2:
        nota = st.select_slider(f"Nota para **{item}**", options=list(range(11)), value=5, key=f"nota_{item}")
        obs = st.text_input(f"Observações sobre {item.lower()}:", key=f"obs_{item}")
        avaliacoes[item] = {"nota": nota, "obs": obs}
        st.write("---")

ajustes_finais = st.text_area("🔧 Ajustes sugeridos para a próxima versão (Geral):")

# --- 3. GERAÇÃO DO PDF ---
def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Relatório de Degustação Técnica", ln=True, align="C")
    pdf.ln(10)
    
    # Cabeçalho
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 8, f"Receita: {nome_receita.upper()}", ln=True)
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 7, f"Data: {data_teste} | Versão: {versao} | Responsável: {responsavel}", ln=True)
    pdf.ln(5)

    # Imagem
    if foto:
        try:
            img = Image.open(foto).convert("RGB")
            img.save("temp_pdf.jpg")
            pdf.image("temp_pdf.jpg", x=10, w=70)
            pdf.ln(5)
        except:
            pass

    # Notas e Observações Detalhadas
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Resultados Detalhados:", ln=True)
    pdf.ln(2)

    for item, dados in avaliacoes.items():
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(40, 7, f"{item}: {dados['nota']}/10", ln=0)
        pdf.set_font("helvetica", "I", 10)
        pdf.cell(0, 7, f" Obs: {dados['obs']}", ln=True)
    
    # Ajustes Finais
    if ajustes_finais:
        pdf.ln(5)
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 7, "Sugestões de Melhoria:", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 7, ajustes_finais)
    
    return pdf.output()

# Botão de Download
st.divider()
if st.button("🚀 Gerar e Baixar Relatório Completo"):
    if nome_receita:
        try:
            pdf_bytes = gerar_pdf()
            st.download_button(
                label="📥 Baixar PDF",
                data=bytes(pdf_bytes),
                file_name=f"Avaliacao_{nome_receita}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
    else:
        st.warning("Por favor, preencha o nome da receita.")