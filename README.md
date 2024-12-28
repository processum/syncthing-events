# Расширение syncthing для сбора событий для заббикса
## Зависимости

> Debian/Ubuntu
> 
> python3+
 
## Функциональность
### Сбор событий
Сбор событий клиента syncthing с сохранением в json
* Cкачать проект
* Cкопировать `.env.example` в `.env`
* Проинициализировать env переменные  в `.env`.
* Настроить ротацию логов. Пример конфга `syncthing_rotate`, обратить внимание указан дефолтный путь.
* Добавить в сron скрипт который будет забирать новые события и сохранять их.
  ```
  */10 * * * *	root	python3 /PATH_TO_SRC/eventsLogger.py
  ```
* Перезагрузить сron.
### Отображаение в заббиксе списка имен синронизированных файлов
* В файле `syncthing_zabbix.conf` отредактировать пути к скриптам `isNewBackupExist.py` и `getLastBackupName.py`
* Скопировать отредактированный `syncthing_zabbix.conf` в `/etc/zabbix/zabbix_agent2.d`
* Примеры запуска где `foldername` это имя папки которая синхранизируется:
  ```
  python3 /PATH_TO_SRC/isNewBackupExist.py foldername
  python3 /PATH_TO_SRC/getLastBackupName.py foldername
  ```
## Настро