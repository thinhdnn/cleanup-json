from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def remove_values(json_obj, values_to_remove):
    if isinstance(json_obj, dict):
        for key, value in list(json_obj.items()):
            if key in values_to_remove or value in values_to_remove:
                del json_obj[key]
            elif isinstance(value, dict) or isinstance(value, list):
                remove_values(value, values_to_remove)
    elif isinstance(json_obj, list):
        for item in json_obj:
            remove_values(item, values_to_remove)

def remove_keys(json_obj, keys_to_remove):
    if isinstance(json_obj, dict):
        for key in keys_to_remove:
            if key in json_obj:
                del json_obj[key]
        for key, value in json_obj.items():
            remove_keys(value, keys_to_remove)
    elif isinstance(json_obj, list):
        for item in json_obj:
            remove_keys(item, keys_to_remove)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        remove_list_str = request.form['remove_list']
        input_json_str = request.form['input_json']

        # Check if remove_list and input_json are valid JSON
        try:
            remove_list = json.loads(remove_list_str)
            input_json = json.loads(input_json_str)
        except json.JSONDecodeError:
            return render_template('index.html', error="Invalid JSON input or remove list")

        # Process JSON
        remove_values(input_json, remove_list)
        output_json = json.dumps(input_json, indent=4)

        return render_template('index.html', output=output_json, remove_list=remove_list_str, input_json=input_json_str)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
