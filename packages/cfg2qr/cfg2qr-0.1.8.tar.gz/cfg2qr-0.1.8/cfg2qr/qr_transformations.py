import qrcode
import cv2
import json

from cfg2qr import file_manip


def check_file_type(file_name):



    _, ext = file_name.split(".")

    return ext #type str

    



def encode(path,input_file,image_save):

    

    if check_file_type(input_file)=='json': 

        input_dictionary=file_manip.open_json(path, input_file)

    elif check_file_type(input_file)=='yaml':

        input_dictionary=file_manip.open_yaml(path, input_file)

    else: 

        print("problem reading file")

    

    input_text = json.dumps(input_dictionary)

    img = qrcode.make(input_text)

    type(img)  # qrcode.image.pil.PilImage

    file_path=path + image_save
    img.save(file_path)



def decode(path, image_file,decoded_file):

    file_path=path + image_file

    image = cv2.imread(file_path)

    qrCodeDetector = cv2.QRCodeDetector()

    

    decoded_text, points, _ = qrCodeDetector.detectAndDecode(image)

    points = points.astype(int)

    

    result_dict=json.loads(decoded_text)

    

    if points is not None:

        # QR Code detected handling code

        if check_file_type(decoded_file)=='json': 

            file_manip.save_json(path, result_dict,decoded_file)

        elif check_file_type(decoded_file)=='yaml':

            file_manip.save_yaml(path, result_dict,decoded_file)

        else: 

            print("Problem saving file")

            

    else:

        print("QR code not detected")
