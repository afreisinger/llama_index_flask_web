
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template, redirect, request
import os
import zipfile
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader


os.environ["OPENAI_API_KEY"] = 'sk-YOUTOKENDEOPENAI'
base_url = "http://localhost:5000"
#base_url = "https://chat2023.pythonanywhere.com"


from llama_index import GPTSimpleVectorIndex


#https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B
#inference = InferenceApi("bigscience/bloom",token='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')
#inference = InferenceApi("EleutherAI/gpt-j-6B",token='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')

#main_pickle_file = "search_index.contador.pickle"
#with open(main_pickle_file, "rb") as f:
#    search_index = pickle.load(f)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
#app.run(port=8888)

@app.route('/demo/<path:dir_name>')
def chat_demo(dir_name):
    try:
        directory = os.path.join(app.config['UPLOAD_FOLDER'], dir_name)
        files = os.listdir(directory)
        print(f'files in {dir_name}:{files}')
        if len(files) > 0:
            return render_template('chat_demo.html',dir_name=dir_name)
    except:
        pass
    return redirect(f"{base_url}/demo/{dir_name}/upload", code=302)
        


@app.route('/demo/<path:dir_name>/pregunta',methods=['GET','POST'])
def chat_demo_pregunta(dir_name):
    try:
        pregunta = request.json['question']
        response = get_index_answer(pregunta,dir_name)
    except:
        pregunta = ""
        response = "Pregunta vacia, respuesta vacia."
    
    return str(response).replace(r'\n','<BR>')

@app.route('/demo/<path:dir_name>/upload', methods=['GET', 'POST'])
def upload(dir_name):
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file:
                # create directory if it doesn't exist
                directory = os.path.join(app.config['UPLOAD_FOLDER'], dir_name)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # check if uploaded file is a zip
                if file.filename.endswith('.zip'): 
                    # extract files from zip to directory
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_ref.extractall(directory) 
                else:
                    # save file to directory
                    filename = file.filename
                    file.save(os.path.join(directory, filename))

                index_info = save_index(dir_name)
                print(f'index_info:{index_info}')

                return redirect(f"{base_url}/demo/{dir_name}", code=302)
        except Exception as ex:
            return render_template('chat_demo_upload.html', dir_name=dir_name, message=f'Hubo un error al subir y procesar el archivo:{ex}')

 
    return render_template('chat_demo_upload.html', dir_name=dir_name)


def save_index(dir_name):
    # proces docs and save index on same dir_name as dir_name.json
    directory = os.path.join(app.config['UPLOAD_FOLDER'], dir_name)
    json_file_name = os.path.join(app.config['UPLOAD_FOLDER'], dir_name, f'{dir_name}.json')

    # save to disk
    try:
        documents = SimpleDirectoryReader(directory).load_data()
        index = GPTSimpleVectorIndex.from_documents(documents)
        index.save_to_disk(json_file_name)
        return 'Index procesado correctamente'
    except Exception as ex:
        return f'Hubo un error procesando el index:{ex}'




def get_index_answer( pregunta , dir_name):

    try:
        directory = os.path.join(app.config['UPLOAD_FOLDER'], dir_name)
        json_file_name = os.path.join(app.config['UPLOAD_FOLDER'], dir_name, f'{dir_name}.json')
        # load from disk
        index = GPTSimpleVectorIndex.load_from_disk(json_file_name)
        response = index.query(pregunta)
        return response
    except Exception as ex:
        return f'Error:{ex}'


