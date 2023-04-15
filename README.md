
## llama_index_flask_web

Este es un código de una aplicación web Flask muy simple que permite a los usuarios cargar documentos en una carpeta específica y hacer preguntas a través de una interfaz de chat. Cuando el usuario carga los documentos, se procesan utilizando la biblioteca llama_index, que utiliza GPT para indexar los documentos y proporcionar respuestas a las preguntas.

La aplicación incluye las rutas /demo/<path:dir_name>, /demo/<path:dir_name>/pregunta y /demo/<path:dir_name>/upload. La primera ruta muestra la página de chat que permite a los usuarios hacer preguntas a los documentos indexados. La segunda ruta procesa la pregunta y devuelve una respuesta utilizando el índice generado anteriormente. La tercera ruta maneja la carga de archivos y la indexación de documentos.

El código también incluye una función save_index que procesa los documentos en la carpeta de documentos y guarda el índice generado en un archivo .json en la misma carpeta. La función get_index_answer carga el índice generado y responde a las preguntas del usuario.

En general, este código es un ejemplo de cómo se puede construir una aplicación web simple que utiliza GPT para indexar documentos y proporcionar respuestas a preguntas específicas.


## Ejemplo

### Requires OpenAI API Key

### Install

```
git clone https://github.com/afreisinger/llama_index_flask_web && cd llama_index_flask_web
```

```
pip install -r requirements.txt

```

### Edit the app.py file with your keys and then run.

```
python3 app.py

```
### Note
macOS Monterey introduced AirPlay Receiver running on port 5000. This prevents your web server from serving on port 5000. Receiver already has the port.

You can either:

turn off AirPlay Receiver, or;
run the server on a different port (normally best)

```
flask run --host=0.0.0.0 --port=8888
```
or
```
python3 -m app.py 8888
```



### Go to browser

```
http://127.0.0.1:5000/demo/test
```
or
```
http://127.0.0.1:5000/demo/another_test_dir_name
```