import pymysql
import json
from datetime import datetime
from pytz import timezone

from pymysql.constants import CLIENT

class SpetialDBManagement():
    host = 'localhost'
    user = None
    password = None
    db_name = None
    charset = 'utf8'
    db_connection = None
    cursor = None
    
    def __init__(self, user, password, db_name) -> None:
        self.user = user
        self.password = password
        self.db_name = db_name

    def init_database(self):
        #MySQL Connection 연결
        self.db_connection = pymysql.connect(host=self.host, 
                                             user=self.user, 
                                             password=self.password,
                                             db=self.db_name, 
                                             charset=self.charset, # 한글처리 (charset = 'utf8')
                                             #client_flag = CLIENT.MULTI_STATEMENTS
                                             )
        #Connection으로부터 Cursor 생성
        self.cursor = self.db_connection.cursor()
        
        # 마켓 정보 테이블
        try:
            create_market_table_sql  = """
            CREATE TABLE market_Table (
            id_market INT(11) PRIMARY KEY,
            market_name VARCHAR(20) NOT NULL,
            market_local POLYGON,
            floor INT(2) NOT NULL,
            sector INT(6),
            detail_type VARCHAR(20)
            );
            """
            #if not exists market_Table
            self.cursor.execute(create_market_table_sql)
            rows = self.cursor.fetchall()
            print(rows)  
        except:
            print("market_Table already exists")
            show_table_sql = """
            SHOW TABLES;
            """
            self.cursor.execute(show_table_sql)
        
        # 사용자 위치정보 테이블
        try:
            create_user_local_Table_sql  = """
            CREATE TABLE user_local_Table (
            id_user INT(11) NOT NULL,
            user_local POINT,
            floor INT(2) NOT NULL,
            time DATETIME NOT NULL
            );
            """
            #if not exists market_Table
            self.cursor.execute(create_user_local_Table_sql)
            rows = self.cursor.fetchall()
            print(rows)  
        except:
            print("user_local_Table already exists")
            show_table_sql = """
            SHOW TABLES;
            """
            self.cursor.execute(show_table_sql)
            
        # 사용자가 방문한 마켓 테이블
        try:
            create_visit_Table_sql  = """
            CREATE TABLE user_visit_Table (
            id_user INT(11) NOT NULL,
            id_market INT(11) NOT NULL,
            market_name VARCHAR(20) NOT NULL,
            time DATETIME NOT NULL
            );
            """
            #if not exists market_Table
            self.cursor.execute(create_visit_Table_sql)
            rows = self.cursor.fetchall()
            print(rows)  
        except:
            print("user_Table already exists")
            show_table_sql = """
            SHOW TABLES;
            """
            self.cursor.execute(show_table_sql)
            
        # 상품 정보 테이블
        try:
            create_product_table_sql  = """
            CREATE TABLE product_Table (
            id_market INT(11) NOT NULL,
            id_product INT(11) PRIMARY KEY,
            product_name VARCHAR(20) NOT NULL,
            product_local POLYGON,
            product_type INT(6),
            FOREIGN KEY (id_market) REFERENCES market_Table(id_market)
            );
            """
            #if not exists market_Table
            self.cursor.execute(create_product_table_sql)
            rows = self.cursor.fetchall()
            print(rows)  
        except:
            print("product_Table already exists")
            show_table_sql = """
            SHOW TABLES;
            """
            self.cursor.execute(show_table_sql)
            
        self.db_connection.commit()
    
    def add_user_local_data(self, id_user, user_local, floor, time):
        # 입력받은 데이터 추가 (local 제외))
        add_user_local_data_sql = """
        INSERT INTO user_local_Table(id_user, floor, time) 
        VALUES(%s,%s,%s)
        """
        params = (id_user, floor, time)
        self.cursor.execute(add_user_local_data_sql, params)  
        
        insert_user_POINT_data_sql = "UPDATE user_local_Table SET user_local = ST_GeomFromText('POINT" + user_local + "') WHERE time = %s;"
        params = (time)
        self.cursor.execute(insert_user_POINT_data_sql, params) 
        
        self.db_connection.commit()
        
    def print_user_local_data(self, time):
        # 데이터베이스에 저장한 데이터 출력
        print_user_local_data_sql = """
        SELECT id_user, ST_AsText(user_local), floor, time 
        FROM user_local_Table 
        WHERE time = %s
        """
        params = time
        self.cursor.execute(print_user_local_data_sql, params)  
        rows = self.cursor.fetchall()
        return rows[0]     
    
    def add_visit_data(self, id_user, id_market, market_name, time):
        # 입력받은 데이터 추가
        insert_market_data_sql = """
        INSERT INTO user_visit_Table(id_user, id_market, market_name, time) 
        VALUES(%s,%s,%s,%s)
        """
        params = (id_user, id_market, market_name, time)
        self.cursor.execute(insert_market_data_sql, params)  
        
        # 데이터베이스에 저장한 데이터 출력
        select_market_data_sql = "SELECT id_user, id_market, market_name, time FROM user_visit_Table WHERE id_user = %s"
        params = id_user
        self.cursor.execute(select_market_data_sql, params)  
        rows = self.cursor.fetchall()
        print("user_location_data = ")
        print(rows)
        
        self.db_connection.commit()
        
    def add_market_data(self, id, name, local, floor, sector, detail_type):
        
        # 입력받은 데이터 추가 (local 제외))
        add_market_data_sql = """
        INSERT IGNORE INTO market_Table(id_market, market_name, floor, sector, detail_type) 
        VALUES(%s,%s,%s,%s,%s)
        """
        params = (id, name, floor, sector, detail_type)
        self.cursor.execute(add_market_data_sql, params)  
        
        insert_local_data_sql = "UPDATE market_Table SET market_local = ST_GeomFromText('POLYGON(" + local + ")') WHERE market_name = %s;"
        params = (name)
        self.cursor.execute(insert_local_data_sql, params) 
        
        # 데이터베이스에 저장한 데이터 출력
        print_market_data_sql = """
        SELECT id_market, market_name, ST_AsText(market_local), floor, sector, detail_type 
        FROM market_Table 
        WHERE id_market = %s
        """
        params = id
        self.cursor.execute(print_market_data_sql, params)  
        rows = self.cursor.fetchall()
        print("add market_data = ")
        print(rows)
        
        self.db_connection.commit()
    
    def add_product_data(self, id_market, id_product, x, y, product_name, product_type):
        valid_area = 1
        
        # 입력받은 데이터 추가 (local 제외))
        add_product_data_sql = """
        INSERT IGNORE INTO product_Table(id_market, id_product, product_name, product_type) 
        VALUES(%s,%s,%s,%s)
        """
        params = (id_market, id_product, product_name, product_type)
        self.cursor.execute(add_product_data_sql, params)  
        
        product_local = "("+ str(x-valid_area/2) + " " + str(y-valid_area/2) + "," + str(x+valid_area/2) + " " + str(y-valid_area/2) + "," + str(x-valid_area/2) + " " + str(y+valid_area/2) + "," + str(x+valid_area/2) + " " + str(y+valid_area/2) + "," + str(x-valid_area/2) + " " + str(y-valid_area/2) + ")"
        insert_product_local_data_sql = "UPDATE product_Table SET product_local = ST_GeomFromText('POLYGON(" + product_local + ")') WHERE id_product = %s;"
        params = (id_product)
        self.cursor.execute(insert_product_local_data_sql, params) 
        
        # 데이터베이스에 저장한 데이터 출력
        print_product_data_sql = """
        SELECT id_market, id_product, product_name, ST_AsText(product_local), product_type 
        FROM product_Table 
        WHERE id_product = %s
        """
        params = id_product
        self.cursor.execute(print_product_data_sql, params)  
        rows = self.cursor.fetchall()
        print("add product data = ")
        print(rows)
        
        self.db_connection.commit()
               
    def within_market(self, floor, x, y):
        get_market_local_sql = """
        SELECT ST_AsText(market_local), id_market, market_name FROM market_Table WHERE floor = %s;
        """
        params = (floor)
        self.cursor.execute(get_market_local_sql, params)  
        market_tuple = self.cursor.fetchall()
        for i in range(len(market_tuple)):
            within_user_in_market_sql = "SELECT (ST_Intersects(ST_GeomFromText('" + market_tuple[i][0] + "'), (" + "POINT(" + str(x) + ","+ str(y) + "))))"    
            self.cursor.execute(within_user_in_market_sql)  
            rows = self.cursor.fetchall()
            if(rows[i][0] != 0):
                return [market_tuple[i][1],market_tuple[i][2]]
                break
            
        return -1
            
            
    def user_hold_product(self, id_market, user_id, x_user, y_user, time):
        get_product_local_sql = """
        SELECT ST_AsText(product_local), id_market, product_name FROM product_Table WHERE id_market = %s;
        """
        params = (id_market)
        self.cursor.execute(get_product_local_sql, params)  
        product_tuple = self.cursor.fetchall()
        for i in range(len(product_tuple)):
            within_user_in_market_sql = "SELECT (ST_Intersects(ST_GeomFromText('" + product_tuple[i][0] + "'), (" + "POINT(" + str(x_user) + ","+ str(y_user) + "))))" 
            self.cursor.execute(within_user_in_market_sql)  
            rows = self.cursor.fetchall()
            if(rows[i][0] != 0):
                return [product_tuple[i][1],product_tuple[i][2]]
                break
            
        return -1
    


def main():

    
    
if __name__ == '__main__': 
    main()
    '''
    # DB 사용 준비
    test = SpetialDBManagement('admin1', '1234', 'location_data')
    now = datetime.now(timezone('Asia/Seoul'))
    test.init_database()

    # DB에 마켓 정보 추가
    test.add_market_data(333,'samsung',"(0 0, 10 0, 0 10, 10 10, 0 0)", 3, 100001, 'electric')

    # DB에 상품 정보 추가
    test.add_product_data(333, 99231, 3, 4, 'galaxy S22', '1001')

    # DB에 사용자 위치 정보 추가
    formatted_data = now.strftime('%Y-%m-%d %H:%M:%S')
    test.add_user_local_data(11022, '(3, 3)', 3, formatted_data)
    test.print_user_local_data(formatted_data)

    # 사용자가 마켓에 들어갔는지 확인
    temp = test.within_market(3,3,3)
    if (temp != -1):
        temp = 'market ID = {market_id}, market name = {market_name}'.format(market_id = temp[0], market_name = temp[1])
        print(temp)

    # 사용자가 상품 근처에 있는지 확인
    formatted_data = now.strftime('%Y-%m-%d %H:%M:%S')
    test.add_user_local_data(11022,"(3 3)", 3, formatted_data)
    temp = test.print_user_local_data(formatted_data)
    print("->  user id = {user_id}, point = {point}, floor = {floor}, time = {time}".format(user_id = temp[0], point = temp[1], floor = temp[2], time = temp[3]))


    temp = test.user_hold_product(333, 99231, 3, 4, formatted_data)
    if (temp != -1):
        temp = 'market ID = {market_id}, product name = {product_name}'.format(market_id = temp[0], product_name = temp[1])
        print('->  ' + temp)
    '''