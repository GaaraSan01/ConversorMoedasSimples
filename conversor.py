import requests

BASE_URL_CURRENCY = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=1000&$format=json'
BASE_URL_COTATION = 'https://economia.awesomeapi.com.br/last/'

class CurrencyData:
    def __init__(self, url):
        self.url = url

    def getAll(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            if 'value' in data:
                return data['value']
            else:
                print('Não foi possivel pegar as informações!')
        else:
            print('API indisponivel no momento!' + response.status_code)


class CurrencyCotation:
    def __init__(self, currency, url):
        self.currency = currency
        self.url = url

    def currencyData(self):
        response = requests.get(f'{self.url}{self.currency}-BRL')
        if response.status_code == 200:
            data = response.json()
            if f'{self.currency}BRL' in data:
                price = data[f'{self.currency}BRL']['high']
                return price
            else:
                print('Não existe essa propriedade!')
        else:
            print('Erro ao buscar dados da API ' + str(response.status_code))
                


from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    typeCurrency = CurrencyData(BASE_URL_CURRENCY)
    currencys = typeCurrency.getAll()

    context = {
        'currency_simbol': currencys,
        'select_field': 'select_currency'
    }

    if request.method == 'POST':
        value = request.form.get('valor')
        currency_simbol = request.form.get('currency')
        if currency_simbol is not None:
            cotation = CurrencyCotation(currency_simbol, BASE_URL_COTATION)
            data = cotation.currencyData()
            result = float(value) * float(data)
            result_format = f'{value} {currency_simbol} equivale à R${result:_.2f}'
            result_format = result_format.replace('.', ',').replace('_', '.')
            return render_template('index.html', result=result_format, **context)
    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=True)