import aiohttp
import asyncio
import datetime
import pylab
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
from statistics import mean


base_url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1'


async def api_request(date: datetime.date, first_currency: str, second_currency: str) -> float:
    url = f'{base_url}/{date}/currencies/{first_currency}/{second_currency}.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
            return result.get(second_currency)


async def main():
    pdf = PdfPages("Exchange_rate.pdf")
    base = datetime.datetime.date(datetime.datetime.today())
    date_list = [base - datetime.timedelta(days=x) for x in range(30)]
    usd_list = []
    gel_list = []

    for date in date_list:
        usd_resp = await api_request(date, 'usd', 'rub')
        gel_resp = await api_request(date, 'gel', 'rub')
        usd_list.append(usd_resp)
        gel_list.append(gel_resp)

    plt.figure(figsize=(20, 10))

    pylab.subplot(2, 1, 1)
    plt.title('USD/RUB')
    plt.plot(date_list, usd_list, label=f'min={min(usd_list)}\nmax={max(usd_list)}\nmean={mean(usd_list)}')
    plt.legend()

    pylab.subplot(2, 1, 2)
    plt.title('GEL/RUB')
    plt.plot(date_list, gel_list, label=f'min={min(gel_list)}\nmax={max(gel_list)}\nmean={mean(gel_list)}')
    plt.legend()

    pdf.savefig()
    plt.close()
    pdf.close()

if __name__ == '__main__':
    asyncio.run(main())


