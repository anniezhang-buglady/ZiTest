import json
import requests

requests.packages.urllib3.disable_warnings()


class RunMethod:

    def post_main(self, url, data=None, header=None, cookies=None):
        res = None
        if header != None:
            res = requests.post(url=url, data=data, headers=header, cookies=cookies, verify=False)
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(data)
            res = requests.post(url=url, data=data, cookies=cookies, verify=False, )
            # print("rrrrrrrrrrrrrr:", res.cookies)
            # print(type(res.cookies))
        return res

    def get_main(self, url, data=None, header=None, cookies=None):
        res = None
        if header != None:
            res = requests.get(url=url, params=data, headers=header, cookies=cookies, verify=False)
        else:
            res = requests.get(url=url, params=data, cookies=cookies, verify=False)
        return res

    def delete_main(self, url, data=None, header=None, cookies=None):
        res = None
        if header != None:
            res = requests.delete(url=url, data=data, header=header, cookies=cookies, verify=False)
        else:
            res = requests.delete(url=url, data=data, cookies=cookies, verify=False)
        return res

    def run_main(self, method, url, data=None, header=None, cookies=None):
        res = None
        if method == 'Post':
            print("post请求：@@@@@@@@@@@@@@@@@")
            res = self.post_main(url, data, header, cookies)
        elif method == 'Get':
            res = self.get_main(url, data, header, cookies)
        else:
            res = self.delete_main(url, data, header, cookies)
        # return json.dumps(res, indent=2, sort_keys=True, ensure_ascii=False)
        return res


if __name__ == '__main__':
    url = 'http://172.16.235.8/api/v1/system/token'
    data = {
        "oauth_consumer_key": "admin",
        "oauth_consumer_secret": "admin"
    }

    run = RunMethod()
    run_test = run.run_main(method="Post", url=url, data=data)
