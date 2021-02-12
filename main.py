import os
import pygame
import requests
from random import choice


def check_answer(img):
    if input().lower() == img.lower():
        return True
    return False


def get_spn(toponym_spn):
    lowerC = list(map(float, toponym_spn['lowerCorner'].split()))
    upperC = list(map(float, toponym_spn['upperCorner'].split()))
    return f'{(upperC[0] - lowerC[0]) / 50},{(upperC[1] - lowerC[1]) / 50}'


def get_image(city):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": city,
        "format": "json"
    }
    return requests.get(geocoder_api_server, params=geocoder_params)


CITIES = ['Nur-Sultan', 'Moscow', 'Almaty', 'Saint-Petersburg', 'Beijing', 'Los-Angeles', 'New-York']
images = []

print('Downloading images...')
for city in CITIES:
    json_response = get_image(city).json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_spn = toponym['boundedBy']['Envelope']
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")

    delta = get_spn(toponym_spn)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": delta,
        "l": choice(["map", "sat"]),
        "lang": "en_US"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    with open(f'{city}.png', 'wb') as img:
        img.write(response.content)
        images.append(img.name)
print('Download is complete\n')

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,270'
screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption('Guess the city')
count = 0
right_ans = 0
wrong_ans = 0

print('Guess city from the picture\n')
while pygame.event.wait().type != pygame.QUIT:
    if count == len(images):
        break
    screen.blit(pygame.image.load(images[count]), (0, 0))
    pygame.display.flip()
    if check_answer(CITIES[count]):
        right_ans += 1
    else:
        wrong_ans += 1
    count += 1
pygame.quit()

for city in images:
    os.remove(city)

print('\nRight answers:', right_ans)
print('Wrong answers:', wrong_ans)
print('\nPress ENTER to exit')

while input() != '':
	pass
