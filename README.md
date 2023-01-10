###### ⚠️ Disclaimer: Reverse engineering process is shown for research purposes only.

# 👏 Get mails from Yopmail inbox
Get mails from a Yopmail inbox, save them as ``.html``


## 📖 Usage:
Install the latest version from PyPI by using [pip](https://pip.pypa.io/):
```
pip install yopmail
```

Instantiate ``Yopmail`` class with username as parameter (with ``@`` or not) and provide proxies if needed
```python
y = Yopmail('test', proxies=None)
```

Using ``get_mail_ids()`` method you get mail ids. You can provide (optional) ``page`` parameter otherwise page 1 is used as default. You can as well provide ``proxy`` parameter which would override instantiated class proxies.
```python
mails_ids = y.get_mail_ids(page=3)
```

Iterate over mail ids to get mail body using:
```python
for mail_id in mails_ids:
    mail = y.get_mail_body(mail_id, show_image=True)
    mail.save()
```
Again you can provide ``proxy`` parameter which would override instantiated class proxies.
``show_image`` is used to load mail images (equivalent to "load remote content" in most mail clients)
You can use ``save()`` method to save mail as ``.html``.


Feel free to contribute 🤝


## 📝 TODO:
- [ ] Add CSS to saved html mail

###### Feel free to contact me wherever you find me
