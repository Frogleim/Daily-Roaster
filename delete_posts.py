import requests
import base64


def remove_posts(post_id):
    wordpress_url = f'https://hooliganreport.com/wp-json/wp/v2/posts/{post_id}'  # Replace with your post ID
    print(f'removing {wordpress_url}')
    username = 'admin'
    password = 'IrWg LkjJ Pim0 ChU7 NCbl f6TV'  # or API token

    credentials = f"{username}:{password}"
    cred_token = base64.b64encode(credentials.encode()).decode('utf-8')
    header = {
        'Authorization': 'Basic ' + cred_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.0.0 Safari/537.36',
        'Content-Type': 'application/json; charset=utf-8',
    }

    response = requests.delete(wordpress_url, headers=header)

    if response.status_code == 200:  # HTTP 204 means successful deletion
        print(f"Post with ID 1254686 deleted successfully.")
    else:
        print(f"Failed to delete post. Status code: {response.status_code}")
        print(response.text)  # Print the error message if any
