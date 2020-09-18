class Conversion():
    def list_dict(self,list,keys_list,n=None):
        if n==None:
            n=0
        for i in  range(n,len(list)):
            data_dict=dict(zip(keys_list[n:],list[n:]))
        return data_dict

if  __name__=="__main__":
    list=[1,2,3]
    keys_list=['a','b','c']
    a=Conversion().list_dict(list,keys_list)
    print(a,type(a))