''' ord(c) returns the encoding of character c.
    chr(e) returns the character encoded by e.
'''
def f(n):
    '''
    >>> f(1)
    A
    >>> f(2)
     A
    CBC
    >>> f(3)
      A
     CBC
    EDCDE
    >>> f(4)
       A
      CBC
     EDCDE
    GFEDEFG
    >>> f(30)
                                 A
                                CBC
                               EDCDE
                              GFEDEFG
                             IHGFEFGHI
                            KJIHGFGHIJK
                           MLKJIHGHIJKLM
                          ONMLKJIHIJKLMNO
                         QPONMLKJIJKLMNOPQ
                        SRQPONMLKJKLMNOPQRS
                       UTSRQPONMLKLMNOPQRSTU
                      WVUTSRQPONMLMNOPQRSTUVW
                     YXWVUTSRQPONMNOPQRSTUVWXY
                    AZYXWVUTSRQPONOPQRSTUVWXYZA
                   CBAZYXWVUTSRQPOPQRSTUVWXYZABC
                  EDCBAZYXWVUTSRQPQRSTUVWXYZABCDE
                 GFEDCBAZYXWVUTSRQRSTUVWXYZABCDEFG
                IHGFEDCBAZYXWVUTSRSTUVWXYZABCDEFGHI
               KJIHGFEDCBAZYXWVUTSTUVWXYZABCDEFGHIJK
              MLKJIHGFEDCBAZYXWVUTUVWXYZABCDEFGHIJKLM
             ONMLKJIHGFEDCBAZYXWVUVWXYZABCDEFGHIJKLMNO
            QPONMLKJIHGFEDCBAZYXWVWXYZABCDEFGHIJKLMNOPQ
           SRQPONMLKJIHGFEDCBAZYXWXYZABCDEFGHIJKLMNOPQRS
          UTSRQPONMLKJIHGFEDCBAZYXYZABCDEFGHIJKLMNOPQRSTU
         WVUTSRQPONMLKJIHGFEDCBAZYZABCDEFGHIJKLMNOPQRSTUVW
        YXWVUTSRQPONMLKJIHGFEDCBAZABCDEFGHIJKLMNOPQRSTUVWXY
       AZYXWVUTSRQPONMLKJIHGFEDCBABCDEFGHIJKLMNOPQRSTUVWXYZA
      CBAZYXWVUTSRQPONMLKJIHGFEDCBCDEFGHIJKLMNOPQRSTUVWXYZABC
     EDCBAZYXWVUTSRQPONMLKJIHGFEDCDEFGHIJKLMNOPQRSTUVWXYZABCDE
    GFEDCBAZYXWVUTSRQPONMLKJIHGFEDEFGHIJKLMNOPQRSTUVWXYZABCDEFG
    '''
    if n <1:
        return
    elif n==1:
        print('A')
    else:
        a_a = ord('A')
        cur_ord = a_a
        for l in range(1, n+1):
            print(' '*(n-l), end='')
            ls = [chr(a_a+(i-a_a)%24) for i in range(cur_ord + l-1, cur_ord-1, -1)] +\
                 [chr(a_a+(i-a_a)%24) for i in range(cur_ord+1, cur_ord + l, 1)]
            print(''.join(ls),end = '')
            print()
            cur_ord += 1




if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # f(3)
