import requests

url = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters'
params_realtime = {
    'key':'e70ae0cf9b665779fa97321e548151c7',
    'city':'410103', # 从城市编码里获取的a丢包code
    'extensions':'base' # 获取实时天气
}
params_estimate = {
    'key':'e70ae0cf9b665779fa97321e548151c7',
    'city':'410103',
    'extensions':'all' #获取预报天气
}

forecast_weather = requests.get(url=url,params=params_estimate) # 预报天气
real_weather = requests.get(url=url,params=params_realtime) # 实时天气

tianqi = forecast_weather.json()
#print(tianqi)
tianqi2 = real_weather.json()
#print(tianqi2)

# print(tianqi.get('forecasts'))
# province = tianqi.get('forecasts')[0].get("province") # 获取省份
#province = tianqi['forecasts'][0]["province"] # 获取省份
#city = tianqi.get('forecasts')[0].get("city") # 获取城市
adcode = tianqi.get('forecasts')[0].get("adcode") # 获取城市编码
#reporttime = tianqi.get('forecasts')[0].get("reporttime") # 获取发布数据时间
date = tianqi.get('forecasts')[0].get("casts")[0].get('date') # 获取日期
week = tianqi.get('forecasts')[0].get("casts")[0].get('week') # 获取星期几
dayweather = tianqi.get('forecasts')[0].get("casts")[0].get('dayweather') # 白天天气现象
#nightweather = tianqi.get('forecasts')[0].get("casts")[0].get('nightweather') # 晚上天气现象
daytemp = tianqi.get('forecasts')[0].get("casts")[0].get('daytemp') # 白天温度
nighttemp = tianqi.get('forecasts')[0].get("casts")[0].get('nighttemp') # 晚上温度
daywind = tianqi.get('forecasts')[0].get("casts")[0].get('daywind') # 	白天风向
#nightwind = tianqi.get('forecasts')[0].get("casts")[0].get('nightwind') # 晚上风向
daypower = tianqi.get('forecasts')[0].get("casts")[0].get('daypower') # 白天风力
#nightpower = tianqi.get('forecasts')[0].get("casts")[0].get('nightpower') # 晚上风力