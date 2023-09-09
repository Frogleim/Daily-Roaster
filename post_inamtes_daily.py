import json
import requests
import base64
import re
import time
from util import files_reader, image_downloader, driver_provider


def read_daily_json(jail_name):
    file_path = f'./data/daily_inmates_data/{jail_name}.json'
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def read_images(image_name, jail_name, address=None):
    try:
        with open(f'./images/daily_images/images_{jail_name}/{image_name} {address or jail_name}.jpg', 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception:
        with open(f'./images/image_placeholeder.jpg', 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string


def read_image(image_name, jail_name, address=None):
    with open(f'./images/daily_images/images_{jail_name}/{image_name} {address or jail_name}.jpg', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string


def restImgUL(img_name, jail_name, address=None):
    try:
        data = open(f'./images/daily_images/images_{jail_name}/{img_name} {address or jail_name}.jpg', 'rb').read()
        res = requests.post(url='https://hooliganreport.com/wp-json/wp/v2/media',
                            data=data,
                            headers={'Content-Type': 'image/jpg',
                                     'Content-Disposition': f'attachment; filename=%s {jail_name}' % img_name},
                            auth=('admin', 'IrWg LkjJ Pim0 ChU7 NCbl f6TV'))
        newDict = res.text
        match = re.search(r'"id":(\d+)', newDict)
        if match:
            id_value = match.group(1)
            print("Found id:", id_value)
            return id_value
        else:
            print("No match found.")
            return None
    except Exception as e:
        print(e)
        data = open(f'./images/image_placeholeder.jpg', 'rb').read()
        res = requests.post(url='https://hooliganreport.com/wp-json/wp/v2/media',
                            data=data,
                            headers={'Content-Type': 'image/jpg',
                                     'Content-Disposition': 'attachment; filename=%s' % img_name},
                            auth=('admin', 'IrWg LkjJ Pim0 ChU7 NCbl f6TV'))
        newDict = res.text
        match = re.search(r'"id":(\d+)', newDict)
        if match:
            id_value = match.group(1)
            print("Found id:", id_value)
            return id_value
        else:
            print("No match found.")
            return None


def make_post(jail_name):
    try:
        json_data = read_daily_json(jail_name)
        post_ids_data = []
        for profiles in json_data[0:2]:
            print(profiles["name"])
            print(profiles["Address"])
            image_string = read_images(profiles["name"], jail_name, profiles["Address"])
            image_id = restImgUL(profiles["name"], jail_name, profiles["Address"])
            print(profiles["name"])
            username = 'admin'
            password = 'IrWg LkjJ Pim0 ChU7 NCbl f6TV'
            url = 'https://hooliganreport.com/wp-json/wp/v2/posts'
            credentials = username + ':' + password
            cred_token = base64.b64encode(credentials.encode())
            header = {
                'Authorization': 'Basic ' + cred_token.decode('utf-8'),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/112.0.0.0 '
                              'Safari/537.36 ',
                'Content-Type': 'application/json; charset=utf-8',

            }

            table_html = f'<style>\n' \
                         f'table {{ border-collapse: collapse; }}\n' \
                         f'td, th {{ border: 1px solid black; padding: 8px; }}\n' \
                         f'</style>\n' \
                         f'<table>\n' \
                         f'<tr><td><b>Name</b>:</td><td>{profiles["name"]}</td></tr>\n' \
                         f'<tr><td><b>Race</b>:</td><td>{profiles["race"]}</td></tr>\n' \
                         f'<tr><td><b>Age</b>:</td><td>{profiles["age"]}</td></tr>\n' \
                         f'<tr><td><b>Gender</b>:</td><td>{profiles["gender"]}</td></tr>\n' \
                         f'<tr><td><b>Booking Date</b>:</td><td>{profiles["booking_date"]}</td></tr>\n' \
                         f'<tr><td><b>Bond</b>:</td><td>{profiles["bond"]}</td></tr>\n' \
                         f'<tr><td><b>Address</b>:</td><td>{profiles["Address"]}</td></tr>\n' \
                         f'<tr><td colspan="2"><b>Charges</b>:</td></tr>\n' \
                         f'<tr><td colspan="2">{profiles["charges"]}</td></tr>\n' \
                         f'</table>'

            image_and_table_html = f'<div style="display: flex;">\n' \
                                   f'    <div style="flex: 1;">\n' \
                                   f'        <a href="data:image/jpeg;base64,{image_string}" download="{profiles["name"]} {jail_name}.jpg">' \
                                   f'            <img src="data:image/jpeg;base64,{image_string}" style="width: 300px; height: 300px;" alt="My Image">\n' \
                                   f'        </a>\n' \
                                   f'    </div>\n' \
                                   f'    <div style="flex: 1;">\n' \
                                   f'        {table_html}\n' \
                                   f'    </div>\n' \
                                   f'</div>'
            post = {
                'title': profiles["name"],
                'status': 'publish',
                'content': image_and_table_html,
                'featured_media': image_id,
                'categories': 54,
            }
            response = requests.post(url, headers=header, json=post)
            post_ids = {
                "id": response.json()['id']
            }
            print(post_ids)
            post_ids_data.append(post_ids)
            print(response.status_code)
            time.sleep(1)
        files_reader.save_post_ids(post_ids_data)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    jail_names = files_reader.xpath_reader()
    for items in jail_names:
        make_post(items['jail_name'])
