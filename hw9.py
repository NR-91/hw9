user_list = []

def decorator_main(func):
    def wrap(*word):
        print('----Phone book Console Bot----\n'
              ' Commands: \n'
              '     hello - start bot\n'
              '     add - add new contact \n'
              '     change - change contact phone \n'
              '     phone - Search by name \n'
              '     show all - Show all list contact\n'
              '     goodbye, close, . - exit')
        print('-'*30)
        print(func())
    return wrap


def decorator_all(func):
    def wrap(*text):
        print(func(*text))
    return wrap

@decorator_all
def save_contacts(source, output):
    s = ''
    with open(output, 'w') as fn_o:
        for l in source:
            for _ in l.items():
                s = "{}, {}".format(l['name'], ",".join([p for p in l['phone']]).strip())
            fn_o.write(s+'\n')
            s = ''
    return 'Save sucssesful'

@decorator_all
def load_contacts(path):
    with open(path, 'r') as fh:
        while True:
            line = fh.readline()
            if not line:
                break
            l = line.split(',')
            user_list.append(dict({'name': str(l[0]), 'phone': l[1:]}))    
    return 'Load sucssesful'

@decorator_all
def hello() -> str:
    decorator_all(load_contacts('contacts.txt'))
    return 'How can I help you?'

@decorator_all
def add():
    n_p = input('Enter name and phone:').split(' ')
    user_list.append(dict({'name': str(n_p[0]).title(), 'phone': list(n_p[1:])}))
    return 'Add sucssesful!'
    
@decorator_all
def change():
    n_p = input('Enter name and phone:').split(' ')

    for dct in user_list:
        if dct['name'] == n_p[0]:
            dct['phone'] = n_p[1:]
            # return "{}, {}".format(dct['name'], ",".join([p for p in dct['phone']]).strip())
    return 'Update sucssesful!'

@decorator_all
def phone() -> str:
    src_by_name = input('Enter name:')
    for dct in user_list:
        if dct['name'] == src_by_name:
            return "Phone: {}".format(",".join([p for p in dct['phone']]))
    return 'Not find!'
        
        
def decor_table(func):
    def wrap(*words):
        print(' -'*19)
        print("|{:^5}|{:^15}|{:^15}".format('#', 'Name', 'Phone'))
        print(' -'*19)
        func(*words)
        print(' -'*19)
    return wrap
 
@decor_table        
def show_all():
    i = 1
    for dct in user_list:
        print("{:^5} {:^15} {:^15}".format(i, dct['name'], ",".join([p for p in dct['phone']]).strip()))
        i += 1
        
@decorator_all
def good_bye():
    return 'Good bye!'


COMMAND_DICT = {'hello': hello,
                 'add': add,
                 'change': change,
                 'phone': phone,
                 'show all': show_all,
                 'goodbye': good_bye,
                 'close': good_bye,
                 '.': good_bye}


def get_command(words):
    if words in COMMAND_DICT:
        return COMMAND_DICT[words]
    raise KeyError("This command doesn't exist")

@decorator_main
def main():
    while True:
        input_c = input(">>> ")
        
        try:
            func = get_command(input_c)
        except KeyError as error:
            print(error)
            continue
        
        func()
        
        if input_c in ['goodbye', 'close', '.']:
            save_contacts(user_list, 'contacts.txt')
            break
        
if __name__ == '__main__':
    main()