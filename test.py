with open('client.csv', 'r', encoding='utf8') as f:
    fs = f.readlines()
    print(fs)
    print(''.join(fs))