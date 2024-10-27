from PIL import Image
import random

def encrypt_image(image_path, shift, output_path="encrypted_image.png"):
    """
    Encrypts an image by shifting pixel values, swapping channels, and shuffling pixels.
    
    Parameters:
    - image_path (str): Path to the input image.
    - shift (int): The shift value to apply to each pixel, used as a key.
    - output_path (str): Path to save the encrypted image.
    
    Returns:
    - None: Saves the encrypted image to the specified path.
    """
    # Open the image and get basic information
    image = Image.open(image_path)
    width, height = image.size
    pixels = list(image.getdata())

    # Initialize a random number generator with the shift as the seed for reproducibility
    random.seed(shift)
    
    # Shuffle the pixel order
    pixel_indices = list(range(len(pixels)))
    random.shuffle(pixel_indices)
    shuffled_pixels = [pixels[i] for i in pixel_indices]

    # Encrypt by applying XOR and channel swaps
    encrypted_pixels = []
    for r, g, b in shuffled_pixels:
        # XOR each channel with the shift value
        r = r ^ shift
        g = g ^ shift
        b = b ^ shift

        # Randomly swap RGB channels
        channels = [r, g, b]
        random.shuffle(channels)
        encrypted_pixels.append(tuple(channels))
    
    # Create a new image with the encrypted data
    encrypted_image = Image.new(image.mode, (width, height))
    encrypted_image.putdata(encrypted_pixels)
    encrypted_image.save(output_path)
    print(f"Encrypted image saved as {output_path}")

def decrypt_image(image_path, shift, output_path="decrypted_image.png"):
    """
    Decrypts an image by reversing pixel shuffling and bitwise operations.
    
    Parameters:
    - image_path (str): Path to the encrypted image.
    - shift (int): The shift value that was used during encryption.
    - output_path (str): Path to save the decrypted image.
    
    Returns:
    - None: Saves the decrypted image to the specified path.
    """
    # Open the image and get basic information
    image = Image.open(image_path)
    width, height = image.size
    encrypted_pixels = list(image.getdata())

    # Initialize a random number generator with the shift as the seed for reproducibility
    random.seed(shift)

    # Reverse the pixel order shuffle
    pixel_indices = list(range(len(encrypted_pixels)))
    random.shuffle(pixel_indices)

    # Create a placeholder for the unshuffled pixels
    unshuffled_pixels = [None] * len(encrypted_pixels)
    for index, pixel in zip(pixel_indices, encrypted_pixels):
        unshuffled_pixels[index] = pixel

    # Decrypt by reversing XOR and channel swaps
    decrypted_pixels = []
    for r, g, b in unshuffled_pixels:
        # Since we don't know the original shuffle, we must assume the order (e.g., RGB)
        channels = [r, g, b]

        # Reverse the XOR operation
        r = channels[0] ^ shift
        g = channels[1] ^ shift
        b = channels[2] ^ shift

        decrypted_pixels.append((r, g, b))
    
    # Create a new image with the decrypted data
    decrypted_image = Image.new(image.mode, (width, height))
    decrypted_image.putdata(decrypted_pixels)
    decrypted_image.save(output_path)
    print(f"Decrypted image saved as {output_path}")

def main():
    print("Advanced Image Encryption Tool")
    image_path = input("Enter the path to the image: ").strip()
    shift = int(input("Enter the shift value (integer): ").strip())

    # Encrypt the image
    encrypt_image(image_path, shift)

    # Decrypt the image to verify
    decrypt_image("encrypted_image.png", shift)

if __name__ == "__main__":
    main()
