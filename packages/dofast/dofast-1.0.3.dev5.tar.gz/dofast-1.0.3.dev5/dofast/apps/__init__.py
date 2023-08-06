import codefast as cf
from dofast.data.dynamic import TOKEN, SERVER_HOST
import sys
from dofast.utils import DeeplAPI, google_translate
from dofast.network import bitly as bitly_shortener
import enum


class TweetText(object):
    def __init__(self, content: str = '') -> None:
        self.content = content

    @property
    def len(self) -> int:
        return sum([2 if cf.nstr(c).is_cn() else 1 for c in self.content])

    def extend(self, text: str) -> None:
        self.content += text

    def __str__(self) -> str:
        return self.content


class Tweet(object):
    def __init__(self) -> None:
        self.BOUND: int = 280
        self.text, self.media = TweetText(), []
        for a in sys.argv[2:]:
            if not cf.io.exists(a):
                self.text.extend(a)
            elif a.endswith(('.txt', '.dat')):
                self.text.extend(cf.io.reads(a))
            else:
                self.media.append(a)

    @cf.utils.retry()
    def post(self) -> None:
        if self.text.len > self.BOUND:
            raise Exception('Tweet text is too long, {}'.format(self.text.len))
        files = [('images', (cf.io.basename(m), open(m, 'rb'), 'image/png'))
                 for m in self.media]
        resp = cf.net.post(SERVER_HOST,
                           params={
                               'text': str(self.text),
                               'token': TOKEN
                           },
                           files=files)
        cf.info('Tweet response: {}'.format(resp))
        cf.info(resp.json())
        return self


class HttpTools(object):
    def __init__(self) -> None:
        pass

    def url_shortener(self, url: str):
        print(
            cf.net.get('http://is.gd/create.php',
                       params={
                           'format': 'simple',
                           'url': url
                       }).text)
        return self

    def bitly(self, url):
        bitly_shortener(url)
        return self


class _TranslatorClient(str, enum.Enum):
    GOOGLE = 'google'
    DEEPL = 'deepl'


class _Translator(object):
    def __init__(self) -> None:
        self.deeplapi = DeeplAPI()

    def run(self, client: _TranslatorClient = 'deepl'):
        if client == _TranslatorClient.DEEPL:
            if len(sys.argv) <= 2:
                self.api.stats
            else:
                text_or_file = sys.argv[2]
                if cf.io.exists(text_or_file):
                    self.api.translate(cf.io.reads(text_or_file))
                else:
                    self.api.translate(text_or_file)
        else:
            texts = ' '.join(sys.argv[2:])
            google_translate(texts)
        return self


class Apps(object):
    def __init__(self) -> None:
        self.tweetbot = Tweet()
        self.httptools = HttpTools()
        self.translator = _Translator()
