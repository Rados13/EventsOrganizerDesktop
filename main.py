import pandas as pd

file = '.\sheet2.xlsx'


def print_hi(name):
    print(f'Hi, {name}')
    df = pd.read_excel(file,engine='openpyxl')
    print(df)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
