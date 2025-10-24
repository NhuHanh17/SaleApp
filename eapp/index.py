from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(template_name_or_list='index.html', msg='Welcome to App!' )

if __name__ == '__main__':
    app.run()