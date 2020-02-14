# -*- coding: utf-8 -*-
from pyut.base_test_case import BaseTestCase, online

class TestDemo(BaseTestCase):
    def test_offline(self):
        print("This is offline test case")
        assert 1==1
    
    @online
    def test_online(self):
        print("This is online test case")
        print(self.testDataDir)
        assert 1==2
        
        
        
        