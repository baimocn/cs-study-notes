xinxi = {
    "name":'baimo',
    "age":20,
    "aihao":'yumaoqiu'
}
print(xinxi["name"])
print(xinxi["age"])
print(xinxi["aihao"])
xinxi["name"]='mobai'
xinxi['aihao']='pinpong'
print(xinxi["name"])
print(xinxi["age"])
print(xinxi["aihao"])
for key,value in xinxi.items():
    print(key,":",value)