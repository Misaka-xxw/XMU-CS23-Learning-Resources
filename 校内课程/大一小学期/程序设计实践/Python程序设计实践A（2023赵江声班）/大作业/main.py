import time, network, urequests, ujson
import ssd1306  # 屏幕
from machine import Pin, PWM, SoftI2C, RTC, Timer
from random import randint, random  # 随机数


# ==================================================================================
# 37120222203439 王柳依
# 基于esp32的大学生多功能随身小助手
# ==================================================================================
def power_supply_init():  # VCC替代引脚定义
    pin42 = Pin(42, Pin.OUT)
    pin42.value(1)
    pin40 = Pin(42, Pin.OUT)
    pin40.value(1)


def homepage_init():  # 主页
    global mode
    show_homepage()
    key = 0
    key_return_list = [9, 10, 11, 5, 6, 7, 1, 2, 3]
    num_list = [i for i in range(1, 10)]
    key_num = dict(zip(key_return_list, num_list))
    while True:
        key = key_press()
        alarm_knock()
        if key in key_return_list:
            mode = key_num[key]
            return


# 屏幕类
def OLED_init():  # OLED屏幕的初始化
    global oled
    i2c = SoftI2C(scl=Pin(11), sda=Pin(12))  # 创建i2c对象,时钟->Pin11，数据->Pin12
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # 创建oled屏幕对象,设置宽度、高度、I2C通信
    oled.fill(0)
    oled.text('Hello,WLY!', 0, 0)
    oled.line(0, 20, 128, 20, 2)
    oled.text('Nice to see you', 0, 30)
    oled.show()
    time.sleep(1)


def show_homepage():  # 主页展示
    oled.fill(0)
    for i in range(1, 3):
        oled.line(42 * i, 0, 42 * i, 64, 1)
        oled.line(0, 21 * i, 128, 21 * i, 1)
    sentences = ('Time', 'Weather', 'Alarm', 'calculator', 'Note', 'Snake', '2048(1<<n', ' ', 'Music')
    for i in range(3):
        for j in range(3):
            str_len = len(sentences[i * 3 + j])
            oled.text(str(i * 3 + j + 1), j * 42 + 2, (2 - i) * 21 + 2)
            oled.text(sentences[i * 3 + j][0:4], j * 42 + 10, (2 - i) * 21 + 2)
            if str_len > 4:
                oled.text(sentences[i * 3 + j][4:str_len], j * 42 + 2, (2 - i) * 21 + 10)

    oled.show()


def show_time():  # 屏幕显示时间,(2023, 7, 25, 2, 8, 0, 0)
    _time = rtc.datetime()
    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    oled.fill(0)
    oled.text('{:d}-{:d}-{:d}'.format(_time[0], _time[1], _time[2]), 2, 2)
    oled.text(weekday[_time[3]], 2, 12)
    oled.text('{:02d}:{:02d}:{:02d}'.format(_time[4], _time[5], _time[6]), 2, 22, 3)
    oled.show()


def show_weather(location, weather, temperature, last_update):  # 屏幕显示天气
    if location:
        last_update = last_update[0:10] + last_update[11:]
        oled.fill(0)
        oled.text(location, 0, 0)
        oled.text(weather, 0, 12)
        oled.text('{}degree'.format(temperature), 0, 24)
        oled.text(last_update, 0, 36)
        oled.show()


def draw_sth_not_show(pen: tuple or list, black=1):  # 画一个东西，留在缓冲区
    for dot in pen:
        oled.pixel(dot[0], dot[1], black)


def draw_sth_and_show(pen: tuple or list, black=1):  # 画一个东西，屏幕展示
    draw_sth_not_show(pen, black)
    oled.show()


# 蜂鸣器/喇叭
def music_init():  # 蜂鸣器初始化
    global music, my_melody, my_delay, note2fre
    music = PWM(Pin(41, Pin.OUT))
    note2fre = (262, 294, 330, 349, 370, 392, 440, 494, 523, 587, 659, 698, 784, 880, 988)
    my_melody = [6, 7, 8, 7, 5, 6, 0, 6, 7, 8, 7, 5, 6, 6, 7, 8, 7, 6, 5, 7, 8, 6, 0, 6, 7, 8, 9, 10, 6, 10, 9, 8, 7, 7,
                 13, 10]
    my_delay = [1.5, 0.5, 1, 1, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 1, 1.5, 0.5, 1, 1, 1, 1, 0.5, 0.5, 2, 1, 0.5, 0.5, 0.5, 0.5,
                1, 1.5, 0.5, 0.5, 0.5, 1, 1, 1, 3]
    for i in range(len(my_delay)):
        my_delay[i] *= 500


def play1note(note, delay_time):  # 一次演奏
    if note:
        music.duty(512)
        music.freq(note2fre[note])
    else:
        music.duty(0)
    time.sleep_ms(int(delay_time))


def play1song(melody, delay_list):  # 根据列表演奏一首曲子
    global mode
    home_key = Pin(13, Pin.IN)
    if len(melody) <= len(delay_list):
        for i, note in enumerate(melody):
            print(note)
            if home_key.value() == 0:
                time.sleep_ms(10)
                if home_key.value() == 0:
                    mode = 0
                    music.deinit()  # 释放pwm
                    return
            play1note(note, delay_list[i])
            play1note(0, 10)


# wifi
def wifi_init():  # wifi初始化定义
    global wifi
    wifi = network.WLAN(network.STA_IF)  # 配置wifi的STA


def wifi_connect():  # wifi连接
    global mode
    home_key = Pin(13, Pin.IN)
    if home_key.value() == 0:  # 中断，回到主页
        mode = 0
        return homepage_init()
    oled.fill(0)
    if not wifi.isconnected():
        oled.text('wifi connecting', 0, 2)
        oled.show()
        print('wifi连接中')
        wifi.active(True)
        try:
            wifi.connect('wly', 'ababwdrd')  # 账号, 密码
        except Exception as e:
            print(str(e))
            oled.text('wifi isnot open', 0, 10)
            oled.text('Press the key to return', 0, 18)
            oled.show()
            if home_key.value() == 0:
                mode = 0
                return
        count = 0
        while not wifi.isconnected():
            if home_key.value() == 0:
                mode = 0
                return
            count += 1
            print(count)
            time.sleep(1)
            if count > 8:
                print('wifi取消连接')
                oled.fill(0)
                oled.text('Wifi connect FAILED')
                oled.show()
                wifi.active(False)
                return
    if wifi.isconnected():
        wifi_connected = True
        print('wifi已连接')
        oled.text('successed!', 0, 20)
        oled.show()
        print('network config:', wifi.ifconfig())  # wifi信息


# 时间
def time_init():  # rtc实类时钟的定义
    global rtc
    rtc = RTC()
    rtc.init((2023, 7, 25, 2, 8, 0, 0, 0))


def time_mode():  # 展示时间
    global mode
    while mode:
        key = 0
        while not key:
            show_time()
            alarm_knock()
            key = snake_key_press()
        if key == 17:
            mode = 0
            return
        elif key == 5:
            while not wifi.isconnected() and mode:
                wifi_connect()
            if mode:
                get_time()
        else:
            return time_mode()


def get_time():  # 更新网络时间
    try:
        result_time = urequests.get(r'https://worldtimeapi.org/api/timezone/Asia/Shanghai')
        apart = ujson.loads(result_time.text)
        time_str = str(apart["datetime"])
        year = int(time_str[0:4])
        month = int(time_str[5:7])
        day = int(time_str[8:10])
        weekday = int(apart["day_of_week"])  # 修改此行
        hour = int(time_str[11:13])
        minute = int(time_str[14:16])
        second = int(time_str[17:19])
        rtc.init((year, month, day, weekday, hour, minute, second, 0))
    except Exception as e:
        print('获取时间失败：', str(e))


# 天气
def get_weather():  # 获取网络天气
    global mode
    home_key = Pin(13, Pin.IN)
    while not wifi.isconnected() and mode:
        wifi_connect()
    if mode:
        try:
            result_weather = urequests.get(
                r'https://api.seniverse.com/v3/weather/now.json?key=S-m7v2UufcofjAwGE&location=xiamen&language=en&unit=c')  # 心知天气的api接口，爬取厦门市天气
            apart = ujson.loads(result_weather.text)
            location = apart['results'][0]['location']['name']
            weather = apart['results'][0]['now']['text']
            temperature = apart['results'][0]['now']['temperature']
            last_update = apart['results'][0]['last_update']
            print(location, weather, temperature, last_update)
            show_weather(location, weather, temperature, last_update)
        except Exception as e:  # 获取错误
            print('获取天气失败：', str(e))
    while home_key.value():
        time.sleep_ms(30)
    mode = 0
    return


def key_press():  # 一次按键获取
    global mode
    key_row = [Pin(1, Pin.OUT), Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)]
    key_col = [Pin(6, Pin.IN), Pin(7, Pin.IN), Pin(8, Pin.IN), Pin(9, Pin.IN)]
    key2 = [Pin(13, Pin.IN), Pin(14, Pin.IN), Pin(15, Pin.IN), Pin(16, Pin.IN)]
    for i, col in enumerate(key2):
        if col.value() == 0:
            time.sleep_ms(30)  # 按键消抖
            if col.value() == 0:
                print(i + 17)
                return i + 17
    for i, row in enumerate(key_row):  # 轮流供电，行列读取
        for t in key_row:
            t.value(0)
        row.value(1)
        time.sleep_ms(10)
        for j, col in enumerate(key_col):
            if col.value() == 1:
                time.sleep_ms(50)  # 按键消抖
                if col.value() == 1:
                    time.sleep_ms(30)
                    print(i * 4 + j + 1)
                    return i * 4 + j + 1
    return 0  # 没有按键


# 计算
def calculate_input():  # 数字的输入
    global mode
    oled.fill(0)
    # oled.text("888888888888888888",0,0) # oled屏测试
    oled.show()
    num = []
    x, y = 0, 0
    key_num_list = ('0', '7', '8', '9', '+', '4', '5', '6', '-', '1', '2', '3', '*', '(', '0', ')', '/', 'home', '.',
                    '<-', '=')
    while mode:
        temp = 0
        while not temp:
            temp = key_press()
        if temp == 19:  # <-
            if len(num):
                if x == 0:
                    x = 120
                    y -= 8
                else:
                    x -= 8
                oled.fill_rect(x, y, 8, 8, 0)
                num.pop()
                oled.show()
        elif temp == 17:  # homepage
            mode = 0
            break
        elif temp == 20:  # =
            print('=', end='')
            oled.text('=', x, y)
            oled.show()
            try:
                calculate_result(''.join(num), 0, y + 10)
            except Exception as e:
                print(e)
            while not temp:
                temp = key_press()
        else:
            print(key_num_list[temp], end='')
            num.append(key_num_list[temp])
            oled.text(key_num_list[temp], x, y)
            oled.show()
            if x > 120:
                x = 0
                y += 8
            else:
                x += 8


def calculate_result(sentence, x, y):
    try:
        result = eval(sentence)
        print(result)
        oled.text(str(result), x, y)
    except Exception as e:
        print("输入错误:", e)
        e = str(e)
        oled.text(e, x, y)
    oled.show()
    temp = 0
    time.sleep(1)
    while not temp:
        temp = key_press()
    if temp != 17:  # not homepage
        calculate_input()


def snake_key_press():  # 贪吃蛇的按键输入
    global mode
    snake_row = [Pin(1, Pin.OUT), Pin(2, Pin.OUT), Pin(4, Pin.OUT)]
    snake_col = [Pin(6, Pin.IN), Pin(7, Pin.IN), Pin(8, Pin.IN)]
    home_key = Pin(13, Pin.IN)
    if home_key.value() == 0:
        time.sleep_ms(20)  # 按键消抖
        if home_key.value() == 0:
            mode = 0
            print(17)
            return 17  # 返回主页
    for i, row in enumerate(snake_row):
        for t in snake_row:
            t.value(0)
        row.value(1)
        time.sleep_ms(10)
        for j, col in enumerate(snake_col):
            if col.value() == 1:
                time.sleep_ms(30)  # 按键消抖
                if col.value() == 1:
                    time.sleep_ms((2 - i) * 10)
                    print(i * 3 + j + 1)
                    return i * 3 + j + 1
    time.sleep_ms(30)
    return 0  # 没有按键


def snake_init():
    oled.fill(0)
    oled.text('Press any key', 0, 25)
    oled.text('to start', 0, 33)
    oled.show()
    print('wait for game')
    while not snake_key_press():
        pass
    snake_game()


def snake_draw(x: int, y: int, black_or_white=1):  # 画蛇的一个像素
    pen = ((x * 2, y * 2),
           (x * 2, y * 2 + 1),
           (x * 2 + 1, y * 2),
           (x * 2 + 1, y * 2 + 1))
    draw_sth_not_show(pen, black_or_white)


def snake_obstacle_draw(x: int, y: int, black_or_white=1):  # 画一个障碍物
    pen = ((x * 2, y * 2), (x * 2 - 1, y * 2 - 1),
           (x * 2 - 1, y * 2 + 1),
           (x * 2 + 1, y * 2 - 1),
           (x * 2 + 1, y * 2 + 1),
           (x * 2 - 2, y * 2 - 2),
           (x * 2 - 2, y * 2 + 2),
           (x * 2 + 2, y * 2 - 2),
           (x * 2 + 2, y * 2 + 2))
    draw_sth_not_show(pen, black_or_white)


def snake_game():  # 贪吃蛇的运行函数
    oled.fill(0)
    snake_width = 32
    snake_height = 32
    score = 0
    maxscore0 = 0
    maxscore = 0
    with open('maxscore.txt', 'r') as f:
        maxscore0 = maxscore = int(f.read())
    oled.line(64, 0, 64, 64, 2)
    # 坐标：(j,i) snake_state(j,i) snake_list[i][j]
    snake_state = [(snake_width // 2, snake_height // 2 + 2), (snake_width // 2, snake_height // 2 + 1),
                   (snake_width // 2, snake_height // 2), (snake_width // 2, snake_height // 2 - 1)]  # 蛇身坐标
    snake_list = [[0 for j in range(snake_width)] for i in range(snake_height)]  # 棋盘状态
    for i in snake_state:
        snake_list[i[1]][i[0]] = 1
        snake_draw(i[0], i[1])

    x, y = snake_state[0][0], snake_state[0][1]  # 第几列，第几排
    food = None
    obstacle = None
    # 0 左上 上 右上 左 停 右 左下 下 右下
    dx = (0, -1, 0, 1, -1, 0, 1, -1, 0, 1)
    dy = (0, -1, -1, -1, 0, 0, 0, 1, 1, 1)
    direction = 7  # 下
    oled.text('SCORE:', 70, 18)
    oled.text(str(score), 70, 26)
    oled.text('MAXSCORE:', 70, 36)
    oled.text(str(maxscore), 70, 44)
    end_game = False
    change_food = True
    while not end_game:
        if obstacle != None:
            snake_list[obstacle[1]][obstacle[0]] = 3
            snake_obstacle_draw(obstacle[0], obstacle[1])
        while change_food:  # 换食物
            food = [randint(3, snake_width - 4), randint(3, snake_height - 4)]  # 列号，排号
            if snake_list[food[1]][food[0]] == 0:
                snake_list[food[1]][food[0]] = 2
                snake_draw(food[0], food[1])
                change_food = False
                if random() < 0.4:  # 加减障碍物
                    if obstacle == None:
                        obstacle = [randint(0, snake_width - 1), randint(0, snake_height - 1)]  # 列号，排号
                        while snake_list[obstacle[1]][obstacle[0]] != 0:
                            obstacle = [randint(0, snake_width - 1), randint(0, snake_height - 1)]  # 列号，排号
                        snake_list[obstacle[1]][obstacle[0]] = 3
                        snake_obstacle_draw(obstacle[0], obstacle[1], 1)
                    else:
                        snake_list[obstacle[1]][obstacle[0]] = 0
                        snake_obstacle_draw(obstacle[0], obstacle[1], 0)
                        obstacle = None
        oled.show()
        key = snake_key_press()
        if key == 17:
            end_game = True
        else:
            if key and not (key == 2 and direction == 8) and key != 5:  # 弥补矩阵键盘硬件识别总是输错
                direction = key
            x, y = snake_state[0][0] + dx[direction], snake_state[0][1] + dy[direction]
            if x < 0:
                x = snake_width - 1
            elif x >= snake_width:
                x = 0
            if y < 0:
                y = snake_height - 1
            elif y >= snake_height:
                y = 0
            if snake_list[y][x] == 0:  # 空地
                snake_draw(snake_state[-1][0], snake_state[-1][1], 0)
                snake_draw(x, y, 1)
                snake_list[y][x] = 1
                snake_list[snake_state[-1][1]][snake_state[-1][0]] = 0
                snake_state.pop()
                snake_state.insert(0, (x, y))
            elif snake_list[y][x] == 1 or snake_list[y][x] == 3:  # 碰到蛇身或者障碍物，游戏结束
                end_game = True
                print('end game')
                # print(snake_list)
                oled.text('GAME OVER', 70, 1)
                oled.show()
                if maxscore > maxscore0:
                    with open('maxscore.txt', 'w') as f:
                        f.write(str(maxscore))
                time.sleep(3)
                snake_init()
            elif snake_list[y][x] == 2:  # 碰到食物，加分
                oled.text(str(score), 70, 26, 0)
                score += 1
                oled.text(str(score), 70, 26)
                if score > maxscore:
                    oled.text(str(maxscore), 70, 44, 0)
                    maxscore = score
                    oled.text(str(maxscore), 70, 44)
                snake_state.insert(0, (x, y))
                snake_list[y][x] = 1
                change_food = True


def game2048_init():  # 2048初始化
    global board, oled
    board = [[0 for i in range(0, 4)] for j in range(0, 4)]  # 创建数字列表，每一块24*16，每一分割线宽度为1
    oled.fill(0)
    oled.show()
    for i in range(randint(1, 2)):
        game2048_new_block()
    oled.text('NOW:', 98, 18)
    oled.text('MAX:', 98, 36)

    game2048_start()


def game2048_start():  # 2048运行函数
    global board, mode
    end_game = False
    score0 = score = 0
    with open('maxscore2048.txt', 'r') as f:  # 读取最高分
        maxscore = int(f.read())
        oled.text(str(maxscore), 98, 44)
    while not end_game:
        oled.text(str(score0), 98, 26, 0)
        oled.text(str(score), 98, 26)
        score0 = score
        game2048_new_block()
        if game2048_isFailed():
            end_game = True
            if score > maxscore:
                oled.text(str('New'), 98, 44)
                oled.text(str('Rec'), 98, 51)
                oled.text(str('ord'), 98, 58)
                oled.show()
                with open('maxscore2048.txt', 'w') as f:  # 记录最高分
                    f.write(str(score))
            game2048_showFailed()
            key = 0
            while not key:
                key = snake_key_press()
            if key == 17:
                mode = 0
                break
            else:
                game2048_init()
        elif game2048_isSuccessed():
            end_game = True
            if score > maxscore:
                oled.text(str('New'), 98, 44)
                oled.text(str('Rec'), 98, 51)
                oled.text(str('ord'), 98, 58)
                oled.show()
                with open('maxscore2048.txt', 'w') as f:  # 记录最高分
                    f.write(str(score))
            game2048_showSuccessed()
            while not key:
                key = snake_key_press()
            if key == 17:
                mode = 0
                break
            else:
                game2048_init()
        key = 0
        while key != 2 and key != 4 and key != 6 and key != 8 and key != 17 or key != 17 and not game2048_can_move(key):
            key = snake_key_press()
        if key != 17:
            score += game2048_change(key)
        else:
            end_game = True


def game2048_draw_new_block(x: int, y: int, n: int):  # 新方块出现动画
    n = str(n)
    x = x * 24 + 7
    y = y * 16 + 7
    w = 10
    h = 2
    for t in range(7):
        oled.rect(x, y, w, h, 0)
        x -= 1
        y -= 1
        w += 2
        h += 2
        oled.rect(x, y, w, h, 1)
        oled.show()
        # time.sleep_ms(1)
    oled.text(str(n), x + 4, y + 4)
    oled.show()


def game2048_draw_move_block(move_block):  # 移动方块的动画：move_back:由元组(x0,y0,x1,y1,n,final_change:bool)组成的列表
    d = []
    for i in move_block:
        d.append(((i[2] - i[0]) * 3, (i[3] - i[1]) * 2))
    for t in range(8):
        for i, change in enumerate(d):
            oled.rect(move_block[i][0] * 24 + t * change[0], move_block[i][1] * 16 + t * change[1], 24, 16, 0)
            oled.text(str(move_block[i][4]), move_block[i][0] * 24 + 4 + t * change[0],
                      move_block[i][1] * 16 + 4 + t * change[1], 0)
            oled.rect(move_block[i][0] * 24 + (t + 1) * change[0], move_block[i][1] * 16 + (t + 1) * change[1], 24, 16,
                      1)
            oled.text(str(move_block[i][4]), move_block[i][0] * 24 + 4 + (t + 1) * change[0],
                      move_block[i][1] * 16 + 4 + (t + 1) * change[1], 1)
        oled.show()
    for change in move_block:
        if change[5]:
            oled.text(str(change[4]), change[2] * 24 + 4, change[3] * 16 + 4, 0)
            oled.text(str(change[4] + 1), change[2] * 24 + 4, change[3] * 16 + 4, 1)
    oled.show()


def game2048_new_block():  # 新方块随机生成
    new_block = (randint(0, 3), randint(0, 3))  # (x.y)
    while board[new_block[1]][new_block[0]]:
        new_block = (randint(0, 3), randint(0, 3))  # (x.y)
    if random() < 0.8:
        board[new_block[1]][new_block[0]] = 1
    else:
        if random() < 0.8:
            board[new_block[1]][new_block[0]] = 2
        else:
            board[new_block[1]][new_block[0]] = 3
    game2048_draw_new_block(new_block[0], new_block[1], board[new_block[1]][new_block[0]])


def game2048_change(key: int) -> int:  # 根据按键移动和加分
    add_score = 0
    direction = {2: (0, 1, 0, 4), 8: (0, -1, 3, -1), 4: (1, 0, 0, 4),
                 6: (-1, 0, 3, -1)}  # 上下左右,（0横坐标移动，1纵坐标移动，2开始搜索，3结束搜索）
    move = direction[key]
    search = direction[10 - key]
    move_block = []
    can_add = [[True for i in range(0, 4)] for j in range(0, 4)]  # 没有被加过
    if move[1]:  # 上下
        for j in range(4):  # 逐列搜索
            for i in range(move[2] + move[1], move[3], move[1]):
                move_to = move[2]
                moved = False
                if board[i][j]:
                    # 查找前面是否有可合并的方块,目标是i0
                    for i0 in range(i + search[1], search[3], search[1]):
                        if board[i0][j]:  # 找到相邻的数
                            move_to = i0 + move[1]
                            if board[i][j] == board[i0][j] and can_add[i0][j]:
                                add_score += (board[i][j] + 1)
                                move_block.append((j, i, j, i0, board[i][j], True))
                                board[i0][j] += 1
                                board[i][j] = 0
                                can_add[i0][j] = False
                                moved = True
                            break
                        else:
                            move_to = i0
                    # 前面有空
                    if board[i][j] - board[move_to][j] != 0 and not moved:
                        move_block.append((j, i, j, move_to, board[i][j], False))
                        board[move_to][j] = board[i][j]
                        board[i][j] = 0
    elif move[0]:  # 左右
        for i in range(4):  # 逐行搜索
            for j in range(move[2] + move[0], move[3], move[0]):
                move_to = move[2]
                moved = False
                if board[i][j]:
                    # 查找前面是否有可合并的方块,目标是j0
                    for j0 in range(j + search[0], search[3], search[0]):
                        if board[i][j0]:  # 找到相邻的数
                            move_to = j0 + move[0]
                            if board[i][j] == board[i][j0] and can_add[i][j0]:
                                add_score += (board[i][j] + 1)
                                move_block.append((j, i, j0, i, board[i][j], True))
                                board[i][j0] += 1
                                board[i][j] = 0
                                can_add[i][j0] = False
                                moved = True
                            break
                        else:
                            move_to = j0
                    # 前面有空
                    if board[i][j] - board[i][move_to] != 0 and not moved:
                        move_block.append((j, i, move_to, i, board[i][j], False))
                        board[i][move_to] = board[i][j]
                        board[i][j] = 0
    game2048_draw_move_block(move_block)
    return add_score  # 返回增加的分数


def game2048_can_move(key: int):  # 判断是否能按照某个方向移动
    global board
    direction = {2: (0, -1, 1, 4, 0, 4), 8: (0, 1, 0, 3, 0, 4), 4: (-1, 0, 0, 4, 1, 4),
                 6: (1, 0, 0, 4, 0, 3)}  # 上下左右,（0横坐标移动，1纵坐标移动，2行开始，3，行结束，4列开始，5列结束）
    move = direction[key]
    for i in range(move[2], move[3]):
        for j in range(move[4], move[5]):
            if board[i][j]:
                if board[i + move[1]][j + move[0]] == 0:
                    return True
                if board[i][j] == board[i + move[1]][j + move[0]]:
                    return True
    return False


def game2048_isFailed():  # 判断2048是否失败
    global board
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
    for i in range(1, 4):
        for j in range(0, 4):
            if board[i - 1][j] == board[i][j]:
                return False
    for i in range(0, 4):
        for j in range(1, 4):
            if board[i][j - 1] == board[i][j]:
                return False
    return True


def game2048_isSuccessed():  # 判断2048是否成功
    global board
    for i in range(4):
        for j in range(4):
            if board[i][j] == 11:  # 1<<11=2048
                return True
    return False


def game2048_showFailed():  # 2048展示失败文字
    oled.text('Failed', 98, 1)
    oled.show()


def game2048_showSuccessed():  # 2048展示成功文字
    oled.text('Win!', 98, 1)
    oled.show()


def note_show():  # 展示笔记
    global mode
    home_key = Pin(13, Pin.IN)
    change_key = Pin(16, Pin.IN)
    sentences = None
    with open('note.txt', 'r') as f:
        sentences = f.read()
    oled.fill(0)
    len_s = len(sentences)
    for i in range(len_s // 16 + 1):
        if i and i % 8 == 0:  # 换页
            while change_key.value():  # 翻页
                pass
            oled.fill(0)
        oled.text(sentences[i * 16:], 0, i % 8 * 8)
        oled.show()
    while home_key.value():
        pass
    mode = 0


def alarm_init():  # 闹钟初始化
    global alarm_list
    alarm_list = []  # (hour,minute)


def alarm_set():  # 闹钟设置
    global mode, alarm_list
    n = -1
    num = 0
    key_num_list = {1: 7, 2: 8, 3: 9, 5: 4, 6: 5, 7: 6, 9: 1, 10: 2, 11: 3, 14: 0}

    def location_x(i: int) -> int:  # 屏幕对应展示位置：x
        return (i & 1) * 64

    def location_y(i: int) -> int:  # 屏幕对应展示位置：y
        return 8 + i // 2 * 8

    def alarm_show():  # 展示画面
        nonlocal n, num
        oled.fill(0)
        oled.text('Set alarm', 0, 0)
        for i, alarm in enumerate(alarm_list):
            oled.text('{:02d}:{:02d}'.format(alarm[0], alarm[1]), location_x(i), location_y(i))
        if n >= 0:
            x = location_x(n) + (num + num // 2) * 8
            y = location_y(n)
            oled.fill_rect(x, y, 8, 8, 1)
            if num == 0:
                oled.text(str(alarm_list[n][0] // 10), x, y, 0)
            elif num == 1:
                oled.text(str(alarm_list[n][0] % 10), x, y, 0)
            elif num == 2:
                oled.text(str(alarm_list[n][1] // 10), x, y, 0)
            elif num == 3:
                oled.text(str(alarm_list[n][1] % 10), x, y, 0)
        oled.show()
        return

    alarm_show()
    while mode:
        key = key_press()
        if key == 4:  # +增加一个闹钟
            alarm_list.append([0, 0])
            n += 1
            alarm_show()
        elif key == 8:  # -减掉一个闹钟
            if n != -1:
                alarm_list.pop(n)
                n -= 1
                alarm_show()
        elif key == 17:  # homepage
            mode = 0
            return
        elif key == 13:  # 上一个
            if n >= 1:
                n -= 1
                alarm_show()
        elif key == 15:  # 下一个
            if n < len(alarm_list) - 1:
                n += 1
                alarm_show()
        elif key in key_num_list.keys():  # 设置闹钟的具体数字
            key_num = key_num_list[key]
            if n >= 0 and n < len(alarm_list):
                if num == 0:
                    if key_num > 2:
                        key_num = 2
                    alarm_list[n][0] = alarm_list[n][0] - alarm_list[n][0] // 10 * 10 + key_num * 10
                elif num == 1:
                    alarm_list[n][0] = alarm_list[n][0] - alarm_list[n][0] % 10 + key_num
                elif num == 2:
                    if key_num > 5:
                        key_num = 5
                    alarm_list[n][1] = alarm_list[n][1] - alarm_list[n][1] // 10 * 10 + key_num * 10
                elif num == 3:
                    alarm_list[n][1] = alarm_list[n][1] - alarm_list[n][1] % 10 + key_num
            num = (num + 1) % 4  # 切换变化的位数
            alarm_show()


def alarm_knock():  # 闹钟响铃
    global mode
    _time = rtc.datetime()  # 时间格式,(2023, 7, 25, 2, 8, 0, 0)
    knock = False
    for i in alarm_list:
        if i[0] == _time[4] and i[1] == _time[5] and _time[6] < 5:
            knock = True
            break
    if knock:
        oled.fill(0)
        oled.text('GET UP!', 1, 2)
        oled.text('{:02d}:{:02d}'.format(_time[4], _time[5]), 5, 12)
        oled.show()
        mode = 9
        while mode:
            music_init()
            play1song(my_melody, my_delay)
        return homepage_init()


# ====================================== * main * ============================================
mode = 0
power_supply_init()
OLED_init()
time_init()
wifi_init()
alarm_init()
while True:
    print('mode', mode)
    if mode == 0:
        homepage_init()
    elif mode == 1:
        time_mode()
    elif mode == 2:
        get_weather()
    elif mode == 3:
        alarm_set()
    elif mode == 4:
        calculate_input()
    elif mode == 5:
        note_show()
    elif mode == 6:
        snake_init()
    elif mode == 7:
        game2048_init()
    elif mode == 8:
        mode = 0
    elif mode == 9:
        music_init()
        play1song(my_melody, my_delay)
