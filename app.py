from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ключ для работы с flash-сообщениями

# Путь к файлу JSON
JSON_FILE = 'characters.json'


# Функция для загрузки персонажей из файла JSON
def load_characters():
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, 'r') as f:
        return json.load(f)


# Функция для сохранения персонажей в файл JSON
def save_characters(characters):
    with open(JSON_FILE, 'w') as f:
        json.dump(characters, f, indent=4)


def generate_user_id():
    return random.randint(1000000, 9999999)  # Генерация 7-значного ID

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form['nickname']
        print(f"Полученный ник: {nickname}")  # Отладочный вывод
        characters = load_characters()
        print(f"Существующие персонажи: {characters}")  # Отладочный вывод

        if nickname in characters:
            print("Ник уже занят!")  # Отладочный вывод
            return render_template('registration.html', error="Такой ник уже существует. Пожалуйста, выберите другой.")

        user_id = generate_user_id()

        while str(user_id) in characters:
            user_id = generate_user_id()

        new_character = {
            'id': user_id,
            'nickname': nickname,
            'level': 1,
            'current_experience': 0,
            'required_experience': 100,
            'credits': 500,
            'strength': 1,
            'accuracy': 1,
            'skills': {
                'melee': {'level': 1, 'experience': 0, 'required_experience': 100},
                'cold_weapon': {'level': 1, 'experience': 0, 'required_experience': 100},
                'ranged_weapon': {'level': 1, 'experience': 0, 'required_experience': 100},
            },
            'abilities': {
                'power_strike': 1,
                'dodge': 1,
            }
        }
        characters[str(user_id)] = new_character
        save_characters(characters)

        return redirect(url_for('main_menu', user_id=user_id))

    return render_template('registration.html')




@app.route('/main_menu/<int:user_id>')
def main_menu(user_id):
    characters = load_characters()
    character = characters.get(str(user_id))
    if not character:
        return "Пользователь не найден", 404

    return render_template('main_menu.html', character=character)


@app.route('/character/<int:user_id>')
def character_view(user_id):
    characters = load_characters()
    character = characters.get(str(user_id))
    if not character:
        return "Пользователь не найден", 404

    return render_template('character.html', character=character)


@app.route('/skills/<int:user_id>', methods=['GET'])
def skills_view(user_id):
    characters = load_characters()
    character = characters.get(str(user_id))
    if not character:
        return "Пользователь не найден", 404

    return render_template('skills.html', character=character)


@app.route('/attributes/<int:user_id>', methods=['GET'])
def attributes_view(user_id):
    characters = load_characters()
    character = characters.get(str(user_id))
    if not character:
        return "Пользователь не найден", 404

    return render_template('attributes.html', character=character)


@app.route('/abilities/<int:user_id>', methods=['GET', 'POST'])
def abilities_view(user_id):
    characters = load_characters()
    character = characters.get(str(user_id))
    if not character:
        return "Пользователь не найден", 404

    messages = []
    if request.method == 'POST':
        ability = request.form.get('ability')
        if ability in character['abilities']:
            character['abilities'][ability] += 1  # Повышение уровня способности
            save_characters(characters)
            messages.append(f"Уровень способности '{ability}' повышен до {character['abilities'][ability]}.")
        else:
            messages.append(f"Способность '{ability}' не найдена.")

    return render_template('abilities.html', character=character, messages=messages)


@app.route('/upgrade_characteristic/<int:user_id>/<characteristic>', methods=['POST'])
def upgrade_characteristic(user_id, characteristic):
    characters = load_characters()
    character = characters.get(str(user_id))
    if not character:
        return "Пользователь не найден", 404

    upgrade_cost = 100
    if character['credits'] >= upgrade_cost:
        character['credits'] -= upgrade_cost
        if characteristic == 'strength':
            character['strength'] += 1
        elif characteristic == 'accuracy':
            character['accuracy'] += 1

        save_characters(characters)
        flash('Уровень характеристики успешно повышен!')
        return redirect(url_for('attributes_view', user_id=user_id))

    flash('Недостаточно кредитов для повышения уровня характеристики.')
    return redirect(url_for('attributes_view', user_id=user_id))


@app.route('/upgrade_skill/<int:user_id>/<skill>', methods=['POST'])
def upgrade_skill(user_id, skill):
    characters = load_characters()
    character = characters.get(str(user_id))
    if not character:
        return "Пользователь не найден", 404

    upgrade_cost = 50
    skills = character['skills']

    if character['credits'] >= upgrade_cost:
        if skill in skills:
            character['credits'] -= upgrade_cost

            # Увеличение опыта для навыка
            skills[skill]['experience'] += 50

            # Проверка на повышение уровня
            while skills[skill]['experience'] >= skills[skill]['required_experience']:
                skills[skill]['level'] += 1
                skills[skill]['experience'] -= skills[skill]['required_experience']
                # Увеличение необходимого опыта для следующего уровня
                skills[skill]['required_experience'] = int(skills[skill]['required_experience'] * 1.5)  # Пример масштаба

            save_characters(characters)
            flash(f"Уровень навыка '{skill}' повышен до {skills[skill]['level']}!")
            return redirect(url_for('skills_view', user_id=user_id))
        else:
            return "Навык не найден", 400

    flash('Недостаточно кредитов для повышения уровня навыка.')
    return redirect(url_for('skills_view', user_id=user_id))


@app.route('/learn_ability/<int:user_id>/<ability>', methods=['POST'])
def learn_ability(user_id, ability):
    characters = load_characters()
    character = characters.get(str(user_id))
    if not character:
        return "Пользователь не найден", 404

    learning_cost = 150
    if character['credits'] >= learning_cost:
        character['credits'] -= learning_cost
        if ability in character['abilities']:
            character['abilities'][ability] += 1  # Повышение уровня способности

            save_characters(characters)
            flash(f"Уровень способности '{ability}' повышен до {character['abilities'][ability]}!")
            return redirect(url_for('abilities_view', user_id=user_id))

    flash('Недостаточно кредитов для повышения уровня способности.')
    return redirect(url_for('abilities_view', user_id=user_id))




@app.route('/inventory')
def inventory():
    return render_template('inventory.html')


@app.route('/battle')
def battle():
    return render_template('battle.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/arena')
def arena():
    return render_template('arena.html')


if __name__ == '__main__':
    app.run(debug=True)
