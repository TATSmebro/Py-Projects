import os #file manipulation
from PIL import Image #image manipulation

def main(): #Main menu
    #Asks for process
    processes = ['encrypt', 'decrypt', 'exit']
    inp = input('Select program mode: (encrypt/decrypt/exit): ')
    
    #Incase of invalid input
    while not(inp in processes):
        print('Invalid input, chooose a different item!')
        inp = input('Select program mode: ')
    
    #Checks if file exists
    if inp == 'encrypt' or inp == 'decrypt':
        file = input('Enter image filename: ')
        file_path, image_file = os.path.split(file)
        file_name, file_extension = os.path.splitext(image_file)

        #Incase of invalid file
        while not(os.path.exists(file)) or (file_extension != '.jpg' and file_extension != '.jpeg'):
            print('Invalid image file.')
            file = input('Enter image filename: ')
            file_path, image_file = os.path.split(file)
            file_name, file_extension = os.path.splitext(image_file)
        
        #Fetch image data and save path
        image_size, image_data = load_image_data(file)
        txt_save_path = os.path.join(os.getcwd() + '\output', file_name + '_decoded_message.txt')
        img_save_path = os.path.join(os.getcwd() + '\output', 'modified_' + image_file)

        #Directs program to next process
        if inp == 'encrypt': #encryption
            secret_key, message = get_data_to_encrypt(image_size)
            encrypted_message = encrypt_text(message, secret_key)
            bin_key = ascii_to_binary(char_to_ascii(secret_key))
            bin_encrypted_message = ascii_to_binary(char_to_ascii(encrypted_message))
            modified_image_data = encode_message(image_data, bin_key, bin_encrypted_message)
            save_image_to_file(img_save_path, image_size, modified_image_data)

        if inp == 'decrypt': #decryption
            decoded_message = bin_key, bin_encrypted_message = decode_message(image_data)
            if decoded_message == (None, None) or bin_key == [] or bin_encrypted_message == []:
                print('Error: cannot decode message!')
                main()
            else:
                secret_key = binary_to_ascii_string(bin_key)
                encrypted_message = binary_to_ascii_string(bin_encrypted_message)
                message = decrypt_text(encrypted_message, secret_key)
                save_file(txt_save_path, message)

    #Exit block
    if inp == 'exit':
        print('Thank you for using this program!')

def get_data_to_encrypt(image_size):
    
    #Get key and message
    key = input('Enter Key: ')
    message = input('Enter Message: ')

    #Checks if all characters in key are valid
    matched_list = [character == 'u' or character == 'd' for character in key]
    key_flag = all(matched_list)

    #Checks if all characters in message are valid
    message_matched_list = [32 <= ord(character) <= 126 for character in message]
    message_flag = all(message_matched_list)
    
    #Checks if key is valid and loops otherwise
    min_pixels = (len(message) + len(key)) * 8 / 3 + 6
    min_pixels_round_up = int(-(-min_pixels // 1))

    if not(3 <= len(key) <= 20) or key_flag == False or not(10 <= len(message) <= 1000) or message_flag == False:
        print('Invalid Key/Message. Please Try again.')
        return get_data_to_encrypt(image_size)
    
    if ((image_size[0]*image_size[1]) < min_pixels_round_up):
        print('Message and Key cannot fit in the image')
        return get_data_to_encrypt(image_size)
    
    else:
        return key, message

def load_image_data(filename):
    image = Image.open(filename) #Opens image
    size = image.size #Fetches image dimension
    image_data = list(image.getdata()) #Fetches image pixel data
    image.close() #Closes image
    return size, image_data

def save_image_to_file(filename, image_dimension, image_data):
    new_image = Image.new('RGB', image_dimension) #Creates a new RGB image with the specified image dimension
    new_image.putdata(image_data) #Applies specified image data to image file
    new_image.save(filename, format='png') #Saves new image file
    main()

def encrypt_text(text, key):
    encrypted_text = '' #This is where we store the encrypted characters

    #Encryption proper
    curr_key = 0
    for character in text:

        curr_shift = key[curr_key] #This determines whether we shift up or down

        #This code encrypts the given string
        if curr_shift == 'u':
            encrypted_text += chr((ord(character)+len(key)-32)%95+32)
        else:
            encrypted_text += chr((ord(character)-len(key)-32)%95+32)

        #This code loops the key
        if curr_key + 1 < len(key):
            curr_key += 1    
        else:
            curr_key -= len(key) - 1

    return encrypted_text
   
def decrypt_text(encrypted_text, key):
    decrypted_text = '' #This is where we store the decrypted characters

    #Checks if all characters are valid
    matched_list = [character == 'u' or character == 'd' for character in key]
    flag = all(matched_list)
    
    #Checks if key is valid and presents an error message otherwise
    if key == '' or flag == False or encrypted_text == '':
        print('Error: cannot decode message!')
        main() #directs back to main menu
    else:
        #Decryption proper
        curr_key = 0
        for character in encrypted_text:

            curr_shift = key[curr_key] #This determines whether  we shift up or down

            #This code encrypts the given string
            if curr_shift == 'd':
                decrypted_text += chr((ord(character)+len(key)-32)%95+32)
            else:
                decrypted_text += chr((ord(character)-len(key)-32)%95+32)

            #This code loops the key
            if curr_key + 1 < len(key):
                curr_key += 1    
            else:
                curr_key -= len(key) - 1

        return decrypted_text

def char_to_ascii(word):
    ascii_values = [] #Stores ascii values
    for character in word: #iterates on every character on the given word
        ascii_values.append(ord(character)) #appends ascii converted characters
    return ascii_values
  
def ascii_to_binary(ascii_values):
    binary_values = [] #stores binary values
    for value in ascii_values: #iterates over all values in ascii list
        binary = bin(value)[2:] #converts ascii to binary and truncates the first two characters '0b'
        
        #converts converted binary into 8-bit binary
        while len(binary) < 8:
            binary = '0' + binary

        binary_values.append(binary) #appends converted 8-bit 
    return binary_values

def binary_to_ascii_string(binary_values):
    ascii = [] #stores values converted into ascii
    string = '' #stores values converted into string
    
    #converts binary to ascii decimal
    for binary in binary_values:
        ascii.append(int(binary, 2))

    #converts ascii to string
    for value in ascii:
        string += chr(value)
    return string

def encode_message(image_data, binary_key, binary_encrypted_message):
    
    list_image_data = make_all_list(image_data)
    bin_to_encode = concatenate(binary_key, binary_encrypted_message) 
    list_modified_image_data = []
    tracker = 0

    for pixel in list_image_data:
        new_pixel = []
        for pel in pixel:
            if tracker <= len(bin_to_encode)-1:
                new_pixel.append(int(bin(pel)[2:-1]+bin_to_encode[tracker], 2))
                tracker += 1
            else:
                new_pixel.append(pel)
        list_modified_image_data.append(new_pixel)
    return make_all_tuple(list_modified_image_data)

def decode_message(image_data):

    list_image_data = make_all_list(image_data)
    key = []        
    message = []
    buffer_counter = 0
    byte = ''
    for pixel in list_image_data:
        for pel in pixel:
            byte += bin(pel)[-1]
            if buffer_counter == 0:            
                if len(byte) == 8 and byte != '11111111':
                    key.append(byte)
                    byte = ''
                if byte == '11111111':
                    buffer_counter += 1
                    byte = ''
            else:
                if len(byte) == 8 and byte != '11111111':
                    message.append(byte)
                    byte = ''
                if byte == '11111111':
                    buffer_counter += 1
                    return key, message
    return None, None

def make_all_list(image_data):
    list_of_list = []
    for element in image_data:
        list_of_list.append(list(element))
    return list_of_list
    
def make_all_tuple(list_modified_image_data):
    list_of_tuple = []
    for element in list_modified_image_data:
        list_of_tuple.append(tuple(element))
    return list_of_tuple

def concatenate(binary_key, binary_encrypted_message):
    clean = ''
    for bin in binary_key:
        clean += bin
    clean += '11111111'
    for bin in binary_encrypted_message:
        clean += bin
    clean += '11111111'
    return clean

def save_file(filename, text):
    file = open(filename, 'w')
    file.write(text)
    file.close()
    main()


if __name__ == '__main__':
    main()