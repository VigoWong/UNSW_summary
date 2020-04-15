def solution_3(word):
    word_num_dict = {w: word.count(w) for w in word}
    visited_ls = []
    ret = ''

    for w in range(len(word) - 1, -1, -1):
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
                if len(ret) % 2 == 0:
                    append_ls = [word[w - 1], '_', word[w]]
                else:
                    append_ls = ['_', word[w - 1], '_', word[w]]

                visited_ls.append(word[w - 1])

            elif word[w] == word[w - 3]:
                if word[w-1] == word[w-2]:
                    return False
                elif word[w - 1] not in visited_ls and word[w - 2] not in visited_ls:
                    if len(ret) % 2 == 0:
                        append_ls = [word[w - 1], '_', word[w], '_', word[w - 2]]
                    else:
                        append_ls = ['_', word[w - 1], '_', word[w], '_', word[w - 2]]
                elif word[w - 1] in visited_ls:
                    return False

                visited_ls.append(word[w - 1])
                visited_ls.append(word[w - 2])

            else:
                return False

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
                return False

        elif word_num_dict[word[w]] == 4:
            visited_ls.append(word[w])
            if word[w] == word[w - 2] == word[w - 3] == word[w - 4]:
                if len(ret) % 2 == 0:
                    append_ls = [word[w - 1], '_', word[w]]
                else:
                    append_ls = ['_', word[w - 1], '_', word[w]]
                visited_ls.append(word[w - 1])
            else:
                return False

        else:
            return False

        for i in append_ls:
            ret += i
    a = ret[::-1]
    return ret[::-1]


# false
# print(solution_3('abcdefghijabcdefghij'))
# print(solution_3('aaaYeXbbbcccdddeee'))
# print(solution_3('abcdeabcde'))
# print(solution_3('ABBACDEFGH'))
# print(solution_3('ABAAA'))
# print(solution_3('ABCDEFA'))
# print(solution_3('ABAB'))
# print(solution_3('MSSM'))


# correct
solution_3('fhdssszsxcccbcnmmmNmBVVVXVZAAASDGGHJLLPOUUYTEEWQ') #hfds_zxc_bnm_NBV_XZA_SDG_HJL_POU_YTEQW

# solution_3('tgggvnnLAAAKSSFJHDERRTWWW')     # tgvnLAKSJFDHERTW
# solution_3('KKKJJJHHZZXCVVRRQQQWWW')     # K_J_H_Z_XCV_R_Q_W
# solution_3('iyoppplkkjhgdazxccvbbbmb')     # yioplkhjdgzaxcvb_m
# solution_3('uvcfdrzzzeeaQQCCCHVYRE')     # ucvdfrz_eaQ_C_HYVER
# solution_3('CEEGGGIikmMoOOqQQQSR')     # CE_G_IkiMmoOqQRS
# solution_3('brbwwqaaaZZZXCCKBOPL')     # b_r_wqa_ZXC_KOBLP
# solution_3('kdjshffyyyMAAADDGDT')     # dksjhf_yMA_D_G_T
# solution_3('lllkkkjjhhmxxvvqqqppp')     # l_k_j_hmx_v_q_p
# solution_3('eteuuiooolllkjjghfds')     # e_t_uio_lkj_gfhsd
# solution_3('lljjggffsswwccbbnn')     # l_j_g_f_s_w_c_b_n
# solution_3('IIUUUtTRRB')     # I_U_tTR_B
# solution_3('ERRTYYY')     # ERTY
# solution_3('hjgrt')     # hgjtr
# solution_3('LPPP')     # LP
# solution_3('qp')     # pq
# solution_3('X')     # X
#
# solution_3('fhdssszsxcccbcnmmmNmBVVVXVZAAASDGGHJLLPOUUYTEEWQ')  # hfds_zxc_bnm_NBV_XZA_SDG_HJL_POU_YTEQW
# solution_3('IOOPPPLlkjJhHHgGGGFGDFsSSSaAAzZxCcVVVBBN')  # IO_P_LklJjhHgG_F_DsSaAZzCxcV_B_N
# solution_3('kdjshffyyyMAAADDGDT')  # dksjhf_yMA_D_G_T
# solution_3('IIUUUtTRRB')  # I_U_tTR_B
# solution_3('YUUIIIOoplLkKKjJJJHJGHfFFFdDDsSaZzXXXCCV')  # YU_I_OpoLlkKjJ_H_GfFdDSsZazX_C_V
#