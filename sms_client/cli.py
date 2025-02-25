import argparse
from .client import SMSClient
from .config import Config


def main():
    parser = argparse.ArgumentParser(description="Отправка SMS через API")
    parser.add_argument("--sender", required=True, help="Номер отправителя", nargs="?")
    parser.add_argument("--recipient", required=True, help="Номер получателя", nargs="?")
    parser.add_argument("--message", required=True, help="Текст сообщения", nargs="?")
    args = parser.parse_args()

    config = Config.from_file()
    client = SMSClient(config)
    response = client.send_sms(args.sender, args.recipient, args.message)

    print(f"Код ответа: {response.status_code}")
    print(f"Тело ответа: {response.body.decode()}")


if __name__ == "__main__":
    main()
