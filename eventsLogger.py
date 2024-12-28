import requests
import json
import time
import os

from dotenv import load_dotenv, dotenv_values

load_dotenv()

# Настройки
SYNCTHING_API_URL = os.getenv("SYNCTHING_API_URL")
SYNCTHING_API_KEY = os.getenv("SYNCTHING_API_KEY")
OUTPUT_FILE = os.getenv("OUTPUT_FILE")


headers = {"X-API-Key": SYNCTHING_API_KEY}


def fetch_events(since):
    params = {"since": since} if since else {}
    response = requests.get(SYNCTHING_API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def load_existing_events():
    # Проверяем, существует ли файл и не пустой ли он
    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
        with open(OUTPUT_FILE, "r") as f:
            events = []
            for line in f:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    print("Ошибка чтения JSON, пропускаем поврежденную строку.")
                    continue  # Пропускаем поврежденные строки
            return events
    return []


def save_events(events):
    try:
        with open(OUTPUT_FILE, "a") as f:
            for event in events:
                json.dump(event, f, ensure_ascii=False)
                f.write("\n")  # Каждый объект на новой строке
    except Exception as e:
        print(f"Ошибка при сохранении событий: {e}")


def main():
    existing_events = load_existing_events()
    last_time = (
        existing_events[-1]["time"] if existing_events else None
    )  # Последнее сохраненное время

    try:
        events = fetch_events(last_time)

        # Если last_time равен None, добавляем все события
        if last_time is None:
            new_events = events
        else:
            new_events = [
                event for event in events if event["time"] > last_time
            ]  # Фильтруем новые события

        if new_events:
            save_events(new_events)
            last_time = new_events[-1]["time"]  # Обновляем последнее время

        time.sleep(1)
    except requests.RequestException as e:
        print(f"Ошибка получения событий Syncthing: {e}")


if __name__ == "__main__":
    main()
