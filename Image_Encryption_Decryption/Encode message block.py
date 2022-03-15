'''
Encoding 011 to (225, 12, 99)
225 - 11100001  => 11100000 - 224
12  - 1100      => 1101     - 13
99  - 1100011   => 1100011  - 99
Result = (224, 13, 99)

binary_key = ['01110101', '01100100']
binary_encrypted_message = ['01001011', '01100010']
image_data = [
(85, 85, 35), (78, 77, 33), (69, 65, 36), (61, 56, 37), (52, 48, 37), (51, 46, 40), 
(94, 91, 38), (87, 83, 36), (77, 72, 40), (68, 62, 40), (58, 52, 40), (53, 46, 38), 
(105, 96, 37), (97, 87, 34), (87, 78, 37), (76, 67, 38), (65, 56, 39), (58, 50, 39), 
(109, 104, 38), (103, 99, 38), (95, 89, 39), (83, 75, 38), (68, 60, 39), (60, 51, 36), 
(103, 114, 38), (104, 111, 41), (102, 103, 45), (90, 87, 42), (73, 66, 38), (64, 53, 35), 
(97, 116, 35), (100, 114, 39), (102, 108, 44), (93, 91, 42), (77, 70, 41), (66, 55, 35)
]
'''

image_data = [(225, 12, 99), (155, 2, 50), (99, 51, 15),
(15, 55, 22), (155, 61, 87), (63, 30, 17),
(1, 55, 19), (99, 81, 66), (219, 77, 91),
(69, 39, 50), (18, 200, 33), (25, 54, 190)]
binary_key = ['01110101']
binary_encrypted_message = ['01001011']


def encode_message(image_data, binary_key, binary_encrypted_message):
    
    def make_all_list(image_data):
        list_of_list = []
        for element in image_data:
            list_of_list.append(list(element))
        return list_of_list

    def concatenate(binary_key, binary_encrypted_message):
        clean = ''
        for bin in binary_key:
            clean += bin
        clean += '11111111'
        for bin in binary_encrypted_message:
            clean += bin
        clean += '11111111'
        return clean
    
    def make_all_tuple(list_modified_image_data):
        list_of_tuple = []
        for element in list_modified_image_data:
            list_of_tuple.append(tuple(element))
        return list_of_tuple
    
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


if __name__ == '__main__':
    print(encode_message(image_data, binary_key, binary_encrypted_message))
