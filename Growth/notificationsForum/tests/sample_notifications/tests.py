import os
from unittest import skipUnless

import swapper
from notificationsForum.tests.tests import AdminTest as BaseAdminTest
from notificationsForum.tests.tests import NotificationTest as BaseNotificationTest

NotificationForum = swapper.load_model('notificationsForum', 'NotificationForum')


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django-notificationsForum models')
class AdminTest(BaseAdminTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BaseAdminTest.app_name = 'sample_notificationsForum'


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django-notificationsForum models')
class NotificationTest(BaseNotificationTest):
    pass
