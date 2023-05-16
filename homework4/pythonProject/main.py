import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

import pandas as pd
from matplotlib.animation import FuncAnimation

# 读取数据
df = pd.read_csv(r'C:\Users\Meng Rui\Desktop\data - 副本.csv', encoding='GB2312')

# 设置国家为索引，然后将数据框转置，使得行标签是年份，列标签是国家
df.set_index('country', inplace=True)
df = df.transpose()

# 将索引转换为整数类型的年份
df.index = df.index.astype(int)

# 对缺失的数据进行插值
df = df.interpolate()

# 计算除2000年之外的前15个国家的最大值和最小值
global_min = df[df.index != 2000].apply(lambda x: x.nsmallest(15).min()).min()
global_max = df[df.index != 2000].apply(lambda x: x.nsmallest(15).max()).max()

# 计算2000年的最大值
year_2000_max = df.loc[2000].nsmallest(15).max()

# 创建画布
fig, ax = plt.subplots(figsize=(15, 8))

# 提取出所有的年份
years = df.index.unique()[::-1]

# 定义动画绘制的函数
def draw_barchart(year):
    dff = df.loc[year].nsmallest(15)
    ax.clear()
    ax.barh(dff.index, dff.values)
    if year == 2000:  # 如果年份是2000年，设置x轴范围为全局最小值到这一年的最大值
        ax.set_xlim(global_min, year_2000_max)
    else:
        ax.set_xlim(global_min, global_max)  # 设置x轴的范围
    ax.set_title(f'Year: {year}')  # 设置标题为年份

plt.suptitle('1971-2020世界各国人口增长率最低15国排行')  # 添加主标题

# 创建动画
animator = FuncAnimation(fig, draw_barchart, frames=years, interval=1000)

# 保存动画
animator.save('animation.mp4', writer='ffmpeg')
