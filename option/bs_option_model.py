# @Time : 2020/7/30
# @Author : 大太阳小白
# @Software: PyCharm
# @blog：https://blog.csdn.net/weixin_41579863
import numpy as np
import scipy.stats as stats
from scipy.optimize import fsolve
import math


def d1(s, k, r, t, v):
    a = math.log(s / k) + (r + v * v / 2) * t
    b = v * math.sqrt(t)
    return a / b


def d2(s, k, r, t, v):
    d = d1(s, k, r, t, v)
    return d - v * math.sqrt(t)


def call_price(s, k, r, t, v, q=0):
    d1_v = d1(s, k, r, t, v)
    d2_v = d2(s, k, r, t, v)
    c = s * math.exp(-q * t) * stats.norm.cdf(d1_v) - k * math.exp(-r * t) * stats.norm.cdf(d2_v)
    return c


def put_price(s, k, r, t, v, q=0):
    d1_v = d1(s, k, r, t, v)
    d2_v = d2(s, k, r, t, v)
    p = k * np.exp(-r * t) * stats.norm.cdf(-d2_v) - s * np.exp(-q * t) * stats.norm.cdf(-d1_v)
    return p


def call_delta(s, k, r, t, v, q=0):
    d1_v = d1(s, k, r, t, v)
    return np.exp(-q*t)*stats.norm.cdf(d1_v)


def put_delta(s, k, r, t, v, q=0):
    d1_v = d1(s, k, r, t, v)
    return np.exp(-q * t) * (stats.norm.cdf(d1_v)-1)


def gamma(s, k, r, t, v, q=0):
    d1_v = d1(s, k, r, t, v)
    a = stats.norm.pdf(d1_v) * np.exp(-q*t)
    b = s * v * np.sqrt(t)
    return a/b


def vega(s, k, r, t, v, q=0):
    d1_v = d1(s, k, r, t, v)
    return s * np.sqrt(t) * stats.norm.pdf(d1_v) * np.exp(-q*t)


def call_theta(s, k, r, t, v, q=0):
    d1_v = d1(s, k, r, t, v)
    d2_v = d2(s, k, r, t, v)
    a = -s * stats.norm.pdf(d1_v) * v * np.exp(-q * t) / (2 * np.sqrt(t))
    b = q * s * stats.norm.cdf(d1_v) * np.exp(-q * t)
    c = r * k * np.exp(-r * t) * stats.norm.cdf(d2_v)
    return a + b - c


def put_theta(s, k, r, t, v, q=0):
    d1_v = d1(s, k, r, t, v)
    d2_v = d2(s, k, r, t, v)
    a = -s * stats.norm.pdf(-d1_v) * v * np.exp(-q * t) / (2 * np.sqrt(t))
    b = q * s * stats.norm.cdf(-d1_v) * np.exp(-q * t)
    c = r * k * np.exp(-r * t) * stats.norm.cdf(-d2_v)
    return a - b + c


def call_rho(s, k, r, t, v, q=0):
    d2_v = d2(s, k, r, t, v)
    return k*t*np.exp(r*t)*stats.norm.cdf(d2_v)


def put_rho(s, k, r, t, v, q=0):
    d2_v = d2(s, k, r, t, v)
    return -k*t*np.exp(r*t)*stats.norm.cdf(-d2_v)


def impv(c, s, k, r, t, cp):
    if cp == 1:
        c_func = lambda v: call_price(s, k, t, v, r) - c
    elif cp == -1:
        c_func = lambda v: put_price(s, k, t, v, r) - c
    iv_value = fsolve(c_func, 0.2)
    return iv_value


def greeks(s, k, r, t, v, cp, q=0):
    greeks_dict = {}
    if cp == 1:
        greeks_dict['price'] = call_price(s, k, r, t, v, q)
        greeks_dict['delta'] = call_delta(s, k, r, t, v, q)
        greeks_dict['theta'] = call_theta(s, k, r, t, v, q)
        greeks_dict['rho'] = call_rho(s, k, r, t, v, q)
    elif cp == -1:
        greeks_dict['price'] = put_price(s, k, r, t, v, q)
        greeks_dict['delta'] = put_delta(s, k, r, t, v, q)
        greeks_dict['theta'] = put_theta(s, k, r, t, v, q)
        greeks_dict['rho'] = put_rho(s, k, r, t, v, q)
    greeks_dict['gamma'] = gamma(s, k, r, t, v, q)
    greeks_dict['vega'] = vega(s, k, r, t, v, q)
    return greeks_dict


def price(s, k, r, t, v, cp, q=0):
    if cp == 1:
        return call_price(s, k, r, t, v, q)
    else:
        return put_price(s, k, r, t, v, q)


# if __name__ == '__main__':
#     s = 3.284
#     k = 3.2
#     t = 27 / 365
#     r = 0.02
#     v = 0.23
#     c_value = 0.09
#     g = greeks(s,k,t,v,r,1)
#     print(g)
