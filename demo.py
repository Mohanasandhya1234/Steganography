import numpy as np

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def encode_image(image_path, message):
    img = Image.open(image_path)
    width, height = img.size
    binary_message = message_to_binary(message) + '1111111111111110'  # Adding a delimiter '1111111111111110' at the end

    if len(binary_message) > width * height * 3:
        raise ValueError("Message too long to encode in the image")

    data_index = 0
    binary_message_length = len(binary_message)

    img_array = np.array(img)

    for row in img_array:
        for pixel in row:
            r, g, b = pixel

            if data_index < binary_message_length:
                pixel[0] = r & ~1 | int(binary_message[data_index])
                data_index += 1

            if data_index < binary_message_length:
                pixel[1] = g & ~1 | int(binary_message[data_index])
                data_index += 1

            if data_index < binary_message_length:
                pixel[2] = b & ~1 | int(binary_message[data_index])
                data_index += 1

            if data_index >= binary_message_length:
                break

        if data_index >= binary_message_length:
            break

    encoded_image = Image.fromarray(img_array)
    encoded_image.save('encoded_image.png')
    print("Image encoded successfully.")

def decode_image(image_path):
    img = Image.open(image_path)
    img_array = np.array(img)

    binary_message = ''
    for row in img_array:
        for pixel in row:
            r, g, b = pixel
            binary_message += bin(r)[-1]
            binary_message += bin(g)[-1]
            binary_message += bin(b)[-1]

    binary_message_chunks = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''.join(chr(int(chunk, 2)) for chunk in binary_message_chunks)

    delimiter_index = message.find('1111111111111110')
    if delimiter_index != -1:
        message = message[:delimiter_index]

    print("Decoded message:", message)

if _name_ == "_main_":
    # Example usage:
    message = "Hello, this is a secret message!"
    image_path = "example_image.png"

    encode_image(image_path, message)
    decode_image("encoded_image.png")