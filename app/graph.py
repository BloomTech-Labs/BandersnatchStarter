from altair import Chart, Tooltip
from pandas import DataFrame
import altair as alt

# Define a custom theme
def custom_theme():
    return {
        'config': {
            'axis': {
                'labelColor': '#aaaaaa',
                'titleColor': '#aaaaaa',
                'tickColor': '#4f4f4f',
                'domainColor': '#aaaaaa',
                'gridColor': '#4f4f4f'
            },
            'legend': {
                'labelColor': '#aaaaaa',
                'titleColor': '#aaaaaa',
            },
            'title': {
                'color': '#aaaaaa',
                'fontSize': 24
            },
        }
    }

# Register and enable the custom theme
alt.themes.register('custom', custom_theme)
alt.themes.enable('custom')


def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    graph = Chart(
        df,
        title=f"{y} by {x} for {target}",
    ).mark_circle(size=100).encode(
        x=x,
        y=y,
        color=target,
        tooltip=Tooltip(df.columns.to_list())
    ).properties(
        width=600,
        height=600,
        background='#2b2b2b',
        padding=25
    )
    return graph

