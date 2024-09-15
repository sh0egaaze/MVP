from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('main_menu.html')

@app.route("/link1")
def link1():
    return render_template("link1.html")

@app.route("/link2")
def link2():
    return render_template('link2.html')

@app.route("/link3")
def link3():
    return render_template('link3.html')

@app.route("/link4")
def link4():
    return render_template('link4.html')

@app.route("/link5")
def link5():
    return render_template('link5.html')

@app.route("/link6")
def link6():
    return render_template('link6.html')

@app.route("/link7")
def link7():
    return render_template('link7.html')

@app.route("/link8")
def link8():
    return render_template('link8.html')

@app.route("/link9")
def link9():
    return render_template('link9.html')

@app.route("/link10")
def link10():
    return render_template('link10.html')

@app.route("/link11")
def link11():
    return render_template('link11.html')

@app.route("/link12")
def link12():
    return render_template('link12.html')

@app.route("/arena")
def arena():
    return render_template('arena.html')

@app.route('/character')
def character():
    return render_template('character.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

if __name__ == '__main__':
    app.run(debug=True)