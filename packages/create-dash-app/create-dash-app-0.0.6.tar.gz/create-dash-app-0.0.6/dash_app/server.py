from dash_app.components.index import Layout
from dash_app.server import app

# In order for callbacks to work, they must be imported where Dash is instantiated 
# noinspection PyUnresolvedReferences
import dash_app.callbacks.index

server = app.server
app.layout = Layout


if __name__ == '__main__':
    app.runserver(debug=True)
    
