import pytest
import json
from model.data_preprocessing import clear_text, text2numbers

# @pytest.skip(allow_module_level=True)

def to_tokens(text):
    with open('model/data/word_dict.json', 'r') as f:
        word_dict = json.loads(f.read())

    return text2numbers(text, word_dict)

def test_clear_annd_convert_text_to_tokens():
    text =  '''Анна Якубаб «Глорию Скотт»\n@VekshinaI 
    обожаю тебя и наши покатушки на машинке:*\nRT @make_me_strong_: @smille_Tommo
     пхаххаха:D Заипись\n06.12.2013 / Вечерний Маскарад:) http://t.co/oYSJpAawmX
     \nСанкт-Петербургская, 9:00 - 12:15 день, О центре развития Baby time, 
     .Спасибо Анхель и Хорхе, 7.10.2020 года, конкурс3\n)В. А. Рождественский  
     Школа №321 нам 3.3 года. \n\nМы уже не ждали и не надеялись...\nЗакончил 
     академию BARBER WANTED 15.02.2019 года'''

    cleared_text = clear_text(text)
    tokens = to_tokens(cleared_text)

    assert cleared_text == '''обожать ты и наш покатушка на машинка пха ха_хий заипеться вечерний маскарад санкт петербургский день о центр развитие спасибо и год конкурс мы год мы уже не ждать и не надеяться закончить академия год'''
    assert len(tokens) > 10

def test_empty_string():
    cleared_text = clear_text('')
    tokens = to_tokens(cleared_text)
    assert len(tokens) == 0
    print(len(tokens))

def test_english_string():
    cleared_text = clear_text('Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the s, when an unknown printer')
    tokens = to_tokens(cleared_text)
    assert len(tokens) == 0
    print(len(tokens))

def test_en_and_ru_string():
    cleared_text = clear_text('Lorem Ipsum is simply позволяет легко писать небольшие, легко читаемые тесты и может масштабироваться для поддержки сложного функционального тестирования  dummy typesetting industry.')
    tokens = to_tokens(cleared_text)
    assert len(tokens) > 0
    print(len(tokens))

if __name__ == "__main__":
    test_empty_string()
    test_english_string()
    test_en_and_ru_string()