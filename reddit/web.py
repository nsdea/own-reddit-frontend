import reddit

import flask

app = flask.Flask(__name__, static_url_path='/')

@app.route('/')
def index():
    return flask.redirect('/r/all')

@app.route('/r/<name>')
def r(name):
    sort = flask.request.args.get('sort') or 'hot'
    return flask.render_template('index.html', posts=reddit.posts(name, sort=sort), sub=reddit.sub(name), sort=sort)

@app.route('/u/<name>')
def u(name):
    sort = flask.request.args.get('sort') or 'hot'
    return flask.render_template('index.html', posts=reddit.posts(name, sort=sort, is_user=True), sub=reddit.user(name), sort=sort)

# @app.route('/upvote/<sub>/<post>')
# def upvote(sub, post):
#     reddit.upvote(post)
#     return flask.redirect(f'/r/{sub}')

# @app.route('/downvote/<sub>/<post>')
# def downvote(sub, post):
#     reddit.downvote(post)
#     return flask.redirect(f'/r/{sub}')

app.run(port=1111, debug=True)