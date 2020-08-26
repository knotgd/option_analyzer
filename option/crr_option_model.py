# @Time : 2020/8/25
# @Author : 大太阳小白
# @Software: PyCharm
# @blog：https://blog.csdn.net/weixin_41579863
import numpy as np
import math


def price(s, k, r, t, v, cp, M=100):
    dt = t / M
    df = math.exp(-r * dt)
    u = math.exp(v * math.sqrt(dt))
    d = 1 / u
    q = (math.exp(r * dt) - d) / (u - d)
    mu = np.arange(M + 1)
    mu = np.resize(mu, (M + 1, M + 1))
    md = np.transpose(mu)
    mu = u ** (mu - md)
    md = d ** md
    st = s * mu * md
    if cp == 1:
        V = np.maximum(st - k, 0)
    else:
        V = np.maximum(k - st, 0)
    z = 0
    for t in range(M - 1, -1, -1):
        V[0:M - z, t] = (q * V[0:M - z, t + 1] + (1 - q) * V[1:M - z + 1, t + 1]) * df
        z += 1
    return V, u, d


def call_price(s, k, r, t, v):
    V, _, _ = price(s, k, r, t, v, 1)
    return V[0][0]


def put_price(s, k, r, t, v):
    return price(s, k, r, t, v, -1)[0][0]


def delta(s, k, r, t, v, cp):
    V, u, d = price(s, k, r, t, v, cp)
    fu = V[0][1]
    fd = V[1][1]

    return (fu - fd) / (s * (u - d))


def gamma(s, k, r, t, v, cp):
    V, u, d = price(s, k, r, t, v, cp)
    fuu = V[0][2]
    fdd = V[2][2]
    fud = V[1][2]
    uu = u * u
    dd = d * d
    h = 0.5 * s * (uu - dd)
    value = (fuu - fud) / (s * (uu - 1)) - (fud - fdd) / (s * (1 - dd))
    return value / h


def vega(s, k, r, t, v, cp):
    e = 0.01
    f1 = price(s, k, r, t, v, cp)[0][0][0]
    t += e
    f2 = price(s, k, r, t, v, cp)[0][0][0]
    return (f2 - f1) / e


def theta(s, k, r, t, v, cp):
    V, u, d = price(s, k, r, t, v, cp)
    fu = V[0][1]
    fd = V[1][1]
    f0 = V[0][0]
    return (fu + fd - 2 * f0) / (2 * t / 100)


def rho(s, k, r, t, v, cp):
    e = 0.01
    f1 = price(s, k, r, t, v, cp)[0][0][0]
    r += e
    f2 = price(s, k, r, t, v, cp)[0][0][0]
    return (f2 - f1) / e


def greeks(s, k, r, t, v, cp):
    greeks_dict = dict()
    greeks_dict['price'] = price(s, k, r, t, v, cp)[0][0][0]
    greeks_dict['delta'] = delta(s, k, r, t, v, cp)
    greeks_dict['theta'] = theta(s, k, r, t, v, cp)
    greeks_dict['rho'] = rho(s, k, r, t, v, cp)
    greeks_dict['gamma'] = gamma(s, k, r, t, v, cp)
    greeks_dict['vega'] = vega(s, k, r, t, v, cp)
    return greeks_dict
