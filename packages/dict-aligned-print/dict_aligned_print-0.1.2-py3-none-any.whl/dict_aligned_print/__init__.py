def print_dict(dct, return_instead_of_print=False):
    max_key_length = max([len(k) for k in dct.keys()]) + 1
    max_key_length = str(max_key_length)
    raw_format = "{: >" + max_key_length + "} : {}"
    output = "\n".join([raw_format.format(k, v) for k, v in dct.items()])
    output += '\n' + '-' * 50 + '\n'
    if return_instead_of_print:
        return output
    else:
        print(output)


if __name__ == "__main__":
    dct = dict(my_key="hi", a=42, b='bb', my_key2=3)
    dct['another key'] = dict(a=4)
    print_dict(dct)
