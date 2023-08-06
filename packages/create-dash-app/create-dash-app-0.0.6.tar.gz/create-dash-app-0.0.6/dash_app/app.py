import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG, 
    ],
    # Dash throws exceptions about callbacks from components that might be not loaded yet if
    # elements like Tabs are used. These alerts are annoying so suppress them.
    suppress_callback_exceptions=True,
    title=dash_app,
)
cache = Cache(
    app.server,
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': os.path.join(/Users/eli.woods/personal/create-dash-app, 'dash-cache'),
    }
)

