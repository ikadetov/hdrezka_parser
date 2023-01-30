from foder_manage import check_folder_films
from driver import create_driver
import requests
import json
import time
import os


def write_networks(perf):
    with open("network.json", "w") as f:
        f.write("[")

        for log in perf:
            network_log = json.loads(log['message'])['message']

            if "Network.response" in network_log['method'] or "Network.request" in network_log[
'method'] or "Network.webSocket" in network_log['method']:
                f.write(json.dumps(network_log) + ",")
        f.write("{}]")


def get_mp4_url():
    json_file_path = "network.json"

    with open(json_file_path, "r") as f:
        logs = json.loads(f.read())  # Open logs

    networks_list = []
    for log in logs:  # Iterate the logs
        try:
            episode_url = log["params"]["request"]["url"]  # URL is present inside the following keys
            # if episode_url[len(episode_url) - 23:-19] == ".mp4":  # Checks if the extension is .mp4
            if ".mp4" in episode_url:
                networks_list.append(episode_url.split(".mp4")[0]+".mp4")
        except Exception as e:
            pass

    try:
        return networks_list[-1]
    except:
        print("Возникла ошибка. Ссылка на серию не найдена!")


def download_film(url, title):
    folder_exist = check_folder_films(title)
    if folder_exist:
        print("Папки созданы")

    response = requests.get(url, stream=True)
    with open(f"hdrezka/{title}/{title}.mp4", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024*1024):
            if chunk:
                file.write(chunk)
                print(f"Фильм в процессе загрузки...")
        print("Фильм загружен успешно!")


def films(url, title):
    try:
        driver = create_driver(10)
        print("Фильм взят в обработку")
        driver.get(url)
    except:
        pass
    finally:
        time.sleep(3)
        perf = driver.get_log('performance')
        write_networks(perf)
        print("Поиск ссылки на видео")
        film_url = get_mp4_url()
        driver.quit()
        os.remove("network.json")
        print("Приступаем к загрузке!")
        download_film(film_url, title)
        print("Нажмите ENTER для выхода")
        input()
