from flask import Flask, render_template, request
from models import Character, Skill, Battle




hero1 = Character("Игрок 1", health=100, stamina=50, energy=50)
hero2 = Character("Игрок 2", health=100, stamina=50, energy=50)

app = Flask(__name__)

battle = Battle(hero1, hero2)

@app.route('/battle', methods=['GET', 'POST'])
def battle_view():
    # Обработка хода
    if request.method == 'POST':
        # Получаем выбранный навык (например, "Мощный удар")
        player_skill = request.form.get('skill')

        # Производим обмен ударами, используя навык игрока 1
        result_p1, result_p2 = battle.exchange_turn(player_skill, "Мощный удар")  # Игрок 2 всегда использует "Мощный удар"

        # Проверяем, закончилась ли битва
        battle_result = battle.is_battle_over()

        return render_template('battle.html', result_p1=result_p1, result_p2=result_p2, battle_result=battle_result)

    # Отображаем страницу боя
    return render_template('battle.html')

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

if __name__ == '__main__':
    app.run(debug=True)