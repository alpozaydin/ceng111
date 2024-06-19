def mother(lst):
    if lst.count("m") == 0:
        return "0"
    f1 = list(filter(lambda x: x[1] == "m", enumerate(lst)))
    f2 = list(map(lambda x: x[0] % 5, f1))
    s = set(f2)
    if len(s) > 1:
        return False
    else:
        return lst.count("m") * 10


def father(lst):
    if lst.count("f") == 0:
        return "0"
    if lst.count("f") > 2:
        return False
    if lst.count("f") < 2:
        return 20 * lst.count("f")
    elif lst.count("f") == 2:
        a = lst.index("f")
        b = lst.index("f", a + 1)
        if b - a == 1 and abs((b % 5) - (a % 5)) != 4:
            return False
        else:
            return 20 * lst.count("f")


def babysitter(lst, index = 0, cost = 0):
    if lst.count("b") == 0:
        return "0"
    count = lst.count("b")

    if count <= 1:
        return count * 30 + cost
    else:
        index = lst.index("b", index)  # find the index of the current b we are working
        if "b" in lst[index + 1:]:  # checking if there is a trailing b
            next_index = lst.index("b", index + 1)
            if next_index - index < 4 and index % 5 - next_index % 5 < 0:
                cost += (next_index - index) * 30
            elif next_index - index < 4 and index % 5 - next_index % 5 == 4:
                cost += 90
            else:
                cost += 30

            return babysitter(lst, next_index, cost)
        else:
            cost += 30
            return cost


def grandma(lst):
    if lst.count("g") == 0:
        return "0"
    f1 = list(filter(lambda x: x[1] == "g", enumerate(lst)))
    f2 = list(map(lambda x: x[0] % 5, f1))
    if f2.count(2) > 1:
        return False
    else:
        return lst.count("g") * 50

def aunt1(lst):
    if lst.count("a1") == 0:
        return "0"
    f1 = list(filter(lambda x: x[1] == "a1", enumerate(lst)))
    f2 = list(map(lambda x: x[0] % 5, f1))
    if 0 in f2 or 2 in f2 or 3 in f2:
        return False
    else:
        return lst.count("a1") * 32


def aunt2(lst):
    if lst.count("a2") == 0:
        return "0"
    index = list(filter(lambda x: x[1] == "a2" and x[0] != 0, enumerate(lst)))
    filt = list(filter(lambda x: lst[x[0] - 1] == "a1" and (x[0] - 1) % 5 != 4, index))
    if len(filt) > 0:
        return False
    else:
        return lst.count("a2") * 27


def neighbour(lst):
    index = list(filter(lambda x: x[1] == "n", enumerate(lst)))
    filt = list(map(lambda x: x[0] % 5 , index))
    if 3 in filt or 4 in filt:
        return False
    elif lst.count("n") > 1:
        power = list(map(lambda x: 5 ** x, range(lst.count("n"))))
        return sum(power) - 1
        
    else:
        return "0"


def check_month(lst):
    elements = set(lst)
    out = []
    out += [mother(lst)] + [father(lst)] + [babysitter(lst)] + [grandma(lst)] + [aunt1(lst)] + [aunt2(lst)] + [neighbour(lst)]
    if False in out:
        filtered = list(filter(lambda x: x[1] == False, enumerate(out)))
        indexed = list(map(lambda x: x[0] + 1, filtered))
        return indexed
    else:
        out = [int(mother(lst))] + [int(father(lst))] + [int(babysitter(lst))] + [int(grandma(lst))] + [int(aunt1(lst))] + [int(aunt2(lst))] + [int(neighbour(lst))]
        return sum(out)
