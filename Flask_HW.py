from flask import Flask, request
from faker import Faker
import csv
import requests

faker = Faker()

app = Flask(__name__)


@app.route("/requirements/")
def get_requirements():
    with open("requirements.txt", "r") as file:
        data_list = file.readlines()
        data = "<br/>".join(data_list)
    return data


# 127.0.0.1:5000/generate-users?quantity=10
@app.route("/generate-users/")
def get_users():
    quantity = request.args.get('quantity', default=100, type=int)
    user_list = []
    for i in range(quantity):
        user = faker.name() + " " + faker.email()
        user_list.append(user)
    users = "<br/>".join(user_list)
    return users


@app.route("/mean/")
def get_mean():
    general_list = []
    with open("hw.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            general_list.append(row)
    total_height = 0
    total_weight = 0
    for i in range(len(general_list)):
        total_height += float(general_list[i][' "Height(Inches)"'])
        total_weight += float(general_list[i][' "Weight(Pounds)"'])
    mean_height = total_height / len(general_list) * 2.54
    mean_weight = total_weight / len(general_list) / 2.205
    final_values = "Mean height is " + str(round(mean_height, 3)) + " cm. Mean weight is " + \
        str(round(mean_weight, 3)) + " kg."
    return final_values


@app.route("/space/")
def get_astronauts():
    r = requests.get("http://api.open-notify.org/astros.json")
    astro_dict = r.json()
    total_astros = "At the moment the number of astronauts in space is " + str(astro_dict["number"])
    return total_astros


if __name__ == "__main__":
    app.run()
