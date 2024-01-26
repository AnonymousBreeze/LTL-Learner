import os
import pandas as pd

def calculate_mean_variance_accuracy(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_excel(file_path)
                    # BLEU score calculation
                    if 'BLEU' in df.columns:
                        mean_value = df['BLEU'].mean()
                        variance_value = df['BLEU'].var()
                        print(f"File: {file_path}\nBLEU - Mean: {mean_value}, Variance: {variance_value}")
                    
                    # Accuracy calculation
                    if 'Result' in df.columns:
                        accuracy = (df['Result'] == True).mean()
                        print(f"Accuracy: {accuracy * 100:.2f}%\n")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
# Evaluate ExpI
folder_path = 'Exp/ExpI/'
                    
# Evaluate ExpIV    
# folder_path = 'Exp/ExpIV/'
calculate_mean_variance_accuracy(folder_path)
