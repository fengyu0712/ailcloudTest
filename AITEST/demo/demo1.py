from common.http_request_new import Request
from  common.read_xls_news import Read_xls

url="https://nlu.sit.aimidea.cn:22012/nlu/v1"
data={"currentUtterance":"鸡蛋放在哪里","sourceDevice":"","multiDialog":"false","slotMiss":"false","suite":"fridge520","deviceId":"9493427850897384","userGroup":"meiju","userGroupCredential":"b82063f4-d39b-4940-91c3-5b67d741b4d3"}
yuliao1='{}放在哪个位置'
yuliao2='{}放在冰箱哪个位置'
data1=data
data2=data

foodname_data_path="E:\AITEST\demo\demo_data\冰箱食材清单.xlsx"
result_path="E:\AITEST\demo\demo_data\冰箱食材清单测试结果.xlsx"


r=Read_xls(foodname_data_path)
foodname_data=r.read_data(start_line=2)
# print(foodname_data)
new_book=r.copy_book()


# foodname=foodname_data[0][redis_case]
# yuliao1=yuliao1%foodname
# # yuliao2 = yuliao2 % foodname
# data1["currentUtterance"]=yuliao1
# result1=Request().requests(url,data1,'POST')
# print(result1)
# if result1["intent"]["intentType"]=="questionWhichRoomStore":
#     print("pass")



for i in range(len(foodname_data)):
    foodname=foodname_data[i][1]
    yuliao1 = yuliao1.format(foodname)
    yuliao2 = yuliao2.format(foodname)
    data1["currentUtterance"]=yuliao1
    result1=Request().requests(url,data1,'POST')
    if result1["intent"]["intentType"]=="questionWhichRoomStore":
        print("食材【{}：{}】无冰箱语料测试结果：{}".format(i,foodname,"pass"))
        r.write_onlydata(new_book,i+1,3,"Pass")
    else:
        print("食材【{}：{}】无冰箱语料测试结果：{}".format(i, foodname, "fail"))
        r.write_onlydata(new_book, i+1, 3, "Fail")
    data2["currentUtterance"] = yuliao2
    result2 = Request().requests(url, data2, 'POST')
    # print(result)
    if result2["intent"]["intentType"] == "questionWhichRoomStore":
        print("食材【{}：{}】有冰箱语料测试结果：{}".format(i, foodname, "pass"))
        r.write_onlydata(new_book, i+1, 2, "PASS")
    else:
        print("食材【{}：{}】有冰箱语料测试结果：{}".format(i, foodname, "pass"))
        r.write_onlydata(new_book, i + 1, 2, "Fail")
r.save_write(new_book,result_path)
