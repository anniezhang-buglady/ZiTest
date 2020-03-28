import json,requests
from util.operation_json import OperationJson
from base.runmethod import RunMethod


class OperationHeader:

    def __init__(self, response):
        self.response = response

    def get_response_token(self):
        '''
        获取登录返回的token
        '''
        token = {"data": {"account_token": self.response['account_token']}}
        print("token:", token)
        return token

    def write_token(self):
        op_json = OperationJson()
        op_json.write_token(self.get_response_token())


    def get_cookie(self):
        '''
        获取cookie的jar文件
        '''
        cookie_jar = self.response.cookies
        cookie = requests.utils.dict_from_cookiejar(cookie_jar).get("SSO_COOKIE_KEY")
        cookies = {"cookie": {'SSO_COOKIE_KEY': cookie}}
        print("cookie:", cookie)
        return cookies


    def write_cookie(self):
        op_json = OperationJson()
        op_json.write_cookie(self.get_cookie())


if __name__ == '__main__':

    url = 'http://172.16.235.8/api/v1/system/token'

    data = {
        "oauth_consumer_key": "admin",
        "oauth_consumer_secret": "admin"
    }
    run_method=RunMethod()
    # res = json.dumps(requests.post(url, data).json())
    res=run_method.run_main('Post', url, data)
    op = OperationHeader(res)
    op.write_token()
