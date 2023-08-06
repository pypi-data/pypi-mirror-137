import os
import pickle
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

MONGO_ADDR = "mongodb+srv://hj3415:piyrw421@nfs.2mnb4.mongodb.net/005930?retryWrites=true&w=majority"
IPTIME_ADDR = 'mongodb://hj3415:piyrw421@hj3415.iptime.org:27017'
ATLAS_ADDR = "mongodb+srv://hj3415:piyrw421@nfs.2mnb4.mongodb.net/005930?retryWrites=true&w=majority"
LOCAL_ADDR = 'mongodb://localhost:27017'
INTERNAL_ADDR = 'mongodb://192.168.0.173:27017'

FILENAME = 'db_path.pickle'
FULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME)


def load() -> str:
    try:
        with open(FULL_PATH, "rb") as fr:
            s = pickle.load(fr)
            logger.debug(s)
            return s
    except (EOFError, FileNotFoundError) as e:
        print(f"File not found: {FILENAME} => Create file with default path: {LOCAL_ADDR}")
        with open(FULL_PATH, "wb") as fw:
            pickle.dump(LOCAL_ADDR, fw)
            return LOCAL_ADDR


def save(new_addr: str):
    before = load()
    print(f'Change mongo setting : {before} -> {new_addr}')
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(new_addr, fw)

