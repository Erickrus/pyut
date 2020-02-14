# -*- coding: utf-8 -*-

import traceback
import time
import functools

# 此处声明online, offline两种 test case
# 其中所有test case默认为offline
# online测试用例仅用于测试那些需要外部依赖的用例
def online(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    inner._online_test_case = True
    return inner

def offline(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    inner._online_test_case = False
    return inner

class BaseTestCase:

    def assert_equal_file(self, filename1, filename2):
        content1 = open(filename1, "rb").read()
        content2 = open(filename2, "rb").read()
        assert content1 == content2
    
    def set_up(self):
        pass
    
    def run_test_cases(self):
        succ, fail = [], []
        for func in sorted(dir(self)):
            if func.startswith("test_"):
                fullFuncName = self.__class__.__module__+"."+self.__class__.__qualname__ + "."+func
                print("testing: %s" % fullFuncName)
                try:
                    funcObj = eval("self.%s"%func)
                    if ("_online_test_case" in dir(funcObj) and 
                        funcObj._online_test_case):
                        if not self.execOnline:
                            print("@online test cases skipped")
                            continue
                    eval("self.%s()"% func)
                    succ += [fullFuncName]
                except:
                    traceback.print_exc()
                    print()
                    fail += [fullFuncName]
                time.sleep(0.01)
        return succ, fail
    
    def tear_down(self):
        pass