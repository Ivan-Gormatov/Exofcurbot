import json
import requests

currency = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR',
    'юань': 'CNY',
    'йена': "JPY"
}


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = currency[base.lower()]
            sym_key = currency[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта не найдена!\n {Convertor.AvailCurr()}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не верный формат количества валюты  {amount}!")

        r = requests.get(f"https://api.coingate.com/v2/rates/merchant/{base_key}/{sym_key}")
        resp = json.loads(r.content)
        resp = float(resp)
        message = f"За валюту {base} в количестве {amount}  мы получим валюту {sym} в количестве {resp * amount}"
        return message

    def AvailCurr():
        text = 'Доступные валюты:'
        for i in currency.keys():
            text = '\n'.join((text, i))
        return (text)
