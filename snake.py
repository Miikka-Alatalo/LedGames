#!/usr/bin/python3
from samplebase import SampleBase
import time
import sys
import threading
from flask import Flask, render_template, Response
from flask_restful import reqparse, Resource, Api
from random import randint

waitTime = 0.25

snakeColorR = 0
snakeColorG = 255
snakeColorB = 0

foodColorR = 255
foodColorG = 0
foodColorB = 0




app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('direction')

direction = "R";

class HelloWorld(Resource):
    def get(self):
        return {'direction': direction,
                'waitTime': waitTime}

    def put(self):
        args = parser.parse_args()
        try:
            global direction
            direction = args['direction']
        except Exception as e:
            return "fail", 400
        return "success", 200

class HelloHTML(Resource):
    def get(self):
        return Response(render_template('index.html'),mimetype='text/html')

api.add_resource(HelloWorld, '/api')
api.add_resource(HelloHTML, '/')

def startRest():
    app.run(host='192.168.10.50')

threadt = threading.Thread(target=startRest)
threadt.daemon = True

class SimpleClock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleClock, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()

        def printBlock(canvas, x, y, r, g, b):
            x=x*2
            y=y*2
            canvas.SetPixel(x, y, r, g, b)
            canvas.SetPixel(x+1, y, r, g, b)
            canvas.SetPixel(x, y+1, r, g, b)
            canvas.SetPixel(x+1, y+1, r, g, b)

        snakeXCoord = 0
        snakeYCoord = 0
        foodXCoord = randint(0,15)
        foodYCoord = randint(0,7)

        while True:
            # if the .txt reads 'stop' then exit everything
            if open("/home/sortsit/git/LedGames/shouldRun.txt").read() == "stop\n":
                print("txtStop")
                sys.exit(0)

            canvas = self.matrix.CreateFrameCanvas()



            if (direction == 'U'):
                snakeYCoord-=1
            elif (direction == 'D'):
                snakeYCoord+=1
            elif (direction == 'L'):
                snakeXCoord-=1
            elif (direction == 'R'):
                snakeXCoord+=1

            if (snakeXCoord > 15):
                snakeXCoord = 0
            elif (snakeXCoord < 0):
                snakeXCoord = 15
            if (snakeYCoord > 7):
                snakeYCoord = 0
            elif (snakeYCoord < 0):
                snakeYCoord = 7

            if(snakeXCoord == foodXCoord and snakeYCoord == foodYCoord):
                foodXCoord = randint(0,15)
                foodYCoord = randint(0,7)
            #food
            printBlock(canvas, foodXCoord, foodYCoord, foodColorR, foodColorG, foodColorB)

            #snake
            printBlock(canvas, snakeXCoord, snakeYCoord, snakeColorR, snakeColorG, snakeColorB)

            offset_canvas = self.matrix.SwapOnVSync(canvas)

            time.sleep(0.25)

if __name__ == "__main__":
    threadt.start()
    simple_clock = SimpleClock()
    if not simple_clock.process():
        simple_clock.print_help()
