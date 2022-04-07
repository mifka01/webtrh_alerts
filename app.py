from Alert import Alert
from test_dotenv import valid_environment
from sys import exit


if __name__ == "__main__":
    print('[info] Starting webtrh alerts')
    print('[info] Testing enviroment')
    if (valid_environment()):
        print('[info] Running...')
        print('--------------------')
        Alert().run()
    exit(1)
