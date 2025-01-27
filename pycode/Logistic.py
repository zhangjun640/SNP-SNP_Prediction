import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
import os

# 读取文件夹路径
input_folder = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position1\position1_EDM-2_csv"
output_file = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position1\position1_EDM-2_csv\all_significant_points.csv"

# 创建一个空列表来存储所有文件的显著点集合
all_significant_points = []

# 遍历文件夹中的所有CSV文件（假设文件名为 position1_EDM-1_001.csv 到 position1_EDM-1_100.csv）
for i in range(1, 101):
    file_name = f"position1_EDM-2_{i:03}.csv"  # 根据i生成文件名，例如 position1_EDM-1_001.csv
    file_path = os.path.join(input_folder, file_name)

    if os.path.exists(file_path):
        print(f"正在处理文件：{file_name}")

        # 1. 读取数据
        df = pd.read_csv(file_path, sep=',', header=0)

        # 2. 拆分 X, y
        X = df.drop(columns=['Class'])
        y = df['Class']

        # 3. 对每个位点单独做 Logistic 回归，并获取 p-value
        p_values = {}
        for col in X.columns:
            feature = X[col]

            # 如果该列全是空值或只有单一值（导致回归无法进行），可考虑跳过
            if feature.dropna().nunique() < 2:
                continue

            # 为逻辑回归准备数据：添加截距列
            feature_with_const = sm.add_constant(feature, prepend=True)

            # 拟合Logistic回归模型
            try:
                model = sm.Logit(y, feature_with_const)
                result = model.fit(disp=0)  # disp=0 关闭拟合过程的打印输出

                # 获取每个特征的p-value
                p_val = result.pvalues[col]
                p_values[col] = p_val
            except:
                # 如果因为数据原因（比如完美分离）拟合失败，可在此跳过或记录
                continue

        # 4. Benjamini-Hochberg 多重检验校正
        p_vals = list(p_values.values())
        reject, pvals_corrected, _, _ = multipletests(p_vals, alpha=0.05, method='fdr_bh')

        # 创建校正后的 p-value 字典
        p_values_corrected = {col: pvals_corrected[i] for i, col in enumerate(p_values.keys())}

        # 5. 计算显著位点（校正后的 p-value 小于 0.05）
        significant_points = [col for col, p_val in p_values_corrected.items() if p_val < 0.08]

        # 6. 将显著点集合添加到结果列表中，确保每一行是该文件的显著点
        all_significant_points.append(", ".join(significant_points))

    else:
        print(f"文件 {file_name} 不存在，跳过该文件。")

# 7. 将所有显著点写入一个 CSV 文件，每一行对应一个文件的显著点集合
significant_df = pd.DataFrame(all_significant_points, columns=["Significant Points"])

# 保存到 CSV 文件
significant_df.to_csv(output_file, index=False)

print(f"所有显著点已保存至：{output_file}")
