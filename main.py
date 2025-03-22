from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

def open_image(image_path):
    try:
        with Image.open(image_path) as img:
            return img
    except Exception as e:
        return None

def get_metadata(image):
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            metadata = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value
            return metadata
        else:
            return "No EXIF metadata found."
    except Exception as e:
        return str(e)

def view_binary_data(image_path):
    try:
        with open(image_path, 'rb') as file:
            binary_data = file.read()
        return binary_data
    except Exception as e:
        return str(e)

def view_geolocation(image):
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            gps_info = exif_data.get(34853)
            if gps_info:
                gps_data = {}
                for tag, value in gps_info.items():
                    gps_data[TAGS.get(tag, tag)] = value
                return gps_data
            else:
                return "No GPS information found."
        else:
            return "No EXIF metadata found."
    except Exception as e:
        return str(e)

def destroy_metadata(input_image_path, output_image_path):
    try:
        # Open the input image
        img = Image.open(input_image_path)
        # Create a new image without EXIF data
        img_without_metadata = Image.new('RGB', img.size)
        img_without_metadata.putdata(list(img.getdata()))
        # Save the modified image without metadata
        img_without_metadata.save(output_image_path)
        return "Metadata successfully removed from the original image and saved as a new image."
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    while True:
        print("Choose an option:")
        print("1. View Metadata")
        print("2. View Binary Data")
        print("3. View Geolocation")
        print("4. Create New Image without Metadata")
        print("5. Exit")

        option = input("Enter the option number: ")

        if option == '1' or option == '2' or option == '3' or option == '4':
            image_path = input("Enter the path to the image file: ")
            if not os.path.exists(image_path):
                print("File not found. Please check the file path and try again.")
                continue

        img = open_image(image_path)

        if option == '1':
            if img is not None:
                metadata = get_metadata(img)
                if isinstance(metadata, dict):
                    print("Metadata:")
                    for key, value in metadata.items():
                        print(f"{key}: {value}")
                else:
                    print(metadata)
            else:
                print("Error opening the image.")

        elif option == '2':
            binary_data = view_binary_data(image_path)
            if isinstance(binary_data, bytes):
                print("Binary data:")
                print(binary_data)
            else:
                print(binary_data)

        elif option == '3':
            if img is not None:
                gps_metadata = view_geolocation(img)
                if isinstance(gps_metadata, dict):
                    print("Geolocation Information:")
                    for key, value in gps_metadata.items():
                        print(f"{key}: {value}")
                else:
                    print(gps_metadata)
            else:
                print("Error opening the image.")

        elif option == '4':
            if img is not None:
                new_image_path = input("Enter the path to save the new image without metadata: ")
                destroy_result = destroy_metadata(image_path, new_image_path)
                print(destroy_result)
            else:
                print("Error opening the image.")

        elif option == '5':
            break

        else:
            print("Invalid option. Please choose a valid option.")
