import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Cria os gráficos da aplicação
def criar_graf(df):
    # Histograma
    fig1 = px.histogram(df, x='salario', nbins=30, title='Distribuição de Salários')

    # Gráfico de pizza
    fig2 = px.pie(df, names='area_atuacao', color='area_atuacao',hole=.2, color_discrete_sequence=px.colors.sequential.RdBu)

    # Gr[afico de bolha
    fig3 = px.scatter(df, x='idade', y='salario', size='anos_experiencia', color='area_atuacao', hover_name='estado', size_max=60)
    fig3.update_layout(title='Salário por idade e anos de experiência')

    # Gráfico de linhas
    fig4 = px.line(df, x='idade', y='salario', color='area_atuacao', facet_col='nivel_educacao')
    fig4.update_layout(
        title='Salário por Idade e Área de Atuação para cada Nível de Educação',
        xaxis_title='Idade',
        yaxis_title='Salário'
    )

    # Gráfico 3D
    fig5 = px.scatter_3d(df, x='idade', y='salario', z='anos_experiencia', color='nivel_educacao')

    # Gráfico de Barra
    fig6 = px.bar(df, x='estado_civil', y='salario', color='nivel_educacao', barmode='group', color_discrete_sequence=px.colors.sequential.Blues, opacity=0.8)
    fig6.update_layout(
        title='Salário por Estado Civil e Nível de Educação',
        xaxis_title='Estado Civil',
        yaxis_title='Salário',
        legend_title='Nivel de Educação',
        plot_bgcolor='#306782',
        paper_bgcolor='#e3f6ff'
    )

    return fig1, fig2, fig3, fig4, fig5, fig6

# Cria a aplicação com os gráficos
def criar_app(df):
    app = Dash(__name__)
    fig1, fig2, fig3, fig4, fig5, fig6 = criar_graf(df)

    app.layout = html.Div([
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6)
    ])

    return app

# Lendo o Dataframe
df = pd.read_csv('../dados/clientes-v3.csv')

# Executa o app
if __name__ == '__main__':
    app = criar_app(df)
    app.run(debug=True, port=8050) # default
