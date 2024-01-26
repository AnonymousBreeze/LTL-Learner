import argparse

def parse_args():
    parser = argparse.ArgumentParser(
                        prog = 'LTL_Learner',
                        description = 'Translates natural language to LTL formulas')

    parser.add_argument('--model', required=False, default="gpt-3.5-turbo", help='chose the LLM (gpt-3.5-turbo, gpt-4, gemini)')
    parser.add_argument('--file', required=True, default="", help='input file to batch translate') 
    parser.add_argument('--prompt_type', required=False, default="similar",  help='choose from (zero, few, similar)')
    parser.add_argument('--neigh_num', required=False, default="", help='number of similar neighbour')
    parser.add_argument('--keyfile', required=False, default="", help='provide your LLM api key (openai)')
    parser.add_argument('--prompt_path', required=False, default="", help='secifies the dir of the promptfile')
    parser.add_argument('--output_dir', required=False, default=64, help='where the result file will be stored')
    args = parser.parse_args()
    return args