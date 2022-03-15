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
                    break

    if buffer_counter == 2:
        return key, message
    else:
        return None, None

def make_all_list(image_data):
    list_of_list = []
    for element in image_data:
        list_of_list.append(list(element))
    return list_of_list