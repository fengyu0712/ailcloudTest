import json
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, func, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased

# from sqlalchemy import aliased
from AsrContrasts.public import fields

Base = declarative_base()


class Asrcaselist(Base):
    __tablename__ = 'asrcaselist'

    id = Column(Integer, primary_key=True)
    filename = Column(Text)
    dict_assert = Column(Text)
    suiteid = Column(Integer)


class Result(Base):
    # 指定本类映射到users表
    __tablename__ = 'AsrEngineResults'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定name映射到name字段; name字段为字符串类形，
    filename = Column(String(255))
    sbc = Column(String(255))
    xf = Column(String(255))
    lh = Column(String(255))
    taskname = Column(String(100))
    text = Column(String(255))
    category = Column(String(32))
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, onupdate=datetime.now, comment='更新时间')
    __mapper_args__ = {"order_by": filename.desc()}

    def __init__(self, filename, category, text, taskname):
        self.filename = filename
        self.category = category
        # self.text = text
        self.taskname = taskname
        self.sbc = '未测试'
        self.lh = '未测试'
        self.xf = '未测试'
        if category == 'sbc':
            self.sbc = text
        elif category == 'xf':
            self.xf = text
        elif category == 'lh':
            self.lh = text


class EngineDb():
    def __init__(self):
        _sql_address = "rm-bp1kqqxzzi7b5xkf4uo.mysql.rds.aliyuncs.com"
        _sql_username = "testadmin"
        _sql_password = "FnTAD9jTnmu8m25"
        _sql_db = "result"
        self._engine = create_engine(
            'mysql+pymysql://{name}:{password}@{host}/{db}'.format(name=_sql_username, password=_sql_password,
                                                                   host=_sql_address, db=_sql_db))

        # self.engine = create_engine('sqlite:///{}/result_asr.db'.format(os.getcwd()))
        # self.engine = create_engine('sqlite:///{}/result_asr.db'.format('D:\MyData\ex_kangyong\Desktop'))
        # self.engine = create_engine(
        #     'sqlite:///{}/result.db'.format('/home/kangyong/Data/PythonProject/AsrResult/AarContrasts'))
        self.table = None
        # engine是2.2中创建的连接
        Session = sessionmaker(bind=self._engine)

        # 创建Session类实例
        self.session = Session()

    def close(self):
        self.session.close()

    def child_select(self, name):
        stmt = self.session.query(self.table).filter(self.table.category == name).subquery()
        # print(self.session.query(self.table).outerjoin((stmt, self.table.id == stmt.id)).all())

    def select_table(self, table):
        Result.__table__.name = table

    def create_table(self):
        # Result.__table__.name = table
        # Result.__table__.create(self._engine, checkfirst=True)
        Asrcaselist.__table__.create(self._engine, checkfirst=True)
        # self.table = Result

    def save_asr_result(self, filename, category, text, taskname):

        if category == 'sbc':
            data = self.session.query(Result).filter(Result.filename == filename, Result.taskname == taskname).first()
            if data:
                data.sbc = text
            else:
                t = Result(filename, category, text, taskname)
                self.session.add(t)
        elif category == 'lh':
            data = self.session.query(Result).filter(
                Result.filename == filename, Result.taskname == taskname).first()
            if data:
                data.lh = text
            else:
                t = Result(filename, category, text, taskname)
                self.session.add(t)
        elif category == 'xf':
            data = self.session.query(Result).filter(
                Result.filename == filename, Result.taskname == taskname).first()
            if data:
                data.xf = text
            else:
                t = Result(filename, category, text, taskname)
                self.session.add(t)

        # self.commit()

    def commit(self):
        self.session.commit()

    def select_result(self):
        return self.session.query(self.table.filename, self.table.category, self.table.url,
                                  self.table.respone).order_by(self.table.category.desc()).all()

    def group(self):
        return self.session.query(Result.category, func.count(Result.category)).group_by(Result.category).all()

    def get_asr_result(self, taskname, name, pagesize=10, pageindex=1):
        t = self.session.query(Result).filter(Result.category == name, Result.taskname == taskname).limit(
            pagesize).offset(
            (pageindex - 1) * pagesize).all()

        return t

    def result(self, taskname, pagesize=10, pageindex=1):
        subq = self.session.query(Result). \
            filter_by(category='sbc', taskname=taskname).subquery()
        xfsubq = self.session.query(Result). \
            filter_by(category='xf', taskname=taskname).subquery()
        lhsubq = self.session.query(Result). \
            filter_by(category='lh', taskname=taskname).subquery()
        # Use alias to associate mapped class to a subquery.
        dmalias = aliased(Result, subq)
        dmalias_xf = aliased(Result, xfsubq)
        dmalias_lh = aliased(Result, lhsubq)
        data = self.session.query(dmalias.filename, dmalias.text, dmalias_lh.text, dmalias_xf.text).join(dmalias_lh,
                                                                                                         dmalias_lh.filename == dmalias.filename).join(
            dmalias_xf, dmalias_xf.filename == dmalias.filename).limit(
            pagesize).offset(
            (pageindex - 1) * pagesize).all()
        return data

    def filename(self, taskname, pagesize=100, pageindex=1):
        t = self.session.query(Result.filename).filter(Result.taskname == taskname).group_by(Result.filename).limit(
            pagesize).offset(
            (pageindex - 1) * pagesize).all()
        return t

    def asr_result(self, filename):
        data = self.session.query(Result).filter(Result.filename == filename).all()
        return data

    def results(self, taskname, pagesize=10, pageindex=1):
        data = self.session.query(Result). \
            filter_by(taskname=taskname).limit(
            pagesize).offset(
            (pageindex - 1) * pagesize).all()
        # xfsubq = self.session.query(Result). \
        #     filter_by(category='xf', taskname=taskname).subquery()
        # lhsubq = self.session.query(Result). \
        #     filter_by(category='lh', taskname=taskname).subquery()
        # # Use alias to associate mapped class to a subquery.
        # dmalias = aliased(Result, subq)
        # dmalias_xf = aliased(Result, xfsubq)
        # dmalias_lh = aliased(Result, lhsubq)
        # data = self.session.query(dmalias.filename, dmalias.text, dmalias_lh.text, dmalias_xf.text).join(dmalias_lh,
        #                                                                                                  dmalias_lh.filename == dmalias.filename).join(
        #     dmalias_xf, dmalias_xf.filename == dmalias.filename).limit(
        #     pagesize).offset(
        #     (pageindex - 1) * pagesize).all()
        return data

    def insertcase(self, data):
        print(data)
        self.session.execute(Asrcaselist.__table__.insert(), data)
        self.session.commit()

    def select_case(self, item, sheet=None, filename=None, reportID=None, pagesize=None, pageindex=None,
                    done_case=None, run_case=None):
        data = []
        if not done_case:
            done_case = []
        if not run_case:
            run_case = []
        fields_title = {'filename': fields.String, 'dict_assert': fields.format_json,
                        'case_id': fields.Integer(attribute='id'),
                        'file': fields.String(default=filename), 'sheet': fields.String(default=sheet),
                        'reportID': fields.Integer(default=reportID)}
        if run_case:
            if pageindex and pagesize:
                if isinstance(item, list):
                    data = self.session.query(Asrcaselist).filter(Asrcaselist.suiteid.in_(item),
                                                                  Asrcaselist.filename.in_(run_case)).limit(
                        pagesize).offset(
                        (pageindex - 1) * pagesize).all()
                elif isinstance(item, int):
                    data = self.session.query(Asrcaselist).filter(Asrcaselist.suiteid == item,
                                                                  Asrcaselist.filename.in_(run_case)).limit(
                        pagesize).offset(
                        (pageindex - 1) * pagesize).all()
                data = json.loads(json.dumps(fields.marshal(data, fields_title)))
            else:
                # print(done_case)
                if isinstance(item, list):
                    data = self.session.query(Asrcaselist).filter(Asrcaselist.suiteid.in_(item),
                                                                  Asrcaselist.filename.in_(run_case)).all()
                elif isinstance(item, int):
                    data = self.session.query(Asrcaselist).filter(Asrcaselist.suiteid == item,
                                                                  Asrcaselist.filename.in_(run_case)).all()
                data = json.loads(json.dumps(fields.marshal(data, fields_title)))
        else:
            if pageindex and pagesize:
                if isinstance(item, list):
                    data = self.session.query(Asrcaselist).filter(Asrcaselist.suiteid.in_(item),
                                                                  Asrcaselist.filename.notin_(done_case)).limit(
                        pagesize).offset(
                        (pageindex - 1) * pagesize).all()
                elif isinstance(item, int):
                    data = self.session.query(Asrcaselist).filter(Asrcaselist.suiteid == item,
                                                                  Asrcaselist.filename.notin_(done_case)).limit(
                        pagesize).offset(
                        (pageindex - 1) * pagesize).all()
                data = json.loads(json.dumps(fields.marshal(data, fields_title)))
            else:
                # print(done_case)
                if isinstance(item, list):
                    data = self.session.query(Asrcaselist).filter(Asrcaselist.suiteid.in_(item),
                                                                  Asrcaselist.filename.notin_(done_case)).all()
                elif isinstance(item, int):
                    data = self.session.query(Asrcaselist).filter(Asrcaselist.suiteid == item,
                                                                  Asrcaselist.filename.notin_(done_case)).all()
                data = json.loads(json.dumps(fields.marshal(data, fields_title)))
        return data

    def select_done_id(self, taskname, asrtype):
        data = None
        datalist = []
        if asrtype == 'sbc':
            data = self.session.query(Result.filename).filter(Result.taskname == taskname, Result.sbc != '未测试').all()
        if asrtype == 'lh':
            data = self.session.query(Result.filename).filter(Result.taskname == taskname, Result.lh != '未测试').all()
        if asrtype == 'xf':
            data = self.session.query(Result.filename).filter(Result.taskname == taskname, Result.xf != '未测试').all()

        for i in data:
            datalist.append(i[0])
        return datalist

    def select_run_none_id(self, taskname, asrtype):
        '''
        查询返回为空的用例重新测试
        :param taskname:
        :param asrtype:
        :return:
        '''
        data = None
        datalist = []
        if asrtype == 'sbc':
            data = self.session.query(Result.filename).filter(Result.taskname == taskname, Result.sbc == '',
                                                              Result.lh != '', Result.xf != '').all()
        if asrtype == 'lh':
            data = self.session.query(Result.filename).filter(Result.taskname == taskname, Result.lh == '',
                                                              Result.sbc != '', Result.xf != '').all()
        if asrtype == 'xf':
            data = self.session.query(Result.filename).filter(Result.taskname == taskname, Result.xf == '',
                                                              Result.sbc != '', Result.lh != '').all()

        for i in data:
            datalist.append(i[0])
        return datalist

    def count_done_case(self, taskname, asrtype):
        data = 0
        if asrtype == 'sbc':
            data = self.session.query(func.count(Result.id)).filter(Result.taskname == taskname,
                                                                    Result.sbc != '未测试').scalar()
        if asrtype == 'lh':
            data = self.session.query(func.count(Result.id)).filter(Result.taskname == taskname,
                                                                    Result.lh != '未测试').scalar()
        if asrtype == 'xf':
            data = self.session.query(func.count(Result.id)).filter(Result.taskname == taskname,
                                                                    Result.xf != '未测试').scalar()
        return data

    def count_case_number(self, item):
        data = self.session.query(func.count(Asrcaselist.id)).filter(Asrcaselist.suiteid.in_(item)).scalar()
        return data


if __name__ == '__main__':
    db = EngineDb()
    d=db.select_run_none_id('AsrEngineResult20200911173923','sbc')
    data = db.select_case([10], pagesize=1000, pageindex=1, run_case=d)
    print(len(d),d)
    for i in data:
        print(len(data),i)

    # n = 1
    # while True:
    #     res = db.result(pageindex=n, pagesize=2000)
    #     n = n + 1
    #     if res:
    #         for i in res:
    #             print(i)
    #     else:
    #         break
    # db.create_table('AsrEngineResult')
