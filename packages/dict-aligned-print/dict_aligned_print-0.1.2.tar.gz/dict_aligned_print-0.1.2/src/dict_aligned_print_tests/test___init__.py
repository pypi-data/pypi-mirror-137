from unittest import TestCase
from dict_aligned_print import print_dict


class Test(TestCase):
    def test_print_dict(self):
        """
        only checking if not compiling
        :return:
        """
        try:
            dct = dict(a=4, aaa="hi")
            print_dict(dct)
        except Exception as e:
            self.fail(e)

