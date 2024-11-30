from flask import Flask, request, jsonify, send_file
import datetime
from PIL import Image, ImageDraw, ImageFont
import sys
import os

def generate_answer_image(input_text, output_name):

    bg_image_width = 697
    bg_image_height = 135
    font_size = 85
    font_path = "./src/font.ttf"
    text = input_text
    output_file = output_name
    color = (236,75,104)
    bg_img = "./src/bg.png"


    if len(text) > 10:
        raise ValueError("Text exceeds the maximum limit of 10 characters.")

    image = Image.open(bg_img)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("ERROR FONT FILE FOUND")
        sys.exit()

    text_width, text_height = draw.textsize(text, font=font)
    x_position = (bg_image_width - text_width) // 2
    y_position = (bg_image_height - text_height) // 2
    draw.text((x_position, y_position), text, color, font=font)

    # Save the image
    image.save(output_file)
    print(f"Image saved as {output_file}")


def clean_generations(directory_path):
    try:
        for filename in os.listdir(directory_path):
            if filename.endswith('.png'):
                os.remove(os.path.join(directory_path, filename))
        return "All files deleted successfully."
    except:
        return "Error occurred while deleting files."
    


app = Flask(__name__)

@app.route('/generate_image', methods=['GET'])
def generate():
    ct =  datetime.datetime.now()
    image_name = f"{str(ct).replace(' ','-').replace('.','-')}.png"
    output_image = f"./exports/{image_name}"
    text = request.args.get('text')
    generate_answer_image(text, output_image)

    return send_file(output_image, mimetype='image/png')

@app.route('/clean', methods=['GET'])
def clean():
    out = clean_generations('./exports')
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
    app.run()