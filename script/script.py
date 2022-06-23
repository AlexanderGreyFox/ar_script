import datetime
import pylab
import requests
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
from statistics import mean


base_url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1'

ex = {
        'usd': 'rub',
        'gel': 'rub'
      }


def api_request(date: datetime.date, first_currency: str, second_currency: str) -> float:
    url = f'{base_url}/{date}/currencies/{first_currency}/{second_currency}.json'
    resp = requests.get(url)
    return resp.json().get(second_currency)


def main():
    pdf = PdfPages("../Exchange_rate_example.pdf")
    base = datetime.datetime.date(datetime.datetime.today())
    date_list = [base - datetime.timedelta(days=x) for x in range(30)]
    ex_dict = {}

    for k, v in ex.items():
        for date in date_list:
            resp = api_request(date, k, v)
            if k in ex_dict:
                ex_dict[k].append(resp)
            else:
                ex_dict[k] = [resp]

    plt.figure(figsize=(20, 10))

    size = len(ex_dict)
    pos = 1
    for k, v in ex_dict.items():
        pylab.subplot(size, 1, pos)
        plt.title(f'{k} exchange rate')
        plt.xlabel("date")
        plt.ylabel("rub")
        plt.plot(date_list, v, label=f'min={min(v)}\nmax={max(v)}\nmean={mean(v)}')
        plt.legend()
        pos += 1

    pdf.savefig()
    plt.close()
    pdf.close()


if __name__ == '__main__':
    main()
