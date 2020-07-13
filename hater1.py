#!/bin/python3
print('нужно создать максимум хейта, используя минимальное количество хейтеров.\
используем для этого жадный алгоритм.\n')

def inputdata(type_of_person):
    inputdata = []
    print('ввевем список %s. если %s достаточно, нажмите q\n' % (type_of_person, type_of_person))
    while True:
        b=input('одно из имен %s \n' % type_of_person)
        if b=='q':
            break
        else:
            inputdata.append(b)
    return inputdata

def maxcover_by_min_items(items_to_be_covered, items_to_choose):
    min_items_covers_max = set()
    while items_to_be_covered:
        best_item = None
        now_covered = set()
        for key, value in items_to_choose.items():
            covered_by_current_item = items_to_be_covered & value
            if len(covered_by_current_item) > len(now_covered):
                best_item = key
                now_covered = covered_by_current_item
        items_to_be_covered -= now_covered
        min_items_covers_max.add(best_item)
    return min_items_covers_max

who_is_hated = inputdata('хейтеримых')
who_is_hated = set(who_is_hated)

haters = inputdata('хейтеров')
haters = dict.fromkeys(haters, {})

for name in haters.keys():
    print('люди, которых хейтит %s' % name)
    haters_list = inputdata('хейтеримых хейтером %s' % name)
    haters[name] = set(haters_list)

max_hate_by_minhaters = maxcover_by_min_items(who_is_hated, haters)
print('вот минимальный список хейтеров, хейтящих максимум людей', max_hate_by_minhaters)

