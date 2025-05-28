from new.utils import get_currency_rates


def currency_data(request):
    raw_data = get_currency_rates()
    print(">>>>> RAW DATA:", raw_data)  # bu logda ko‘rinasiz

    readable_data = {}
    for bank_key, rates in raw_data.items():
        usd_rates = [rate for rate in rates if rate.get('currency') == 'USD']
        if usd_rates:
            readable_name = bank_key.replace("_", " ").capitalize()
            readable_data[readable_name] = usd_rates

    print(">>>>> USD CURRENCY DATA:", readable_data)
    return {'currency_data': readable_data}
