import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime,timedelta
import pandas as pd


# Função que calcula os preços diários a partir dos dados históricos
def calcular_precos_diarios(acao):
    return acao['Adj Close']

# Função que calcula os retornos semanais consolidados a partir dos dados históricos
def calcular_retornos_semanais(acao):
    acao['Retorno Diário'] = acao['Adj Close'].pct_change().mul(100)
    retornos_semanais = acao['Retorno Diário'].resample('W').sum()
    return retornos_semanais

# Função que calcula o volume semanal consolidado a partir dos dados históricos
def calcular_volume_semanal(acao):
    volumes_semanais = acao['Volume'].resample('W').sum()
    return volumes_semanais
# Função que calcula a variação do volume em relação à semana anterior
def calcular_variacao_volume_semanal(acao):
    acao['Variação Volume'] = acao['Volume'].pct_change().mul(100)
    variacao_volume_semanal = acao['Variação Volume'].resample('W').sum()
    return variacao_volume_semanal
# Função que calcula os retornos mensais consolidados a partir dos dados históricos
def calcular_retornos_mensais(acao):
    acao['Retorno Diário'] = acao['Adj Close'].pct_change().mul(100)
    retornos_mensais = acao['Retorno Diário'].resample('M').sum()
    return retornos_mensais

# Função que será executada quando o botão for clicado
def funcao_submit(ativos,dias):
    if not dias:
        # Definir data de início para um ano atrás em relação à data atual
        dias = '252'
    #figuras
    fig_preco = go.Figure()
    fig_retorno = go.Figure()
    fig_volume = go.Figure()
    fig_variacao_volume = go.Figure()
    fig_retorno_mensal = go.Figure()

    # Criar um dicionário vazio para armazenar os dados dos retornos semanais consolidados
    dados_retornos_semanais = {}
    dados_volumes_semanais = {}
    dados_variacao_volume_semanal = {}
    dados_precos_diarios = {}
    dados_retornos_mensais = {}

    # Criar um dicionário vazio para armazenar os dados dos desvios padrão
    # desvios_padrao = {}
    # desvios_padrao_negativo = {}


    for ativo in ativos:
        if ativo=="IBOV":
            acao = yf.download('^BVSP', period=dias+'d')
            # Definir uma espessura maior para a linha do IBOV (3)
            espessura_linha = 3.5
        else:
            acao = yf.download(ativo+'.SA', period=dias+'d')
            # Definir uma espessura maior para a linha do IBOV (3)
            espessura_linha = 1.5

        normalized_prices = acao['Adj Close'] / acao['Adj Close'].iloc[0]
        # Definir manualmente a legenda para cada ativo
        fig_preco.add_trace(go.Scatter(x=normalized_prices.index, y=normalized_prices, name=ativo, showlegend=True, 
                                       line=dict(width=espessura_linha)))
        # Adicionar anotação para o nome do ativo ao final da linha
        # Adicionar anotação para o nome do ativo ao final da linha
        ultimo_preco = normalized_prices.iloc[-1]
        fig_preco.add_annotation(
            x=normalized_prices.index[-1],
            y=ultimo_preco,
            text=ativo,
            showarrow=False,  # Remover a seta da anotação
            font=dict(size=8, family='bold'),  # Deixar o texto em negrito
                yshift=3  # Ajustar a posição vertical da anotação (subir 5 pixels)
        )
        
        # Calcular os retornos semanais consolidados
        retornos_semanais = calcular_retornos_semanais(acao)
        fig_retorno.add_trace(go.Bar(x=retornos_semanais.index, y=retornos_semanais, name=ativo, showlegend=True))

        # # Calcular o volume semanal consolidado
        volumes_semanais = calcular_volume_semanal(acao)
        fig_volume.add_trace(go.Bar(x=volumes_semanais.index, y=volumes_semanais, name=ativo, showlegend=True))

        # Calcular a variação do volume em relação à semana anterior
        variacao_volume_semanal = calcular_variacao_volume_semanal(acao)
        fig_variacao_volume.add_trace(go.Bar(x=variacao_volume_semanal.index, y=variacao_volume_semanal, name=ativo,
                                             showlegend=True))

        # Calcular os preços diários
        precos_diarios = calcular_precos_diarios(acao)
        dados_precos_diarios[ativo] = precos_diarios

        # Calcular os retornos mensais consolidados
        retornos_mensais = calcular_retornos_mensais(acao)
        fig_retorno_mensal.add_trace(go.Bar(x=retornos_mensais.index, y=retornos_mensais, name=ativo, showlegend=True))

        # Adicionar os dados do ativo aos dicionários
        dados_retornos_semanais[ativo] = retornos_semanais
        dados_volumes_semanais[ativo] = volumes_semanais
        dados_variacao_volume_semanal[ativo] = variacao_volume_semanal
        dados_retornos_mensais[ativo] = retornos_mensais

        

        # # Calcular o desvio padrão dos retornos semanais consolidados
        # desvio_padrao = retornos_semanais.std()
        # desvio_padrao_negativo = -desvio_padrao
        # desvios_padrao[ativo] = desvio_padrao
        # desvios_padrao_negativo[ativo] = desvio_padrao_negativo

    fig_preco.update_layout(
        title='Variação de Preço Anual',
        xaxis_title='Data',
        yaxis_title='Preço',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    fig_retorno.update_layout(
        title='Retornos Consolidados por Semana',
        xaxis_title='Data',
        yaxis_title='Retorno Semanal(%)',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )    
    fig_volume.update_layout(
        title='Volume Acumulado por Semana',
        xaxis_title='Data',
        yaxis_title='Volume',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    fig_variacao_volume.update_layout(
        title='Variação de Volume em Relação à Semana Anterior',
        xaxis_title='Data',
        yaxis_title='Variação Volume(%)',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    fig_retorno_mensal.update_layout(
        title='Retornos Consolidados por Mês',
        xaxis_title='Data',
        yaxis_title='Retorno Mensal(%)',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    # Adicionar a linha reta para o desvio padrão no gráfico de retornos consolidados por semana
    # Definir uma paleta de cores para as linhas de desvio padrão
    # cores = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive']
    # i=0
    # for ativo, desvio in desvios_padrao.items():
    #     fig_retorno.add_shape(
    #         type="line",
    #         x0=retornos_semanais.index[0],
    #         x1=retornos_semanais.index[-1],
    #         y0=desvio,
    #         y1=desvio,
    #         line=dict(color=cores[i], width=2, dash="dash"),
    #         opacity=0.3,
    #         visible=False,  # Inicialmente oculto
    #         name=f"Desvio Padrão ({ativo})"
    #     )
    #     i=i+1
    # i=0
    # for ativo, desvio_padrao_negativo in desvios_padrao_negativo.items():
    #     fig_retorno.add_shape(
    #         type="line",
    #         x0=retornos_semanais.index[0],
    #         x1=retornos_semanais.index[-1],
    #         y0=desvio_padrao_negativo,
    #         y1=desvio_padrao_negativo,
    #         line=dict(color=cores[i], width=2, dash="dash"),
    #         opacity=0.3,
    #         visible=False,  # Inicialmente oculto
    #         name=f"Desvio Padrão Negativo ({ativo})"
    #     )
    #     i=i+1
    # Exibir os gráficos
    st.plotly_chart(fig_preco, use_container_width=True)
    st.plotly_chart(fig_retorno, use_container_width=True)
    st.plotly_chart(fig_retorno_mensal, use_container_width=True)
    st.plotly_chart(fig_volume, use_container_width=True)
    st.plotly_chart(fig_variacao_volume, use_container_width=True)
    

    # # Adicionar botão para exibir desvio padrão no gráfico
    # if st.button("Calcular Desvio Padrão"):
    #     for ativo, desvio in desvios_padrao.items():
    #         fig_retorno.update_traces(visible=True, selector=f"name='Desvio Padrão Positivo ({ativo})'")
    #         fig_retorno.update_traces(visible=True, selector=f"name='Desvio Padrão Negativo ({ativo})'")

    # Criar a tabela de retornos semanais consolidados
    tabela_retornos = pd.DataFrame(dados_retornos_semanais)

    # Inverter as linhas do DataFrame para exibir os valores mais recentes primeiro
    tabela_retornos = tabela_retornos.iloc[::-1]

    # Renomear o índice para 'Data'
    tabela_retornos = tabela_retornos.rename_axis('Data')

    # Converter o índice em uma coluna regular e renomear a coluna para 'Data'
    tabela_retornos.reset_index(inplace=True)

    # Formatar a coluna de datas para o formato "dd-mm-yyyy"
    tabela_retornos['Data'] = tabela_retornos['Data'].dt.strftime('%d-%m-%Y')

    # Adicionar as colunas de volume semanal e variação do volume em relação à semana anterior na tabela
    # Adicionar as colunas de volume semanal e variação do volume em relação à semana anterior na tabela
    # for ativo in ativos:
        
    #     volume_semanal = dados_volumes_semanais[ativo]
    #     variacao_volume_semanal = dados_variacao_volume_semanal[ativo]

    #     volume_semanal_formatado = volume_semanal.apply(lambda x: '{:,.0f}'.format(x).replace(',', '.'))
    #     variacao_volume_semanal_formatada = variacao_volume_semanal.apply(lambda x: '{:.2f}'.format(x).replace('.', ','))

    #     tabela_retornos[f'Volume Semanal ({ativo})'] = volume_semanal_formatado
    #     tabela_retornos[f'Variação Volume em Relação à Semana Anterior ({ativo})'] = variacao_volume_semanal_formatada

    # Formatando os valores de retorno para o formato "x,y" em todas as colunas de ativos
    for coluna in tabela_retornos.columns[1:]:
        tabela_retornos[coluna] = tabela_retornos[coluna].apply(lambda x: '{:.2f}'.format(x).replace('.', ','))

    # Criar a tabela de preços diários
    tabela_precos = pd.DataFrame(dados_precos_diarios)

    # Inverter as linhas do DataFrame para exibir os valores mais recentes primeiro
    tabela_precos = tabela_precos.iloc[::-1]

    # Renomear o índice para 'Data'
    tabela_precos = tabela_precos.rename_axis('Data')

    # Converter o índice em uma coluna regular e renomear a coluna para 'Data'
    tabela_precos.reset_index(inplace=True)

    # Formatar a coluna de datas para o formato "dd-mm-yyyy"
    tabela_precos['Data'] = tabela_precos['Data'].dt.strftime('%d-%m-%Y')

    # Formatando os valores de preço para o formato "x,y" em todas as colunas de ativos
    for coluna in tabela_precos.columns[1:]:
        tabela_precos[coluna] = tabela_precos[coluna].apply(lambda x: '{:.2f}'.format(x).replace('.', ','))

    # Escrever a tabela
    st.write("Tabela de Preços Diários:")
    # Adicionar o botão de download para exportar a tabela em formato Excel
    csv_export = tabela_precos.to_csv(index=False, sep=';', decimal=',')
    st.download_button(label="Exportar para Excel", data=csv_export, file_name="tabela_retornos.csv")
    # Exibir a tabela
    st.table(tabela_precos)

    # Escrever a tabela
    st.write("Tabela de Retornos Semanais Consolidados:")
    # Adicionar o botão de download para exportar a tabela em formato Excel
    csv_export = tabela_retornos.to_csv(index=False, sep=';', decimal=',')
    st.download_button(label="Exportar para Excel", data=csv_export, file_name="tabela_retornos.csv")
    # Exibir a tabela
    st.table(tabela_retornos)

    #exibir data de atualização
    st.write("Data de atualização: " + datetime.today().strftime('%d-%m-%Y %H:%M:%S'))
    

# Criar a interface do aplicativo com o Streamlit
def main():
    
    
    # URL da imagem hospedada no Imgur
    url_imagem = "https://i.ibb.co/x5C1Txs/image.png"

    # Exibindo a imagem no Streamlit
    st.image(url_imagem, width=200, use_column_width=False)

    # Título do aplicativo
    st.title('Relatório de Análise de Ativo(s)')

    # Adicionar um campo de entrada de texto para os ativos
    input_name = st.text_input('Insira os ativos (separados por vírgula)')

    # Adicionar um campo de entrada de texto para a data de início
    dias = st.text_input('Quantos dias atrás?(Default=1 ano, deixar em branco)')

    # Converter os ativos em uma lista e transformá-los em letras maiúsculas
    ativos = [ativo.strip().upper() for ativo in input_name.split(',')]


    # Adicionar o botão "Submit"
    if st.button('Submit'):
        # Chamar a função quando o botão for clicado
        funcao_submit(ativos,dias)

if __name__ == '__main__':
    main()