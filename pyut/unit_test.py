# -*- coding: utf-8 -*-
import importlib
import glob
import os
import traceback

class UnitTest:
    def __init__(self, testDir="pyut", testDataDir="", execOnline=False):
        self.baseDir = self.get_library_path()
        self.testDir = [self.get_library_path()]
        self.testDir += (testDir + "/**/*.py").split("/")
        self.testDir = os.path.join(*self.testDir)
        self.ignoreList = ["base_test_case.py", "unit_test.py", "__init__.py"]
        if testDataDir == "":
            testDataDir = "./"
        else:
            self.testDataDir = testDataDir
        self.execOnline=execOnline
    
    def get_library_path(self):
        path = __file__
        return path[:path.rfind("pyut")-1]
    
    def parse_filename(self, filename):
        # retrieving the last item
        shortFilename = filename.split(os.path.sep)[-1]
        # converting to camel cases
        className = "".join([(item[0].upper()+ item[1:]) for item in shortFilename[:-3].split("_")])
        # join with dot
        packageName = ".".join(filename[len(self.baseDir)+1:].split(os.path.sep))[:-3]
        
        return shortFilename, className, packageName
    
    def run_test_cases(self):
        totalSucc, totalFail = [], []
        
        
        for filename in glob.glob(self.testDir, recursive=True):
            shortFilename = filename.split(os.path.sep)[-1]
            if (shortFilename in self.ignoreList):
                continue
            shortFilename, className, packageName = self.parse_filename(filename)
            print(shortFilename, className, packageName)
            module = importlib.import_module(packageName)
            # 注入testDataDir, execOnline 两个变量
            currTestCase = eval("module."+className+"()")
            currTestCase.testDataDir = [self.get_library_path()] + "data/test".split("/")
            currTestCase.testDataDir = os.path.join(*currTestCase.testDataDir)
            currTestCase.execOnline = self.execOnline

            try:
                currTestCase.set_up()
            except AttributeError:
                print("%s.%s.set_up() is not defined" % (packageName, className))
            except:
                pass
            try:
                succ, fail = currTestCase.run_test_cases()
                totalSucc += succ
                totalFail += fail
            except:
                traceback.print_exc()
                pass
            
            try:
                currTestCase.tear_down()
            except AttributeError:
                print("%s.%s.tear_down() is not defined" % (packageName, className))
            except:
                pass
            
        print("success: %d, failure: %d"%(len(totalSucc), len(totalFail)))
        if len(totalFail)>0:
            print("failure:")
            for fail in sorted(totalFail):
                print("    %s" % fail)
            

if __name__ == "__main__":
    UnitTest(execOnline=True).run_test_cases()
    