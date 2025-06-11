import json


def get_file(content):
    extension = _get_file_type(content)
    file = content[content.index(b'\r\n\r\n', 4):]
    file = file[:-1 *len(b'\r\n--0679254358eb18f6089186a3493cc3f4--\r\n')]
    # print(file)
    return file, extension

def _get_file_type(content):
    start_str = b'filename="'
    start = content.index(start_str)
    end = content.index(b'"\r\n\r\n', start)
    file_type = content[start + len(start_str): end]
    return file_type.decode('utf-8').split('.')[-1]

def load_word_dict():
    word_dict = {}
    with open('model/data/word_dict.json', 'r') as f:
        word_dict = json.loads(f.read())
    return word_dict