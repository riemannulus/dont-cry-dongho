import logging

import requests

logger = logging.getLogger('pythecamp')


class LetterInfo:
    content = None
    subject = None
    trainee_msg_seq = None

    def __init__(self, content, subject, trainee_msg_seq=792934):
        self.content = "<p>" + content + "</p>"
        self.subject = subject
        self.trainee_msg_seq = trainee_msg_seq


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/76.0.3809.132 Safari/537.36"
    })
    session.hooks = {
        'response': [
            lambda r, *args, **kwargs: print(f'RESPONSE {r.status_code} {r.text}'),
            lambda r, *args, **kwargs: r.raise_for_status(),
        ]
    }

    return session


class TheCampRequestError(Exception):
    ...


class TheCampClient:
    API_HOST = 'https://www.thecamp.or.kr'
    LOGIN_PATH = "/login/loginA.do"
    SEND_LETTER_PATH = "/consolLetter/insertConsolLetterA.do"
    CONTENT_TYPE = "application/x-www-form-urlencoded; charset=UTF-8"
    REFERER = "https://www.thecamp.or.kr/consolLetter/viewConsolLetterInsert.do"

    def __init__(self):
        self.session = build_session()

    def _request(self, endpoint: str, data: dict) -> dict:
        without_credential = data.copy()
        if 'userPwd' in without_credential:
            without_credential['userPwd'] = '********'
        print(f'REQUEST {endpoint} with data {without_credential}')
        res = self.session.post(f'{self.API_HOST}{endpoint}', data=data)

        if res.json()['resultCd'] != "0000":
            raise TheCampRequestError(f'TheCamp 응답 코드가 예상 응답 코드와 다릅니다. {res.text}')

        return res.json()

    def login(self, username: str, password: str) -> None:
        print(f'로그인을 시도합니다. username: {username}')
        self._request(self.LOGIN_PATH, {
            'state': 'email-login', 'autoLoginYn': 'N', 'userId': username, 'userPwd': password
        })
        print('로그인에 성공하였습니다.')

    def write_letter(
        self,
        letter_info: LetterInfo,
    ) -> None:

        print(f'편지를 씁니다.')
        self._request(self.SEND_LETTER_PATH, {
            'boardDiv': 'sympathyLetter',
            'tempSaveYn': 'N',
            'traineeMgrSeq': letter_info.trainee_msg_seq,
            'sympathyLetterContent': letter_info.content,
            'sympathyLetterSubject': letter_info.subject,
        })
        print('편지 쓰기 완료!')
