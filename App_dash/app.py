import html
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash import Dash, html, dcc

df = pd.read_csv('ecommerce_estatistica.csv')
# print(df.head().to_string())

# Deixa os parâmetros do plot em uma função para não repetir sempre
def plt_inst(title, x_label, y_label, rotation):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    plt.show()
    return plt

# Parâmetros de layout básico do dash:
def dash_inst(figure, title, xaxis_title, yaxis_title, legend):
    figure.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend
    )
    return figure

def cria_graf(df):
    # Histograma - 'Preços'
    fig1 = px.histogram(df, x='Preço', color='Qtd_Vendidos')
    dash_inst(fig1, 'Quantidade Vendida por Preço', 'Preço', 'Frequência', 'Quantidade Vendida')


    # Gráfico de dispersão - 'Desconto x Nota'
    fig2 = px.scatter(df, x='Desconto', y='Nota', color_discrete_sequence=px.colors.qualitative.Pastel)
    dash_inst(fig2, 'Dispersão - Desconto x Notas', 'Desconto', 'Nota', '')


    # Mapa de Calor - Variáveis Numéricas
    corr = df[['Nota', 'N_Avaliações', 'Desconto', 'Preço_MinMax', 'Qtd_Vendidos_Cod']].corr()
    fig3 = go.Figure(data=go.Heatmap(
        x=corr.columns,
        y=corr.index,
        z=corr.values,
        colorscale=[[0, '#0f4c96'], [1, '#700a22']], zmin=0, zmax=1
    ))
    dash_inst(fig3, 'Correlação de Variáveis Numéricas', '', '', '')


    # Gráfico de Barras - Marca x Preço Médio
    top_marcas = df['Marca'].value_counts().head(10).index # 10 marcas mais vendidas
    df_top_marcas = df[df['Marca'].isin(top_marcas)]
    preco_por_marca = df_top_marcas.groupby('Marca')['Preço'].mean().sort_values().reset_index() # Preço médio por marca
    # Cria o gráfico:
    fig4 = px.bar(preco_por_marca, x='Marca', y='Preço', color_discrete_sequence=['salmon'])
    dash_inst(fig4, 'Preço médio por marca (Top 10', 'Marcas', 'Preço Médio', '')


    # Gráfico de Pizza - Top 8 materiais mais usados
    pie_x = df['Material'].value_counts().head(8).index
    pie_y = df['Material'].value_counts().head(8).values
    fig5 = px.pie(names=pie_x, values=pie_y, hole=.2, color_discrete_sequence=px.colors.qualitative.Pastel)
    dash_inst(fig5, 'Top 8 - Materiais mais usados', '', '', '')


    # Gráfico de Densidade - Densidade de Preços
    fig6 = ff.create_distplot([df['Preço']], ['Distribuição de Preços'], show_hist=False, show_rug=False)
    dash_inst(fig6, 'Densidade de Preços', 'Preços', 'Densidade', '')

    # # Gráfico de Regressão - Materiais x Preço
    fig7 = px.scatter(df, x='Material_Cod', y='Preço', opacity=0.6, trendline='ols', trendline_color_override='darkblue')
    dash_inst(fig7, 'Relação de Material e Preço', 'Material (por códgio)', 'Preço', '')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7

def cria_app(df):
    app = Dash(__name__)
    fig1, fig2, fig3, fig4, fig5, fig6, fig7 = cria_graf(df)

    app.layout = html.Div(
        style={
            'margin': 'auto',
            'width': '80%',
            'padding': '20px',
            'borderRadius': '15px',
            'backgroundColor': '#292929',
            'color': 'white',
            'textAlign': 'center'
        },
        children=[
            html.H1('Aplicação - Visualização Interativa de Dados'),
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4),
            dcc.Graph(figure=fig5),
            dcc.Graph(figure=fig6),
            dcc.Graph(figure=fig7)
        ]
    )
    return app

# Executando o app:
if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug=True, port=8050)
