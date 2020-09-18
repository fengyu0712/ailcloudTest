import re
# # #
# # # def excel_to_html(filepath):
# # #     xd = pd.ExcelFile(filepath)
# # #     df = xd.parse()
# # #     with codecs.open('/Users/wangxingfan/Desktop/1.html', 'w', 'utf-8') as html_file:
# # #         html_file.write(df.to_html(header=True, index=False))
# # #     file = open('/Users/wangxingfan/Desktop/1.html').read()
# # #     return file
# #
# #
# # a="D:\\Users\lijq36\Downloads\\2020-05-28.log"
# # b=open(a,'r',encoding='utf8')
# # c=b.read()
# # pattern="sessionId\":	\"(.*)\""
# #
# # result=re.findall(pattern,c)
# # temp = []
# # [temp.append(i) for i in result if i not in temp]
# #
# # from Common import read_xls_news
# # excel_path="D:\\Users\lijq36\Desktop\\result2020-05-28.xls"
# # result_path="D:\\Users\lijq36\Desktop\\result2020-05-28_1.xls"
# # r = read_xls_news.Read_xls(excel_path)
# # w = r.copy_book()
# #
# # # booknames=r.get_sheet_names()
# # sheetname = "014"
# # booknames = [sheetname]
# # data = []
# # for i in range(len(booknames)):
# #     tdata = r.read_data(booknames[i], start_line=3)
# #     data += tdata
# #     i += 1
# # print(data[:200])
# #
# # for i in range(len(temp)):
# #     print(i)
# #     r.write_onlydata(w,i+2,4,temp[i])
# # r.save_write(w, result_path)
# # # print(len(temp))
# # # print(len(result))
# import json
# a='''{
# 	"test_output":	{
# 		"ev":	"online tts",
# 		"text":	"明天佛山天气怎么样",
# 		"data":	0,
# 		"info":	"{\n\t\"reply\":\t\"佛山明天全天雷阵雨，气温26~30℃，有西北风1级，出门不要忘记带伞\",\n\t\"mid\":\t\"5aff5370-a181-11ea-859c-b3a020e523eb\"\n}"
# 	}}'''
# pattern='''{
# 	"test_output":	{
# 		"ev":	"online tts",
# 		"text":	"(.*)",
# 		"data":	0,
# 		"info":	"{\n\t\"reply\":\t\".*\",\n\t\"mid\":\t\"(.*)\"\n}"
# 	}}'''
# b=re.findall(pattern,a)
# c=json.loads(json.dumps(a))
# print(b)
# print((c))