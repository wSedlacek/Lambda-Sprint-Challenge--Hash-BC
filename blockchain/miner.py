import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


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


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # TODO: Your code here!
    pass


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
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    # Load or create ID
    user_id = load_user()
    coins_mined = 0

    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")

        data = r.json()
        new_proof = proof_of_work(data['proof'])

        post_data = {"id": user_id, "proof": new_proof}
        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        if data['message'] == 'New Block Forged':
            coins_mined += 1
            print(f"Total coins mined: {coins_mined}")
        else:
            print(data['message'])
