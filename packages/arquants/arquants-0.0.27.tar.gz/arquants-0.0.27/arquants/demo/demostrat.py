from datetime import datetime
import traceback
from arquants import Strategy, Order
import math


class DemoStrat(Strategy):

    def __init__(self, qty=10):
        print('here 0')
        self.qty = qty
        self.cum_qty = 0
        self.active_order = None

    def next(self):
        print('next')
        # test : generate an error

        try:
            self.info('Cambio de MD')

            if self.cum_qty >= self.qty and self.active_order is None:
                self.info('Fin de ejecucion')
                self.pause()
                return

            px = self.data0.offer_px[0]
            op = round(float(px), 3) if px and not math.isnan(px) else None
            self.info('op={}'.format(op))

            size = self.data0.offer_qty[0]
            os = round(float(size), 3) if size and not math.isnan(size) else None
            self.info('os={}'.format(os))

            if op is None or os is None:
                self.info('no hay book')
                return

            if not self.active_order:
                self.active_order = self.buy(data=self.data0, price=op, size=os, exectype=Order.Limit, send=False)
                self.sendOrders([self.active_order])
                self.info('Mando cantidad {} a precio {}'.format(op, os))
                self.cum_qty += os
            else:
                self.info('Tenemos una orden activa')

        except BaseException:
            self.info(traceback.format_exc())
            self.on_error()

    def notify_order(self, order):
        try:
            self.info("actualiza orden {} - status={}".format(order.m_orderId, Order.Status[order.status]))

            if order.status in (Order.Completed, Order.Rejected):
                self.active_order = None

        except BaseException:
            self.info(traceback.format_exc())
            self.on_error()

    def on_pause(self):
        self.info('on_pause')

    def info(self, message):
        # self.log('{} : {}'.format(datetime.now().time().isoformat(timespec='milliseconds'), message))
        print('{} : {}'.format(datetime.now().time().isoformat(timespec='milliseconds'), message))

    def validate(self):
        print('validate')
        try:
            num = int(self.qty)
        except Exception as e:
            self.info('Valor ilegal {} para el parametro {}'.format(self.qty, "qty"))
            self.pause()
