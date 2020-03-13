import random

from gc import disable
from hashlib import sha256
from requests import get, post
from sys import argv
from timeit import default_timer as timer
from uuid import uuid4


disable()


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here

    print(f"Proof found: {proof} in {timer() - start}")

    return proof


def valid_proof(last_proof: int, proof: int):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    last_hash = hash_proof(last_proof)
    current_hash = hash_proof(proof)

    return last_hash[-6:] == current_hash[:6]


def hash_proof(proof):
    string = str(proof).encode("utf-8")
    return str(sha256(string).hexdigest())


def load_user():
    f = open("my_id.txt", "r")
    user_id = f.read()
    print("ID is", user_id)
    f.close()

    if user_id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    return user_id


if __name__ == '__main__':
    # What node are we interacting with?
    if len(argv) > 1:
        node = argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    # Load or create ID
    user_id = load_user()
    coins_mined = 0

    while True:
        # Get the last proof from the server
        response = get(url=node + "/last_proof")

        last = response.json()
        new_proof = proof_of_work(last['proof'])

        potential_block = {"id": user_id, "proof": new_proof}
        response = post(url=node + "/mine", json=potential_block)
        data = response.json()

        if data['message'] == 'New Block Forged':
            coins_mined += 1
            print(f"Total coins mined: {coins_mined}")
        else:
            print(data['message'])
