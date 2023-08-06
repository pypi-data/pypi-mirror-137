import os
import pickle
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

FILENAME = 'db_path.pickle'
FULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME)


def make_path(id_pass: tuple = None) -> dict:
    if id_pass is None:
        prefix = ''
    else:
        prefix = ''.join([id_pass[0], ':', id_pass[1], '@'])
    return {
        'ATLAS': f"mongodb+srv://{prefix}nfs.2mnb4.mongodb.net/005930?retryWrites=true&w=majority",
        'LOCAL': f"mongodb://{prefix}localhost:27017",
        'INNER': f'mongodb://{prefix}192.168.0.173:27017',
        'OUTER': f'mongodb://{prefix}hj3415.iptime.org:27017'
    }


def load() -> str:
    local_addr = make_path()['LOCAL']
    try:
        with open(FULL_PATH, "rb") as fr:
            s = pickle.load(fr)
            logger.debug(s)
            return s
    except (EOFError, FileNotFoundError) as e:
        print(f"File not found: {FILENAME} => Create file with default path: {local_addr}")
        with open(FULL_PATH, "wb") as fw:
            pickle.dump(local_addr, fw)
            return local_addr


def save(new_addr: str):
    before = load()
    print(f'Change mongo setting : {before} -> {new_addr}')
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(new_addr, fw)

