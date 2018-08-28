# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt 
import numpy as np
import codecs
from decimal import Decimal
import matplotlib
import pandas as pd

def save_figure(folder_name,figure_name):
    plt.savefig(folder_name+"/"+figure_name, transparent=False, dpi=80, bbox_inches="tight")
# 閉塞と非閉塞の間の境界線を計算する関数
def get_boundary_line( normal_mus , normal_cohs , hang_up_mus , hange_up_cohs ):

    mus_used = []
    boundary_line_mus = []
    boundary_line_cohs = []
    for normal_mu in normal_mus:
        if normal_mu in mus_used or not(normal_mu == normal_mu): continue
        mus_used.append(normal_mu)
        
        # 获取mu位置并计算这些位置中mu对应的coh最大值
        mu_pos = [idx for idx,val in enumerate(normal_mus) if val==normal_mu]
        chos = [ normal_cohs[idx] for idx in mu_pos ]
        if len(chos) == 0:
            print(chos)
        max_normal_coh = max(chos)
        # 获取mu位置并计算这些位置中mu对应的coh最小值
        if not normal_mu in hang_up_mus: continue
        pos = [idx for idx,val in enumerate(hang_up_mus) if val==normal_mu]
        chos = [ hange_up_cohs[idx] for idx in pos ]
        min_hang_up_coh = min(chos)
        # 计算平均coh
        average_coh = (max_normal_coh+min_hang_up_coh)/2
        # 加入list
        boundary_line_mus.append(normal_mu)
        boundary_line_cohs.append(average_coh)


    boundary_line_mus, boundary_line_cohs = zip(*sorted(zip(boundary_line_mus, boundary_line_cohs)))
    
    #print(boundary_line_mus)    
    #print(boundary_line_cohs)
    return boundary_line_mus, boundary_line_cohs

def get_min_coh(boundary_line_mus, boundary_line_cohs):
     chos = []
     for idx,mu in enumerate(boundary_line_mus):
         if mu >= 4:
             chos.append( boundary_line_cohs[idx])
     if len(chos) == 0: return 0
     return sum(chos)/len(chos)    

def plot_hang_up_figure(root_dir,filename,D,H,min_coh = None):

    
    # 从csv文件中读取数据
    if not root_dir == None:
        path = root_dir+"/"+filename
    else:
        path = filename
    f = codecs.open(path, encoding = 'utf-8')
    normal_mu,normal_coh,hang_up_mu,hang_up_coh = np.genfromtxt(f,delimiter=",",usecols=(0,1,2,3),unpack=True,skip_header=True)
    f.close()
    # 绘制散点
    plt.scatter(normal_coh,normal_mu,c="b",s=120)
    plt.scatter(hang_up_coh,hang_up_mu,marker="s",c="r",s=120)
    
    # 计算鼻塞和非闭塞的边界线，并绘制曲线
    boundary_line_mus, boundary_line_cohs=get_boundary_line(normal_mu,normal_coh,hang_up_mu,hang_up_coh)
    plt.plot(boundary_line_cohs,boundary_line_mus)
    
    # 计算界限粘着力并绘制直线和Minium Cohesion的标注
#    if min_coh == None:
#        min_coh = get_min_coh(boundary_line_mus, boundary_line_cohs)
#    elif min_coh == "off":
#        pass
#    if not (min_coh == "off"):
#        plt.axvline(min_coh, ls='-', color='g',linewidth =3)
        
        
#        anotate_text = '$Minium\ Cohesion$\n$'+"{:.2e}".format(Decimal(min_coh)).replace("e+",r"\times10^{")+'}$'
#        plt.annotate(anotate_text, xy=(min_coh,-1), xytext=(min_coh+2e4,4),arrowprops=dict(facecolor='black', shrink=0.05),fontsize=20)

    
    # *** 图表的格式调整 ***
    # 指定x轴为科学计数法
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0),useMathText=True)
    # 指定图表的x轴y轴坐标的取值范围
    plt.axis([0,15e4,0,4])
    # x坐标轴名字
    plt.xlabel("$Cohesion\ N/m^2$",size=20)
    # y坐标轴名字
    plt.ylabel("$Friction\ Coeffiction$",size=20)
    # 调整xy坐标轴标签的文字大小
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    # 调整x轴启用科学计数法后，10^n文字过小问题
    plt.gca().xaxis.get_offset_text().set_fontsize(15)
    # 设置图表title
    plt.title("D%s %.1fH" % (str(D),H) , size = 30)
    # 绘制图表格子
    plt.grid()
    # 绘制图表中右边的Hang_Up Region文字
    plt.text(3e4, 2, r'Hang-Up Region',size = 30)
    
    return
    df = read_mincho_map(root_dir+"/"+"min_coh_map.csv")

    if df.H0[ df.H0 == H ].size  < 1:
        df2 = pd.DataFrame({"H0":[0.8],"min_coh":[666]})
        df.append(df2)
    print(df)
    return df
def plot_exit_hang_up_figure(root_dir,filename,D,H,min_coh = None):

    
    # 从csv文件中读取数据
    if not root_dir == None:
        path = root_dir+"/"+filename
    else:
        path = filename
    f = codecs.open(path, encoding = 'utf-8')
    normal_mu,normal_coh,hang_up_mu,hang_up_coh = np.genfromtxt(f,delimiter=",",usecols=(0,1,2,3),unpack=True,skip_header=True)
    f.close()
    # 绘制散点
    plt.scatter(normal_coh,normal_mu,c="b",s=120)
    plt.scatter(hang_up_coh,hang_up_mu,marker="s",c="r",s=120)
    
    # 计算鼻塞和非闭塞的边界线，并绘制曲线
    boundary_line_mus, boundary_line_cohs=get_boundary_line(normal_mu,normal_coh,hang_up_mu,hang_up_coh)
    plt.plot(boundary_line_cohs,boundary_line_mus)
    
    # 计算界限粘着力并绘制直线和Minium Cohesion的标注
    if min_coh == None:
        min_coh = get_min_coh(boundary_line_mus, boundary_line_cohs)
    elif min_coh == "off":
        pass
    if not (min_coh == "off"):
        plt.axvline(min_coh, ls='-', color='g',linewidth =3)
        
        
        anotate_text = '$Minium\ Cohesion$\n$'+"{:.2e}".format(Decimal(min_coh)).replace("e+",r"\times10^{")+'}$'
        plt.annotate(anotate_text, xy=(min_coh,-1), xytext=(min_coh+2e4,4),arrowprops=dict(facecolor='black', shrink=0.05),fontsize=20)

    
    # *** 图表的格式调整 ***
    # 指定x轴为科学计数法
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0),useMathText=True)
    # 指定图表的x轴y轴坐标的取值范围
    plt.axis([0,20e4,-1,12])
    # x坐标轴名字
    plt.xlabel("$Cohesion\ N/m^2$",size=20)
    # y坐标轴名字
    plt.ylabel("$Friction\ Coeffiction$",size=20)
    # 调整xy坐标轴标签的文字大小
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    # 调整x轴启用科学计数法后，10^n文字过小问题
    plt.gca().xaxis.get_offset_text().set_fontsize(15)
    # 设置图表title
    plt.title("D%s %.1fH" % (str(D),H) , size = 30)
    # 绘制图表格子
    plt.grid()
    # 绘制图表中右边的Hang_Up Region文字
    plt.text(1e5, 6, r'Hang-Up Region',size = 30)
    
    return
    df = read_mincho_map(root_dir+"/"+"min_coh_map.csv")

    if df.H0[ df.H0 == H ].size  < 1:
        df2 = pd.DataFrame({"H0":[0.8],"min_coh":[666]})
        df.append(df2)
    print(df)
    return df
def plot_experiment_resault(filename,title):


    
    # 从csv文件中读取数据
    f = codecs.open(filename, encoding = 'utf-8')
    circle_well_D,circle_well_hangup_num,circle_well_normal_num,rect_well_W,rect_well_hangup_num,rect_well_nonrmal_num= np.genfromtxt(f,delimiter=",",usecols=(0,1,2,3,4,5),unpack=True,skip_header=2)
    f.close()

    point_size = [100,150,300]
    plt.scatter(circle_well_D,circle_well_hangup_num,s=point_size,alpha=0.5,c="r")
    plt.scatter(circle_well_D,rect_well_hangup_num,alpha=0.5,marker="s",s=point_size)
    
    fp = matplotlib.font_manager.FontProperties("Yu Mincho",size=20)
    plt.axis([78,103,-0.5,10.5])
    plt.tight_layout()
    plt.xlabel(r"内径 $mm$",fontproperties=fp)
    plt.ylabel(r"閉塞回数",fontproperties=fp)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(title,size=20)
    plt.grid()


def read_mincho_map(fname):
    try:
        df:pd.DataFrame = pd.read_csv(fname)
    except FileNotFoundError as FN:
        print("No csv File Found, Create A New DataFrame")
        df = pd.DataFrame({"H0":[0.1,0.2],"min_coh":[200,300]})
    return df