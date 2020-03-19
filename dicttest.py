import sys

output_dict = {}

def handle_data(arg):
    for arg in sys.argv[1:]:
        k, v = arg.split(":")
        output_dict[k] = v
                
def print_data():
    for key in output_dict:
        print("ID:{} Name:{}".format(key, output_dict[key]))

def print_dataaaa(d):
    for key in d:
        print("ID:{} Name:{}".format(key, d[key]))

if __name__ == '__main__':
    s = sys.argv[1:]
    handle_data(s)
    #print_data()
    print_dataaaa(output_dict)
