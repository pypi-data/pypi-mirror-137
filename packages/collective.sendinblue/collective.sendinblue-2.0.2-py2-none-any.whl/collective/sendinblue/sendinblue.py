# -*- coding: utf-8 -*-

from plone.registry.interfaces import IRegistry
from sib_api_v3_sdk.rest import ApiException
from zope.component import getUtility
from zope.interface import implementer
import logging
import sib_api_v3_sdk

from collective.sendinblue.interfaces import ISendinblueAPI
from collective.sendinblue.interfaces import ISendinblueSettings

_marker = object()
logger = logging.getLogger("collective.sendinblue")


@implementer(ISendinblueAPI)
class SendinblueAPI(object):
    """Utility for Sendinblue API calls"""

    key_accounts = "collective.sendinblue.cache.accounts"
    key_lists = "collective.sendinblue.cache.lists"

    def __init__(self):
        self.registry = None
        self.settings = None
        self.api_keys = []

    def initialize(self):
        """Load settings from registry"""
        if self.registry is None:
            self.registry = getUtility(IRegistry)
        if self.settings is None:
            self.settings = self.registry.forInterface(ISendinblueSettings)
        self.api_keys = self.settings.api_keys

    def connect(self, api_key):
        """Create client"""
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = api_key
        client = sib_api_v3_sdk.ApiClient(configuration)
        return client

    def lists(self):
        """Retrieves lists (cached)"""
        self.initialize()
        cache = self.registry.get(self.key_lists, _marker)
        if cache and cache is not _marker:
            return cache
        return self._lists()

    def _lists(self):
        """The actual API call for lists"""
        lists = {}
        for api_key in self.api_keys:
            client = self.connect(api_key)
            api_list = sib_api_v3_sdk.ListsApi(client)
            try:
                response = api_list.get_lists()
                for listinfo in response.lists:
                    list_id = listinfo.get("id")
                    listdata = api_list.get_list(list_id)
                    if api_key in lists:
                        lists[api_key].append(listdata)
                    else:
                        lists[api_key] = [listdata]
            except ApiException:
                logger.exception("Exception getting list details.")
        return lists

    def subscribe(self, account_id, list_id, email_address):
        """API call to create a contact and subscribe it to a list"""
        self.initialize()
        client = self.connect(account_id)
        api_contact = sib_api_v3_sdk.ContactsApi(client)
        user = sib_api_v3_sdk.CreateContact(email=email_address)
        try:
            api_contact.create_contact(user)
        except ApiException:
            logger.exception("Exception creating user %s" % email_address)
            return

        api_lists = sib_api_v3_sdk.ListsApi(client)
        user_in_list = sib_api_v3_sdk.AddContactToList()
        user_in_list.emails = [email_address]
        try:
            response = api_lists.add_contact_to_list(list_id, user_in_list)
        except ApiException:
            logger.exception("Exception subscribing %s" % email_address)
            return
        if len(response.contacts.success) == 1:
            return True
        else:
            return False

    def accounts(self):
        """Retrieves accounts details (cached)"""
        self.initialize()
        cache = self.registry.get(self.key_accounts, _marker)
        if cache and cache is not _marker:
            return cache
        return self._accounts()

    def _accounts(self):
        """The actual API call for accounts"""
        accounts = {}
        for api_key in self.api_keys:
            client = self.connect(api_key)
            try:
                account = sib_api_v3_sdk.AccountApi(client).get_account()
                accounts[api_key] = account
            except ApiException:
                logger.exception("Exception getting account details.")
        return accounts

    def updateCache(self):
        """
        Update cache of data from the sendinblue server. First reset
        our sendinblue object, as the user may have picked a
        different api key. Alternatively, compare
        self.settings.api_keys and self.sendinblue.api_keys.
        """
        self.initialize()
        if not self.settings.api_keys:
            self.registry[self.key_accounts] = {}
            self.registry[self.key_lists] = {}
            return
        # Note that we must call the _underscore methods. These
        # bypass the cache and go directly to Sendinblue, so we are
        # certain to have up to date information.
        accounts = self._accounts()
        lists = self._lists()

        # Now save this to the registry, but only if there are
        # changes, otherwise we would do a commit every time we look
        # at the control panel.
        if type(accounts) is dict:
            if self.registry[self.key_accounts] != accounts:
                self.registry[self.key_accounts] = accounts
        if type(lists) is dict:
            if self.registry[self.key_lists] != lists:
                self.registry[self.key_lists] = lists
