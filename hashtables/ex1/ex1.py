#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(limit)

    for i in range(length):
        indexes = hash_table_retrieve(ht, weights[i]) or []
        indexes.append(i)
        hash_table_insert(ht, weights[i], indexes)

    higher = limit
    lower = 0
    while higher >= lower:
        higher_value = hash_table_retrieve(ht, higher)
        lower_value = hash_table_retrieve(ht, lower)

        if higher_value and lower_value:
            higher_value_index = higher_value[0]
            lower_value_index = lower_value[-1]

            if higher_value_index > lower_value_index:
                return (higher_value_index, lower_value_index)
            else:
                return (lower_value_index, higher_value_index)

        higher -= 1
        lower += 1

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
