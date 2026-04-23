from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

class ReviewConstructor:
    def __init__(self):
        self.tech_specs = {
            "гидравлическую тележку": ["грузоподъёмность"],
            "самоходную тележку": ["грузоподъёмность", "аккумулятор"],
            "штабелёр": ["грузоподъёмность", "высота подъёма вил"],
            "ричтрак": ["грузоподъёмность", "высота подъёма вил"],
            "подъёмный стол": ["грузоподъёмность", "максимальная высота"],
            "комплектовщик заказов": ["грузоподъёмность", "высота подъёма вил"],
            "ручную тележку": ["грузоподъёмность", "диаметр колеса"],
            "строительную люльку": ["грузоподъёмность", "длина", "длина троса"],
            "строительный подъёмник": ["грузоподъёмность", "рабочая высота"],
            "виброплиту": ["вес", "глубина уплотнения"],
            "вибротрамбовку": ["вес", "двигатель"],
            "виброрейку": ["вес", "двигатель"],
            "колесо/опору": ["диаметр колеса", "нагрузка"],
            "таль": ["грузоподъёмность", "высота подъёма"],
            "лебёдку": ["грузоподъёмность", "длина каната"],
            "домкрат": ["грузоподъёмность", "высота подхвата"],
            "монтажный блок": ["грузоподъёмность", "габариты"],
            "такелажную тележку": ["грузоподъёмность", "габариты"],
            "гидравлический кран": ["грузоподъёмность", "высота подъёма"],
            "козловой кран": ["грузоподъёмность", "габариты"],
            "крановые весы": ["грузоподъёмность", "габариты"],
            "пульт управления": ["тип тали", "количество кнопок"],
            "стропу": ["грузоподъёмность", "длина"]
        }
        
        self.openers_pos = ["Ребята, спасибо!", "Отдельное спасибо!", "Хочу поделиться!", "Вот это техника!", "Офигеть!", "🔥 Супер!", "Крутая покупка!"]
        self.connectors_pos = ["кстати,", "отдельно радует,", "и главное,", "что важно,"]
        self.closers_pos = ["Рекомендую!", "Берём ещё.", "Для работы — находка", "Не пожалели", "Всем советую!"]
        self.openers_neg = ["К сожалению,", "Разочарован,", "Не повезло,", "Обидно, но", "Честно — не зашло,", "Минус один продавец,"]
        self.connectors_neg = ["хуже всего,", "бесит, что", "главная проблема,", "неприятно удивило,"]
        self.closers_neg = ["Больше не куплю.", "Не рекомендую.", "Обращаться не буду."]
        
        self.extra_questions = [
            {"id": "task", "text": "Для каких задач используете?", "options": ["склад", "стройка", "производство", "магазин"]},
            {"id": "plus", "text": "Что понравилось / не понравилось больше всего?", "options": ["надёжность", "удобство управления", "мощность", "цена", "компактность"]},
            {"id": "frequency", "text": "Как часто используете?", "options": ["каждый день", "несколько раз в неделю", "по необходимости"]}
        ]
    
    def get_spec_questions(self, tech):
        specs = self.tech_specs.get(tech, ["грузоподъёмность"])
        questions = []
        for spec in specs:
            if spec == "грузоподъёмность":
                questions.append({"id": "load_capacity", "text": "Какая грузоподъёмность?", "options": ["500 кг", "1 тонна", "1.5 тонны", "2 тонны", "3 тонны", "5 тонн"]})
            elif spec == "высота подъёма вил":
                questions.append({"id": "lift_height", "text": "Какая высота подъёма вил?", "options": ["1.5 м", "2 м", "3 м", "4 м", "5 м", "6 м"]})
            elif spec == "высота подъёма":
                questions.append({"id": "lift_height", "text": "Какая высота подъёма?", "options": ["1 м", "2 м", "3 м", "4 м", "5 м", "6 м"]})
            elif spec == "аккумулятор":
                questions.append({"id": "battery", "text": "Какой аккумулятор?", "options": ["литий-ионный", "свинцово-кислотный", "гелевый", "AGM"]})
            elif spec == "диаметр колеса":
                questions.append({"id": "wheel", "text": "Какой диаметр колеса?", "options": ["125 мм", "150 мм", "180 мм", "200 мм", "250 мм"]})
            elif spec == "вес":
                questions.append({"id": "weight_spec", "text": "Какой вес техники?", "options": ["50 кг", "80 кг", "100 кг", "150 кг", "200 кг"]})
            elif spec == "глубина уплотнения":
                questions.append({"id": "depth", "text": "Какая глубина уплотнения?", "options": ["20 см", "30 см", "40 см", "50 см"]})
            elif spec == "двигатель":
                questions.append({"id": "engine", "text": "Какой двигатель?", "options": ["бензиновый", "дизельный", "электрический"]})
            elif spec == "длина":
                questions.append({"id": "length", "text": "Какая длина?", "options": ["3 м", "5 м", "7 м", "10 м", "12 м"]})
            elif spec == "длина троса":
                questions.append({"id": "rope_length", "text": "Какая длина троса?", "options": ["20 м", "30 м", "40 м", "50 м", "100 м"]})
            elif spec == "рабочая высота":
                questions.append({"id": "work_height", "text": "Какая рабочая высота?", "options": ["6 м", "9 м", "12 м", "15 м", "18 м"]})
            elif spec == "максимальная высота":
                questions.append({"id": "max_height", "text": "Какая максимальная высота?", "options": ["0.5 м", "1 м", "1.5 м", "2 м"]})
            elif spec == "нагрузка":
                questions.append({"id": "load", "text": "Какая нагрузка на колесо?", "options": ["300 кг", "500 кг", "800 кг", "1000 кг"]})
            elif spec == "габариты":
                questions.append({"id": "dimensions", "text": "Какие габариты?", "options": ["компактные", "средние", "крупногабаритные"]})
            elif spec == "тип тали":
                questions.append({"id": "hoist_type", "text": "Какой тип тали?", "options": ["цепная", "канатная", "червячная"]})
            elif spec == "количество кнопок":
                questions.append({"id": "buttons", "text": "Сколько кнопок на пульте?", "options": ["2", "4", "6", "8"]})
            elif spec == "высота подхвата":
                questions.append({"id": "hook_height", "text": "Какая высота подхвата?", "options": ["100 мм", "150 мм", "200 мм", "250 мм"]})
        return questions
    
    def generate_positive_review(self, answers, stars, tech):
        opener = random.choice(self.openers_pos)
        connector = random.choice(self.connectors_pos)
        closer = random.choice(self.closers_pos)
        star_phrase = {5: "5 звёзд — заслуженно!", 4: "4 звезды — твёрдо!"}.get(stars, f"{stars} звезды — хорошо!")
        specs_text = ""
        if answers.get('load_capacity'):
            specs_text += f" грузоподъёмность {answers['load_capacity']},"
        if answers.get('lift_height'):
            specs_text += f" подъём {answers['lift_height']},"
        if answers.get('battery'):
            specs_text += f" аккумулятор {answers['battery']},"
        if answers.get('wheel'):
            specs_text += f" колесо {answers['wheel']},"
        specs_text = specs_text.rstrip(',')
        if specs_text:
            specs_text = "(" + specs_text + ")"
        task = answers.get('task', 'склад')
        plus = answers.get('plus', 'надёжность')
        frequency = answers.get('frequency', 'каждый день')
        plus_phrases = {"надёжность": "ломаться не собирается", "удобство управления": "рулится одной левой", "мощность": "тянет всё, что обещали", "цена": "деньги отдал и забыл", "компактность": "в угол засунул — не мешает"}
        review = f"{opener} {tech} — огонь! {star_phrase} {specs_text}. Для {task}а — самое то. "
        if frequency == "каждый день":
            review += f"Пользуемся {frequency} — полёт нормальный. "
        else:
            review += f"Используем {frequency} — нареканий ноль. "
        review += f"{connector} {plus_phrases.get(plus, 'всё супер')}. {closer}"
        return review
    
    def generate_negative_review(self, answers, stars, tech):
        opener = random.choice(self.openers_neg)
        connector = random.choice(self.connectors_neg)
        closer = random.choice(self.closers_neg)
        star_phrase = {1: "1 звезда — ужас!", 2: "2 звезды — не советую."}.get(stars, f"{stars} звезды — разочарование.")
        specs_text = ""
        if answers.get('load_capacity'):
            specs_text += f" грузоподъёмность {answers['load_capacity']},"
        if answers.get('lift_height'):
            specs_text += f" подъём {answers['lift_height']},"
        specs_text = specs_text.rstrip(',')
        if specs_text:
            specs_text = "(" + specs_text + ")"
        task = answers.get('task', 'склад')
        minus = answers.get('plus', 'надёжность')
        frequency = answers.get('frequency', 'каждый день')
        minus_phrases = {"надёжность": "постоянно ломается", "удобство управления": "рулить невозможно", "мощность": "не тянет заявленное", "цена": "дорого за такое качество", "компактность": "громоздкая, мешается"}
        review = f"{opener} {tech} разочаровал. {star_phrase} {specs_text}. Для {task}а не подходит. Используем {frequency} — каждый раз нервы. {connector} {minus_phrases.get(minus, 'качество ужасное')}. {closer}"
        return review

constructor = ReviewConstructor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_spec_questions', methods=['POST'])
def get_spec_questions():
    data = request.get_json()
    tech = data.get('tech')
    questions = constructor.get_spec_questions(tech)
    return jsonify({'spec_questions': questions, 'extra_questions': constructor.extra_questions})

@app.route('/generate', methods=['POST'])
def generate():
    answers = request.form.to_dict()
    review_type = request.form.get('review_type', 'positive')
    stars = int(request.form.get('stars', 5))
    tech = answers.get('tech', 'погрузчик')
    if review_type == 'manual':
        review = request.form.get('manual_review', '')
        if not review.strip():
            review = "Спасибо за отзыв!"
        stars_display = "⭐" * stars + "☆" * (5-stars)
        review = f"{stars_display}\n\n{review}"
    else:
        if review_type == 'positive':
            review = constructor.generate_positive_review(answers, stars, tech)
        else:
            review = constructor.generate_negative_review(answers, stars, tech)
        stars_display = "⭐" * stars + "☆" * (5-stars)
        review = f"{stars_display}\n\n{review}"
    platforms = ['2ГИС', 'Яндекс']
    return render_template('result.html', review=review, platforms=platforms, review_type=review_type, stars=stars)

if __name__ == '__main__':
    app.run(debug=True)