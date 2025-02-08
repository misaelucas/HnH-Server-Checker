import requests
from bs4 import BeautifulSoup
import time
import pygame
import sys

pygame.mixer.init()

sound_file_path = 'free_alarm_stolen_from_misa.mp3'

try:
    while True:
        try:
            response = requests.get('https://www.havenandhearth.com/portal/', timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            status_div = soup.find('div', {'id': 'status'})
            
            if status_div and status_div.find('h2') and 'The server is up' in status_div.find('h2').text:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Alarm: The server is up.")
                pygame.mixer.music.load(sound_file_path)
                pygame.mixer.music.play()
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] The server might not be up or the status couldn't be found.")
                
        except requests.exceptions.RequestException as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] An error occurred: {e}")
        
        time.sleep(60)

except KeyboardInterrupt:
    print("\nExiting...")
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    sys.exit()
