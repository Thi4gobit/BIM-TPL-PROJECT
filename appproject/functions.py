from datetime import datetime

def create_code():
    t = datetime.now().strftime("%Y/%m/%d+%H:%M:%S:%f")
    t_num = t.replace("/", "").replace(":", "").replace("+", "")
    t_hex = hex(int(t_num))
    return t_hex

# print(create_code())