def maxcover_by_min_items(items_to_be_covered, items_to_choose):
    min_items_covers_max = set()
    items_to_be_covered = set(items_to_be_covered)
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
