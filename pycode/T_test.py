import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import os

# 读取文件夹路径
input_folder = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position1\position1_EDM-2_csv"
output_file = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position1\position1_EDM-2_csv\all_significant_points_ttest.csv"

# 创建一个空列表来存储所有文件的显著点集合
all_significant_points = []

# 遍历文件夹中的所有CSV文件（假设文件名为 position1_EDM-1_001.csv 到 position1_EDM-1_100.csv）
for i in range(1, 101):
    file_name = f"position1_EDM-2_{i:03}.csv"  # 根据i生成文件名，例如 position1_EDM-1_001.csv
    file_path = os.path.join(input_folder, file_name)

    if os.path.exists(file_path):
        print(f"正在处理文件：{file_name}")

        # 读取数据
        df = pd.read_csv(file_path, sep=',', header=0)

        # 将数据根据 Class 列拆分成不同类别
        df_class0 = df[df['Class'] == 0]
        df_class1 = df[df['Class'] == 1]

        # 对每个位点进行 t 检验，并记录 p-value
        p_values = {}
        for col in df.columns:
            if col == 'Class':
                continue

            # 取出该列在不同Class下的值
            group0 = df_class0[col]
            group1 = df_class1[col]

            # 如果该位点在某个分组中全为 NaN 或样本数过低，则跳过
            if group0.dropna().shape[0] < 2 or group1.dropna().shape[0] < 2:
                continue

            # t 检验
            t_stat, p_val = ttest_ind(group0, group1, nan_policy='omit')

            p_values[col] = p_val

        # Benjamini-Hochberg 多重检验校正
        p_vals = list(p_values.values())
        reject, pvals_corrected, _, _ = multipletests(p_vals, alpha=0.05, method='fdr_bh')

        # 创建校正后的 p-value 字典
        p_values_corrected = {col: pvals_corrected[i] for i, col in enumerate(p_values.keys())}

        # 根据校正后的 p-value 筛选显著位点
        significant_points = [col for col, p_val in p_values_corrected.items() if p_val < 0.10]

        # 将显著点集合添加到结果列表中，确保每一行是该文件的显著点
        all_significant_points.append(", ".join(significant_points))

    else:
        print(f"文件 {file_name} 不存在，跳过该文件。")

# 将所有显著点写入一个 CSV 文件，每一行对应一个文件的显著点集合
significant_df = pd.DataFrame(all_significant_points, columns=["Significant Points"])

# 保存到 CSV 文件
significant_df.to_csv(output_file, index=False)

print(f"所有显著点已保存至：{output_file}")
