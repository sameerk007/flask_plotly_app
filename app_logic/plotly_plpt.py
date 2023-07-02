import plotly.graph_objects as go
import pandas as pd


def get_plot(df: pd.DataFrame ,columns: list, title : str):
    fig = go.Figure()
    for column in columns:
        fig.add_trace(go.Scatter(x=df['month_year'].astype('string'), y=df[column], name=column, showlegend=True,mode='markers+lines', marker=dict(size=5),line=dict(width=2)))
    fig.update_layout(   
        title={
        'text': f'<b><i>{title}</i></b>',
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top'
    }, showlegend=True)
    return fig