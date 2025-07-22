import pandas as pd
from dash import html, Dash, dcc, Input, Output, dash
import plotly.express as px

df = pd.read_csv('dados/clientes-v3.csv')
lista_nivel_educacao = df['nivel_educacao'].unique()
options = [{'label': nivel, 'value': nivel} for nivel in lista_nivel_educacao]

def cria_graficos(selecao_nivel_educacao):
    #Gráfico de barra:
    filtro_df = df[df['nivel_educacao'].isin(selecao_nivel_educacao)]

    fig1 = px.bar(filtro_df, x='estado_civil', y='salario', color='nivel_educacao', barmode='group', color_discrete_sequence=px.colors.sequential.Purples)
    fig1.update_layout(
        title='Salário por Estado Civil e Nível de Educação',
        xaxis_title = 'Estado Civil',
        yaxis_title = 'Salário',
        legend_title='Nível de Educação',
        plot_bgcolor='rgba(222,255,253,1)',
        paper_bgcolor='rgba(186,245,241,1)'
    )

    # Gráfico de bolha:
    fig2 = px.scatter(filtro_df, x='idade', y='salario', size='anos_experiencia', color='nivel_educacao', hover_name='estado', size_max=50)
    fig2.update_layout(
        title='Salário por idade, anos de experiência e nível de educação',
        xaxis_title = 'Idade',
        yaxis_title = 'Salário',
    )

    return fig1, fig2


def cria_app():
    # Criar o app:
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1('Dashboard Interativo'),
        html.Div(['''
            Interatividade entre os dados.
            '''
        ]),
        html.Br(),
        html.H2('Gráfico de Salário por Estado Civil e Nível de Educação'),
        dcc.Checklist(
            id='id_selecao_nivel_educacao',
            options=options,
            value=[lista_nivel_educacao[0]], # Valor padrão
        ),
        dcc.Graph(id='id_graf_barra'),
        dcc.Graph(id='id_graf_bolha')
    ])
    return app


# Executa o app:
if __name__ == '__main__':
    app = cria_app()

    @app.callback(
        [
        Output('id_graf_barra', 'figure'),
        Output('id_graf_bolha', 'figure')
        ],
        [Input('id_selecao_nivel_educacao', 'value')]
    )
    def atualiza_grafico(selecao_nivel_educacao):
        fig1, fig2 = cria_graficos(selecao_nivel_educacao)
        return [fig1, fig2]
    app.run(debug=True, port=8050)