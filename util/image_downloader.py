import requests
from PIL import Image
import io
import os

current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
data_directory = os.path.join(parent_directory, 'images')
# files_in_data_directory = os.listdir(data_directory)
print(data_directory)


def download_image(profile_name, address, url, dir_name, jail_name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(address)

        image = Image.open(io.BytesIO(response.content))
        resized_image = image.resize((500, 500))  # Set the desired size (e.g., 500x500)
        if address is None:
            with open(f'{data_directory}\\{dir_name}\\{profile_name} {jail_name}.jpg', 'wb') as file:
                resized_image.save(file, 'JPEG')
        else:
            with open(f'{data_directory}\\{dir_name}\\{profile_name} {address}.jpg', 'wb') as file:
                resized_image.save(file, 'JPEG')  # Save the resized image as JPEG

        print(f"Saved {profile_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        print(f"No photo for {profile_name}")


def download_daily_image(profile_name, address, url, dir_name, jail_name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(address)

        image = Image.open(io.BytesIO(response.content))
        resized_image = image.resize((500, 500))  # Set the desired size (e.g., 500x500)
        if address is None:
            with open(f'{data_directory}\\daily_images\\{dir_name}\\{profile_name} {jail_name}.jpg', 'wb') as file:
                resized_image.save(file, 'JPEG')
        else:
            with open(f'{data_directory}\\daily_images\\{dir_name}\\{profile_name} {address}.jpg', 'wb') as file:
                resized_image.save(file, 'JPEG')  # Save the resized image as JPEG

        print(f"Saved {profile_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        print(f"No photo for {profile_name}")
