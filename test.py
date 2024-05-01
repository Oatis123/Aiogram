with open('client.txt', 'w') as f:
    for i in range(1, 11):
        f.write(f'{i}\n')
    f.close()