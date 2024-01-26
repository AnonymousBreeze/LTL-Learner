from flask import Flask, render_template, request, jsonify, send_file
from src.Global import *
from src.prompt_speedup import *
import pandas as pd
app = Flask(__name__)
from flask_cors import CORS
CORS(app)


@app.route('/batch_translate', methods=['POST'])
def batch_translate():
    uploaded_file = request.files['excelFile']
    if uploaded_file.filename != '':
        upload_path = os.path.join(project_dir,"Dataset\\uploaded_excel.xlsx")
        uploaded_file.save(upload_path)

        translated_excel_file = translate_from_file(upload_path)   
        return send_file(translated_excel_file, as_attachment=True)

    return 'No file uploaded.'

@app.route('/convert_nl_to_ltl', methods=['POST'])
def convert_nl_to_ltl():
    if request.method == 'POST':
        nl_input = request.form.get('nlInput')
        set_global_natual_language(nl_input)
        print("nl_input = " + nl_input)

        ltl_result = ""   
        model = request.form.get('model')
        prompt_type = request.form.get('prompt_type') #  dynamic, static, zero-shot
        temperature = request.form.get('temperature')  # 0-1
        print("model = " + model)
        print("prompt_type = " + prompt_type)
        print("temperature = " + temperature)
        ltl_result, status = translate_by_gpt_similar(nl_input,model,prompt_type,temperature)
        status_data = status.value
        print("result = " + ltl_result )
        return jsonify({"ltlResult": ltl_result, "status":status_data})
    
@app.route('/optimize_prompt', methods=['POST','GET'])
def open_optimize_prompt():
    nl_input = request.args.get('nlInput')
    print("="*100)
    # print("测试： nl_input:" + nl_input)
    return render_template('optimize_prompt.html',nlInput = nl_input)

@app.route('/submit_new_prompt', methods=['POST'])
def submit_new_prompt():
    data = request.get_json()  
    file = "prompt_set/new_prompt.txt"
    nl = data['nl']
    sub_translate = data['rule']
    add_new_prompt(nl,sub_translate, file)
    print("Add new translation rule in " + file )
    # 返回成功响应
    return jsonify({'message': 'Success'})


if __name__ == '__main__':
    app.run(debug=True)
