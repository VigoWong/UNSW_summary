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
    if n == 1:
        print('A')
    else:
        a_a = ord('A')
        cur = 0
        for i in range(1, n+1):
            print(' '*(n-i), end= '')
            out_ls = [chr(a_a +(cur+a-1)%26) for a in range(i, 0, -1)]
            out = ''.join(out_ls) + ''.join(out_ls[-2::-1])
            print(out)
            cur += 1

            
        






if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # f(3)
