from flask import Flask, request, jsonify, send_file
import utils
import datetime

app = Flask(__name__)

@app.route('/generate_image', methods=['GET'])
def generate():
    ct =  datetime.datetime.now()
    image_name = f"{str(ct).replace(' ','-').replace('.','-')}.png"
    output_image = f"./exports/{image_name}"
    text = request.args.get('text')
    utils.generate_answer_image(text, output_image)

    return send_file(output_image, mimetype='image/png')

@app.route('/clean', methods=['GET'])
def clean():
    out = utils.clean_generations('./exports')
    status = {
        'status' : out
    }
    return jsonify(status)

@app.route('/', methods=['GET'])
def root():
    return "<h1>WELCOME TO POPQUEST API </h1>"

'''
@app.route('/generate_answer')
def generate_answer():
    ct =  datetime.datetime.now()
    image_name = f"{str(ct).replace(' ','-').replace('.','-')}.png"
    output_image = f"./exports/{image_name}"
    
    text = request.args.get('text')

    utils.generate_answer_image(text, output_image)
    data = {
        'text' : text,
        'image_name' : image_name,
        'path' : output_image
    }
    return jsonify(data)
'''


if __name__ == '__main__':
    app.run(debug=True)