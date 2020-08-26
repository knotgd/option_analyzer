# @Time : 2020/8/25
# @Author : 大太阳小白
# @Software: PyCharm
# @blog：https://blog.csdn.net/weixin_41579863
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class OptionData:
    """
    期权数据对象
    """
    symbol: str = ""
    name: str = ""
    price: float = 0
    cp: int = 0
    exe_price: float = 0
    last_trade_date: str = ""
    underlying_price: float = 0
    iv: float = 0
    r: float = 0
    holding: float = 0
    delta: float = 0
    gamma: float = 0
    theta: float = 0
    vega: float = 0
    rho: float = 0
    chg: float = 0
    volume: float = 0
    underlying: str = ""
    direction: str = ""
    profit: float = 0
    time_value: float = 0
    t: float = 0

    def t(self):
        last_datetime = datetime.strptime(self.last_trade_date, "%Y-%m-%d")
        self.t = float((last_datetime-datetime.today()).days/365)
        return self.t

    def calc_time_value(self):
        time_value = 0
        if self.cp == 1:
            if self.exe_price < self.underlying_price:
                # 实值认购
                time_value = self.price - (self.underlying_price - self.exe_price)
            else:
                time_value = self.price
        elif self.cp == -1:
            if self.exe_price > self.underlying_price:
                # 实值认沽
                time_value = self.price - (self.exe_price - self.underlying_price)
            else:
                time_value = self.price
        self.time_value = time_value

    def set_greeks(self, greeks):
        self.price = abs(greeks['price']) * self.volume
        self.gamma = abs(greeks['gamma']) * self.volume
        self.delta = abs(greeks['delta']) * self.volume
        self.theta = abs(greeks['theta']) * self.volume
        self.vega = abs(greeks['vega']) * self.volume
        self.rho = abs(greeks['rho']) * self.volume
        if self.direction == 'long':
            if self.cp == 1:
                self.theta *= -1
            else:
                self.delta *= -1
                self.rho *= -1
        elif self.direction == 'short':
            if self.cp == 1:
                self.gamma *= -1
                self.delta *= -1
                self.vega *= -1
                self.rho *= -1
            else:
                self.vega *= -1
                self.gamma *= -1

    def output(self):
        json_str = json.dumps(self.__dict__,indent=4)
        print(json_str)
