import requests


class MESConnector:
	def __init__(self, server: str, port: int = 80):
		self.__server = server
		self.__port = port

	def build_url(self, tool: str) -> str:
		url = f'http://{self.__server}:{self.__port}/mrs/{tool}'
		return url

	def execute_tool(self, tool: str, params: dict):
		url = self.build_url(tool)
		feedback = requests.post(url=url, params=params)
		result = dict()
		if feedback.status_code != 200:
			result['error_code'] = -1
			result['message'] = f'MES 工具调用失败。页面状态码: {feedback.status_code}'
		else:
			json = feedback.json()
			result['error_code'] = json['msgId']
			result['message'] = json['msgStr']
		return result

	def check_route(self, pcb_seq: str, prod_no: str, station_no: str, retest: bool):
		params = {
			'pcbSeq': pcb_seq,
			'prodNo': prod_no,
			'stationNo': station_no,
			'retest': 'true' if retest else 'false'
		}
		return self.execute_tool('checkRoute', params)

	def create_route(
			self, pcb_seq: str, prod_no: str, station_no: str, result: bool, user_no: str
	):
		params = {
			'pcbSeq': pcb_seq,
			'prodNo': prod_no,
			'stationNo': station_no,
			'result': 'PASS' if result else 'FAIL',
			'remark': '',
			'testItem': '',
			'userNo': user_no,
			'weight': 0,
			'packNo': '',
			'rmk1': '',
			'rmk2': '',
			'rmk3': '',
			'rmk4': '',
		}
		return self.execute_tool('createRoute', params)
