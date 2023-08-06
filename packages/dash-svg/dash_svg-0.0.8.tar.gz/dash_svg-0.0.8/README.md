## dash-svg

![](docs/img/dash-minimal.png)

Scalable Vector Graphics (SVG) library for [Plotly/Dash](https://dash.plotly.com/)

## Usage

Dash clone of the ubiquitous *create-react-app* default project,
```
import dash
from dash import html
from dash_svg import Svg, G, Path, Circle


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Header([
        Svg([
            G([
                Path(d='...'),
                Circle(cx="420.9", cy="296.5", r='45.7'),
                Path(d='M520.5 78.1z')
            ], fill='#61DAFB')
        ], viewBox='0 0 841.9 595.3', className="App-logo", alt="logo"),
        html.P(["Edit ", html.Code("usage.py"), " and save to reload."]),
        html.A("Learn Dash", className="App-link", href="https://dash.plotly.com/",  target="_blank", rel="noopener noreferrer")
    ], className="App-header")
], className="App")


if __name__ == '__main__':
    app.run_server(debug=True)
```

To run demo:

    pip install dash-svg

    python usage.py

