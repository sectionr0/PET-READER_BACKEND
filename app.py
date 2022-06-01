import os
import os.path
import werkzeug
import cv2
from flask import Flask, jsonify, send_file, request
from flask_restful import Resource, Api, reqparse
from werkzeug.sansio.multipart import MultipartEncoder

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

            breed = yolov5.detect.run(weights="yolov5/runs/train/dogtest5_yolov5m_results2/weights/best.pt", source=file_path)
            safety = yolov5.detect.run(weights="yolov5/runs/train/dogsafety/best_safety.pt", source=file_path)
            muzzle = yolov5.detect.run(weights="yolov5/runs/train/dogmuzzle/dog-muzzle-best.pt", source=file_path)

            # print("result", breed, safety, muzzle)

            # 기본 세팅
            result_breed = False
            result_safety = False
            result_muzzle = False

            print("======result_breed======")
            print(breed["result"])
            count_breed_check1 = 0
            count_breed_check2 = 0
            count_breed_check3 = 0
            count_breed_check4 = 0

            for x in breed["result"]:
                if "Rottweiler" in x:
                    count_breed_check1 = count_breed_check1 + 1
                    # result_muzzle = True
                    # print("result_muzzle = True")
                elif "tosa" in x:
                    count_breed_check2 = count_breed_check2 + 1
                    # result_muzzle = True
                    # print("result_muzzle = True")
                elif "dangerous_dog" in x:
                    count_breed_check3 = count_breed_check3 + 1
                    # result_muzzle = True
                    # print("result_muzzle = True")
                else:
                    count_breed_check4 = count_breed_check4 + 1
                    # result_muzzle = False
                    # print("result_muzzle = False")
            print("======result_breed222======")
            print("count_breed_check1 ")
            print(count_breed_check1)
            print("count_breed_check2 ")
            print(count_breed_check2)
            print("count_breed_check3 ")
            print(count_breed_check3)
            print("count_breed_check4 ")
            print(count_breed_check4)

            max_count = max(count_breed_check1, count_breed_check2, count_breed_check3, count_breed_check4)

            print("max_count ")
            print(max_count)
            print("======result_breed222======")

            if max_count == count_breed_check1:
                result_breed = True
                print("result_breed = True")
            elif max_count == count_breed_check2:
                result_breed = True
                print("result_breed = True")
            elif max_count == count_breed_check3:
                result_breed = True
                print("result_breed = True")
            else:
                result_breed = False
                print("result_breed = False")

            print(breed["path"])
            # img_breed = cv2.imread(breed["path"], cv2.IMREAD_COLOR)
            # cv2.imshow('img_breed', img_breed)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            print("======result_breed======")

            # for abc in breed['result']:
            #     if "Dog" in abc:
            #         print(abc)
            #
            # for abc in breed['result']:
            #     print(abc)

            print("======result_safety======")
            print(safety["result"])
            count_safety_check1 = 0
            count_safety_check2 = 0

            for x in safety["result"]:
                if "leash-detect-not" in x:
                    count_safety_check2 = count_safety_check2 + 1
                else:
                    count_safety_check1 = count_safety_check1 + 1

            print("======result_safety222======")
            print("count_safety_check1 ")
            print(count_safety_check1)
            print("count_safety_check2 ")
            print(count_safety_check2)

            max_count_safety = max(count_safety_check1, count_safety_check2)

            print("max_count_safety ")
            print(max_count_safety)

            print("======result_safety222======")

            if max_count_safety == count_safety_check1:
                result_safety = True
                print("result_safety = True")
            else:
                result_safety = False
                print("result_safety = False")

            print(safety["path"])
            # img_safety = cv2.imread(safety["path"], cv2.IMREAD_COLOR)
            # cv2.imshow('img_safety', img_safety)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            print("======result_safety======")

            print("======result_muzzle======")
            print(muzzle["result"])
            count_muzzle_check1 = 0
            count_muzzle_check2 = 0

            for x in muzzle["result"]:
                if "no-muzzle" in x:
                    count_muzzle_check2 = count_muzzle_check2 + 1

                else:
                    count_muzzle_check1 = count_muzzle_check1 + 1


            print("======result_muzzle222======")
            print("count_muzzle_check1 ")
            print(count_muzzle_check1)
            print("count_muzzle_check2 ")
            print(count_muzzle_check2)

            max_count_muzzle = max(count_muzzle_check1, count_muzzle_check2)
            print("max_count_muzzle ")
            print(max_count_muzzle)

            print("======result_muzzle222======")

            if max_count_muzzle == count_muzzle_check2:
                result_muzzle = False
                print("result_muzzle = True")
            else:
                result_muzzle = True
                print("result_muzzle = False")

            print(muzzle["path"])
            # img_muzzle = cv2.imread(muzzle["path"], cv2.IMREAD_COLOR)
            # cv2.imshow('img_muzzle', img_muzzle)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            print("======result_muzzle======")

            # img = cv2.imread('lena.jpg', cv2.IMREAD_COLOR)
            # return send_file(
            #     img_breed, mimetype='image/jpeg'
            #     # img_safety,
            #     # img_muzzle
            # )

            # return send_file(
            #     img_muzzle,
            #     as_attachment = True,
            #     attachment_filename = 'test.jpg',
            #     mimetype = 'image/jpeg'
            # )

            # m = MultipartEncoder(fields={'markdown': "> Block quotes are written like so in markdown.",
            #                              'toPersonEmail': 'd@d.com',
            #                              'files': (img_muzzle, open(img_muzzle, 'rb'),
            #                                        'image.png')})
            #
            # return (m.to_string(), {'Content-Type': m.content_type})

            return jsonify({
                'result': file_path,
                'result_breed': result_breed,
                'result_muzzle': result_muzzle,
                'result_safety': result_safety,
                'result_breed_imgPath': breed['path'],
                'result_muzzle_imgPath': muzzle['path'],
                'result_safety_imgPath': safety['path']
            })

            # return send_file(breed["path"])


api.add_resource(Upload, '/upload')


@app.route('/download/breed')
def breed():
    json = request.get_json()
    return send_file(json['path'])


@app.route('/download/muzzle')
def muzzle():
    json = request.get_json()
    return send_file(json['path'])


@app.route('/download/safety')
def safety():
    json = request.get_json()
    return send_file(json['path'])


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
