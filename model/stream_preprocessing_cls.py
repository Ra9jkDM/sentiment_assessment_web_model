from multiprocessing import Process, Manager
import pandas as pd
import model.data_preprocessing as data_preprocessing
# import data_preprocessing
import queue
import threading
import json
import time


def load_data(path, extension):
    ext_func = {'csv': pd.read_csv, 'xlsx': pd.read_excel}
    df = ext_func[extension](path)
    return df

class Task:
    def __init__(self, data, func):
        self.data = data
        self.func = func

class BackgroundProcessing:
    MAX_CORES = 4
    CLEAR_TEXT = 'clear_text'
    TOKENS = 'tokens'
    main_thread = None

    work_queue = queue.Queue()
    manager = Manager()
    lock = manager.Lock()
    preprocessed_data = manager.dict()

    def __init__(self, word_dict, pred_func, max_cores = 4):
        self.word_dict = word_dict
        self.pred_func = pred_func
        self.MAX_CORES = max_cores

        self.create_and_start_main_process()

    def devide_file(self, df, parts):
        length = len(df)//parts
        data = []
        amount = 0
        
        for i in range(parts):
            if i + 1 == parts:
                data.append(df[i*length:-1])
            else:
                data.append(df[i*length:(i+1)*length])
                
            amount+=len(data[i])
        
        # print('Amount:', amount)
        # for i, value in enumerate(data, start = 1):
        #    print(f'Part {i}, data len: {len(value)}')

        return data

    # ToDo: вынести функцию ниже из класса т.к. она может меняться
    def _preprocess_text(self, column):
        def wrapper(row, *args, **kwargs):
            row[self.CLEAR_TEXT] = data_preprocessing.clear_text(str(row[column]))
            row[self.TOKENS] = data_preprocessing.text2numbers(row[self.CLEAR_TEXT], self.word_dict)
            return row
        return wrapper
    
    def preprocess_simple_text(self, text):
        clear_text = data_preprocessing.clear_text(str(text))
        tokens = data_preprocessing.text2numbers(clear_text, self.word_dict)
        return clear_text, tokens

    # def preprocess_data_worker(self, data, task_name, part):
    #     text = data.apply(self._preprocess_text(data.columns[0]), axis=1)
    #     self.lock.acquire()
    #     self.preprocessed_data[f'{task_name}_{part}'] = text
    #     self.lock.release()
    #     # print(self.preprocessed_data)

    def preprocess_data_worker(self, data, part):
        text = data.apply(self._preprocess_text(data.columns[0]), axis=1)
        self.lock.acquire()
        self.preprocessed_data[part] = text
        self.lock.release()

    def run_data_preprocess(self):
         while True:
            if not self.work_queue.empty():
                print('New task added')
                thread_list = []

                task = self.work_queue.get()
                data = self.devide_file(task.data, self.MAX_CORES)
                for i in range(self.MAX_CORES):
                    thread_list.append(Process(target=self.preprocess_data_worker, args=(data[i], i)))
                    thread_list[i].start()

                for i in range(self.MAX_CORES):
                    print('MulT', i)
                    thread_list[i].join()

                data = self.join_results()
                result = self.pred_func(data, row_name=self.TOKENS) # notify NN
                task.func(*result)
            else:
                break
        

    def join_results(self):
        all_data = pd.concat(self.preprocessed_data.values())
        for i in range(self.MAX_CORES):
            self.preprocessed_data.pop(i, None)

        return all_data

    def create_and_start_main_process(self):
        print('Create main thread')
        self.main_thread = threading.Thread(target=self.run_data_preprocess)
        self.main_thread.start()
        # main_thread.join()
        # print(main_thread.is_alive())

    def add_task(self, task):
        self.work_queue.put(task)

        if not self.main_thread.is_alive():
            print('Tread dead')
            self.create_and_start_main_process()


if __name__ == '__main__':
    data = load_data(f'files/test_ml_3.xlsx', 'xlsx')
    task = Task(data, lambda *args, **kwargs: print('End function'))

    word_dict = {}
    with open('model/data/word_dict.json', 'r') as f:
        word_dict = json.loads(f.read())

    bg = BackgroundProcessing(word_dict, lambda x, row_name: print('Finish...'))
    bg.add_task(task)
    print('First task added')
    bg.add_task(task)
    print('All tasks added')
    # print(bg.result_data)

