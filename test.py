# with open('client.csv', 'r', encoding='utf8') as f:
#     fs = f.readlines()
#     print(''.join(fs))

import yaml
# from yaml import FullLoader

with open('texts.yaml', 'r', encoding='utf-8') as file:
    TEXTS = yaml.safe_load(file)
    name = 'me'
    print(TEXTS['greet'].format(name=name))


string = '64r7457567 pedro'

print(string.rsplit(maxsplit=1))