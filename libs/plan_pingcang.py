#encoding=utf-8

import logging
import json
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='./trade.log',
                    filemode='w')

def trade(okcoin, _type, amount, current_price, orders):

    check_cancel_order(okcoin, orders)

    orders_info = okcoin.future_trade('btc_usd','quarter','',amount, _type,'1','10')
    if _type == '3':
        category = '平多'
    elif _type == '4':
        category = '平空'

    logging.info('以%s价格平%s：数量%s' % (current_price, category, amount))

# 对手价
def plan(trend, current_price, plan_price, amount, okcoin, _type, orders):

    if trend == '>=':
        if current_price >= plan_price:
            trade(okcoin, _type, amount, current_price, orders)
    elif trend == '<=':
        if current_price <= plan_price:
            trade(okcoin, _type, amount, current_price, orders)

def check_cancel_order(okcoin, orders):
    for order in orders:
        status = int(order['type'])
        order_id = order['order_id']
        # 平仓单, 如果不能及时止损，取消挂单
        if status == 3 or status == 4:
            print("cancel order: %s" % order_id)
            time.sleep(0.5)
            okcoin.future_cancel('btc_usd', 'quarter', order_id)
