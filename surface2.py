# -*- coding: utf-8 -*-

import random
import time
from turtledemo import clock

import pygame
pygame.init()

# 初始化音乐和音效
pygame.mixer.init()  # 初始化混音器

# 设置未按按钮前的背景音乐
pygame.mixer.music.load(r'D:\Python\打飞机\music\起床了.mp3')  # 加载背景音乐
pygame.mixer.music.set_volume(0.5)  # 设置背景音乐音量

# 新增运行中的游戏音乐
running_music = pygame.mixer.Sound(r'D:\Python\打飞机\music\haha.mp3')  # 加载运行中游戏音乐
running_music.set_volume(0.1)  # 设置运行中音乐音量

# 加载音效
crash_sound = pygame.mixer.Sound(r'D:\Python\打飞机\music\及.mp3')  # 加载碰撞音效
crash_sound.set_volume(0.7)  # 设置碰撞音效音量

disp_width=800
disp_height=600

gameDim=pygame.display.set_mode((disp_width,disp_height))#创建一个窗口

pygame.display.set_caption("Jerk off")#标题

black=(200,1,0)
white=(253,253,253)
red=(0,0,0)
green=(0,200,0)
blue=(0,0,200)

block_color=(53,115,0)

car_width=73

gameDim.fill(black)#标题填充颜色
gameDim.fill(white)

# 添加图标
icon = pygame.image.load(r'D:\Python\打飞机\image\laikun.jpg')
pygame.display.set_icon(icon)

clock=pygame.time.Clock()#刷新屏幕
crashed=False
carImg=pygame.image.load(r'D:\Python\打飞机\image\fei.png')
carImg=pygame.transform.scale(carImg,(73,90))#缩放图片

# 新增小形状图相关变量
bullet_img = pygame.image.load(r'D:\Python\打飞机\image\zidan.png')  # 加载小形状图
bullet_img = pygame.transform.scale(bullet_img, (20, 20))  # 缩放小形状图
# bullet_img = pygame.transform.rotate(bullet_img, 90)  # 逆时针旋转 90 度
bullets = []  # 存储所有子弹
last_bullet_time = 0  # 上一次发射子弹的时间戳

# 加载指定的图形图片
thingImg = pygame.image.load(r'D:\Python\打飞机\image\cai.png')
thingImg = pygame.transform.scale(thingImg, (100, 100))  # 缩放图片

# 文本显示避开多少对象
def things_dodged(count):
    font=pygame.font.SysFont(None,25)
    text=font.render("Dodged:"+str(count),True,black)
    gameDim.blit(text,(0,0))

# 绘制指定图片
def things(thingx,thingy):
    gameDim.blit(thingImg, (thingx, thingy))

def car(x,y):
    gameDim.blit(carImg,(x,y))

def text_object(text,font):
    textSurface=font.render(text,True,black)
    return textSurface,textSurface.get_rect()

def message_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)
    TextSurf,TextRect=text_object(text,largeText)
    TextRect.center = ((disp_width / 2), (disp_height / 2))
    gameDim.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)#结束后等待2秒
    game_loop()



def crash():
    global dodged, crash_count, life_count  # 声明 dodged, crash_count 和 life_count 为全局变量
    pygame.mixer.music.stop()  # 停止背景音乐
    running_music.stop()  # 停止运行中背景音乐
    crash_sound.play()  # 播放碰撞音效
    time.sleep(0.2)  # 缩短等待时间到0.2秒

    # 更新崩溃次数和生命值
    crash_count += 1
    life_count -= 1  # 每次碰撞生命值减1

    # 如果生命值小于等于0，游戏结束
    if life_count <= 0:
        crash_screen = True
        while crash_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDim.fill(white)

            # 显示最终分数
            largeText = pygame.font.Font('freesansbold.ttf', 50)
            TextSurf, TextRect = text_object(f"Your Score: {dodged}", largeText)
            TextRect.center = ((disp_width / 2), (disp_height / 2))
            gameDim.blit(TextSurf, TextRect)

            # 绘制继续按钮
            button("Go on", 150, 450, 100, 50, green, bright_green, game_loop)
            # 绘制结束按钮
            button("C T A E", 550, 450, 100, 50, red, bright_red, game_intro)

            pygame.display.update()
            clock.tick(15)
    else:
        # 如果还有生命值，移除当前的 cai.png 并继续游戏
        global thin_stay, thin_stax, thin_speed, thin_width  # 声明相关变量为全局变量
        thin_stay = -650  # 将 cai.png 移出屏幕
        thin_stax = random.randrange(0, int(disp_width - thin_width))  # 重置 cai.png 的 x 位置
        dodged -= 3  # 得分减3
        return  # 不执行后续代码，继续游戏

def button(msg, x, y, w, h, ic, ac, action=None):
    """绘制按钮并处理点击事件"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # 检查鼠标是否悬停在按钮上
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDim, ac, (x, y, w, h), border_radius=10)  # 鼠标悬停时的颜色，增加圆角
        if click[0] == 1 and action is not None:
            pygame.mixer.music.stop()  # 停止当前背景音乐
            if msg == "Begin":
                running_music.play(-1)  # 播放运行中背景音乐并循环
            action()  # 执行按钮点击后的操作
            
            # 修改：每次按钮按下时更新 last_power_up_time
            global last_power_up_time
            last_power_up_time = pygame.time.get_ticks()
    else:
        pygame.draw.rect(gameDim, ic, (x, y, w, h), border_radius=10)  # 默认按钮颜色，增加圆角

    smallText = pygame.font.SysFont(None, 20)  # 使用系统默认字体替代自定义字体路径
    textSurf, textRect = text_object(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDim.blit(textSurf, textRect)

# 定义按钮的颜色变量
bright_green = (0, 255, 0)  # 亮绿色
bright_red = (255, 0, 0)    # 亮红色

def game_intro():
    intro = True

    # 加载指定的图片
    try:
        introImg = pygame.image.load(r'D:\Python\打飞机\image\caibu.jpg')  # 替换为指定的图片路径
        introImg = pygame.transform.scale(introImg, (disp_width // 2, disp_height // 2))  # 缩小图片
    except Exception as e:
        print(f"图片加载失败: {e}")
        introImg = None  # 如果图片加载失败，设置为 None

    # 播放未按按钮前的背景音乐
    pygame.mixer.music.play(-1)  # 循环播放背景音乐

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDim.fill(white)

        # 如果图片加载成功，绘制图片,否则显示默认文字
        if introImg is not None:
            # 计算图片位置，使其位于屏幕上方
            img_x = (disp_width - introImg.get_width()) // 2
            img_y = (disp_height - introImg.get_height()) // 4
            gameDim.blit(introImg, (img_x, img_y))  # 绘制图片

            # 在图片下方显示文字
            largeText = pygame.font.SysFont(None, 50)  # 使用系统默认字体
            TextSurf, TextRect = text_object("Jerk off", largeText)
            TextRect.center = ((disp_width / 2), (disp_height / 2 + introImg.get_height() / 2))
            gameDim.blit(TextSurf, TextRect)
        else:
            largeText = pygame.font.SysFont(None, 115)  # 使用系统默认字体
            TextSurf, TextRect = text_object("Jerk off", largeText)
            TextRect.center = ((disp_width / 2), (disp_height / 2))
            gameDim.blit(TextSurf, TextRect)

        # 绘制开始按钮
        button("Begin", 150, 450, 100, 50, green, bright_green, game_loop)
        # 绘制结束按钮
        button("C T A E", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

def quit_game():
    """退出游戏的函数"""
    pygame.quit()
    quit()

def game_loop():
    global crashed, bullets, last_bullet_time, dodged, bullet_speed, bullet_size, last_power_up_time, power_up_active, crash_count, thin_stay, thin_stax, thin_speed, thin_width, is_paused, life_count
    x = (disp_width * 0.45)
    y = (disp_height * 0.8)
    x_change = 0
    y_change = 0
    base_speed = 5  # 基础移动速度
    shift_speed = 7  # 按下Shift键时的移动速度
    current_speed = base_speed  # 当前移动速度

    # 新增变量 is_paused，用于控制游戏暂停状态
    is_paused = False

    # 新增变量 pause_start_time，记录暂停开始的时间
    pause_start_time = 0

    # 新增变量 crash_count，用于记录崩溃次数
    crash_count = 0

    # 添加背景图片
    try:
        background_img = pygame.image.load(r'D:\Python\打飞机\image\beij.png')  # 加载背景图片
        background_img = pygame.transform.scale(background_img, (disp_width, disp_height))  # 调整图片大小以适应窗口
    except Exception as e:
        print(f"背景图片加载失败: {e}")
        background_img = None  # 如果图片加载失败，设置为 None

    # 添加图形位置
    thin_width = 100
    thin_height = 100
    thin_stax = random.randrange(0, int(disp_width - thin_width))  # 将结果转换为整数
    thin_stay = -650  # 起始 y 位置
    thin_speed = 7  # 每帧移动速度

    thingCount = 0

    dodged = 0  # 初始化 dodged 变量
    bullet_speed = 10  # 初始化子弹速度
    bullet_size = 20  # 初始化子弹大小
    power_up_active = False  # 新增变量，用于控制加强界面是否已触发
    last_power_up_time = 0  # 新增变量，记录上一次触发提示框的时间
    power_up_start_time = 0  # 新增变量，记录提示框显示的起始时间

    # 新增变量 bullet_frequency，用于动态调整子弹发射频率
    bullet_frequency = 200  # 初始子弹发射间隔从300毫秒调整为200毫秒

    crashed = False

    # 新增变量 life_count，用于记录生命值
    life_count = 3  # 初始生命值为3

    # 重新加载并播放运行中背景音乐
    running_music.play(-1)  # 循环播放运行中背景音乐

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -current_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = current_speed
                elif event.key == pygame.K_UP:
                    y_change = -current_speed
                elif event.key == pygame.K_DOWN:
                    y_change = current_speed
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # 新增：检测按下Shift键
                    current_speed = shift_speed  # 将当前速度设置为Shift键的速度
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # 新增：检测松开Shift键
                    current_speed = base_speed  # 恢复基础速度

        # 检测鼠标点击事件，用于暂停/继续游戏
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pause_button_x = disp_width - 50  # 暂停按钮的x坐标
        pause_button_y = 10  # 暂停按钮的y坐标
        if pause_button_x + 40 > mouse[0] > pause_button_x and pause_button_y + 40 > mouse[1] > pause_button_y:
            if click[0] == 1:
                if is_paused:
                    # 如果已经暂停，再次点击暂停按钮则提前结束暂停
                    is_paused = False
                else:
                    # 如果未暂停，点击暂停按钮则开始暂停
                    is_paused = True
                    pause_start_time = pygame.time.get_ticks()  # 记录暂停开始时间

        # 如果游戏处于暂停状态，检查是否达到20秒或再次点击暂停按钮
        if is_paused:
            current_time = pygame.time.get_ticks()
            if current_time - pause_start_time >= 20000:  # 暂停20秒后自动恢复
                is_paused = False
            # 绘制暂停界面
            gameDim.fill((0, 0, 0))  # 黑色背景
            font = pygame.font.SysFont(None, 40)
            text = font.render("Game Paused", True, (255, 255, 255))
            gameDim.blit(text, (disp_width // 2 - text.get_width() // 2, disp_height // 2 - text.get_height() // 2))
            pygame.display.update()
            continue  # 跳过后续游戏逻辑

        # 游戏逻辑继续执行
        x += x_change
        y += y_change

        # 限制 y 的范围，确保不会越过窗口底部
        if y > disp_height - carImg.get_height():
            y = disp_height - carImg.get_height()

        # 绘制背景图片
        if background_img is not None:
            gameDim.blit(background_img, (0, 0))  # 绘制背景图片
        else:
            gameDim.fill(white)  # 如果背景图片加载失败，使用白色填充

        things(thin_stax, thin_stay)  # 绘制图形
        thin_stay += thin_speed  # speed 每次移动 7 像素添加到 thin_stay
        car(x, y)

        # 显示得分和生命值
        font = pygame.font.SysFont(None, 25)
        score_text = font.render(f"Dodged: {dodged}  Life: {life_count}", True, black)
        gameDim.blit(score_text, (0, 0))

        # 动态调整子弹发射频率
        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_time > bullet_frequency:  # 使用动态调整的子弹发射间隔
            bullets.append([x + carImg.get_width() // 2 - 10, y])  # 在飞机上方中间位置发射子弹
            last_bullet_time = current_time

            # 每10秒减少子弹发射间隔10毫秒
            if (current_time // 10000) > 0 and (current_time % 10000 == 0):
                bullet_frequency = max(100, bullet_frequency - 10)  # 最小间隔为100毫秒

        # 更新子弹位置并绘制
        bullets = [bullet for bullet in bullets if bullet[1] > 0]  # 过滤掉超出边界的子弹
        for bullet in bullets[:]:  # 使用切片避免修改列表时出错
            bullet[1] -= bullet_speed  # 子弹向上移动，速度由bullet_speed控制
            gameDim.blit(bullet_img, bullet)  # 绘制子弹

            # 检测子弹与cai.png的碰撞
            if (thin_stay < bullet[1] < thin_stay + thin_height) and \
               (thin_stax < bullet[0] < thin_stax + thin_width):
                bullets.remove(bullet)  # 子弹消失
                thin_stay = -650  # cai.png重置位置
                dodged += 1  # 分数加1
                thin_speed += 1  # 速度增加
                thin_width += random.uniform(0, 1.5)  # 随机增加宽度

        # 边缘位置
        if x > disp_width - carImg.get_width() or x < 0:
            crash()

        # 移动像素 stay 创建随机位置
        if thin_stay > disp_height:
            thin_stay = 0 - thin_height
            thin_stax = random.randrange(0, int(disp_width - thin_width))
            dodged += 1
            thin_speed += 0.5  # 修改: 将速度增加量从 1 减小为 0.5
            thin_width += random.uniform(0, 1.5)

        # 创建崩溃逻辑 (撞到就结束)
        if y < thin_stay + thin_height and y > thin_stay:
            if x > thin_stax and x < thin_stax + thin_width or x + car_width > thin_stax and x + car_width < thin_stax + thin_width:
                crash()

        # 每过15秒弹出提示框
        if current_time - last_power_up_time > 15000:  # 15秒触发一次
            last_power_up_time = current_time  # 更新时间戳
            bullet_speed += 5  # 增加子弹速度
            thin_speed += 0.4  # 修改: 将速度增加量从 0.8 减小为 0.4
            power_up_active = True  # 触发提示框
            power_up_start_time = current_time  # 记录提示框显示的起始时间

        # 绘制提示框
        if power_up_active:
            # 计算窗口中心的坐标
            center_x = disp_width // 2
            center_y = disp_height // 4  # 偏上位置

            # 计算文字的尺寸
            font = pygame.font.SysFont(None, 20)
            text = font.render("Increase speed", True, (0, 0, 0))
            text_width, text_height = font.size("Increase speed")

            # 创建一个刚好容纳文字的半透明Surface
            power_up_surface = pygame.Surface((text_width + 20, text_height + 10), pygame.SRCALPHA)
            power_up_surface.fill((255, 255, 0, 128))  # 设置颜色和透明度

            # 绘制文字到Surface上
            power_up_surface.blit(text, (10, 5))

            # 将Surface绘制到屏幕上，调整为窗口中心偏上位置
            gameDim.blit(power_up_surface, (center_x - (text_width + 20) // 2, center_y - (text_height + 10) // 2))

            # 检查提示框是否已显示超过两秒
            if current_time - power_up_start_time > 2000:  # 提示框持续2秒
                power_up_active = False

        # 绘制暂停按钮
        pygame.draw.rect(gameDim, (255, 0, 0), (pause_button_x, pause_button_y, 40, 40))  # 绘制红色暂停按钮
        font = pygame.font.SysFont(None, 20)
        text = font.render("Pause", True, (0, 0, 0))
        gameDim.blit(text, (pause_button_x + 10, pause_button_y + 10))

        pygame.display.update()
        clock.tick(60)  # 确保帧率稳定在60 FPS

game_intro()
game_loop()
pygame.quit()#结束
quit()









