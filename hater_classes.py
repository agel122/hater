"""Greedy algorithm is used in the class Greedy to choose minimum set of items,
cover maximum set of another items.
items_to_be_covered - covered items
items_to_choose - initial set of items, cover all another items with overlap
As result, we get:
min_items_covers_max - optimal set of items, as selected set of items_to_choose,
which cover items_to_be_covered in optimal way"""

#!/bin/python3
import copy, sys

class Greedy:
    def __init__(self, items_to_be_covered, items_to_choose):
        self.items_to_be_covered = items_to_be_covered
        self.items_to_choose = items_to_choose
        self.maxcover_by_min_items()

    def maxcover_by_min_items(self):
        min_items_covers_max = set()
        items_to_be_covered_inwork = copy.copy(self.items_to_be_covered)
        items_to_choose = self.items_to_choose
        while items_to_be_covered_inwork:
            best_item = None
            now_covered = set()
            for key, value in items_to_choose.items():
                covered_by_current_item = items_to_be_covered_inwork & value
                if len(covered_by_current_item) > len(now_covered):
                    best_item = key
                    now_covered = covered_by_current_item
            items_to_be_covered_inwork -= now_covered
            min_items_covers_max.add(best_item)
        self.min_items_covers_max = min_items_covers_max


class DataInputter:
    def __init__(self, type_of_person, opt=1):
        self.type_of_person = type_of_person
        if opt == 1:
            self.data = set(self.inputdata1(par=1))
        else:
            self.data = self.inputdata2()

    def inputdata1(self, par=2):
        inputdata = []
        if par == 1:
            print(f"please, input names of {self.type_of_person}. if you have enough {self.type_of_person}, press q\n")
        else:
            print('please, input names or press q')
        while True:
            b = input('one of the names\n')
            if b == 'q':
                break
            else:
                inputdata.append(b)
        return inputdata

    def inputdata2(self):
        inputdata = dict.fromkeys(self.inputdata1(par=1), {})
        for name in inputdata.keys():
            print(f"items, covered by {name}")
            inputdata[name] = set(self.inputdata1(par=2))
        return inputdata


if __name__ == '__main__':
    hated_persons = DataInputter('hated persons', opt=1).data
    haters = DataInputter('haters', opt=2).data
    optimal_result = Greedy(hated_persons, haters)
    print('there is a list of hated persons', optimal_result.items_to_be_covered)
    print('there is a list of haters', optimal_result.items_to_choose)
    print('there is a optimal set of haters', optimal_result.min_items_covers_max)








