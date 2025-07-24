import html

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dash import Dash, html, dcc

df = pd.read_csv('ecommerce_estatistica.csv')
print(df.head().to_string())

# Deixa os parâmetros do plot em uma função para não repetir sempre
def plt_inst(title, x_label, y_label, rotation):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    plt.show()
    return plt

def cria_graf(df):
    # Histograma - 'Preços'
    fig1 = px.histogram(df, x='Preço', color='Qtd_Vendidos')
    fig1.update_layout(
        title = 'Quantidade Vendida por Preço',
        xaxis_title = 'Preço',
        yaxis_title = 'Frequência',
        legend_title = 'Quantidade Vendida'
    )
    return fig1

def cria_app(df):
    app = Dash(__name__)
    fig1 = cria_graf(df)

    app.layout = html.Div(
        style={
            'backgroundColor': 'black',
            'color': 'white',
            'width': '1000px',
            'textAlign': 'center'
        },
        children=[
            html.H1('Aplicação'),
            dcc.Graph(figure=fig1)
        ]
    )
    return app

# Executando o app:
if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug=True, port=8050)

# # Gráfico de dispersão - 'Desconto x Nota'
# sns.jointplot(x='Desconto', y='Nota', data=df, kind='scatter')
# plt_inst('Dispersão - Desconto x Notas', 'Desconto', 'Notas', 0)
#
#
# # Mapa de Calor - Variáveis Numéricas
# corr = df[['Nota', 'N_Avaliações', 'Desconto', 'Preço_MinMax', 'Qtd_Vendidos_Cod']].corr()
# plt.figure(figsize=(12,7))
# sns.heatmap(corr, annot=True, fmt='.2f')
# plt.title('Correlação de variáveis numéricas')
# plt.show()
#
#
# # Gráfico de Barra - Marca x Preço Médio
# top_marcas = df['Marca'].value_counts().head(10).index # Filtra as 10 marcas mais vendidas
# df_top_marcas = df[df['Marca'].isin(top_marcas)]
# preco_por_marca = df_top_marcas.groupby('Marca')['Preço'].mean().sort_values() # Calcula a média de preço por marca
# # Cria o gráfico:
# plt.figure(figsize=(10, 6))
# preco_por_marca.plot(kind='bar', color='salmon')
# plt_inst('Preço médio por marca (Top 10)', 'Marcas', 'Preço Médio', 45)
#
#
# # Gráfico de Pizza - Top 8 materiais mais frequentes
# x = df['Material'].value_counts().head(8).index
# y = df['Material'].value_counts().head(8).values
# plt.pie(y, labels=x, autopct='%.1f%%', startangle=0)
# plt.title('Top 8 - Materiais mais usados')
# plt.show()
#
#
# # Gráfico de Densidade - Densidade de Preços
# plt.figure(figsize=(12,7))
# sns.kdeplot(df['Preço'], fill=True, color='skyblue')
# plt_inst('Densidade de Preços', 'Preços', 'Densidade', 0)
#
#
# # Gráfico de Regressão - Nota x Preço
# plt.figure(figsize=(12,7))
# sns.regplot(x='Nota_MinMax', y='Preço', data=df, color='#345f23', scatter_kws={'alpha':.6, 'color': '#345f23'})
# plt_inst('Relação de Nota e Preço', 'Nota (Normalizado)', 'Preço', 0)
