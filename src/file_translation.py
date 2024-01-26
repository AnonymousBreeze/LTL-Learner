import os
current_path = os.getcwd()
import sys
sys.path.append(current_path)
from src.prompt_speedup import *
from tqdm import tqdm
import numpy as np
from nltk.translate.bleu_score import sentence_bleu
import pandas as pd
import time
import parameter_parser





def call(args):
    file = args.file
    prompt_path = args.prompt_path
    base_file_path = args.output_dir
    neigh_num = args.neigh_num
    engine = args.model
    prompt_type= args.prompt_type
    print(file)
    print(prompt_path)
    print(base_file_path)
    print(neigh_num)
    print(engine)
    print(prompt_type)
    translate_from_file(filename = file, prompt_type=prompt_type,neigh = neigh_num, engine = engine, prompt_path= prompt_path, output_filedir_path= base_file_path )
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The code execution is completed and it takes {execution_time} seconds in total.")
  

if __name__ == "__main__":
    start_time = time.time()
    args = parameter_parser.parse_args()
    call(args)
    
