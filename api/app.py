from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request, jsonify, g
import lights
import asyncio
import utilityfunctions
import json
import logging
from yaml import safe_load

#set up handler for logging
file_handler = logging.FileHandler(filename='logger/logfile.log')
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
file_handler.setLevel(logging.DEBUG)

#set root logger handler to be the configured file handler
root = logging.getLogger()
root.addHandler(file_handler)

app = Flask(__name__)

stream = open("config.yaml", "r")
conf = safe_load(stream)
stream.close()
app.config['SECRET_KEY'] = '2decf1d53dd9c26c755be2c6702bbfe568f15bab34097cde'
#lightList = lights.getAllLightsTest()
#commented out for testing when not on a network with lights.
lightList = asyncio.run(lights.getAllLights("192.168.254.255"))

@app.errorhandler(Exception)
def exception_handler(e):
    #response = e.get_response()
    #response.data = json.dumps({
    #    "code": e.code,
    #    "name": e.name,
    #    "description": e.description,
    #})
    #response.content_type = "application/json"
    app.logger.exception("An error occurred")
    return render_template("error.html")

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.before_request
def load_navs():
    navlinks = utilityfunctions.parseAppRoutes("./app.py")
    g.navlinks = navlinks

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/lightpanel', methods=['GET', 'POST'])
def lightpanel():
    global navlinks
    if request.method == 'POST':
        for light in lightList:
            input = request.form[f'{light.listNumber}']
            print(input)
            hexColor = input.lstrip('#')
            rgb = utilityfunctions.hexToRGB(hexColor)
            red = rgb[0]
            green = rgb[1]
            blue = rgb[2]
            asyncio.run(lights.setLightColor(light.ip, red, green, blue))
    return render_template("lightpanel.html", lightList=lightList)

@app.route('/setAllLights', methods=['GET', 'POST'])
def setAllLights():
    if request.method == 'POST':
        input = request.form['setColor']
        hexColor = input.lstrip('#')
        rgb = utilityfunctions.hexToRGB(hexColor)
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        for light in lightList:
            asyncio.run(lights.setLightColor(light.ip, red, green, blue))
    return render_template("setAllLights.html")

@app.route('/api/v1/setAll', methods=['GET','POST'])
def api_lights_set_all():
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data['color'])
        hexColor = data['color']
        rgb = utilityfunctions.hexToRGB(hexColor.strip())
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]

        if data['color'] and not data['color'].isspace():
            for light in lightList:
                asyncio.run(lights.setLightColor(light.ip, red, green, blue))
            return jsonify({'success': 'Successful request'})
        else:
            return jsonify({'error': 'Invalid JSON request'})
    elif request.method == 'GET':
        return jsonify({'':''})
    else:
        return ""

@app.route('/api/v1/toggle/', methods=['GET','POST'])
def api_lights_toggle():
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data['toggle'])
        if data['toggle'].lower() == 'on':
            for light in lightList:
                asyncio.run(lights.setLightPowerOn(light.ip))
            return jsonify({'success': 'Successful request'})
        elif data['toggle'].lower() == 'off':
            for light in lightList:
                asyncio.run(lights.setLightPowerOff(light.ip))
            return jsonify({'message': 'Successful request'})
        else:
            return jsonify({'message': 'Invalid JSON request'})
    elif request.method == 'GET':
        return jsonify({'message' : 'There are definitely some lights'})
    else:
        return ""

@app.route('/api/v1/sunset', methods=['GET','POST'])
def api_lights_sunset():
    hexColor = "DE3E3E"
    hexColor = conf['sunset']
    if request.method == 'POST':
        rgb = utilityfunctions.hexToRGB(hexColor.strip())
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        for light in lightList:
            asyncio.run(lights.setLightColor(light.ip, red, green, blue))
        return jsonify({'success': 'Successful request'})
    elif request.method == 'GET':
        return jsonify({'value': hexColor})
    return ""

@app.route('/api/v1/moon', methods=['GET','POST'])
def api_lights_moon():
    hexColor = "95B2C4"
    hexColor = conf['moon']
    if request.method == 'POST':
        rgb = utilityfunctions.hexToRGB(hexColor.strip())
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        for light in lightList:
            asyncio.run(lights.setLightColor(light.ip, red, green, blue))
        return jsonify({'success': 'Successful request'})
    elif request.method == 'GET':
        return jsonify({'value': hexColor})
    return ""

@app.route('/api/v1/sunrise', methods=['GET','POST'])
def api_lights_sunrise():
    hexColor = "E3E9D1"
    hexColor = conf['sunrise']
    if request.method == 'POST':
        rgb = utilityfunctions.hexToRGB(hexColor.strip())
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        for light in lightList:
            asyncio.run(lights.setLightColor(light.ip, red, green, blue))
        return jsonify({'success': 'Successful request'})
    elif request.method == 'GET':
        return jsonify({'value': hexColor})
    return ""

@app.route('/api/v1/noon', methods=['GET','POST'])
def api_lights_noon():
    hexColor = "FCFCFC"
    hexColor = conf['noon']
    if request.method == 'POST':
        rgb = utilityfunctions.hexToRGB(hexColor.strip())
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        for light in lightList:
            asyncio.run(lights.setLightColor(light.ip, red, green, blue))
        return jsonify({'success': 'Successful request'})
    elif request.method == 'GET':
        return jsonify({'value': hexColor})
    return ""

@app.route('/api/v1/evening', methods=['GET','POST'])
def api_lights_evening():
    hexColor = "D2C2BF"
    hexColor = conf['evening']
    if request.method == 'POST':
        rgb = utilityfunctions.hexToRGB(hexColor.strip())
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        for light in lightList:
            asyncio.run(lights.setLightColor(light.ip, red, green, blue))
        return jsonify({'success': 'Successful request'})
    elif request.method == 'GET':
        return jsonify({'value': hexColor})
    return ""

@app.route('/refreshLights', methods=['GET','POST'])
def refreshLights():
    if request.method == 'POST':
        global lightList
        lightList = asyncio.run(lights.getAllLights("192.168.254.255"))
    return render_template("refreshLights.html")

if __name__ == "__main__":
    app.logger.info('Started')
    app.run()

