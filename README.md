# Webtrh alerts

## Requirements

- [python3](https://www.python.org/) - Programming language
- [python-poetry](https://github.com/python-poetry/poetry) - Dependency Management
- [Webtrh account](https://webtrh.cz/) - The site this project is about
- [Pushbullet account](https://www.pushbullet.com/) - Alerting service

## Installation

1. Install requirements

2. Clone [this repository](https://github.com/mifka01/webtrh_alerts) with `git`

```shell
git clone https://github.com/mifka01/webtrh_alerts.git && cd webtrh_alerts
```

3. Run poetry to install all dependencies
```shell
poetry install
```
4. Create your own environment file and fill the variables inside
```shell
cp .sample_env .env
```
5. Add message which will app sent to people [message.txt](https://github.com/mifka01/webtrh_alerts/blob/master/message.txt) file

6. Run poetry shell and start the app
```shell
poetry shell
python3 app.py
```

## Usage

- Get yourself a [Pushbullet](https://www.pushbullet.com/) you can use it as mobile app, browser extension, desktop app or all of them at the same time.
- When new deal will appear notification will be sent into pushbullet chat.
- If you wanna send an email to the sender just use:
```shell
  /mail <4-digit-code>
```
You can find the 4 digit code at the end of every notification.

## Configuration
For configuration you can use [config.py](https://github.com/mifka01/webtrh_alerts/blob/master/config.py) file
- You will probably be most interested in WEBTRH_CATEGORIES
```python
# List of categories to alert from
WEBTRH_CATEGORIES = ['https://webtrh.cz/f101', 'https://webtrh.cz/f93']
```
You can simply add more categories by adding link to the list.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

