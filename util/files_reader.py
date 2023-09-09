import json
import os

current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
data_directory = os.path.join(parent_directory, 'data')
# files_in_data_directory = os.listdir(data_directory)
print(data_directory)


def read_websites_json():
    with open(f'{data_directory}\\scraping_data\\websites.json', 'r') as file:
        data = json.load(file)
    return data


def xpath_reader(county_name=None):
    file = read_websites_json()
    xpath_list = []
    for xpath in file['websites']:
        if xpath['data']['county_name'] == county_name:
            jail_name = county_name
            xpath_data = xpath['data']['xpath']

            d = {
                "jail_name": jail_name,
                "xpath": xpath_data
            }
            xpath_list.append(d)
        elif county_name is None:
            jail_name = xpath['data']['county_name']
            xpath_data = xpath['data']['xpath']
            d = {
                "jail_name": jail_name,
                "xpath": xpath_data
            }
            xpath_list.append(d)
    return xpath_list


def read_urls_json(jail_name):
    with open(f'{data_directory}\\profiles_urls_data\\{jail_name}_profiles_urls.json', 'r') as file:
        data = json.load(file)
    return data


def read_daily_urls_json(jail_name):
    with open(f'{data_directory}\\daily_data\\{jail_name}_daily_profiles_urls.json', 'r') as file:
        data = json.load(file)
    return data


def save_urls_json(jail_name, data):
    with open(f'{data_directory}\\profiles_urls_data\\{jail_name}_profiles_urls.json', 'w') as f:
        json.dump(data, f)
    print(f"json file for {jail_name} saved successfully")


def save_posts_id(data):
    with open(f'{data_directory}\\daily_inmates_data\\post_ids.json', 'w') as f:
        json.dump(data, f)
    print(f"json file for post_ids saved successfully")


def read_post_id_json():
    with open(f'{data_directory}\\profiles_urls_data\\post_ids.json', 'r') as file:
        data = json.load(file)
    return data


def save_daily_urls_json(jail_name, data):
    with open(f'{data_directory}\\daily_data\\{jail_name}_daily_profiles_urls.json', 'w') as f:
        json.dump(data, f)
    print(f"json file for {jail_name} saved successfully")


def save_post_ids(data):
    with open(f'{data_directory}\\profiles_urls_data\\post_ids.json', 'w') as f:
        json.dump(data, f)
    print(f"json file saved successfully")


def save_json(jail_name, data):
    with open(f'{data_directory}\\{jail_name}.json', 'w') as f:
        json.dump(data, f)
    print(f"json file for {jail_name} saved successfully")


def save_daily_json(jail_name, data):
    with open(f'{data_directory}\\daily_inmates_data\\{jail_name}.json', 'w') as f:
        json.dump(data, f)
    print(f"json file for {jail_name} saved successfully")


def remove_duplicates(data):
    tuple_list = [tuple(d.items()) for d in data]
    unique_tuple_set = set(tuple_list)
    unique_list = [dict(t) for t in unique_tuple_set]
    print(len(unique_list))
    return unique_list


def create_directory(jail_name):
    parent_directory = "./images"
    subdirectory = f"{parent_directory}/images_{jail_name}"
    os.makedirs(parent_directory, exist_ok=True)
    os.mkdir(subdirectory)
    directory_name = os.path.basename(subdirectory)

    return directory_name


if __name__ == '__main__':
    import os

    # county_name = 'Cross County'
    res = xpath_reader()
    print(res)
    # res = read_websites_json()
