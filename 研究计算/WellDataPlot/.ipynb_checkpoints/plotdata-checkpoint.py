# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import codecs
from decimal import Decimal
import matplotlib
import pandas as pd
from WellDataPlot.ReadData import readDataFromXlsx
from numpy import trapz

def save_figure(folder_name, figure_name):
    plt.savefig(folder_name + "/" + figure_name, transparent=False, dpi=150, bbox_inches="tight")


# 閉塞と非閉塞の間の境界線を計算する関数
def get_boundary_line(normal_mus, normal_cohs, hang_up_mus, hange_up_cohs):
    mus_used = []
    boundary_line_mus = []
    boundary_line_cohs = []

    hang_up_mus, hange_up_cohs, normal_mus, normal_cohs = normal_mus, normal_cohs, hang_up_mus, hange_up_cohs
    for normal_mu in normal_mus:
        if normal_mu in mus_used or not (normal_mu == normal_mu): continue
        if normal_mu >4: continue
        mus_used.append(normal_mu)

        # 获取mu位置并计算这些位置中mu对应的coh最大值
        mu_pos = [idx for idx, val in enumerate(normal_mus) if val == normal_mu]
        chos = [normal_cohs[idx] for idx in mu_pos]
        if len(chos) == 0:
            print(chos)
        max_normal_coh = min(chos)
        # 获取mu位置并计算这些位置中mu对应的coh最小值
        if not normal_mu in hang_up_mus:
            min_hang_up_coh = max_normal_coh
        else:
            pos = [idx for idx, val in enumerate(hang_up_mus) if val == normal_mu]
            chos = [hange_up_cohs[idx] for idx in pos]
            min_hang_up_coh = max(chos)
        # 计算平均coh
        average_coh = (max_normal_coh + min_hang_up_coh) / 2
        # 加入list
        boundary_line_mus.append(normal_mu)
        boundary_line_cohs.append(average_coh)
    
    boundary_line_mus, boundary_line_cohs = zip(*sorted(zip(boundary_line_mus, boundary_line_cohs)))
    
    area = trapz(boundary_line_cohs,boundary_line_mus,0.01)
    print(area)
    print(boundary_line_mus)
    print(boundary_line_cohs)
    return boundary_line_mus, boundary_line_cohs , area


def get_min_coh(boundary_line_mus, boundary_line_cohs):
    chos = []
    for idx, mu in enumerate(boundary_line_mus):
        if mu >= 4:
            chos.append(boundary_line_cohs[idx])
    if len(chos) == 0: return 0
    return sum(chos) / len(chos)

def plot_exit_hang_up_figure(root_dir, filename, sheet_name, xrange=[-1,15e4],yrange=[0,4],title=None,titlesize=30,hangeup_text_position=(4e4, 2.25)):
    ax = plt.gca()
    
    d1, d2, d3 = readDataFromXlsx(filename, sheet_name, root_dir)
    d1 = np.array(d1)
    d2 = np.array(d2)
    d3 = np.array(d3)
    

    # 绘制散点
    plt.scatter(d1[:, 1], d1[:, 0], c="b", s=120 , label="None Hang Up")
    plt.scatter(d2[:, 1], d2[:, 0], marker="s", c="r", s=120 , label="Hang Up" )
    if len(d3) > 0:
        plt.scatter(d3[:, 1], d3[:, 0], marker="^", c="g", s=120, label="Hang Up(Exit)")

    # 计算鼻塞和非闭塞的边界线，并绘制曲线
    if len(d3) > 0:
        boundary_line_mus, boundary_line_cohs ,area = get_boundary_line(d1[:, 0], d1[:, 1], np.append(d2[:, 0], d3[:, 0]),
                                                     np.append(d2[:, 1], d3[:, 1]))
    else: 
        boundary_line_mus, boundary_line_cohs ,area = get_boundary_line(d1[:, 0], d1[:, 1], d2[:, 0],d2[:, 1])
    plt.plot(boundary_line_cohs, boundary_line_mus)
    #plt.text(1e4,0.4,str(area),size=12)
    # *** 图表的格式调整 ***
    # 指定x轴为科学计数法
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0), useMathText=True)
    # 指定图表的x轴y轴坐标的取值范围
    plt.axis(xrange+yrange)
    # x坐标轴名字
    plt.xlabel(r"Cohesion $\mathrm{N/m^2}$", size=20)
    # y坐标轴名字
    plt.ylabel(r"Friction Coefficient", size=20)
    # 调整xy坐标轴标签的文字大小
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    # 调整x轴启用科学计数法后，10^n文字过小问题
    plt.gca().xaxis.get_offset_text().set_fontsize(15)
    # 设置图表title
    # if title is not None: plt.title(title, size=titlesize)
    # 绘制图表格子
    plt.grid()
    # 绘制图表中右边的Hang_Up Region文字
    #plt.text(hangeup_text_position[0], hangeup_text_position[1], r'Hang-Up Region', size=20)
    #mark_text = matplotlib.lines.Line2D([], [],color='white', marker='.', label=title)
    #plt.legend(handles=[mark_text],handlelength=0,fontsize=15)
    return boundary_line_mus, boundary_line_cohs

def plot_hang_up_figure(root_dir, filename, sheet_name, min_coh=None ,xrange=[0,15e4],yrange=[0,10],title=None,titlesize=30,hangeup_text_position=(8e4,6),anotate_position=(5e4,4)):
    boundary_line_mus, boundary_line_cohs = plot_exit_hang_up_figure(root_dir, filename, sheet_name,xrange=xrange,yrange=yrange,title=title,titlesize=titlesize,hangeup_text_position=hangeup_text_position)

    # 计算界限粘着力并绘制直线和Minium Cohesion的标注
    if min_coh == None:
        min_coh = get_min_coh(boundary_line_mus, boundary_line_cohs)
    elif min_coh == "off":
        pass
    if not (min_coh == "off"):
        plt.axvline(min_coh, ls='-', color='g', linewidth=3)
    
    anotate_text = '$Minium\ Cohesion$\n$' + "{:.2e}".format(Decimal(min_coh)).replace("e+", r"\times10^{") + '}$'
    plt.annotate(anotate_text, xy=(min_coh, 0), xytext=anotate_position,
                 arrowprops=dict(facecolor='black', shrink=0.01, width=1), fontsize=12)

    return
    df = read_mincho_map(root_dir + "/" + "min_coh_map.csv")

    if df.H0[df.H0 == H].size < 1:
        df2 = pd.DataFrame({"H0": [0.8], "min_coh": [666]})
        df.append(df2)
    print(df)
    return df




def plot_experiment_resault(filename, title):
    # 从csv文件中读取数据
    f = codecs.open(filename, encoding='utf-8')
    circle_well_D, circle_well_hangup_num, circle_well_normal_num, rect_well_W, rect_well_hangup_num, rect_well_nonrmal_num = np.genfromtxt(
        f, delimiter=",", usecols=(0, 1, 2, 3, 4, 5), unpack=True, skip_header=2)
    f.close()

    point_size = [100, 150, 300]
    plt.scatter(circle_well_D, circle_well_hangup_num, s=point_size, alpha=0.5, c="r")
    plt.scatter(circle_well_D, rect_well_hangup_num, alpha=0.5, marker="s", s=point_size)

    fp = matplotlib.font_manager.FontProperties("Yu Mincho", size=20)
    plt.axis([78, 103, -0.5, 10.5])
    plt.tight_layout()
    plt.xlabel(r"内径 $mm$", fontproperties=fp)
    plt.ylabel(r"閉塞回数", fontproperties=fp)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(title, size=20)
    plt.grid()


def read_mincho_map(fname):
    try:
        df: pd.DataFrame = pd.read_csv(fname)
    except FileNotFoundError as FN:
        print("No csv File Found, Create A New DataFrame")
        df = pd.DataFrame({"H0": [0.1, 0.2], "min_coh": [200, 300]})
    return df