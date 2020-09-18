import pymysql
from common.conf import Conf
import Project_path

class MySql:
    def __init__(self,config):
        self.cnn = pymysql.connect(**config)
        self.cursor = self.cnn.cursor()
    def creat_table(self, create_date_sql):
        self.cursor.execute(create_date_sql)
    def insert_data(self, insert_sql, data):
        self.cursor.execute(insert_sql, data)
        self.cnn.commit()
    def insert_manydata(self, insert_sql,data):
        self.cursor.executemany(insert_sql,data)
        self.cnn.commit()
    def read_data(self,select_sql):
        self.cursor.execute(select_sql)
        data=self.cursor.fetchall()
        self.cnn.commit()
        for (cdata,) in data:   #pymysql读取的数据多括号和都好，这里进行转换
            return cdata
    def close(self):
        self.cursor.close()
        self.cnn.close()



create_data_sql= "create table test_data("\
                  "id int not null PRIMARY key auto_increment," \
                  "url varchar(50) ," \
                  "mobilephone varchar(15)," \
                  "amount int(12)," \
                  "type varchar(12)," \
                  "test_result varchar(100) ," \
                  "create_date datetime," \
                  "update_date datetime" \
                  ")DEFAULT CHARSET=utf8"

getdata_sql="select url from test.test_data where id=redis_case"

# insert_sql='insert into test_data (created_day,name,count) values(%s,%s,%s)'

if __name__ == '__main__':
    insert_sql = 'INSERT INTO `test`.`test_data`(`id`, `url`, `mobilephone`, `amount`, `type`, `test_result`, `create_date`, `update_date`) VALUES (%s, NULL, NULL, NULL, NULL, NULL, NULL, NULL)'
    conf_path = Project_path.conf_path + "db.ini"
    config = Conf(conf_path).get_value("Mysql", "config")
    a=MySql(config)
    a.creat_table(create_data_sql)
    a.insert_manydata(insert_sql,data=[2,3])
    b=a.read_data(getdata_sql)
    print(b)
    # pd.DataFrame(result)
    # print(eval(b[0][0]))
    # print(type(eval(b))
    # a.close()
    # print(b)
    # print(type(b[redis_case][3]))