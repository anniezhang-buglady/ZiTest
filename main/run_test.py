from base.runmethod import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from data.dependent_data import DependentData
from util.send_mail import SendEmail
from util.operation_header import OperationHeader
from util.operation_json import OperationJson
import json


class RunTest:

    def __init__(self):
        self.run_method = RunMethod()
        self.data = GetData()
        self.com_util = CommonUtil()
        self.send_email = SendEmail()

    def go_on_run(self):
        """程序执行"""
        pass_count = []
        fail_count = []
        no_run_count = []
        res = None
        # 获取用例数
        rows_count = self.data.get_case_lines()
        print(rows_count)
        # 第一行索引为0
        for i in range(1, rows_count):
            print("i:", i)
            is_run = self.data.get_is_run(i)
            print(is_run)
            if is_run:
                url = self.data.get_request_url(i)
                print("url:", url)
                method = self.data.get_request_method(i)
                print("method:", method)
                request_data = self.data.get_data_for_json(i)
                print("request_data:", request_data)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", type(request_data))
                expect = self.data.get_expect_data(i)
                print("expect:", expect)
                header = self.data.is_header(i)
                print("header:", header)
                token = self.data.is_token(i)
                print("token:", token)
                depend_case = self.data.is_depend(i)
                print("depend_case:", depend_case)

                if depend_case != None:
                    self.depend_data = DependentData(depend_case)
                    # 获取依赖的响应数据
                    print("#### i", i)
                    depend_response_data = self.depend_data.get_data_for_key(i)
                    print("##################")
                    print("1depend_response_data:", depend_response_data)
                    # 获取依赖的key
                    depend_key = self.data.get_depend_field(i)
                    print("depend_key:", depend_key)
                    # 更新请求字段
                    request_data.get('params')[depend_key] = depend_response_data
                    #request_data = json.dumps(request_data, ensure_ascii=False)
                    print("request_data:", request_data)
                    print(type(request_data))
                # 如果header字段值为write则将该接口的返回的token写入到token.json文件，如果为yes则读取token.json文件
                if header == "write_token":
                    print("********************")
                    res = self.run_method.run_main(method, url, request_data).json()
                    print("res:", res)
                    print("res type", type(res))
                    #print("res.json():", res.json())
                    op_header = OperationHeader(res)
                    op_header.write_token()
                elif header == 'write_cookie' and token == 'yes':
                    print("case22222222222222")
                    op_json = OperationJson("../dataconfig/token.json")
                    token = op_json.get_data('data')
                    request_data = dict(request_data, **token)  # 把请求数据与登录token合并，并作为请求数据
                    print("login_data", request_data)
                    res = self.run_method.run_main(method, url, request_data)
                    print("res_login:", res)
                    print(type(res))
                    op_header = OperationHeader(res)
                    op_header.write_cookie()
                elif header == 'get_cookie' and token == 'yes':
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    op_json1 = OperationJson('../dataconfig/cookie.json')
                    op_json2 = OperationJson('../dataconfig/token.json')
                    cookies = op_json1.get_data('cookie')
                    token = op_json2.get_data('data')
                    request_data = dict(request_data, **token)
                    print("post_data:", request_data)
                    print("cookie:", cookies)
                    new_value = json.dumps(request_data.get("params"))
                    request_data["params"] = new_value
                    res = self.run_method.run_main(method, url, request_data, cookies=cookies)
                    print("res:", type(res))
                else:
                    res = self.run_method.run_main(method, url, request_data)

                if expect != None:
                    if self.com_util.is_contain(expect, res):
                        self.data.write_result(i, "Pass")
                        pass_count.append(i)
                        if type(res) is dict:
                            self.data.write_real_res(i, json.dumps(res))
                        else:
                            self.data.write_real_res(i, json.dumps(res.json()))
                    else:
                        self.data.write_result(i, "Fail")
                        fail_count.append(i)
                        if type(res) is dict:
                            self.data.write_real_res(i, json.dumps(res))
                        else:
                            self.data.write_real_res(i, json.dumps(res.json()))
                else:
                    print(f"用例ID：case-{i}，预期结果不能为空")
            else:
                self.data.write_result(i, "Not run")
                no_run_count.append(i)

        # 发送邮件

        print(f"通过用例数：{len(pass_count)}")
        print(f"失败用例数：{len(fail_count)}")
        print(f"未执行败用例数：{len(no_run_count)}")

        self.send_email.send_main(pass_count, fail_count, no_run_count)


if __name__ == '__main__':
    run = RunTest()
    run.go_on_run()
