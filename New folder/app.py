import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_auth import BasicAuth
from database import db, User, ContactUs, create_tables

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Set up the SQLite database
app.server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app.server)

# Basic authentication for the login page
auth = BasicAuth(app, {'username': 'password'})
# Signup Page
signup_layout = html.Div([
    html.H2('Sign Up'),
    dcc.Input(id='sign-username-input', type='text', placeholder='Enter your username'),
    dcc.Input(id='sign-password-input', type='password', placeholder='Enter your password'),
    html.Button('Sign Up', id='sign-button', n_clicks=0),
    html.Div(id='signup-message')
])
# Login Page
login_layout = html.Div([
    html.H2('Login'),
    dcc.Input(id='username-input', type='text', placeholder='Enter your username'),
    dcc.Input(id='password-input', type='password', placeholder='Enter your password'),
    html.Button('Login', id='login-button', n_clicks=0),
    html.Div(id='login-message')
])

# Contact Us Page
contact_us_layout = html.Div([
    html.H2('Contact Us'),
    dcc.Input(id='name-input', type='text', placeholder='Enter your name'),
    dcc.Input(id='email-input', type='email', placeholder='Enter your email'),
    dcc.Textarea(id='message-input', placeholder='Enter your message'),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='submit-message')
])

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Callback to handle signup logic
@app.callback(
    Output('signup-message', 'children'),
    [Input('sign-button', 'n_clicks')],
    [State('sign-username-input', 'value'),
     State('sign-password-input', 'value')]

)
def signup(n_clicks, username, password):
    if n_clicks:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return "signedup successfully goto /login"


# Callback to handle login logic
@app.callback(
    Output('login-message', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value')]

)
def login(n_clicks, username, password):
    if n_clicks > 0:
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return 'Logged in successfully goto /contact'
        else:
            return 'Invalid credentials'


# Callback to handle contact us form submission
@app.callback(
    Output('submit-message', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('name-input', 'value'),
     State('email-input', 'value'),
     State('message-input', 'value')]
)
def submit_contact_us(n_clicks, name, email, message):
    if n_clicks > 0:
        new_contact = ContactUs(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        return 'Message submitted successfully'


# Callback to display different pages based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/signup':
        create_tables()
        return signup_layout
    elif pathname == '/login':
        create_tables()
        return login_layout
    elif pathname == '/contact':
        return contact_us_layout
    else:
        return '404 - Page not found'


def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run_server(debug=True)
