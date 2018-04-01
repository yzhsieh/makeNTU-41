from imgurpython import ImgurClient
from config import client_id, client_secret, album_id, access_token, refresh_token

def upload(path):
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    config = {
        'album': album_id,
        'name': 'test-name!',
        'title': 'test-title',
        'description': 'test-description'
    }
    print("Uploading image... ")
    image = client.upload_from_path(path, config=config, anon=False)
    print("Done")
    print(image['link'])
    return image['link']

if __name__ == "__main__":
    upload('./yohao.png')
