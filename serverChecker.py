import os
import requests
from bs4 import BeautifulSoup
import time
import pygame

pygame.mixer.init()

audio_path = 'free_alarm_stolen_from_misa.mp3'

while True:
    try:
        response = requests.get('https://www.havenandhearth.com/portal/')
        soup = BeautifulSoup(response.text, 'html.parser')

        status_div = soup.find('div', {'id': 'status'})
        if status_div and status_div.find('h2') and 'The server is up' in status_div.find('h2').text:
            print("The server is up")
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        else:
            print("The server might not be up or the status couldn't be found.")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    time.sleep(60)
