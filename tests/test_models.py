__author__ = 'Xu Zhao'

import unittest
import logging
from app import create_app, db
from app.models import Principal
from datetime import datetime
class DBTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_db_create(self):
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger('testlog')
        t1 = Principal.query.all()
        log.debug("t1=%r", t1)
        principal = Principal(Email='abc@163.com',
                              Password='123',
                              Name=u'ABC',
                              Role='1',
                              Address=u'somewhere',
                              Contacts=u'DD',
                              Telephone='12345',
                              RegTime=datetime.now())
        db.session.add(principal)
        db.session.commit()
        t2 = Principal.query.all()
        log.debug("t2=%r", t2)
        self.assertNotEqual(t1, t2)

if __name__ == '__main__':
    unittest.main()
