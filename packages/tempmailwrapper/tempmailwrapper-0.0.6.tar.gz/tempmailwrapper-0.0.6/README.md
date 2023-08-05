# tempmailwrapper

This is an improved and updated version of the outdated Github project [Tempmail][tempmail-repo-outdated]. Changes:
-  Completely up to date with the new Temp Mail API on RapidAPI.
-  Full Python3 support
-  Code improvements

## Description
Python API wrapper for [Temp Mail][tempmail-website]. **Disposable email** - is a free email service that allows to receive email at a temporary address that self-destructed after a certain time elapses. You can view full API specification in [here][tempmail-api] or [here][rapidapi].


## Prerequisites
- Python 3.X


## Installation
    $ pip install tempmailwrapper

## Usage
Start by navigating to [RapidAPI][rapidapi] to obtain an API key. Create an account, fill in your details and subscribe to one of the plans. There's a free plan allowing for up to 100 request/day for free.

Once you have the API key, you can follow these examples:

Setting up a temporary email:

    $ from tempmailwrapper import tempmailwrapper
    $ tm = tempmailwrapper.TempMail(api_key="YOUR_API_KEY_HERE")
    $ random_email_address = tm.get_email_address()
    $ specific_email_address = tm.get_email_address(username='testing', domain='subcaro.com')

---

Get list of all emails for an email address:

    $ from tempmailwrapper import tempmailwrapper
    $ tm = tempmailwrapper.TempMail(api_key="YOUR_API_KEY_HERE")
    $ email_address = tm.get_email_address()
    $ print(random_email_address) # Now send an email here.
    $ emails_list = tm.get_emails(email_address)

---

Get specific email:

    $ from tempmailwrapper import tempmailwrapper
    $ tm = tempmailwrapper.TempMail(api_key="YOUR_API_KEY_HERE")
    $ email_address = tm.get_email_address()
    $ print(random_email_address) # Now send an email here.
    $ emails_list = tm.get_emails(email_address)
    $ first_email_id = emails[0]['mail_id']
    $ email = tm.get_one_message(first_email_id)
    $ print(email.text) # Tip: use a library like BeautifulSoup to navigate your way easier through HTML-formatted emails.

    
    


[tempmail-repo-outdated]: <https://github.com/CITGuru/tempmail>

[tempmail-website]: <https://temp-mail.org/>
[tempmail-api]: <https://temp-mail.org/en/api/>
[rapidapi]: <https://rapidapi.com/Privatix/api/temp-mail>

