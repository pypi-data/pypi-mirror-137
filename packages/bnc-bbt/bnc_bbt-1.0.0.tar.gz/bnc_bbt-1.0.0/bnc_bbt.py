import requests
import random
import time
import json

nft_auction_ids = {
    '95': [26848451, 26848513, 26848560, 26848632, 26848768, 26848834, 26848910, 26848971, 26849034, 26849086],
    '190': [26849170, 26849232, 26849287, 26849353, 26849414, 26849470, 26849532, 26849640, 26850877, 26850943],
    '285': [26850992, 26851048, 26851109, 26851156, 26851206, 26851260, 26851314, 26851371, 26851433, 26851480],
    '380': [26851507, 26851654, 26851718, 26851784, 26851841, 26851885, 26851932, 26854697],
    '475': [
        26853783, 26853857, 26853919, 26853988, 26854281, 26854334, 26854418, 26854492, 26854564, 26854614, 26854854, 26854938, 26861588, 26862158, 26863733, 
        26866831, 26866888, 26866966, 26867035, 26867097
    ],
    '550': [26854789, 26855255, 26855406, 26855501, 26855586, 26855711, 26855823, 26855914, 26860299, 26860374],
    '600': [26860552, 26860665, 26860796, 26860894, 26860990, 26861092, 26861177, 26861315, 26861400, 26861502],
    '700': [26862073, 26862278, 26863391, 26863485, 26863558, 26863649, 26863837, 26863960, 26867162, 26867213],
    '800': [26865508, 26865572, 26865660, 26865715, 26865769, 26865834, 26865876, 26865921, 26865984, 26866042],
    '900': [26866101, 26866169, 26866236, 26866296, 26866434, 26866527, 26866582, 26866642, 26866685, 26866744],
}


def start_sale_box(headers):
    bpi = 'https://www.binance.com/bapi/asset/v2/private/asset-service/wallet/balance?needBalanceDetail=true'
    resp = requests.get(bpi, headers=headers).json()['data'][0]['assetBalances']
    balance = 475.0
    for r in resp:
        if r['asset'] == 'BUSD':
            balance = float(r['free'])
    while balance >= 95:
        if balance >= 95 and balance < 190:
            productId = random.choice(nft_auction_ids['95'])
            amount = '95'
        if balance >= 190 and balance < 285:
            productId = random.choice(nft_auction_ids['190'])
            amount = '190'
        if balance >= 285 and balance < 380:
            productId = random.choice(nft_auction_ids['285'])
            amount = '285'
        if balance >= 380 and balance < 475:
            productId = random.choice(nft_auction_ids['380'])
            amount = '380'
        if balance >= 475 and balance < 550:
            productId = random.choice(nft_auction_ids['475'])
            amount = '475'
        if balance >= 550 and balance < 600:
            productId = random.choice(nft_auction_ids['550'])
            amount = '550'
        if balance >= 600 and balance < 700:
            productId = random.choice(nft_auction_ids['600'])
            amount = '600'
        if balance >= 700 and balance < 800:
            productId = random.choice(nft_auction_ids['700'])
            amount = '700'
        if balance >= 800 and balance < 900:
            productId = random.choice(nft_auction_ids['800'])
            amount = '800'
        if balance >= 900:
            productId = random.choice(nft_auction_ids['900'])
            amount = '900'
        nft_auction_ids[amount].remove(productId)
        order_create_url = 'https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/order-create'
        response = requests.post(order_create_url, headers=headers, data=json.dumps({'amount': amount, 'productId': productId, 'tradeType': 0}))
        if response.status_code == 200:
            balance -= float(amount)
        else:
            balance -= 100
        time.sleep(1)
