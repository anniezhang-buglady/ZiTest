from util.operation_excel import OperationExcel
from base.runmethod import RunMethod
from data.get_data import GetData
from jsonpath_rw import jsonpath, parse
import json


class DependentData:
    """解决数据依赖问题"""

    def __init__(self, case_id):
        self.case_id = case_id
        self.opera_excel = OperationExcel()
        self.data = GetData()

    def get_case_line_data(self):
        """
        通过case_id去获取该case_id的整行数据
        :param case_id: 用例ID
        :return:
        """
        rows_data = self.opera_excel.get_row_data(self.case_id)
        return rows_data

    def run_dependent(self):
        """
        执行依赖测试，获取结果
        :return:
        """
        run_method = RunMethod()
        row_num = self.opera_excel.get_row_num(self.case_id)
        #获取第三行
        print("1.row_num:", row_num)
        #直接获取第三行执行结果即可
        real_res = self.data.get_real_res(row_num)
        print("依赖case的执行结果：", real_res)
        return json.loads(real_res)

    def get_data_for_key(self, row):
        """
        根据依赖的key去获取执行依赖case的响应然后返回
        :return:
        """
        print(">>>>>>>>>>>>>>>>", row)
        depend_data = self.data.get_depend_key(row)
        print("2.depend_data:", depend_data)
        response_data = self.run_dependent()
        print("3.response_data", response_data)
        print("$$$$$$$$$$$$$$$:", [match.value for match in parse(depend_data).find(response_data)][0])
        return [match.value for match in parse(depend_data).find(response_data)][0]