# @Time : 2020/8/25
# @Author : 大太阳小白
# @Software: PyCharm
# @blog：https://blog.csdn.net/weixin_41579863
from core.objects import OptionData
from option import bs_option_model, crr_option_model


def calc(option: OptionData, model_type: str = 'bs') -> OptionData:
    s = option.underlying_price
    k = option.exe_price
    t = option.t
    r = option.r
    v = option.iv
    cp = option.cp
    option.calc_time_value()
    if model_type == 'bs':
        greeks = bs_option_model.greeks(s, k, r, t, v, cp)
    elif model_type == 'crr':
        greeks = crr_option_model.greeks(s, k, r, t, v, cp)
    option.set_greeks(greeks)


if __name__ == '__main__':
    option = OptionData()
    option.underlying_price = 3.3590
    option.iv = 0.2387
    option.exe_price = 3.3
    option.t = 29 / 365
    option.r = 0.02
    option.cp = 1
    option.volume = 1
    option.direction = 'long'
    calc(option)
    option.output()
    calc(option, 'crr')
    option.output()

    option = OptionData()
    option.underlying_price = 3.351
    option.iv = 0.2613
    option.exe_price = 3.3
    option.t = 28 / 365
    option.r = 0.02
    option.cp = -1
    option.volume = 1
    option.direction = 'long'
    calc(option)
    option.output()
    calc(option, 'crr')
    option.output()

