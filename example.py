#!/usr/bin/python
import sys
from ym import Yopmail

def main():
    y = Yopmail('test', proxies=None)
    mails_ids = y.get_mail_ids(page=3)
    for mail_id in mails_ids:
        mail = y.get_mail_body(mail_id)
        mail.save()

if __name__ == "__main__":
    main()
    sys.exit()
