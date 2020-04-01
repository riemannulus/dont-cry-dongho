import os

from dotenv import load_dotenv, find_dotenv
from pythecamp import TheCampClient, LetterInfo


load_dotenv(find_dotenv(), encoding='utf-8')


def get_env_variable(var_name, default=None):
    try:
        return os.environ[var_name]

    except KeyError:
        if default is None:
            error_msg = '필수 환경 변수 {}가 설정되지 않았습니다.'.format(var_name)
            raise ValueError(error_msg)

        return default


def send_message(title: str, content: str) -> None:
    client = TheCampClient()
    email = get_env_variable('DONTCRY_EMAIL')
    pw = get_env_variable('DONTCRY_PW')
    trainee_id = get_env_variable('DONTCRY_TRAINEE_ID')
    client.login(email, pw)
    letter_info = LetterInfo(title, content, trainee_id)
    client.write_letter(letter_info)


def chunk_and_send_message(title: str, content: str) -> None:
    content = content.replace('\r\n', '\n')
    content = content.replace('\r', '\n')
    content = content.replace('\n', '    ')

    print('##############\n', content)

    if len(title) > 15:
        title = title[:15] + '...'

    for index, chunk in enumerate(range(0, len(content), 1500)):
        msg_chunked = content[chunk:chunk + 1500]
        msg_chunked = msg_chunked
        title_chunked = f'{title}({index + 1})'
        print(f'타이틀: {title_chunked}\n메세지: {msg_chunked}\n메세지를 전송합니다. {index}')

        send_message(title_chunked, msg_chunked)
