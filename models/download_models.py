import requests
import os

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def main():
    file_ids = ["1Gzpi-V_Sj7SSFQMNzy6bcgkEwaZBhGWS", "1eUqku9yAZ8MfxCS5FxlsagZmcP1PN-JU", "1XPw_hhm_ZwhD-_TppMXgCbOe3XTr641u"]
    file_names = ["cnn-rico-1.h5", "cnn-wireframes-only.h5", "cnn-generalized.h5"]
    
    root_dir = os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).find("smart_ui_tf20")+13]
    
    for file_id, file_name in zip(file_ids, file_names):
        print(f"Downloading {file_name}...")   
        file_name = os.path.join(root_dir, "models", file_name)
        download_file_from_google_drive(file_id, file_name)


if __name__ == "__main__":
    main()