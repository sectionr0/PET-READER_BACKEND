import os
import os.path
import subprocess
import werkzeug

from flask import Flask, jsonify, send_file
from flask_restful import Resource, Api, reqparse

import yolov5.detect

app = Flask(__name__)
api = Api(app)


class Upload(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        file_object = args['file']
        print(file_object)
        if file_object is None:
            return jsonify({'result': 'fail'})
        else:
            file_path = os.path.join(os.getcwd(), file_object.filename)

            file_object.save(dst=file_object.filename)
            print(file_path)

            breed = yolov5.detect.run(weights="yolov5/runs/train/dogtest5_yolov5m_results2/weights/best.pt",source=file_path)
            safety = yolov5.detect.run(weights="yolov5/runs/train/dogsafety/best_safety.pt", source=file_path)
            muzzle = yolov5.detect.run(weights="yolov5/runs/train/dogmuzzle/dog-muzzle-best.pt",
                                       source=file_path)

            # print("result", breed, safety, muzzle)

            # 기본 세팅
            result_breed = False
            result_safety = False
            result_muzzle = False


            print("======result_breed======")
            print(breed["result"])
            for x in breed["result"]:
                if "Rottweiler" in x:
                    result_muzzle = True
                    print("result_muzzle = True")
                elif "tosa" in x:
                    result_muzzle = True
                    print("result_muzzle = True")
                elif "dangerous_dog" in x:
                    result_muzzle = True
                    print("result_muzzle = True")
                else:
                    result_muzzle = False
                    print("result_muzzle = False")

            print(breed["path"])
            print("======result_breed======")

            print("======result_safety======")
            print(safety["result"])
            for x in safety["result"]:
                if "leash-detect" in x:
                    result_safety = True
                    print("result_safety = True")
                else:
                    result_safety = False
                    print("result_safety = False")

            print(safety["path"])
            print("======result_safety======")

            print("======result_muzzle======")
            print(muzzle["result"])
            for x in muzzle["result"]:
                if "muzzle" in x:
                    result_muzzle = True
                    print("result_muzzle = True")
                else:
                    print("result_muzzle = False")

            print(muzzle["path"])
            print("======result_muzzle======")

            send_file(

            )

            return jsonify({
                'result': file_path,
                'result_breed': result_breed,
                'result_muzzle': result_muzzle,
                'result_safety': result_safety
                            })


api.add_resource(Upload, '/upload')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
