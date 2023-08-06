# 作图
# 创建人：曾逸夫
# 创建时间：2022-01-27

import sys
import csv
import time
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator
from opencv_webcam.utils.time_format import time_format


OWS_VERSION = 'OpenCV Webcam Script v0.5'  # 项目名称与版本号
ROOT_PATH = sys.path[0]  # 项目根目录
COLOR_LIST = ['#f96801']  # 颜色列表

# -----------字体库-----------
# 宋体
SimSun = font_manager.FontProperties(
    fname=f'{ROOT_PATH}/fonts/SimSun.ttc', size=12)
# 新罗马字体
TimesNesRoman = font_manager.FontProperties(
    fname=f'{ROOT_PATH}/fonts/TimesNewRoman.ttf', size=12)


# 创建折线图
def createLineChart(frames_y, date_list, time_list):
    chart_startTime = time.time()  # 作图开始时间

    # -----------作图开始-----------
    # 画布尺寸
    plt.figure(figsize=(8, 4))
    # 设置线型
    plt.plot(time_list, frames_y, color=COLOR_LIST[0], marker='o',
             label='时间点', markerfacecolor=COLOR_LIST[0], markersize=5)

    plt.ylim(ymin=0)  # 纵坐标限定
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))  # 纵坐标设置为整数
    plt.grid(axis="y", ls='--')  # 横向网格线

    ax = plt.gca()
    ax.spines['right'].set_color('none')  # 消除有边框
    ax.spines['top'].set_color('none')  # 消除上边框

    # 显示点值
    for a, b in zip(time_list, frames_y):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10.5)

    # -----------标题、横纵轴、图例等-----------
    plt.title(OWS_VERSION, fontsize=12, fontproperties=TimesNesRoman)  # 标题

    plt.xlabel(date_list[0], fontsize=12,
               fontproperties=TimesNesRoman)  # 横轴标签，时间
    plt.ylabel('帧数', fontsize=12, fontproperties=SimSun)  # 纵轴标签，帧数

    plt.xticks(fontproperties=TimesNesRoman, rotation=45, fontsize=12)  # 横轴刻度
    plt.yticks(fontproperties=TimesNesRoman, fontsize=12)  # 纵轴刻度
    plt.legend(prop=SimSun, fontsize=12, loc='best')  # 图例

    # chart保存信息
    os.makedirs("DateFrames", exist_ok=True)  # 创建DateFrames目录
    date_frames_chart_path = f'{ROOT_PATH}/DateFrames/date_frames_{date_list[0]}.png'

    # 保存图像
    plt.savefig(date_frames_chart_path, dpi=300, bbox_inches='tight')

    # -----------作图结束-----------
    chart_endTime = time.time()  # 作图开始时间
    chart_totalTime = chart_endTime - chart_startTime  # 作图用时
    print(
        f'日期-帧数图创建成功！用时：{time_format(chart_totalTime)}，已保存在{date_frames_chart_path}，总帧数：{sum(frames_y)}')


# csv2chart
def csv2chart(csv_path):
    f = open(csv_path, 'r')  # 读取csv
    f_list = list(csv.reader(f))  # csv2list

    d_list = []  # 日期列表
    t_list = []  # 时间列表
    frames_list = []  # 时间列表

    tmp_date = f_list[0][0].split(' ')[0]  # 临时日期
    for i in range(len(f_list)):
        date_item = f_list[i][0].split(' ')[0]  # 日期
        time_item = f_list[i][0].split(' ')[1]  # 时间

        if (tmp_date != date_item):
            createLineChart(frames_list, d_list, t_list)  # 创建日期-帧数图
            tmp_date = date_item  # 替换
            # -----------清空列表-----------
            d_list = []
            t_list = []
            frames_list = []

        d_list.append(date_item)  # 日期
        t_list.append(time_item)  # 时间
        frames_list.append(int(f_list[i][1]))  # 帧数
        if (i == len(f_list)-1):
            # 最后一组
            createLineChart(frames_list, d_list, t_list)  # 创建日期-帧数图
