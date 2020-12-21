from views import app, index

app.add_url_rule('/', 'index', index)