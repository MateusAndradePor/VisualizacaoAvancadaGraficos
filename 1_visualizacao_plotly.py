import plotly.express as px
import pandas as pd

df = pd.read_csv('dados/clientes-v3.csv')

# Visualização de dados com Plotly
# Gráfico de Dispersão:
fig = px.scatter(df, x='idade', y='salario', color='nivel_educacao', hover_data=['estado_civil'])
fig.update_layout(
    title = 'Dispersão - Idade x Salário por Nível de Educação',
    xaxis_title = 'Idade',
    yaxis_title = 'Salário'
)

fig.show()
