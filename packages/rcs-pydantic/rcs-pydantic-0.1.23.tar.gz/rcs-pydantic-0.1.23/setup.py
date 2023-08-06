# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rcs_pydantic']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'rcs-pydantic',
    'version': '0.1.23',
    'description': '',
    'long_description': '# RCS-PYDANTIC\n\n<p align="center">\n<a href="https://github.com/xncbf/rcs-pydantic/actions?query=workflow%3ATests+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/xncbf/rcs-pydantic/workflows/Tests/badge.svg?event=push&branch=main" alt="Test">\n</a>\n<a href="https://codecov.io/gh/xncbf/rcs-pydantic" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/xncbf/rcs-pydantic?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/rcs-pydantic" target="_blank">\n    <img src="https://img.shields.io/pypi/v/rcs-pydantic?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/rcs-pydantic" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/rcs-pydantic.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n- [RCS-PYDANTIC](#rcs-pydantic)\n  - [Introduce](#introduce)\n  - [Installation](#installation)\n  - [Quick start](#quick-start)\n  - [제공되는 항목](#제공되는-항목)\n    - [제공되는 데이터 구조체](#제공되는-데이터-구조체)\n    - [제공되는 데이터 관련 Enum](#제공되는-데이터-관련-enum)\n    - [제공되는 에러 코드 Enum](#제공되는-에러-코드-enum)\n  - [Features](#features)\n    - [RcsMessage](#rcsmessage)\n    - [MessageException](#messageexception)\n  - [Contribution](#contribution)\n\n## Introduce\n\n한국 통신사 rcs 를 위한 pydantic 구조체\n\n## Installation\n\n```sh\npip install rcs-pydantic\n```\n\n## Quick start\n\n```py\nfrom rcs_pydantic import MessageInfo, RcsMessage\n\nmessage_info = {\n    "replyId": "B01RDSFR.KcNNLk67ui.FDSAF432153214",\n    "eventType":"newUser",\n    "displayText": "안녕",\n    "userContact":"01012341234",\n    "chatbotId":"0212351235",\n    "timeStamp": "2020-03-03T04:43:55.867+09"\n}\n\nrcs = {\n    "message_base_id": "SS000000",\n    "service_type": "RCSSMS",\n    "agency_id": "<str: agency_id>",\n    "body": {\n        "title": "타이틀",\n        "description": "일반 RCSSMS 테스트 메시지 입니다."\n    }\n}\n\n\nrcs_message = RcsMessage(message_info=MessageInfo(**message_info), **rcs)\n```\n\n```sh\n>>> print(rcs_message.send_info)\ncommon=CommonInfo(\n    msgId=\'4be0072f-0f05-4b3a-adc8-90d7ef309c53\',\n    userContact=\'01012341234\',\n    scheduleType=<ScheduleTypeEnum.IMMEDIATE: 0>,\n    msgServiceType=<MessageServiceTypeEnum.RCS: \'rcs\'>\n)\nrcs=RcsInfo(\n    chatbotId=\'0212351235\',\n    agencyId=\'<str: agency_id>\',\n    messagebaseId=\'SS000000\',\n    serviceType=<ServiceTypeEnum.SMS: \'RCSSMS\'>,\n    expiryOption=<ExpiryOptionEnum.AFTER_SETTING_TIMES: 2>,\n    header=<HeaderEnum.NOT_ADVERTISE: \'0\'>,\n    copyAllowed=True,\n    body=RcsSMSBody(title=\'타이틀\', description=\'일반 RCSSMS 테스트 메시지 입니다.\'),\n)\n>>>\n```\n\n## 제공되는 항목\n\n국내 통신사 RCS 문서에서 제공되는 모든 데이터 구조체를 지원합니다.\n\n### 제공되는 데이터 구조체\n\n```python\nRcsMessage\nRCSErrorCode\nRcsSMSBody\nRcsLMSBody\nRcsMMSBody\nRcsCHATBody\nRcsTMPLBody\nRcsSMSCarouselBody\nRcsLMSCarouselBody\nRcsMMSCarouselBody\nRcsCHATCarouselBody\nLocationInfo\nShowLocationInfo\nOpenUrlInfo\nCreateCalendarEventInfo\nCopyToClipboardInfo\nComposeTextMessageInfo\nDialPhoneNumberInfo\nUrlActionInfo\nLocalBrowserActionInfo\nMapActionInfo\nCalendarActionInfo\nClipboardActionInfo\nComposeActionInfo\nDialActionInfo\nPostbackInfo\nActionInfo\nSuggestionInfo\nButtonInfo\nCommonInfo\nRcsInfo\nLegacyInfo\nStatusInfo\nQuerystatusInfo\nErrorInfo\nResponseErrorInfo\nResponseInfo\nTextMessageInfo\nFileMessageInfo\nGeolocationPushMessage\nUserLocationInfo\nMessageInfo\nSendInfo\nTokenInfo\n```\n\n### 제공되는 데이터 관련 Enum\n\n```python\nEventTypeEnum\nRCSMessageEnum\nMessageEnum\nMessageStatusEnum\nMnoInfoEnum\nBillEnum\nMessageServiceTypeEnum\nServiceTypeEnum\nLegacyServiceTypeEnum\nScheduleTypeEnum\nExpiryOptionEnum\nHeaderEnum\nActionEnum\n```\n\n### 제공되는 에러 코드 Enum\n\n```python\nLegacyErrorCodeEnum\nErrorCodeEnum\nMaaPErrorCodeEnum\nRcsBizCenterErrorCodeEnum\nKTErrorCodeEnum\nRCSErrorCode\n```\n\n## Features\n\n### RcsMessage\n\n`RcsMessage` 클래스는 메세지 전송을 위한 `SendInfo` 구조체를 만듭니다.\n\n```py\nfrom rcs_pydantic import MessageInfo, RcsMessage\n\nmessage_info = {\n    "replyId": "B01RDSFR.KcNNLk67ui.FDSAF432153214",\n    "eventType":"newUser",\n    "displayText": "안녕",\n    "userContact":"01012341234",\n    "chatbotId":"0212351235",\n    "timeStamp": "2020-03-03T04:43:55.867+09"\n}\n\nrcs = {\n    "message_base_id": "SS000000",\n    "service_type": "RCSSMS",\n    "agency_id": "<str: agency_id>",\n    "body": {\n        "title": "타이틀",\n        "description": "일반 RCSSMS 테스트 메시지 입니다."\n    }\n}\n\n\nrcs_message = RcsMessage(message_info=MessageInfo(**message_info), **rcs)\n```\n\n### MessageException\n\n`MessageException` 예외 클래스는 여러 종류의 모든 error 코드를 포함하는 예외 클래스입니다.\n\n```python\nfrom rcs_pydantic.exceptions import MessageException\n\nraise MessageException(40003)\n```\n\n## Contribution\n\n이 프로젝트는 기여를 환영합니다!\n\n패치를 제출하기 전에 issue 티켓을 먼저 제출해주세요.\n\nPull request 는 `main` 브랜치로 머지되며 항상 사용 가능한 상태로 유지해야 합니다.\n\n모든 테스트 코드를 통과한 뒤 리뷰한 후 머지됩니다.\n',
    'author': 'xncbf',
    'author_email': 'xncbf12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xncbf/rcs-pydantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
