class Assert():
    def equalvalue(self,realvalue,exceptvalue):
        assert realvalue == exceptvalue


    # exceptvalue: 预期结果
    # realvalue 实际结果
    def containvalue(self,realvalue,exceptvalue):
        print(exceptvalue,realvalue)
        print(type(exceptvalue))
        print(exceptvalue.find(realvalue)!=-1)
        assert exceptvalue.find(realvalue)!=-1

