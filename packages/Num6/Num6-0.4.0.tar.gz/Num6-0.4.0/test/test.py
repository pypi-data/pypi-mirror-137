import num6
import string
import timeit


txt = f'''This is a character list from python example. It is designed by md. Almas Ali in Bangladesh.\nTry it for more details & read the README.md file for more informations.

{string.ascii_letters}

{string.ascii_lowercase}

{string.ascii_uppercase}

{string.digits}

{string.punctuation}

'''

a = timeit.timeit()
en = num6.encrypt(txt, 400)
b = timeit.timeit()

c = timeit.timeit()
de = num6.decrypt(en, 400)
d = timeit.timeit()

print(f'[+] Encryption time : {b-a}')
print(f'[+] Decryption time : {d-c}')

if txt == de:
    print('[+] TEXT MACHED SUCCESS !')
else:
    print('[-] TEXT MACHED FAILED !')

# print(f'{en}\n\n\n{de}')
