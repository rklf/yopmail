import datetime
import random
import string
import re
import requests
from bs4 import BeautifulSoup


class YopmailHTML:
    def __init__(self, html, username=None, mail_id=None):
        self.html = html
        self.mail_id = mail_id or ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
        self.username = username or ''

    def save(self, filename=None):
        filename = filename or f'{self.username}_{self.mail_id}.html'
        with open(filename, "w", encoding="utf8") as f:
            try:
                f.write(self.html)
                return True
            except Exception as err:
                print(f"[x] Couldn't save mail #{self.mail_id}:", err)
                return False

    def __repr__(self):
        return self.html


class Yopmail:
    def __init__(self, username, proxies=None):
        if not re.compile("^[-a-zA-Z0-9@_.+]{1,}$").match(username):
            raise ValueError("Username is not valid")
        self.username = username.split('@')[0]
        self.url = 'https://yopmail.com/en/'
        self.session = requests.Session()
        self.jar = requests.cookies.RequestsCookieJar()
        self.proxies = proxies
        
        # Yopmail needed parameters:
        self.yp = None
        self.yj = None
        self.ycons = None
        self.ytime = None

    def request(self, url: str, params=None, proxies=None, context: str = None) -> requests.models.Response|None:
        proxies = proxies if proxies is not None else self.proxies
        try:
            if self.yp is None:
                context = 'yp'
                req = self.session.get(self.url, proxies=proxies)
                if not req:
                    if req.status_code == 429:
                        raise requests.ConnectionError(f"Too Many Requests (429 status code) error, use a proxy or try again later")
                    raise Exception(req)
                self.extract_yp(req)
                params = {**params, 'yp': self.yp}

            if self.yj is None:
                context = 'yj'
                req = self.session.get('https://yopmail.com/ver/5.0/webmail.js', proxies=proxies)
                if not req:
                    if req.status_code == 429:
                        raise requests.ConnectionError(f"Too Many Requests (429 status code) error, use a proxy or try again later")
                    raise Exception(req)
                self.extract_yj(req)
                params = {**params, 'yj': self.yj}

            if self.ycons is None:
                context = 'ycons'
                req = self.session.get('https://yopmail.com/consent?c=deny', proxies=proxies) # Set consent cookies
                if not req:
                    if req.status_code == 429:
                        raise requests.ConnectionError(f"Too Many Requests (429 status code) error, use a proxy or try again later")
                    raise Exception(req)
            self.add_ytime()
            return self.session.get(url, params=params, cookies=self.jar, proxies=proxies)
        except requests.exceptions.ProxyError as err:
            print(f"[x] Couldn't process {context} request (ProxyError):", err)
            return None
        except requests.exceptions.ConnectionError as err:
            print(f"[x] Couldn't process {context} request (ConnectionError):", err)
            return None
        except requests.exceptions.Timeout as err:
            print(f"[x] Couldn't process {context} request (Timeout):", err)
            return None
        except Exception as err:
            print(f"[x] Couldn't process {context} request:", err)
            return None

    def add_ytime(self):
        now = datetime.datetime.now().time()
        self.ytime = f'{now.hour}:{now.minute}'
        self.jar.set('ytime', self.ytime, domain='yopmail.com', path='/')

    def extract_yp(self, req):
        # Looking for value of an hidden input element with 'yp' as name and id:
        #   <input type="hidden" name="yp" id="yp" value="XXX" />
        bs = BeautifulSoup(req.text, 'html.parser')
        el = bs.find('input', {'name': 'yp', 'id': 'yp'})
        self.yp = el['value']
    
    def extract_yj(self, req):
        # Looking for:
        #   value+'&yj=QBQVkAQVmZmZ4BQR0ZwNkAN&v='
        YJ_RE = re.compile("value\+\'\&yj\=([0-9a-zA-Z]*)\&v\=\'", re.MULTILINE)
        match = YJ_RE.search(req.text)
        self.yj = match.groups()[0]
    
    def get_inbox(self, page=1, proxies=None) -> requests.models.Response|None:
        params = {
            'login': self.username,
            'p': str(page), # page
            'd': '',        # mailid? to delete?
            'ctrl': '',     # mailid or ''
            'yp': self.yp,
            'yj': self.yj,
            'v': '8.4',
            'r_c': '',      # '' or recaptcha? 
            'id': '',       # idaff / sometimes "none" / nextmailid='last' / mailid = id('m%d'%mail_nr)
            'spam': True,   # False
            # 'scrl': '',
            # 'yf': '005',
        }
        return self.request(f'{self.url}inbox', params=params, proxies=proxies, context='inbox')

    def get_mail_ids(self, page=1, proxies=None) -> list|None:
        # We're looking for mail ids:
        if req := self.get_inbox(page=page, proxies=proxies):
            mails_ids = []
            bs = BeautifulSoup(req.text, 'html.parser')
            for mail in bs.find_all('div', {'class':'m'}):
                mails_ids.append(mail["id"])
            return mails_ids

    def get_mail_body(self, mail_id: int, show_image=False, proxies=None) -> YopmailHTML:
        if show_image:
            mail_id = f'i{mail_id}'
        else:
            mail_id = f'm{mail_id}'
        params = {
            'b': self.username,
            'id': mail_id  # mail_id "{'i' to show images || 'm' to don't}e_ZGpjZGV1ZwRkZwD0ZQNjAmx0AmpkAj=="
        }
        req = self.request(f'{self.url}mail', params=params, proxies=proxies, context='mail body')
        mail_html = str(BeautifulSoup(req.text, 'html.parser').find('div', {'id': 'mail'}))
        return YopmailHTML(mail_html, self.username, mail_id)
