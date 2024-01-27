# Overview

The LTL-Learner tool is dedicated to efficiently transforming unstructured natural language requirements into formalized Linear Temporal Logic specifications. Our innovative approach integrates human-driven prompts with large language models, optimizing the translation process through interactive prompt engineering. This significantly enhances the model's understanding of specific terminologies and language ambiguities. The primary advantage of our tool lies in its memory capability and mechanism for improving translation errors, making LTL-Learner particularly suited for automated batch translations in industrial settings. Verified on public datasets, our method demonstrates a significant improvement in translation accuracy and reliability. For verifiability and reproducibility, all research content is thoroughly documented and referenced within this project.

 
# Install

- python==3.9
- Nodejs==20.11.0
- Every thing in requirements.txt ```pip install -r requirements.txt```


# Preparation
Create the following file and paste your open ai, gemini key into: Keys/oai_key.txt, keys/gemini_key.txt 

# Quick Start with frontend

Start the backend

    python app_start.py

In a new terminal, set up the front end:

    cd Front
    npm i   (Administrator)
    npm run dev
Access the application via the provided website link.

# Quick Start form terminal
## ExpI example
```python src/file_translation.py --model gpt-3.5-turbo --file Dataset/Dataset_1.xlsx --prompt_path prompt_set/ExpI/ExpI_D/SUM_prompt_set.txt  --output_dir Exp/ExpI/GPT35_D/ --prompt_type similar --neigh_num 20 ```

```python src/file_translation.py --model gpt-3.5-turbo --file Dataset/Dataset_1.xlsx --prompt_path prompt_set/nl2spec/nl2spec_prompt.txt  --output_dir Exp/ExpI/nl2spec/ --prompt_type similar --neigh_num 20```
## ExpII example

```python src/file_translation.py --model gpt-3.5-turbo --file Dataset/Dataset_2.xlsx --prompt_path prompt_set/ExpII/prompt_iteration_1_num=5.txt  --output_dir Exp/ExpII/Syn/1_iteration/ --prompt_type similar --neigh_num 20 ```

## ExpIV example(Gemini)
```python src/file_translation.py --model gemini --file Dataset/Dataset_1.xlsx --prompt_path prompt_set/ExpI/ExpI_D/SUM_prompt_set.txt  --output_dir Exp/ExpIV/ --prompt_type similar --neigh_num 20```


