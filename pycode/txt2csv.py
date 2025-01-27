import os
import pandas as pd


def batch_txt_to_csv(txt_folder_path, csv_folder_path, file_prefix, file_range):
    try:
        # 确保输出的 CSV 文件夹存在
        if not os.path.exists(csv_folder_path):
            os.makedirs(csv_folder_path)

        for i in range(file_range[0], file_range[1] + 1):
            # 构造 TXT 文件路径
            txt_file_path = os.path.join(txt_folder_path, f"{file_prefix}_{i:03d}.txt")

            # 构造对应的 CSV 文件路径
            csv_file_path = os.path.join(csv_folder_path, f"{file_prefix}_{i:03d}.csv")

            if os.path.exists(txt_file_path):
                # 读取 TXT 文件
                with open(txt_file_path, 'r') as file:
                    lines = file.readlines()

                # 将每行分割为列表，并将所有行存储到一个二维列表中
                data = [line.strip().split('\t') for line in lines]

                # 将数据转换为 DataFrame
                df = pd.DataFrame(data)

                # 保存为 CSV 文件
                df.to_csv(csv_file_path, index=False, header=False)

                print(f"成功转换: {txt_file_path} -> {csv_file_path}")
            else:
                print(f"文件不存在: {txt_file_path}")
    except Exception as e:
        print(f"转换失败: {e}")


# 示例用法
txt_folder_path = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position3\position3_EDM-2"
csv_folder_path = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position3\position3_EDM-2_csv"
file_prefix = "position3_EDM-2"
file_range = (1, 100)  # 文件编号范围

batch_txt_to_csv(txt_folder_path, csv_folder_path, file_prefix, file_range)