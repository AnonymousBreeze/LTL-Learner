import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 初始化列表
iterations = [1, 2, 3, 4, 5, 6]
GPT35_10_Accuracy, GPT35_10_BLEU_mean, GPT35_10_BLEU_var, GPT35_10_BLEU = [], [], [], []
GPT35_20_Accuracy, GPT35_20_BLEU_mean, GPT35_20_BLEU_var,GPT35_20_BLEU = [], [], [], []
GPT4_Accuracy, GPT4_BLEU_mean, GPT4_BLEU_var,GPT4_BLEU = [], [], [], []

# 遍历文件夹
def calculate_mean_variance_accuracy(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xlsx'):
                # 读取 Excel 文件
                try:
                    df = pd.read_excel(os.path.join(root, file))
                    # df = pd.read_excel(file)
                    # BLEU score calculation
                    if 'BLEU' in df.columns:
                        bleu_mean = df['BLEU'].mean()
                        bleu_var = df['BLEU'].var()
                        # print(f"File: {file}\nBLEU - Mean: {bleu_mean}, Variance: {bleu_var}")
                        bleu = list(df['BLEU'])
                    # Accuracy calculation
                    if 'Result' in df.columns:
                        accuracy = (df['Result'] == True).mean()
                        # print(f"Accuracy: {accuracy * 100:.2f}%\n")
                except Exception as e:
                    print(f"Error processing file {file}: {e}")

                # 判断属于哪个模型并保存数据
                if 'GPT3.5' in root and 'N=10' in root:
                    GPT35_10_Accuracy.append(accuracy)
                    GPT35_10_BLEU_mean.append(bleu_mean)
                    GPT35_10_BLEU_var.append(bleu_var)
                    GPT35_10_BLEU.append(bleu)
                elif 'GPT3.5' in root and 'N=20' in root:
                    GPT35_20_Accuracy.append(accuracy)
                    GPT35_20_BLEU_mean.append(bleu_mean)
                    GPT35_20_BLEU_var.append(bleu_var)
                    GPT35_20_BLEU.append(bleu)
                elif 'GPT4' in root:
                    GPT4_Accuracy.append(accuracy)
                    GPT4_BLEU_mean.append(bleu_mean)
                    GPT4_BLEU_var.append(bleu_var)
                    GPT4_BLEU.append(bleu)

folder_path = 'Exp/ExpII/Syn'
calculate_mean_variance_accuracy(folder_path)



# 打印结果
# print("GPT3.5 N=10 Accuracy:", GPT35_10_Accuracy)
# print("GPT3.5 N=10 BLEU mean:", GPT35_10_BLEU_mean)
# print("GPT3.5 N=10 BLEU var:", GPT35_10_BLEU_var)
# print("GPT3.5 N=20 Accuracy:", GPT35_20_Accuracy)
# print("GPT3.5 N=20 BLEU mean:", GPT35_20_BLEU_mean)
# print("GPT3.5 N=20 BLEU var:", GPT35_20_BLEU_var)
# print("GPT4 Accuracy:", GPT4_Accuracy)
# print("GPT4 BLEU mean:", GPT4_BLEU_mean)
# print("GPT4 BLEU var:", GPT4_BLEU_var)

#  Plotting
plt.figure(figsize=(12, 8))

# BLEU Scores
plt.subplot(2, 1, 1)

df = pd.DataFrame({
    'Iteration': [],
    'BLEU': [],
    'Model': []
})
df_gpt35_10 = pd.DataFrame({'Iteration': sum([[i + 1] * len(bleu_scores) for i, bleu_scores in enumerate(GPT35_10_BLEU)], []),
                            'BLEU': sum(GPT35_10_BLEU, []),
                            'Model': ['GPT3.5(n=10)'] * sum(len(bleu_scores) for bleu_scores in GPT35_10_BLEU)})
df_gpt35_20 = pd.DataFrame({'Iteration': sum([[i + 1] * len(bleu_scores) for i, bleu_scores in enumerate(GPT35_20_BLEU)], []),
                            'BLEU': sum(GPT35_20_BLEU, []),
                            'Model': ['GPT3.5(n=20)'] * sum(len(bleu_scores) for bleu_scores in GPT35_20_BLEU)})
df_gpt4 = pd.DataFrame({'Iteration': sum([[i + 1] * len(bleu_scores) for i, bleu_scores in enumerate(GPT4_BLEU)], []),
                        'BLEU': sum(GPT4_BLEU, []),
                        'Model': ['GPT4(n=10)'] * sum(len(bleu_scores) for bleu_scores in GPT4_BLEU)})
print(df['BLEU'].describe())
print(df_gpt4['BLEU'].describe())
# 合并所有 DataFrame
df = pd.concat([df, df_gpt35_10, df_gpt35_20, df_gpt4], ignore_index=True)
sns.boxplot(x="Iteration", y="BLEU", data=df, hue="Model", linewidth=1.5,whis=5.0)
plt.title('BLEU Scores Across Iterations for Different Models')
plt.xlabel('Iteration')
plt.ylabel('BLEU Score')
plt.legend()

# plt.xticks(positions, ['Iter 1', 'Iter 2', 'Iter 3', 'Iter 4', 'Iter 5', 'Iter 6'])
# plt.title('BLEU Scores (Mean and Variance) Distribution Over Iterations for Different Models')
# plt.xlabel('Iteration')
# plt.ylabel('BLEU Score')
# plt.legend(['GPT-3.5 N=10', 'GPT-3.5 N=20', 'GPT-4'], loc='upper left')
# plt.grid(True)
# plt.show()


# Accuracy
plt.subplot(2, 1, 2)
plt.plot(iterations, GPT35_10_Accuracy, marker='o', color='blue', label='GPT3.5(n=10)')
plt.plot(iterations, GPT35_20_Accuracy, marker='o', color='purple', label='GPT3.5(n=20)')
plt.plot(iterations, GPT4_Accuracy, marker='o', color='green', label='GPT4(n=10)')
plt.title('Accuracy Across Iterations')
plt.xlabel('Iteration')
plt.ylabel('Accuracy (%)')
plt.legend()

plt.tight_layout()
plt.show()