from driver import create_driver
from foder_manage import check_folder_series
import requests
import time
import json
import os


url_list = []


def get_series_number():
    while True:
        try:
            season = int(input("Введите номер сезона: "))
            break
        except:
            print("Недопустимое значение! Вводите только цифры")
            continue
    while True:
        while True:
            try:
                start_episode = int(input("Введите номер серии с которой начать загрузку: "))
                break
            except:
                print("Недопустимое значение! Вводите только цифры")
                continue
        while True:
            try:
                finish_episode = int(input("Введите номер последней серии которая будет загружена: "))
                break
            except:
                print("Недопустимое значение! Вводите только цифры")
                continue
        if start_episode > finish_episode:
            print("Номер начальной серии не может быть больше номера конечной серии")
            continue
        else:
            break
    return season, start_episode, finish_episode


def write_networks(perf):
    with open("network.json", "w") as f:
        f.write("[")

        for log in perf:
            network_log = json.loads(log['message'])['message']

            if "Network.response" in network_log['method'] or "Network.request" in network_log[
'method'] or "Network.webSocket" in network_log['method']:
                f.write(json.dumps(network_log) + ",")
        f.write("{}]")


def get_mp4_url(season, episode):
    json_file_path = "network.json"

    with open(json_file_path, "r") as f:
        logs = json.loads(f.read())  # Open logs

    episode_list = []
    for log in logs:  # Iterate the logs
        try:
            episode_url = log["params"]["request"]["url"]  # URL is present inside the following keys
            # if episode_url[len(episode_url) - 23:-19] == ".mp4":  # Checks if the extension is .mp4
            if ".mp4" in episode_url:
                episode_list.append(episode_url.split(".mp4")[0]+".mp4")
        except Exception as e:
            pass

    try:
        url_list.append({"season": season, "episode": episode, "url": episode_list[-1]})
        return episode_list[-1]
    except:
        print("Возникла ошибка. Ссылка на серию не найдена!")


def download_series(title, season):
    folder_exist = check_folder_series(title, season)
    if folder_exist:
        print("Папки созданы успешно")

    for episode in url_list:
        response = requests.get(url=episode["url"], stream=True)
        with open(f"hdrezka/{title}/{season}/{episode['episode']}.mp4", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
                    print(f"Серия {episode['episode']} процессе загрузки...")
            print(f"Серия {episode['episode']} сезона {season} успешно загружена!")


def series(url, t, title):
    print("Внимание!! При ошибочном вводе сезона или серии будет загружена 1 серия 1 сезона. Вводите внимательно!")
    season, start_episode, finish_episode = get_series_number()

    for episode in range(start_episode, finish_episode+1):
        episode_url = f"{url.split('.html')[0]}.html#t:{t}-s:{season}-e:{episode}"
        try:
            driver = create_driver(10)
            print(f"Серия {episode} взята в обработку")
            driver.get(episode_url)
        except:
            pass
        finally:
            time.sleep(3)
            perf = driver.get_log('performance')
            write_networks(perf)
            print(f"Поиск ссылки на серию {episode}")
            episode_url_mp4 = get_mp4_url(season, episode)
            print("Ссылка на серию записана успешно: " + episode_url_mp4)
            driver.quit()
    else:
        os.remove("network.json")
        print("Все серии записаны, приступаем к загрузке!")
        download_series(title, season)
        print("Все серии успешно загружены! Нажмите ENTER для выхода")
        input()
