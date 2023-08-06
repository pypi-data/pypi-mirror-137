## dict_aligned_print

### print non nested dict in aligned way

```
usage example:
    input:
        from dict_aligned_print import print_dict

        dct = dict(my_key="hi", a=42, b='bb', my_key2=3)
        dct['another key'] = dict(a=4)
        
        print_dict(dct)
    
    output:
             my_key : hi
                  a : 42
                  b : bb
            my_key2 : 3
        another key : {'a': 4}
        --------------------------------------------------
```
