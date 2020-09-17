from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy

weather_app = Flask(__name__)
weather_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(weather_app)


class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@weather_app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = []
    if request.method == "POST":
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = Cities(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

        cities = Cities.query.all()
        your_api_key = ""
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=your_api_key'

        for city in cities:
            response = requests.get(url.format(city.name)).json()

            weather = {
                'description': response['weather'][0]['description'],
                'cname': city.name,
                'icon': response['weather'][0]['icon'],
                'temperature': response['main']['temp']
            }

            print(weather)
            weather_data.append(weather)

    return render_template('homepage.html', weather_data=weather_data)


if __name__ == "__main__":
    weather_app.run(debug=True)
