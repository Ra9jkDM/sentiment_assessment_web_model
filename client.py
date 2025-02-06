import requests

API = 'http://127.0.0.1:8088/api/'

def get():
    r = requests.get(API)
    print(r)
    print(r.content)

def post(data):
    r = requests.post(API+'pred', data=data)
    print(r)
    print(r.content)

def post_file():
    file = {'upload_f': open('files/test_ml_3.xlsx', 'rb')} # csv
    r = requests.post(API+'predict_table', files=file, timeout=10*60) # in seconds
    print(r)
    print(r.content)

def main():
    get()
    # post({'test': 'OK'})
    post_file()

if __name__ == '__main__':
    main()