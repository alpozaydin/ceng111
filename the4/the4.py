# the code does not handle the cases where parent is not found!

def is_male(name):
    alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if name[0] in alp:
        return True


def node(tree):
    if type(tree) == list:
        return tree[0]
    else:
        return tree


def children(tree):
    return tree[1:]


def is_empty(tree):
    return tree == []


def find_parent(tree, pname):
    if is_empty(tree):
        return []
    for child in children(tree):
        if node(child) == pname:
            return node(tree)
        result = find_parent(child, pname)
        if result:
            return result
    return []


def children_list(tree, pname):
    if is_empty(tree):
        return []
    if node(tree) == pname:
        res = []
        for child in children(tree):
            res.append(node(child))
        return res
    for child in children(tree):
        result = children_list(child, pname)
        if result:
            return result
    return []


def brothers(tree, pname):
    if is_empty(tree):
        return []
    for child in children(tree):
        if node(child) == pname:
            res = []
            for sibling in children(tree):
                if is_male(node(sibling)) and node(sibling) != pname:
                    res.append(node(sibling))
            return res
        result = brothers(child, pname)
        if result:
            return result
    return []


def sisters(tree, pname):
    if is_empty(tree):
        return []
    for child in children(tree):
        if node(child) == pname:
            res = []
            for sibling in children(tree):
                if not is_male(node(sibling)) and node(sibling) != pname:
                    res.append(node(sibling))
            return res
        result = sisters(child, pname)
        if result:
            return result
    return []


def siblings(tree, pname):
    parent = find_parent(tree, pname)
    ch = children_list(tree, parent)
    res = []
    for child in ch:
        if child != pname:
            res += [child]
    return res

def uncles(tree, pname):
    parent = find_parent(tree, pname)
    return brothers(tree, parent)


def aunts(tree, pname):
    parent = find_parent(tree, pname)
    return sisters(tree, parent)


def cousins(tree, pname):
    parent = find_parent(tree, pname)
    sib = siblings(tree, parent)
    res = []
    for person in sib:
        res.extend(children_list(tree, person))
    return res
