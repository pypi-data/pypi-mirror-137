"""
API Wrapper for Temp Mail API.
"""
import string
import random
from hashlib import md5

import requests


class TempMail():
    """
    API Wrapper for Temp Mail API.
    """

    def __init__(self, api_key, api_endpoint='privatix-temp-mail-v1.p.rapidapi.com'):
        """
        API Wrapper for Temp Mail API.

        :param api_key: Temp Mail api_key, see README for instructions.
        :param api_endpoint: (optional) domain for temp-mail api.
        Default value is ``privatix-temp-mail-v1.p.rapidapi.com``.
        """

        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.headers = {
            'x-rapidapi-host': api_endpoint,
            'x-rapidapi-key': api_key
        }

    @property
    def domains_list(self):
        """
        Return list of available domains for use in email address.
        """
        if not hasattr(self, '_domains_list'):
            url = f'https://{self.api_endpoint}/request/domains/'
            response = requests.get(url, headers=self.headers)
            domains = response.json()
            setattr(self, '_domains_list', domains)
        return self._domains_list

    def get_emails(self, email):
        """
        Check and get a list of emails for a mailbox.

        :param email: email address.
        """

        email_md5 = self._get_md5_hash(email)
        url = f'https://{self.api_endpoint}/request/mail/id/{email_md5}/'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def delete_message(self, mail_id):
        """
        Delete message, where mail_id unique identifier assigned by the system.

        :param mail_id: unique message identifier.
        """

        url = f'https://{self.api_endpoint}/request/delete/id/{mail_id}/'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_message_attachments(self, mail_id):
        """
        Get message attachments by message id. Content response field encoded in base64 RFC 4648.

        :param mail_id: unique message identifier.
        """

        url = f'https://{self.api_endpoint}/request/atchmnts/id/{mail_id}/'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_one_attachment(self, mail_id, attachment_id):
        """
        Get one message attachments by message id and attachment id from attachments list.
        Content response field encoded in base64 RFC 4648.

        :param mail_id: unique message identifier.
        """
        url = f'https://{self.api_endpoint}/request/one_attachment/id/{mail_id}/{attachment_id}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_one_message(self, mail_id):
        """
        Get one message by id.

        :param mail_id: unique message identifier.
        """

        url = f'https://{self.api_endpoint}/request/one_mail/id/{mail_id}/'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def source_message(self, mail_id):
        """
        Get message source by mail_id.

        :param mail_id: unique message identifier.
        """

        url = f'https://{self.api_endpoint}/request/source/id/{mail_id}/'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_email_address(self, username=None, domain=None):
        """
        Return email address from username and domain.
        Randomly picked if not supplied.

        :param username: (optional) username for email address.
        :param domain: (optional) domain for email address.
        """
        if username is None:
            username = self.random_username()

        domains_list = self.domains_list
        if domain is None:
            domain = random.choice(domains_list)
        elif domain not in domains_list:
            raise ValueError('Domain not found in domains list.')
        return f'{username}{domain}'

    @staticmethod
    def random_username(min_length=6, max_length=10, digits=True):
        """
        Generate random username for email address.

        :param min_length: (optional) min username length.
        Default value is ``6``.
        :param max_length: (optional) max username length.
        Default value is ``10``.
        :param digits: (optional) use digits in username generation.
        Default value is ``True``.
        """
        chars = string.ascii_lowercase
        if digits:
            chars += string.digits
        length = random.randint(min_length, max_length)
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def _get_md5_hash(text):
        """
        Return md5 hash for given text.

        :param text: Any string.
        """
        return md5(text.encode('utf-8')).hexdigest()
