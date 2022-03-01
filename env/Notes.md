- env\Scripts\activate
- route
from flask import url_for, escape
@app.route('/user/<name>')
def user_page(name):
    return 'User page'
    return 'User: %s' % escape(name)
    return url_for('hello')
- 