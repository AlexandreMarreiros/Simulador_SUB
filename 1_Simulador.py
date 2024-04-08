import streamlit as st
import function as fun

# Configuração da página
fun.config("","Simulador de Taxas")

# Título da página
st.title("")
st.header('Simulador de Taxas', divider='green')

def main():
    # Dicionário com links de imagens das adquirentes
    data = {
        'Adiq': 'https://i.ibb.co/0XnDtz7/adiq.png',
        'Getnet': 'https://i.ibb.co/CztNnM8/getnet.png'
    }

    # Dividir a tela em duas colunas
    col1, col2 = st.columns([1, 1])

    # Primeira coluna para o selectbox da adquirente
    with col1:
        adiquirente_selecionado = st.selectbox("Adiquirente:", list(data.keys()))

    # Segunda coluna para exibir a imagem da adquirente selecionada
    with col2:
        if adiquirente_selecionado:
            " "
            " "
            st.image(data[adiquirente_selecionado], width=100) 
    
    # Carregar dados MCC
    dados_mcc = fun.carregar_dados_mcc()
    
    # Carregar dados do banco de dados conforme adquirente selecionada
    if adiquirente_selecionado == 'Adiq':
        dados_do_banco_de_dados = fun.carregar_dados_adiq()
        tipo_taxa = ''
    else: 
        dados_do_banco_de_dados = fun.carregar_dados_getnet()
        tipo_taxa = st.selectbox("Selecione o Tipo de Taxa:", dados_do_banco_de_dados['tipo_taxa'].unique(), placeholder="Tipo de Taxa")
        
    # Selecionar MCC
    mcc_selecionado = st.selectbox("Selecione o MCC:", dados_mcc['mcc'].unique(), placeholder="MCC")
    
    # Obter a descrição correspondente ao MCC selecionado
    descricao_mcc = dados_mcc[dados_mcc['mcc'] == mcc_selecionado]['descricao_mcc'].iloc[0]
    st.write("<b><b/>", descricao_mcc, unsafe_allow_html=True)

    # Dicionário para armazenar os spreads inseridos pelo usuário
    spreads = {}
    
    # Colunas para entrada de spreads
    col1, col2 = st.columns(2)
    with col1:
        spreads['DÉBITO'] = st.number_input(f"Digite o spread para DÉBITO:", min_value=0.0) 
        spreads['2X a 6X'] = st.number_input(f"Digite o spread para 2x a 6x:", min_value=0.0) 

    with col2:
        spreads['CRÉDITO'] = st.number_input(f"Digite o spread para CRÉDITO:", min_value=0.0) 
        spreads['7X a 12X'] = st.number_input(f"Digite o spread para 7x a 12x:", min_value=0.0) 
    
    # Calcular as taxas finais
    taxas_finais = fun.calcular_taxas(mcc_selecionado, adiquirente_selecionado, spreads, dados_do_banco_de_dados, tipo_taxa)
    
    # Exibir as taxas finais formatadas em uma tabela HTML
    st.markdown(taxas_finais.to_html(escape=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
