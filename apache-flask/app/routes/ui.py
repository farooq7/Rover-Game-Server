from flask import redirect, render_template

from app import app

@app.route('/', methods=['GET'])
def root():
    return redirect("/controller", code=302)

@app.route('/controller', methods=['GET'])
def controller():
    return render_template('controller.html')

@app.errorhandler(404)
def handle_404(e):
    return '', 404
