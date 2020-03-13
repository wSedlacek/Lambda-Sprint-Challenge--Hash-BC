from gc import disable
from hashlib import sha256
from requests import get, post
from sys import argv
from threading import Timer
from timeit import default_timer as timer
from typing import Callable


disable()

interrupt: bool = False

counter: int = 0
last_hash: str = ""
last_proof: int = None

coins_mined: int = 0


def set_interval(interval: float, runner: Callable):
    global interrupt
    if not interrupt:
        runner()
        Timer(interval, set_interval, args=[interval, runner]).start()


def update_proof():
    global counter, last_hash, last_proof
    response = get(url=node + "/last_proof")
    current = response.json()

    if last_proof != current['proof']:
        last_proof = current['proof']
        last_hash = hash_proof(last_proof)
        counter = 0
        print(f"Proof Change: {last_proof}")


def mine(user_id: str):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    global interrupt, counter, last_hash, coins_mined

    counter -= 1
    proof = counter
    if valid_proof(last_hash, proof):
        post_proof(user_id, proof)
        update_proof()
        interrupt = coins_mined >= 100


def valid_proof(last_hash: str, proof: int):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    current_hash = hash_proof(proof)

    return last_hash[-6:] == current_hash[:6]


def post_proof(user_id: str, proof: int):
    global coins_mined
    potential_block = {"id": user_id, "proof": proof}
    response = post(url=node + "/mine", json=potential_block)
    data = response.json()

    if data['message'] == 'New Block Forged':
        coins_mined += 1
        print(f"Total coins mined: {coins_mined}")
    else:
        print(data['message'])


def hash_proof(proof: int):
    string = str(proof).encode("utf-8")

    return str(sha256(string).hexdigest())


def load_user():
    file = open("my_id.txt", "r")
    user_id = file.read()
    print("ID is", user_id)
    file.close()

    if user_id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()

    return user_id


if __name__ == '__main__':
    if len(argv) > 1:
        node = argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    user_id = load_user()
    update_freq = 0.01

    set_interval(update_freq, update_proof)
    while not interrupt:
        mine(user_id)
