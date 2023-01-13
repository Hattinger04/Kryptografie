import string


def encrypt_columnar(plaintext, key):
    arr = [[]]
    counter = 0
    for index, char in enumerate(plaintext):
        if index % len(key) == 0 and index != 0:
            arr.append([])
            counter += 1
        arr[counter].append(char)
    keyvalues = get_order_of_keyword(key)
    result = [[]] * len(key)
    for value in keyvalues:
        for a in arr:
            if len(a) > value:
                result[value] = result[value] + list(a[value])
    cipher = ""
    comparing_sorted = sorted(keyvalues.copy())
    for index, key in enumerate(keyvalues):
        cipher = cipher + "".join(result[keyvalues.index(comparing_sorted[index])])
    return cipher


def encrypt_columnar_myszkowski(plaintext, key):
    keyvalues = get_order_of_keyword_myszkowski(key)
    if len(set(keyvalues)) > len(keyvalues):
        return encrypt_columnar(plaintext, key)
    arr = [[]]
    counter = 0
    for index, char in enumerate(plaintext):
        if index % len(key) == 0 and index != 0:
            arr.append([])
            counter += 1
        arr[counter].append(char)

    result = [[]] * len(key)
    double_values = list(set([x for x in keyvalues if keyvalues.count(x) > 1]))
    removed = []
    for index, value in enumerate(keyvalues):
        if value in double_values:
            indices = [i for i, x in enumerate(keyvalues) if x == value]
            for a in arr:
                if len(a) > value:
                    for i in indices:
                        if len(a) > i:
                            result[value] = result[value] + list(a[i])
            double_values.remove(value)
            removed.append(value)
        else:
            if value not in removed:
                for a in arr:
                    if len(a) > index:
                        result[value] = result[value] + list(a[index])
    cipher = ""
    for arr in result:
        cipher = cipher + "".join(arr)
    return cipher


def encrypt_columnar_disrupted(plaintext, key1, key2):
    arr = [[]]
    counter = 0
    updated_text = make_spaces(plaintext, key2)
    key1values = get_order_of_keyword(key1)

    for index, char in enumerate(updated_text):
        if index % len(key1) == 0 and index != 0:
            arr.append([])
            counter += 1
        arr[counter].append(char)

    result = [[]] * len(key1)
    for value in key1values:
        for a in arr:
            if len(a) > value:
                result[value] = result[value] + list(a[value])
    liste = [[]] * len(key1)
    for index, key in enumerate(key1values):
        liste[key] = result[index]
    cipher = ""
    for i in liste:
        cipher = cipher + "".join(i)
    return cipher


def get_order_of_keyword(keyword):
    result = [0] * len(keyword)
    counter = 0
    for letter in string.ascii_uppercase:
        for index, char in enumerate(keyword):
            if char is letter:
                result[index] = counter
                counter += 1
    return result


def get_order_of_keyword_myszkowski(keyword):
    result = [0] * len(keyword)
    counter = 0
    added = False
    for letter in string.ascii_uppercase:
        for index, char in enumerate(keyword):
            if char is letter:
                result[index] = counter
                added = True
        if added:
            added = False
            counter += 1
    return result


def make_spaces(plaintext, key):
    keyorder = get_order_of_keyword(key)
    updated_text = ""
    rounds = len(plaintext) // len(key) + 1
    try:
        for round in range(rounds):
            for k in keyorder:
                for chars in range(k):
                    updated_text += plaintext[0]
                    plaintext = plaintext[1:]
                updated_text += " "
    except IndexError:
        return updated_text
    return updated_text


def decrpyt_columnar(ciphertext, key):
    result = [[]]
    length_small = 0
    if len(ciphertext) % len(key) == 0:
        result *= (len(ciphertext) // len(key))
    else:
        result *= ((len(ciphertext) // len(key)) + 1)
        length_small = len(ciphertext) % len(key)
    for index, l in enumerate(result[:-1]):
        result[index] = [0] * len(key)
    if length_small != 0:
        result[-1] = [0] * length_small
    else:
        result[-1] = [0] * len(key)
    keyvalues = get_order_of_keyword(key)
    counter = 0
    comparing = keyvalues.copy()
    comparing_sorted = sorted(comparing.copy())

    for index, k in enumerate(keyvalues):
        if comparing.index(comparing_sorted[index]) < length_small:
            for i in range(len(ciphertext) // len(key) + 1):
                result[i][comparing.index(comparing_sorted[index])] = ciphertext[counter]
                counter += 1
        else:
            for i in range(len(ciphertext) // len(key)):
                result[i][comparing.index(comparing_sorted[index])] = ciphertext[counter]
                counter += 1
    cipher = ""
    for arr in result:
        cipher = cipher + "".join(arr)
    return cipher


def decrypt_columnar_myszkowski(ciphertext, key):
    pass


def decrypt_columnar_disrupted(ciphertext, key1, key2):
    columnar = decrpyt_columnar(ciphertext, key1)
    keyorder = get_order_of_keyword(key2)
    indexe = []
    current_index = 0
    rounds = 0
    for index, char in enumerate(columnar):
        if keyorder[current_index] + rounds == index:
            indexe.append(index)
            rounds += (1 + keyorder[current_index])
            if current_index == len(keyorder) - 1:
                current_index = 0
            else:
                current_index += 1
    plaintext_list = list(columnar)
    for index in indexe:
        plaintext_list[index] = ""
    return "".join(plaintext_list)


print(encrypt_columnar("BUNDESVERFASSUNGSGESETZ", "PARLAMENT"))
print(encrypt_columnar_myszkowski("BUNDESVERFASSUNGSGESETZ", "PARLAMENT"))
print(encrypt_columnar_disrupted("BUNDESVERFASSUNGSGESETZ", "PARLAMENT", "AUSTRIA"))

print(decrpyt_columnar("UASEUZVGDSTSNESBFENSERG", "PARLAMENT"))
print(decrypt_columnar_myszkowski("UEAUSZNSEDSTEUZSNSNESRG", "PARLAMENT"))
print(decrypt_columnar_disrupted("BRG DA SSSN GZESE U  E  UFSTVNE", "PARLAMENT", "AUSTRIA"))
