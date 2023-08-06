import argparse
from cfg2qr import qr_transformations



def main():

    # Create parser and subparser
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    encoder = subparser.add_parser('encoder')
    decoder = subparser.add_parser('decoder') 

    #Add parser argument for input and result files path
    parser.add_argument(
        '--input_directory',
        type=str,
        required = True
    )


    
    #Add subparser encoder argument: file path to be encoded
    encoder.add_argument(
        '-input_text_name',
        type=str,
        required = True
    )

     #Add subparser encoder argument: encoded images
    encoder.add_argument(
        '-result_image_name',
        type=str,
        required = True
    )

    #Add subparser decoder argument:file path to be decoded
    decoder.add_argument(
        '-input_image_name',
        type=str,
        required=True
    )

    #Add subparser decoder argument:file path to be decoded
    decoder.add_argument(
        '-result_text_name',
        type=str,
        required=True
    )
  
    # Parse the argument
    args = parser.parse_args()


    if args.command == 'encoder':
        qr_transformations.encode(args.input_directory, args.input_text_name, args.result_image_name)
        print("Encoded QR code saved.")
    elif args.command == 'decoder':
        qr_transformations.decode(args.input_directory, args.input_image_name, args.result_text_name)
        print("Decoded text saved.")



if __name__ == "__main__":
    main()
    #print(type(open_yaml("data/","text2.yaml")))
    #python poupou.py --result_file './data/decoded_text.json' decoder -image_file './data/img_test_15.png'