import os
import openai
from tqdm import tqdm
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu
import pandas as pd
import time
import logging
import sys
from src.recommendation import *
from src.Global import *

start_time = time.time()

def add_new_prompt(nl, sub_translation_data, file):
    with open(file, 'a') as f:
        Explanation_dictionary = "{"
        for sub_prompt in sub_translation_data:
            sub_exp = sub_prompt['sub_expression']
            sub_formula = sub_prompt['ltl_formula']
            if sub_exp == nl:
                ltl = sub_formula
                continue
            Explanation_dictionary += "\""+sub_exp+"\" : \"" + sub_formula + "\", "


        if len(sub_translation_data) > 1:
            Explanation_dictionary = Explanation_dictionary[:-2]
        Explanation_dictionary += "}"
        Text_to_append = "\nNatural Language: " + nl + "\n"
        Text_to_append += "Explanation dictionary: " + Explanation_dictionary + "\n"
        Text_to_append += "So the final LTL translation is: " + ltl + ".FINISH\n" 
        f.write(Text_to_append)

def parse_prompt_file(filepath):
    NL_list = []
    explanations = []
    final_ltl = []
    examples_list = []
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Natural Language:'):
                target_nl = line.split('Natural Language: ')[1]
                NL_list.append(target_nl)
            elif line.startswith("Explanation dictionary:"):
                explanations.append(line)
            elif line.startswith("So the final LTL translation is:"):
                if line.split('So the final LTL translation is:')[1] == "":
                    continue
                final_ltl.append(line)
                examples_list.append({
                    "NL" : NL_list[-1],
                    "explanation": explanations[-1],
                    "ltl": final_ltl[-1]
                })
    return NL_list, examples_list
    

def create_best_prompt(nl_to_translate,similar_neighbour_num = 10, source_prompt_file = ""):
    prompt_path = os.path.join(project_dir, 'prompt_set')
    NL_list = []
    examples_list = []
    if source_prompt_file != "":
        NL_list, examples_list = parse_prompt_file(source_prompt_file)
    else:    
        for prompt_file in os.listdir(prompt_path):
            if prompt_file.endswith(".txt"):
                filepath = os.path.join(prompt_path, prompt_file)
                NL_list, examples_list = parse_prompt_file(filepath)

    top_k_example = get_recommendations_from_strings(nl_to_translate,NL_list, int(similar_neighbour_num))
    top_k_list = [examples_list[i] for i in top_k_example]
    similar_file = f'{prompt_path}/Similar/prompt_similar_{similar_neighbour_num}.txt'
    with open(similar_file, 'w') as prompt_file:
        prompt_file.write("You are a Linear Temporal Logic (LTL) expert. Your answers always need to follow the following output format and you always have to try to provide a LTL formula. You may repeat your answers.\n")
        prompt_file.write("Translate the following natural language sentences into an LTL formula and explain your translation step by step.\n")
        prompt_file.write("Remember that X means 'next', U means 'until', G means 'globally', F means 'finally', which means GF means 'infinitely often'. Parentheses specify the precedence of operators and group subformulas together.\n")
        prompt_file.write("The formula should only contain atomic propositions, operators, and parentheses: |, &, !, ->, <->, X, U, G, F, (, ).\n\n")
        prompt_file.write("***MUST answer in this format:***\n")
        prompt_file.write("[\nExplanation dictionary:\nSo the final LTL translation is: \n]\n\nExamples:\n\n")
        for entry in top_k_list:
            prompt_file.write("INPUT" + '\n')
            prompt_file.write("Natural Language: " + entry["NL"] + '\n')
            prompt_file.write("OUPUT" + '\n')
            prompt_file.write(entry["explanation"] + '\n')
            prompt_file.write(entry["ltl"] + '\n')
            prompt_file.write('\n')

    return similar_file
        
    

def gpt_answer(prompt, engine_model):
    while True:
        try:
            response = openai.ChatCompletion.create(
                        model=engine_model,
                        messages = [{"role": "user", "content": prompt}],
                        temperature=0,
                        stop="FINISH",
                    )
            output = response["choices"][0]["message"]["content"]
            return output
        except openai.error.RateLimitError as e:
            print("Rate limit reached, sleeping for 60 seconds...")
            time.sleep(60)



def gemini_answer(prompt):
  while True:
        try:
            response = Gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print("Error! retry after for 30 seconds...")
            time.sleep(30)

def split_formula_to_get_final_LTL(original_answer):

    marker = "the final LTL translation is: "
    suffix = "."
    start_index = original_answer.find(marker)
    if start_index == -1:
        return original_answer
    start_index += len(marker)
    original_answer = original_answer[start_index:]

    suffix_index = original_answer.find(suffix)
    if suffix_index == -1:
        return original_answer
    ans = original_answer[:suffix_index].strip()
    return ans


def translate_by_gpt(source_nl,model = "gpt-3.5-turbo"):
    file = "prompt_set/static/static_prompt.txt"
    final_answer = ""
    status = STATUS.SUCCESS
    try:
        with open(file, 'r') as prompt_file:
            prompt_profix = prompt_file.read()
            final_prompt = (prompt_profix + "\nNatural Language: " 
                            + source_nl )
            response = gpt_answer(final_prompt, model)
            final_answer = split_formula_to_get_final_LTL(response)
    except Exception as e:
        status = STATUS.ERROR
        print("Error: {}".format(e))
    return final_answer, status

def translate_by_gpt_0_shot(source_nl,engine_model = "gpt-3.5-turbo"):
    final_answer = ""
    status = STATUS.SUCCESS
    prompt_path = os.path.join(project_dir, 'prompt_set')
    prompt_file =  os.path.join(prompt_path, "zS/prompt_zero_shot.txt")
    try:
        with open(prompt_file, 'r') as file:
            prompt_profix = file.read()
        final_prompt = (prompt_profix + "\nNatural Language: " 
                        + source_nl )
        response = gpt_answer(final_prompt, engine_model)
        
        final_answer = split_formula_to_get_final_LTL(response)
    except Exception as e:
        status = STATUS.ERROR
        print("Error: {}".format(e))
        print("="*100)

    

    return final_answer, status

# Our Method
def translate_by_gpt_similar(source_nl,model = "GPT35",prompt_type = "dynamic", temperature = 0, prompt_path ="", neigh_num = 10):
    final_answer = ""
    status = STATUS.SUCCESS
    try:
        if prompt_type == "dynamic":
            file = create_best_prompt(source_nl, neigh_num ,prompt_path)
        elif prompt_type == "static":
            file = "prompt_set\static\static_prompt.txt"
        else:  # zero-shot
            file = "prompt_set\zS\prompt_zero_shot.txt"

        if model == "GPT35" or model == "gpt-3.5-turbo":
            engine = "gpt-3.5-turbo"
        elif model == "GPT4" or model == "gpt-4":
            engine = "gpt-4"
        elif model == "gpt-4-1106-preview":
            engine = "gpt-4-1106-preview"
        
        with open(file, 'r') as prompt_file:
            prompt_profix = prompt_file.read()
            final_prompt = (prompt_profix + "\nNatural Language: " 
                            + source_nl )
            if model == "Gemini" or model == "gemini":
                print("Using Gemini")
                response = gemini_answer(final_prompt)
            else:
                response = gpt_answer(final_prompt,engine)
            final_answer = split_formula_to_get_final_LTL(response)

    except Exception as e:
        status = STATUS.ERROR
        print("Error: {}".format(e))
    return final_answer, status



def translate_excel(excel_file):
    df = pd.read_excel(excel_file)

    translated_data = []
    for nl_text in df.iloc[:, 0]:  
        ltl_translation = translate_by_gpt_similar(nl_text)
        translated_data.append([nl_text, ltl_translation[0]])

    translated_df = pd.DataFrame(translated_data, columns=['NL', 'LTL'])  

    translated_excel_file = 'translated_excel.xlsx'
    with pd.ExcelWriter(translated_excel_file, engine='xlsxwriter') as writer:
        translated_df.to_excel(writer, sheet_name='Sheet1', index=False)

    return translated_excel_file


def translate_from_file(filename, prompt_type = 'similar',neigh = 10,engine = "gpt-3.5-turbo",prompt_path = "",output_filedir_path=""):
    df = pd.read_excel(filename)
    data = []
    print("Start")
    print("=" * 50)
    ltl_exists = 'ltl' in df.columns
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        nl = row['en']  
        ltl = row['ltl'] if ltl_exists else None  
        # zero-shot
        if prompt_type == 'zero':
            nl_translation = translate_by_gpt_0_shot(nl,engine)
        elif prompt_type == 'few': # few-shot
            nl_translation = translate_by_gpt(nl,engine)
        elif prompt_type == 'similar':
            nl_translation = translate_by_gpt_similar(source_nl=nl,model=engine,neigh_num=neigh,prompt_path=prompt_path)
        if ltl_exists:
            truth_ltl = ltl.strip()
            result = nl_translation[0].replace(" ", "") == truth_ltl.replace(" ", "")
            reference = list(truth_ltl.replace(" ",""))  
            candidate = list(nl_translation[0].replace(" ", ""))  
            score = sentence_bleu([reference], candidate, weights=(0.5,0.5,0,0))
            data.append([nl, nl_translation[0].replace(" ", ""), truth_ltl.replace(" ", ""), result, score])
        else:
            data.append([nl, nl_translation[0].replace(" ", "")])
    # Create new DataFrame to store results
    if ltl_exists:
        columns = ['NL', 'LTL', 'Truth_LTL', 'Result', 'BLEU']
    else:
        columns = ['NL', 'LTL']   
 
    result_df = pd.DataFrame(data, columns=columns)

    end_time = time.time()
    execution_time = end_time - start_time
    rounded_value = round(execution_time, 3)
    if output_filedir_path != "":
        base_file_name = output_filedir_path + f"/syn_{engine}_{prompt_type}_{rounded_value}_neigh={neigh}"
    else:    
        base_file_name = f'Exp/TranslationResult_{engine}_{prompt_type}_{rounded_value}_neigh={neigh}'
    
    # Check for existing file and increment the suffix number until an unused name is found
    counter = 1
    file_name = f"{base_file_name}_1.xlsx"  # start with _1
    while os.path.exists(file_name):  # if file exists, increment the counter and try a new file name
        counter += 1
        file_name = f"{base_file_name}_{counter}.xlsx"
    
    result_df.to_excel(file_name, index=False)

    prompt_file_list = []
    prompt_path = os.path.join(project_dir, 'prompt_set')
    for prompt_file in os.listdir(prompt_path):
        if prompt_file.endswith(".txt"):
            filepath = os.path.join(prompt_path, prompt_file)
            prompt_file_list.append(filepath)

    
    print(f"The code execution is completed and it takes {execution_time} seconds in total.")
    print(f'Results for {prompt_type} method saved to {file_name}')
    return file_name
    

if __name__ == "__main__":
    filename = "Dataset\Dataset_2.xlsx"
    prompt_path = "prompt_set\Exp II\prompt_iteration_3_num=25.txt"
    translate_from_file(filename, prompt_type="similar", engine = "GPT35", prompt_path = prompt_path)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The code execution is completed and it takes {execution_time} seconds in total.")
