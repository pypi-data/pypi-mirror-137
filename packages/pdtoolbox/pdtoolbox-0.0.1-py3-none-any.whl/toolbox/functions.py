import cbpro

def min_increments(base_increase):
    if '.' not in base_increase:
        dec = ""
    else:
        dec = base_increase.split(".")[1]
    return len(dec)


def get_min_increments(exchanges):
    # get min increment information for trading sizes later

    # dictionary setup for return later
    quote_min_increments = {}
    base_min_increments = {}

    # CBPRO
    if 'cbpro' in exchanges:
        # connect to exchange and make products call
        public_client = cbpro.PublicClient()
        p_data = public_client.get_products()

        # loop through each product
        qmi = {}
        bmi = {}
        for p in p_data:
            qmi[p['id']] = min_increments(p['quote_increment'])
            bmi[p['id']] = min_increments(p['base_increment'])
        quote_min_increments['cbpro'] = qmi
        base_min_increments['cbpro'] = bmi

    # return increments
    return quote_min_increments, base_min_increments


def exchange_connections(exchanges, credentials):
    # dictionary of clients
    clients = {}

    # loop through exchange list
    for e in exchanges:
        if e == 'cbpro':
            clients[e] = cbpro.AuthenticatedClient(**credentials[e])

    return clients
