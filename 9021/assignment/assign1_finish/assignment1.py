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
    elif roman.count('I') > 3 or roman.count('X') > 3 or roman.count('C') > 3 \
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
        elif roman.count(roman[i]) > 3:
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


# bulid a dict that is long enough for it, the keyword is A-Z
q3_dict = 'ABCDEFGHIJKLMNOPQ'
q3_roman_num_dict, q3_num_roman_dict = generalized_roman_dict(q3_dict)


def find_num_match_pattern(word):
    # word = list(reversed(word))
    # max_val = 1
    # for w in range(len(set(word)) - 1):
    #     if str(max_val)[0] == '5':
    #         max_val *= 2
    #     else:
    #         max_val *= 5
    # key_count_dict = {w: word.count(w) for w in word}
    # for k in key_count_dict.keys():
    #     if key_count_dict[k] >= 2:
    #         if str(max_val)[0] == '5':
    #             max_val *= 2
    #         else:
    #             max_val *= 5

    # # build a pattern owned by the input word
    # word_pattern, num = {}, 0
    # for i in word:
    #     if i not in word_pattern.keys():
    #         word_pattern[i] = num
    #         num += 1
    # word_diff = len(list(word_pattern.keys()))
    # w_pa = [word_pattern[i] for i in word]
    # word = list(reversed(word))
    #
    # # find the range that the word can reach
    # if key_count_dict[word[0]] == 1:
    #     upper = max_val
    #     lower = int(max_val * 0.8)
    # else:
    #     i = 0
    #     while word[i] == word[i + 1]:
    #         i += 1
    #     i += 1
    #     if i + 1 != key_count_dict[word[0]]:
    #         upper = max_val * key_count_dict[word[0]]
    #         lower = int(max_val * key_count_dict[word[0]] - max_val / 10)
    #     else:
    #         lower = max_val * key_count_dict[word[0]]
    #         upper = max_val * (key_count_dict[word[0]] + 1)
    #
    # # trverse the whole sequence to find a number which match the pattern
    # # when it is converted to roman
    # for i in range(lower, upper):
    #     pattern, pnum = {}, 0
    #     find_word = num_to_roman(i, q3_num_roman_dict)
    #     if word_diff == len(set(find_word)) and len(find_word) == len(word):
    #         for k in find_word:
    #             if k not in pattern.keys():
    #                 pattern[k] = pnum
    #                 pnum += 1
    #         f_pa = [pattern[a] for a in find_word]
    #         if f_pa == w_pa:
    #             # find the matched number and match the value into word
    #             f_pa_dict = {key: q3_roman_num_dict[key] for key in find_word}
    #             vals = list(f_pa_dict.values())
    #             w_pa_dict = {}
    #             for w in range(len(word_pattern.keys())):
    #                 w_pa_dict[list(word_pattern.keys())[w]] = vals[w]
    #             return i, w_pa_dict
    #     else:
    #         continue
    # return False
    pass


def q3_word_legal(word):
    if word.encode('UTF-8').isalpha():
        return True
    return False


def solution3(word):
    if q3_word_legal(word):

        if find_num_match_pattern(word):
            matched_num, match_dict = find_num_match_pattern(word)
            match_dict = {v: k for k, v in match_dict.items()}
            upper, use_key = 1, ''

            while upper <= max(list(match_dict.keys())):
                if upper in match_dict.keys():
                    use_key += match_dict[upper]
                else:
                    use_key += '_'

                if str(upper)[0] == '1':
                    upper *= 5
                elif str(upper)[0] == '5':
                    upper *= 2

            print('Sure! It is ' + str(matched_num) + ' using ' + use_key[::-1])
        else:
            impossible_to_do()
    else:
        impossible_to_do()


if __name__ == '__main__':
    command = input('How can I help you? ')
    word_ls = command.split()
    if word_ls[0] != 'Please' or word_ls[1] != 'convert':
        print("I don't get what you want, sorry mate!")
    elif len(word_ls) == 3 and word_ls[2] != ' ':
        solution1(word_ls[2])
    elif len(word_ls) == 5 and word_ls[3] == 'using':
        solution2(word_ls[2], word_ls[4])
    elif len(word_ls) == 4 and word_ls[3] == 'minimally':
        solution3(word_ls[2])
    else:
        print("I don't get what you want, sorry mate!")

    # solution1('1990')
    # solution1('MCMXC')
    # solution1('IXI')
    # solution1('035')
    # solution1('4000')
    # solution1('IIII')
    # solution1('IXI')
    # solution1('35')
    # solution1('1982')
    # solution1('3007')
    # solution1('MCMLXXXII')
    # solution1('MMMVII')

    # solution2('123', 'ABC')
    # solution2('XXXVI', 'IVX')
    # solution2('XXXVI', 'XWVI')
    # solution2('I', 'II')
    # solution2('_', '_')
    # solution2('XXXVI', 'XVI')
    # solution2('XXXVI', 'XABVI')
    # solution2('EeDEBBBaA', 'fFeEdDcCbBaA')
    # solution2('49036', 'fFeEdDcCbBaA')
    # solution2('ABCDEFGHIJKLMNOPQRST', 'AbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStT')
    # solution2('1900604', 'LAQMPVXYZIRSGN')

    print(solution3('ABCCDED'))
    # print(solution3('ABCADDEFGF'))
    # print(solution3('VI'))
    # print(solution3('MMMVII'))
    # print(solution3('MDCCLXXXIX'))
    # print(solution3('MDCCLXXXVII'))
    # print(solution3('ABCDEFA'))
    # print(solution3('ABAA'))
    # print(solution3('0I'))

    # print(generalized_roman_dict('fFeEdDcCbBaA'))

#
# except ValueError:
#     print("I don't get what you want, sorry mate!")
#     sys.exit()
