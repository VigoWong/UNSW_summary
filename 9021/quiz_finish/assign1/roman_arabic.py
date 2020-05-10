import re
import sys


def impossible_to_do():
    print("Hey, ask me something that's not impossible to do!")
    sys.exit()


comn_num_roman = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
                  100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X',
                  9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
comn_roman_num = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}


def num_to_roman(num, dict_num_roman):
    # 1. build a dictionary to match the roman symbol
    symbol_num_ls = []
    keys = list(dict_num_roman.keys())

    # 2. traverse the number and match the dict
    for k in range(0, len(keys)):
        while num >= keys[k]:
            num -= keys[k]
            symbol_num_ls.append(dict_num_roman[keys[k]])

    roman_num = ''.join(symbol_num_ls)
    return roman_num


def num_legal(word, dict_num_roman):
    if '.' in word or int(word) not in range(0, max(dict_num_roman.keys()) * 4) or word[0] == '0':
        return False
    else:
        return True


def roman_to_num(roman, dict_roman_num):
    # calculate
    sum, i = 0, 0
    while i <= len(roman) - 2:
        if dict_roman_num[roman[i]] >= dict_roman_num[roman[i + 1]]:
            sum += dict_roman_num[roman[i]]
        else:
            sum -= dict_roman_num[roman[i]]
        i += 1
    sum += dict_roman_num[roman[i]]
    return sum


def q1_roman_legal(roman):
    if not re.match('^[MDCLXVI]+$', roman):
        return False
    elif roman.count('I') > 4 or roman.count('X') > 4 or roman.count('C') > 4 \
            or roman.count('V') > 1 or roman.count('D') > 1 or roman.count('L') > 1:
        return False
    for i in range(len(roman) - 1):
        if comn_roman_num[roman[i]] < comn_roman_num[roman[i + 1]]:
            if (roman[i] + roman[i + 1]) not in comn_num_roman.values():
                return False
    return True


def generalized_roman_dict(key_word):
    gen_roman_num, gen_num_roman = {}, {}
    unit = 1
    # build roman-num dict
    for i in reversed(key_word):
        gen_roman_num[i] = unit
        if str(unit)[0] == '1':
            unit *= 5
        elif str(unit)[0] == '5':
            unit *= 2

    # build num-roman dict
    gen_num_roman = {j: i for i, j in gen_roman_num.items()}
    gen_num_roman = {i: j for i, j in sorted(gen_num_roman.items(), reverse=True)}

    # append multi-roman to the dict
    keys, vals = list(gen_num_roman.keys()), list(gen_num_roman.values())
    for i in range(len(keys)):
        if keys[i] != 1:
            if str(keys[i])[0] == '5':
                gen_num_roman[keys[i] - keys[i + 1]] = vals[i + 1] + vals[i]
            elif str(keys[i])[0] == '1':
                gen_num_roman[keys[i] - keys[i + 2]] = vals[i + 2] + vals[i]
        else:
            break

    # sort the dict again
    gen_num_roman = {i: j for i, j in sorted(gen_num_roman.items(), reverse=True)}
    return gen_roman_num, gen_num_roman


def solution1(word):
    # convert integer to roman
    if word.isdigit():
        if num_legal(word, comn_num_roman):
            print('Sure! It is ' + str(num_to_roman(int(word), comn_num_roman)))
        else:
            impossible_to_do()

    # convert roman to integer
    else:
        if q1_roman_legal(word) and word == num_to_roman(roman_to_num(word, comn_roman_num), comn_num_roman):
            print('Sure! It is ' + str(roman_to_num(word, comn_roman_num)))
        else:
            impossible_to_do()


def q2_roman_legal(roman, gen_roman_num, gen_num_roman):
    for i in range(len(roman) - 1):
        if roman[i] not in gen_roman_num.keys():
            return False
        elif str(gen_roman_num[roman[i]])[0] == '5' and roman.count(roman[i]) > 1:
            return False
        elif roman.count(roman[i]) > 4:
            return False
        elif gen_roman_num[roman[i]] < gen_roman_num[roman[i + 1]]:
            if (roman[i] + roman[i + 1]) not in gen_num_roman.values():
                return False
    return True


def keyword_legal(keyword):
    if re.match('^[A-Za-z]+$', keyword):
        for k in keyword:
            if keyword.count(k) > 1:
                return False
        return True
    else:
        return False


def solution2(word, keyword):
    # keyword
    if keyword_legal(keyword):
        # build the dicts
        gen_roman_num, gen_num_roman = generalized_roman_dict(keyword)
        # num to roman
        if word.isdigit():
            if num_legal(word, gen_num_roman):
                print('Sure! It is ' + str(num_to_roman(int(word), gen_num_roman)))
            else:
                impossible_to_do()
        else:
            if q2_roman_legal(word, gen_roman_num, gen_num_roman) and word == num_to_roman(
                    roman_to_num(word, gen_roman_num), gen_num_roman):
                print('Sure! It is ' + str(roman_to_num(word, gen_roman_num)))
            else:
                impossible_to_do()
    else:
        impossible_to_do()


def q3_word_legal(word):
    if word.encode('UTF-8').isalpha():
        return True
    return False


def q3_find_pattern(word):
    word_num_dict = {w: word.count(w) for w in word}
    visited_ls = []
    ret = ''
    for w in range(len(word) - 1, -1, -1):
        a = word[w]
        append_ls = []
        if word[w] in visited_ls:
            continue
        if word_num_dict[word[w]] == 1:
            if w >= 1:
                if word_num_dict[word[w - 1]] == 1:
                    if len(ret) % 2 == 0:
                        append_ls = [word[w - 1], word[w]]
                        visited_ls.append(word[w])
                        visited_ls.append(word[w - 1])
                    else:
                        append_ls = [word[w]]
                else:
                    append_ls = [word[w]]
            else:
                append_ls = word[w]

        elif word_num_dict[word[w]] == 2:
            if word[w] not in visited_ls:
                visited_ls.append(word[w])
            if word[w] == word[w - 1]:
                if len(ret) % 2 == 1:
                    append_ls = ['_', word[w]]
                else:
                    append_ls = [word[w]]

            elif word[w] == word[w - 2]:
                if word_num_dict[word[w - 1]] > 1:
                    return False, False
                if len(ret) % 2 == 0:
                    append_ls = [word[w - 1], '_', word[w]]
                else:
                    append_ls = ['_', word[w - 1], '_', word[w]]

                visited_ls.append(word[w - 1])

            elif word[w] == word[w - 3]:
                if word[w - 1] == word[w - 2]:
                    return False, False
                elif word[w - 1] not in visited_ls and word[w - 2] not in visited_ls:
                    if len(ret) % 2 == 0:
                        if word.count(word[w-1])>=2:
                            append_ls = [word[w - 1], '_', word[w],'_', word[w - 2]]
                        else:
                            append_ls = [word[w - 1], '_', word[w],'_', word[w - 2]]
                    else:
                        if word.count(word[w - 1]) >= 2:
                            pass
                        else:
                            append_ls = ['_', word[w - 1], '_', word[w], word[w - 2]]

                elif word[w - 1] in visited_ls:
                    return False, False

                visited_ls.append(word[w - 1])
                visited_ls.append(word[w - 2])

            else:
                return False, False

        elif word_num_dict[word[w]] == 3:
            visited_ls.append(word[w])
            if word[w] == word[w - 1] == word[w - 2]:
                if len(ret) % 2 == 0:
                    append_ls = [word[w]]
                else:
                    append_ls = ['_', word[w]]

            elif word[w] == word[w - 2] == word[w - 3] and word[w] != word[w - 1]:
                if len(ret) % 2 == 0:
                    append_ls = [word[w - 1], '_', word[w]]
                else:
                    append_ls = ['_', word[w - 1], '_', word[w]]
                visited_ls.append(word[w - 1])
            else:
                return False, False

        elif word_num_dict[word[w]] == 4:
            visited_ls.append(word[w])
            if word[w] == word[w - 2] == word[w - 3] == word[w - 4]:
                if len(ret) % 2 == 0:
                    append_ls = [word[w - 1],'_', word[w]]
                else:
                    append_ls = ['_', word[w - 1], '_', word[w]]
                visited_ls.append(word[w - 1])
            else:
                return False, False

        else:
            return False, False

        for i in append_ls:
            ret += i

    q3_roman_num_dict, max_unit = {}, 0
    for i in range(len(ret)):
        if max_unit == 0:
            q3_roman_num_dict[ret[i]] = 1
            max_unit = 1
        else:
            if ret[i] == '_':
                if str(max_unit)[0] == '1':
                    max_unit *= 5
                else:
                    max_unit *= 2
            else:
                if str(max_unit)[0] == '1':
                    max_unit *= 5
                    q3_roman_num_dict[ret[i]] = max_unit
                else:
                    max_unit *= 2
                    q3_roman_num_dict[ret[i]] = max_unit
    ret = ret[::-1]
    return ret, q3_roman_num_dict


def solution3(word):
    if q3_word_legal(word):
        pattern, q3_roman_num_dict = q3_find_pattern(word)
        if pattern:
            q3_answer = roman_to_num(word, q3_roman_num_dict)
            print('Sure! It is ' + str(q3_answer) + ' using ' + pattern)
        else:
            impossible_to_do()
    else:
        impossible_to_do()


if __name__ == '__main__':
    command = input('How can I help you? ')
    word_ls = command.split()
    if not word_ls:
        print("I don't get what you want, sorry mate!")
    elif word_ls[0] != 'Please' or word_ls[1] != 'convert':
        print("I don't get what you want, sorry mate!")
    elif len(word_ls) == 3 and word_ls[2] != ' ':
        solution1(word_ls[2])
    elif len(word_ls) == 5 and word_ls[3] == 'using':
        solution2(word_ls[2], word_ls[4])
    elif len(word_ls) == 4 and word_ls[3] == 'minimally':
        solution3(word_ls[2])
    else:
        print("I don't get what you want, sorry mate!")
