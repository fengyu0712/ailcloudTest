list1=['好的,','好呢,']

list2=['正在为你开始','已开始','已设置为']
str0='客厅空调'
str1='强劲风'

list=[]
for i in list1:
    for j in list2:
        str=i+str0+j+str1
        list.append(str)
print(list)

