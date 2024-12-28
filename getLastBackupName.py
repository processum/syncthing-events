import json
import argparse
from datetime import datetime
from dotenv import load_dotenv, dotenv_values

load_dotenv()


EVENTS_FILE = os.getenv("OUTPUT_FILE")


def check_local_index_updated(folder_name):
    # Формируем текущую дату в нужном формате
    today_str = datetime.now().strftime('%Y_%m_%d') + ".7z"
    found_event = False

    try:
        with open(EVENTS_FILE, "r") as f:
            for line in f:
                event = json.loads(line)
                
                # Проверка на тип события LocalIndexUpdated и соответствие папки
                if event.get("type") == "LocalIndexUpdated" and event.get("data", {}).get("folder") == folder_name:
                    # Проверка списка файлов в событии на наличие файла с текущей датой
                    if today_str in event.get("data", {}).get("filenames", []):
                        # "Файл с текущей датой найден в папке {folder_name}: {today_str}"
                        print(1)
                        found_event = True
                        break

        if not found_event:
            # "Файл с текущей датой не найден в папке {folder_name} среди событий LocalIndexUpdated."
            print(0)
    except FileNotFoundError:
        # Файл событий не найден.
        print(-1)
    except json.JSONDecodeError:
        # Ошибка при разборе JSON-файла.
        print(-1)

if __name__ == "__main__":
    # Настраиваем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Поиск файла с текущей датой в событиях Syncthing.")
    parser.add_argument("folder", help="Имя папки для поиска события LocalIndexUpdated")
    args = parser.parse_args()

    # Запускаем проверку для указанной папки
    check_local_index_updated(args.folder)
