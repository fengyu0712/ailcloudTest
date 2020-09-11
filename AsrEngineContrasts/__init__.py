import os
from collections import Counter

import openpyxl
from sqlalchemy import Column, Integer, String, Text, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from AsrContrasts.Api.number2text import ReplaceCharacter
Base = declarative_base()


def get_dynamic_table_name_class(table_name):
    # 定义一个内部类
    class Result(Base):
        # 指定本类映射到users表
        __tablename__ = table_name
        id = Column(Integer, primary_key=True, autoincrement=True)
        # 指定name映射到name字段; name字段为字符串类形，
        filename = Column(String(255))
        text = Column(String(255))
        category = Column(String(32))
        __mapper_args__ = {"order_by": category.desc()}

        def __init__(self, filename, category, text):
            self.filename = filename
            self.category = category
            self.url = text

    return Result


class Result(Base):
    # 指定本类映射到users表
    __tablename__ = 'ast_result_1'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定name映射到name字段; name字段为字符串类形，
    filename = Column(String(255))
    text = Column(String(255))
    category = Column(String(32))
    __mapper_args__ = {"order_by": category.desc()}

    def __init__(self, filename, category, text):
        self.filename = filename
        self.category = category
        self.text = text


class Sqlite():
    def __init__(self):
        # self.engine = create_engine('sqlite:///{}/result_asr.db'.format(os.getcwd()))
        self.engine = create_engine('sqlite:///{}/result_asr.db'.format('D:\MyData\ex_kangyong\Desktop'))
        # self.engine = create_engine(
        #     'sqlite:///{}/result.db'.format('/home/kangyong/Data/PythonProject/AsrResult/AarContrasts'))
        self.table = None
        # engine是2.2中创建的连接
        Session = sessionmaker(bind=self.engine)

        # 创建Session类实例
        self.session = Session()

    def close(self):
        self.session.close()

    def child_select(self, name):
        stmt = self.session.query(self.table).filter(self.table.category == name).subquery()
        # print(self.session.query(self.table).outerjoin((stmt, self.table.id == stmt.id)).all())

    def select_table(self, table):
        Result.__table__.name = table

    def create_table(self, table):
        Result.__table__.name=table
        Result.__table__.create(self.engine, checkfirst=True)
        self.table = Result

    def save_asr_result(self, filename, category, text):
        data = self.session.query(Result).filter(Result.category == category,
                                                 Result.filename == filename).first()
        if data:
            data.text = text
        else:
            t = Result(filename, category, text)
            self.session.add(t)
        # self.commit()

    def commit(self):
        self.session.commit()

    def select_result(self):
        return self.session.query(self.table.filename, self.table.category, self.table.url,
                                  self.table.respone).order_by(self.table.category.desc()).all()

    def get_asr_result(self):
        # stm_sbc = self.session.query(Result.filename.label('filename'), Result.text).filter(
        #     Result.category == 'sbc').subquery()
        # stm_xf = self.session.query(Result.filename.label('filename'), Result.text).filter(
        #     Result.category == 'xf').subquery()
        # print(stm_sbc)
        # stm_lh = self.session.query(Result).filter(Result.category == 'lh').join(stm_xf.c,Result.filename==stm_xf.c.filename).all()
        # # .join(stm_sbc.c).filter(
        # #     Result.filename == stm_sbc.c.filename).all()
        # print(stm_lh)
        # result=self.session.query(stm_lh.c.filename,stm_xf.c.text).join(stm_lh.c,stm_lh.c.filename==stm_xf.c.filename).all()
        t=self.session.query(Result.category,func.count(Result.category)).group_by(Result.category).all()
        print(t)
        max=0
        name=''
        for i in t:
            if i[1]>=max:
                max=i[1]
                name=i[0]
        print(name,max)
        t2= self.session.query(Result.filename).filter(Result.category==name).all()
        ta=openpyxl.Workbook()
        sheet=ta.active
        sheet.append(['filename','sbc','xf','lh','result'])
        n2t=ReplaceCharacter()
        for i in t2:
            filename=i[0].replace('.pcm','.wav')
            data=self.session.query(Result).filter(Result.filename==filename).all()
            datalist=[]
            xf = '该音频未测试！！'
            sbc = '该音频未测试！！'
            lh = '该音频未测试！！'
            filename=''
            for n in data:
                filename=n.filename

                if n.category=='sbc':
                    sbc=n.text
                if n.category=='xf':
                    xf=n.text

                if n.category=='lh':
                    lh=n.text
            re_data=[ n2t.Number2Text(sbc),n2t.Number2Text(xf), n2t.Number2Text(lh)]
            result = Counter(re_data)
            items = list(result.items())
            text = ''
            if len(items) == 1:
                key = items[0][0]
                if key == '该音频未音频未测试！！':
                    test = '全部未测试'
                elif key:
                    text = '完全相同非空'
                else:
                    text = '完全相同空值'
            elif len(items) == 2:
                key = items[0][0]
                value = items[0][1]
                key1 = items[1][0]
                value1 = items[1][1]
                max_key = ''
                if value > value1:
                    max_key = key
                else:
                    max_key = key1
                if max_key:
                    if key == '该音频未测试！！':
                        test = '有两个引擎未测试'
                    else:
                        text = '有两个相同且不为空'
                else:
                    text = '有两个相同的空值'
            elif len(items) == 3:
                if '该音频未测试！！' in list(result.values()):
                    text = '有一个引擎未测试'
                else:
                    text = '完全不相同'
            sheet.append([filename,*re_data,text])
            print(re_data)
        ta.save('reuslt_finally_9-8_1.xlsx')

if __name__ == '__main__':
        tablename = 'ast_result_125'
        sql = Sqlite()
        sql.create_table(tablename)
        sql.select_table(tablename)
        sql.save_asr_result('12345612.wav', 'sbc', '考试')
        sql.save_asr_result('12345621.wav', 'xf', '考试')
        sql.save_asr_result('12345621.wav', 'lh', '考试1')
