import pandas as pd
import numpy as np
import itertools
from sklearn.metrics import mutual_info_score
from sklearn.preprocessing import LabelEncoder
import os
import glob
from tqdm import tqdm


def compute_max_mutual_information_triplet(input_directory, output_csv):
    """
    处理input_directory中的所有CSV文件，计算前30个变量的所有三元组与类别标签的互信息，
    并将每个文件中互信息最大的三元组及其值保存到output_csv中。

    参数:
    - input_directory (str): 输入CSV文件所在的目录路径。
    - output_csv (str): 结果保存的输出CSV文件路径。
    """

    # 匹配CSV文件的模式，根据需要调整
    csv_pattern = os.path.join(input_directory, "position3_EDM-2_*.csv")
    file_list = glob.glob(csv_pattern)

    if not file_list:
        print(f"在目录中未找到CSV文件: {input_directory}")
        return

    print(f"找到 {len(file_list)} 个CSV文件需要处理。")

    # 准备一个列表来存储结果
    results = []

    # 使用进度条遍历每个文件
    for file_path in tqdm(file_list, desc="处理文件中"):
        try:
            # 读取CSV文件，尝试不同的编码格式
            try:
                df = pd.read_csv(file_path, sep=",", header=0, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, sep=",", header=0, encoding='gbk')

            # 检查数据的列数
            num_rows, num_cols = df.shape
            if num_cols < 31:
                print(f"跳过文件 {os.path.basename(file_path)}: 列数不足 ({num_cols})")
                continue  # 跳过列数不足的文件

            # 选择前30个变量列和最后一列作为类别
            variable_columns = df.columns[:30]
            class_column = df.columns[-1]

            X = df[variable_columns]
            y = df[class_column]

            # 对变量和类别进行标签编码
            le = LabelEncoder()
            X_encoded = X.apply(lambda col: le.fit_transform(col.astype(str)), axis=0)
            y_encoded = le.fit_transform(y.astype(str))

            # 生成所有30个变量的三元组组合
            variable_triplets = list(itertools.combinations(variable_columns, 3))

            # 初始化记录最大互信息的变量
            max_mi = -np.inf
            max_triplet = (None, None, None)

            # 遍历每个三元组，计算互信息
            for var1, var2, var3 in variable_triplets:
                # 创建联合特征，通过连接三个变量的编码值
                joint_feature = (
                    X_encoded[var1].astype(str) + "_" +
                    X_encoded[var2].astype(str) + "_" +
                    X_encoded[var3].astype(str)
                )

                # 对联合特征进行编码
                joint_encoded = le.fit_transform(joint_feature)

                # 计算联合特征与类别之间的互信息
                mi = mutual_info_score(joint_encoded, y_encoded)

                # 如果当前互信息大于最大值，则更新
                if mi > max_mi:
                    max_mi = mi
                    max_triplet = (var1, var2, var3)

            # 将当前文件的结果添加到结果列表中
            results.append({
                'Filename': os.path.basename(file_path),
                'MaxMutualInformation': max_mi,
                'Variable1': max_triplet[0],
                'Variable2': max_triplet[1],
                'Variable3': max_triplet[2]
            })

        except Exception as e:
            print(f"处理文件 {os.path.basename(file_path)} 时出错: {e}")
            continue  # 出错时继续处理下一个文件

    # 将结果列表转换为DataFrame
    results_df = pd.DataFrame(results)

    # 将结果保存到输出CSV文件
    results_df.to_csv(output_csv, index=False, encoding='utf-8')

    print(f"处理完成。结果已保存到 {output_csv}")


if __name__ == "__main__":
    # 定义三元组模型的输入和输出路径
    input_directory = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position3\position3_EDM-2_csv"
    output_csv = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position3\position3_EDM-2_csv\max_mutual_information_triplet_results.csv"

    # 调用函数计算并保存结果
    compute_max_mutual_information_triplet(input_directory, output_csv)
