# 🧬 SNP-SNP Prediction (基于统计分析与机器学习的 SNP 交互预测)

**SNP-SNP Prediction** 是一个用于生物信息学中 **SNP（单核苷酸多态性）分析** 的 Python 工具集。  
本项目旨在通过统计检验与机器学习方法，研究 **SNP-SNP 交互作用**，并预测它们对表型（如疾病状态）的影响。

项目包含数据预处理、卡方检验、T 检验、逻辑回归模型训练、交叉验证。

---

## ✨ 核心功能

### 🔧 数据预处理
`txt2csv.py`  
- 将特定格式的 **.txt 基因数据** 转换为标准 **.csv 文件**  
- 方便后续使用 pandas 进行加载与分析  
- 可自定义输入路径与输出路径  

---

## 📊 统计分析模块

### 📌 卡方检验 (Chi-Squared Test)
`Chi_Squared_Test.py`  
- 构建 SNP × Phenotype 或 SNP × SNP 列联表  
- 使用 scipy.stats 计算卡方统计量与 p-value  
- 评估基因位点之间的关联性  

### 📌 T 检验 (T-test)
`T_test.py`  
- 使用 `scipy.stats.ttest_ind`  
- 比较病例组 (case) 与对照组 (control) 在某 SNP 位点上的平均差异  
- 判断基因型是否具有统计显著性影响  

---

## 🤖 机器学习预测模块

### 📌 逻辑回归模型 (Logistic Regression)
`Logistic.py`  
- 从 CSV 数据集中自动加载样本  
- 构建特征矩阵 **X** 和目标变量 **Y**  
- 使用 `sklearn.linear_model.LogisticRegression` 训练模型  
- 使用 `cross_val_score` 执行 **交叉验证**，输出模型预测准确率  

---


## 📂 项目结构

```

.
├── 2_EDM-1_csv/              # 数据集：100 个 EDM-1 模型的 CSV 文件
│   ├── 2_EDM-1_001.csv
│   └── ...
├── position1_EDM-2_csv/      # 100 个 EDM-2 (position 1) 的 CSV 模型
├── position3_EDM-1_csv/      # 100 个 EDM-1 (position 3) 的 CSV 模型
├── test1_EDM-1_csv/          # 100 个 EDM-1 (test 1) 的 CSV 模型
│
├── pycode/                   # 核心分析脚本
│   ├── Chi_Squared_Test.py
│   ├── Logistic.py
│   ├── T_test.py
│   ├── hu.py
│   ├── hu3.py
│   └── txt2csv.py
│
├── LICENSE                   # MIT License
└── README.md                 # 当前文档

````

---

## 🛠️ 依赖库

需要以下 Python 依赖：

- `pandas`
- `numpy`
- `scipy`
- `scikit-learn`

安装方式：

```bash
pip install pandas numpy scipy scikit-learn
````

---

## 🚀 使用指南

### 1️⃣ 数据预处理（可选）

将 `.txt` 转换为 `.csv`：

```bash
python pycode/txt2csv.py
```

> ⚠️ 提示：请根据你的数据路径，修改脚本中的 `path` 与 `newpath`。

---

### 2️⃣ 执行统计分析

#### ✔ 卡方检验

```bash
python pycode/Chi_Squared_Test.py
```

#### ✔ T 检验

```bash
python pycode/T_test.py
```

> 同样需在脚本中将 `path` 修改为你的数据集路径。

---

### 3️⃣ 运行机器学习模型

```bash
python pycode/Logistic.py
```

模型将自动执行交叉验证，并输出类似：

```
0.655
0.600
0.625
...
```

用于评估预测准确率（Accuracy）。

---

## 📄 许可证

本项目基于 **MIT License** 开源。
详情请参阅 `LICENSE` 文件。

---

## 🤝 贡献

欢迎提交 Issue / PR 改进本项目，例如：

* 添加新的统计测试方法
* 增加更多机器学习模型
* 增强特征选择算法
* 扩展数据预处理功能

---

## 📬 联系方式

如果你在使用中遇到问题，欢迎创建 Issue 或联系我。

