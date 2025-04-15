import yfinance as yf
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Lista de moedas: Nome amigável e símbolo do Yahoo Finance
moedas = {
    'Dólar Americano (USD/BRL)': 'BRL=X',
    'Euro (EUR/BRL)': 'EURBRL=X',
    'Libra Esterlina (GBP/BRL)': 'GBPBRL=X',
    'Iene Japonês (JPY/BRL)': 'JPYBRL=X',
    'Franco Suíço (CHF/BRL)': 'CHFBRL=X'
}

# Função para baixar os dados
def baixar_dados(simbolo):
    df = yf.download(simbolo, period='20y', auto_adjust=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    return df.reset_index()

# Inicializa o app
app = Dash(__name__)
app.title = "Cotação de Moedas - Últimos 20 Anos"

# Dados iniciais (USD/BRL)
df_inicial = baixar_dados(moedas['Dólar Americano (USD/BRL)'])

app.layout = html.Div([
    html.H1("Cotação de Moedas", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Selecione a moeda:"),
        dcc.Dropdown(
            id='moeda-dropdown',
            options=[{'label': nome, 'value': nome} for nome in moedas],
            value='Dólar Americano (USD/BRL)',  # valor inicial
            clearable=False
        ),
    ], style={'width': '350px', 'margin': 'auto'}),

    html.Div(id='valor-hoje', style={'textAlign': 'center', 'fontSize': 20, 'marginTop': 10}),

    dcc.DatePickerRange(
        id='date-range',
        min_date_allowed=df_inicial['Date'].min().date(),
        max_date_allowed=df_inicial['Date'].max().date(),
        start_date=df_inicial['Date'].min().date(),
        end_date=df_inicial['Date'].max().date()
    ),

    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    Output('valor-hoje', 'children'),
    Input('moeda-dropdown', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_graph(moeda_nome, start_date, end_date):
    simbolo = moedas[moeda_nome]
    df = baixar_dados(simbolo)

    mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]

    ultimo_valor = filtered_df['Close'].iloc[-1] if not filtered_df.empty else None
    titulo = f'{moeda_nome} - Fechamento Diário'

    fig = px.line(
        filtered_df,
        x='Date',
        y='Close',
        title=titulo,
        hover_data={'Date': True, 'Close': ':.2f'}
    )

    fig.update_layout(xaxis_title='Data', yaxis_title='Cotação (R$)')

    valor_texto = f"Valor mais recente no período selecionado: R$ {ultimo_valor:.2f}" if ultimo_valor else "Nenhum dado disponível para o período selecionado."
    return fig, valor_texto

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
