from log import Log

from collections import OrderedDict
from http.client import HTTPConnection
import hashlib, json, math, random, time, zlib

class Connection:
    defaultServer = 'login.jianniang.com'
    defaultVersion = '2.1.0'
    secretKey = 'ade2688f1904e9fb8d2efdb61b5e398a'
    defaultUrlSettings = '&gz=1&market=2&channel=0'

    userAgent = 'Dalvik/2.1.0 (Linux; U; Android 6.0; sdk_phone_armv7 Build/MRA44C)'
    debugPort = 8080

    def __init__(self, version = None, debug = False):
        if version is None:
            version = Connection.defaultVersion
        self.version = version
        self.server = Connection.defaultServer
        self.cookie = None
        self.debug = debug
        self.lastResponse = None

    def setServer(self, server):
        self.server = server

    def get(self, url):
        Log.d('GET ' + url)
        url = self.completeUrl(url)
        headers = self.createHeaders()
        conn = self.createConnection()
        conn.request('GET', url, None, headers)
        self.lastResponse = self.parseResponse(conn.getresponse())
        return self.lastResponse

    def post(self, url, param):
        Log.d('POST ' + url)
        Log.d('    ' + param)
        url = self.completeUrl(url)
        headers = self.createHeaders(param)
        conn = self.createConnection()
        conn.request('POST', url, param, headers)
        self.lastResponse = self.parseResponse(conn.getresponse())
        return self.lastResponse

    def completeUrl(self, url):
        ts = str(math.trunc(time.time()))
        rand = ''.join([ str(random.randint(0,9)) for i in range(3) ])
        checksum = hashlib.md5((ts + rand + Connection.secretKey).encode('utf-8')).hexdigest()
        return url + '&t=' + ts + rand + '&e=' + checksum + Connection.defaultUrlSettings + '&version=' + self.version

    def getTimestamp():
        time_of_20150101 = 63555667200
        delta = datetime.now() - datetime(2015, 1, 1)
        seconds = delta.total_seconds() + time_of_20150101
        return str(math.trunc(seconds * 10000000))

    def createHeaders(self, param = None):
        if self.cookie is None:
            headers = Connection.basicHeaders
        elif param is None:
            headers = Connection.cookieHeaders
            headers['Cookie'] = self.cookie
        else:
            headers = Connection.postHeaders
            headers['Cookie'] = self.cookie
            headers['Content-Length'] = len(param)
        headers['Host'] = self.server
        return headers

    def createConnection(self):
        if self.debug:
            conn = HTTPConnection('127.0.0.1', Connection.debugPort)
            conn.set_tunnel(self.server)
        else:
            conn = HTTPConnection(self.server)
        return conn

    def parseResponse(self, resp):
        data = zlib.decompress(resp.read())
        data = json.loads(data.decode('utf-8'))
        cookie = resp.getheader('Set-Cookie')
        if cookie is not None:
            self.setCookie(cookie)
        if 'eid' in data:
            Log.w('eid:%d' % data['eid'])
        Log.v(data)
        return data

    def setCookie(self, cookie):
        aliyunPos = cookie.find('aliyungf_tc=')
        if aliyunPos == -1: return
        start = aliyunPos + len('aliyungf_tc=')
        end = cookie.find(';', start)
        aliyun = cookie[start:end]

        hfPos = cookie.find('hf_skey=')
        if hfPos == -1: return
        start = hfPos + len('hf_skey=')
        end = cookie.find(';', start)
        hf = cookie[start:end]

        self.cookie = 'aliyungf_tc=' + aliyun + '; HttpOnly;hf_skey=' + hf + '; path=/;QCLOUD=a'

    basicHeaders = OrderedDict([
        ('Accept-Encoding', 'identity'),
        ('User-Agent', userAgent),
        ('Host', None),
        ('Connection', 'Keep-Alive')
    ])

    cookieHeaders = OrderedDict([
        ('Accept-Encoding', 'identity'),
        ('Cookie', None),
        ('User-Agent', userAgent),
        ('Host', None),
        ('Connection', 'Keep-Alive')
    ])

    postHeaders = OrderedDict([
        ('Accept-Encoding', 'identity'),
        ('Cookie', None),
        ('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', userAgent),
        ('Host', None),
        ('Connection', 'Keep-Alive'),
        ('Content-Length', None)
    ])
