from sqlalchemy import Column, Integer, String, Text, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased

# from sqlalchemy import aliased
Base = declarative_base()


class Result(Base):
    # 指定本类映射到users表
    __tablename__ = 'AsrEngineResult'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定name映射到name字段; name字段为字符串类形，
    filename = Column(String(255))
    text = Column(String(255))
    category = Column(String(32))
    taskname = Column(String(50))
    __mapper_args__ = {"order_by": category.desc()}

    def __init__(self, filename, category, text, taskname):
        self.filename = filename
        self.category = category
        self.text = text
        self.taskname = taskname


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

    def create_table(self, table):
        Result.__table__.name = table
        Result.__table__.create(self._engine, checkfirst=True)
        self.table = Result

    def save_asr_result(self, filename, category, text, taskname):
        data = self.session.query(Result).filter(Result.category == category,
                                                 Result.filename == filename, Result.taskname == taskname).first()
        if data:
            data.text = text
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

    def result(self,taskname, pagesize=10, pageindex=1):
        subq = self.session.query(Result). \
            filter_by(category='sbc',taskname=taskname).subquery()
        xfsubq = self.session.query(Result). \
            filter_by(category='xf',taskname=taskname).subquery()
        lhsubq = self.session.query(Result). \
            filter_by(category='lh',taskname=taskname).subquery()
        # Use alias to associate mapped class to a subquery.
        dmalias = aliased(Result, subq)
        dmalias_xf = aliased(Result, xfsubq)
        dmalias_lh = aliased(Result, lhsubq)
        data = self.session.query(dmalias.filename,dmalias.text, dmalias_lh.text, dmalias_xf.text).join(dmalias_lh,
                                                                                       dmalias_lh.filename == dmalias.filename).join(
            dmalias_xf, dmalias_xf.filename == dmalias.filename).limit(
            pagesize).offset(
            (pageindex- 1) * pagesize).all()
        return data
    def filename(self,taskname,pagesize=100,pageindex=1):
        t = self.session.query(Result.filename).filter(Result.taskname == taskname).group_by(Result.filename).limit(
            pagesize).offset(
            (pageindex- 1) * pagesize).all()
        return t
    def asr_result(self,filename):
        data = self.session.query(Result).filter(Result.filename == filename).all()
        return data


if __name__ == '__main__':
    db = EngineDb()
    n=1
    while True:
        res=db.result(pageindex=n,pagesize=2000)
        n=n+1
        if res:
            for i in res:
                print(i)
        else:
            break
    # db.create_table('AsrEngineResult')
