import requests
import time
from log import log
from trillworks import cookies, params, headers


# 通过jd优惠券的key参数请求得到优惠券,dict_params：将trillworks中params参数中的‘key’替换成要抢的券的key
def get_coupon(dict_params):
    r = requests.get('https://a.jd.com/indexAjax/getCoupon.html', headers=headers, params=dict_params, cookies=cookies)
    return r.text


# 解析requests后得到的response，得到其中success与message两个参数
def parsed_response(result):
    res1 = result.split('{')[1]
    res2 = res1.split('}')[0]
    res3 = res2.split(',', 2)
    r1, r2 = res3[1], res3[2]
    res_success = r1.split(':', 1)[1]
    res_message = r2.split(':', 1)[1]
    return res_success, res_message


# buy_time为购买时间，scale为购买时间前后浮动的时间（单位秒），在这个时间里间隔time.sleep设置的秒数抢券，超过时间停止
def start_get_coupon(buy_time, key, scale=5, time_sleep=0.1):
    # 根据输入的标准购买时间生成时间戳
    format_time = '%Y-%m-%d %H:%M:%S'
    buy_time_array = time.strptime(buy_time, format_time)
    buy_time_stamp = time.mktime(buy_time_array)
    # 处理trillworks中的params中的key，替换为要抢的券的key
    dict_params = dict(params)
    dict_params['key'] = key
    while True:
        # 生成实时时间的时间戳
        now_time_array = time.localtime(time.time())
        now_time_stamp = time.mktime(now_time_array)
        # 判断现在的时间是否在设置的时间范围内
        if buy_time_stamp - scale < now_time_stamp < buy_time_stamp + scale:
            r = get_coupon(dict_params)
            res_success, res_message = parsed_response(r)
            log(res_message)
            # 间隔0.1秒抢券，要想成功率变高，缩短这个时间间隔
            time.sleep(time_sleep)
            # res_status为状态码，true则为抢券成功，输出Successful，程序停止
            if res_success == 'true':
                log('Successful!')
                break
        # 超出时间范围，程序停止
        elif now_time_stamp > buy_time_stamp + scale:
            log('Failed,Time out!')
            break


# buy_time为购买时间，scale为购买时间前后浮动的时间（单位秒），time.sleep抢券的时间间隔，key为券的编码
# 每次网页版推出重新登录，Cookie里的self.cookies都需要更新
def main():
    buy_time = '2020-04-11 14:00:00'
    key = '0271DFD6890D3B60ACB8BA8A9E49BEB17FE8E6323A36834B63FE69E95D38088E8BE4DA30B82920863D9477310EE47514C84F1C772AECA156CB2BF990902C71CFDC0BC5D3945002355F655819439303BD32B3CF26502AF722BD6084C6A7A812D9'
    scale = 5
    time_sleep = 0.1
    start_get_coupon(buy_time, key, scale, time_sleep)


main()