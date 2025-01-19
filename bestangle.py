import math
import scipy.optimize as opt
import numpy as np
import datetime

Fmax = float(input("请输入光伏板最大承受阻力 Fmax:"))
theta = float(input("请输入权重因子 theta:"))
angle = None
angle_in_radians = math.radians(angle)  # 将角度转换为弧度
sin_value = math.sin(angle_in_radians)
cos_value = math.cos(angle_in_radians)

def calculate_drag_force(C_aa, A_t, v_a):
    # 给定空气密度
    rho_a = 1.226  # kg/m³
    # 计算阻力
    R_aa = 0.5 * C_aa * rho_a * A_t * (v_a**2) * (cos_value**2)
    return R_aa

def calculate_days_since_vernal_equinox():
    today = datetime.date.today()
    vernal_equinox = datetime.date(today.year, 3, 20)  # 假定春分为每年的3月20日
    days_since_vernal_equinox = (today - vernal_equinox).days
    return days_since_vernal_equinox

def get_current_time():
    now = datetime.datetime.now().time()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def calculate_DNI(G0, H, phi, ST, D):
    # 计算a, b, c
    a=0.4237-0.00821*(6-H)**2
    b=0.5055+0.00595 * (6.5-H)**2
    c=0.2711+0.01858*(25-H)**2
    # 计算δ
    delta=math.asin(math.sin(math.radians(2*math.pi*D/365))*math.sin(math.radians(23.45)))
    # 计算ω
    w=math.pi/12*(ST-12)
    # 计算sinα_s
    sin_alpha_s=math.cos(delta)*math.cos(math.radians(phi)) * math.cos(w) + math.sin(delta) * math.sin(math.radians(phi))
    # 计算DNI
    DNI = G0 * (a + b * math.exp(-c / (math.sin(math.asin(sin_alpha_s)))))*sin_value
    return DNI

def calculate_DNImax(G0, H, phi, ST, D):
    # 计算a, b, c
    a=0.4237-0.00821*(6-H)**2
    b=0.5055+0.00595 * (6.5-H)**2
    c=0.2711+0.01858*(25-H)**2
    # 计算δ
    delta=math.asin(math.sin(math.radians(2*math.pi*D/365))*math.sin(math.radians(23.45)))
    # 计算ω
    w=math.pi/12*(ST-12)
    # 计算sinα_s
    sin_alpha_s=math.cos(delta)*math.cos(math.radians(phi)) * math.cos(w) + math.sin(delta) * math.sin(math.radians(phi))
    # 计算DNI
    DNImax = G0 * (a + b * math.exp(-c / (math.sin(math.asin(sin_alpha_s)))))
    return DNImax

# 定义目标函数
def target_function(x):
    return eval(user_function)



while True:
    # 阻力模型用户输入
    C_aa = float(input("请输入空气阻力系数 C_aa:"))
    A_t = float(input("请输入横截面积 A_t (平方米):"))
    v_a = float(input("请输入风速 v_a (米/秒):"))
    # 调用函数计算阻力
    result0 = calculate_drag_force(C_aa, A_t, v_a)
    # 输出阻力
    print(f"物体在给定条件下受到的阻力为 {result0} 牛顿")
    
    #获取当前时间与日期
    days_since_vernal_equinox = calculate_days_since_vernal_equinox()
    current_time = get_current_time()
    #输出时间日期
    print(f"当前时间(24小时制): {current_time}")
    print(f"距离春分后的天数: {days_since_vernal_equinox}")
    
    # 太阳辐射用户输入
    G0 = 1366  # 太阳常数，单位为W/m²
    H = float(input("请输入海拔高度(单位:km):"))
    phi = float(input("请输入当地纬度（北纬为正）："))
    ST = float(current_time)
    D = float(days_since_vernal_equinox)
    # 调用函数计算DNI和DNImax
    result1 = calculate_DNI(G0, H, phi, ST, D)
    result2 = calculate_DNImax(G0, H, phi, ST, D)
    # 输出太阳辐射
    print(f"直接法辐射(DNI)为 {result1} W/m²")
    
    #进行归一化
    F=result0/Fmax
    R=result1/result2
    
    # 用户输入需要优化的函数
    user_function = theta*F +(1-theta)*R
    
    # 使用scipy的minimize函数来最大化目标函数
    result = opt.minimize(lambda angle: -target_function(angle), angle0=0, bounds=[(-180, 180)])
    # 输出结果
    if result.success:
      max_value = -result.fun
      max_angle = result.angle[0]
      print(f"最大值为 {max_value}，取得于 angle = {max_angle}")
    else:
      print("未能找到最大值")
    
    