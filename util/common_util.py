import json

class CommonUtil:
    def is_contain(self, str_one, str_two):
        """
        判断一个字符串是否在另一个字符串中
        :param str_one:
        :param str_two:
        :return:
        """
        flag = None
        print("str_two:", str_two)
        if type(str_two) is dict:
            print("%%%%%%%%%%%%%%%%%%%%%%%")
            str_two = json.dumps(str_two)
            if str_one in str_two:
                flag = True
            else:
                flag = False
        else:
            print("::::::::::::::::::::::::")
            str_two = json.dumps(str_two.json())
            if str_one in str_two:
                flag = True
            else:
                flag = False
        return flag

