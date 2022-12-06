from datetime import datetime
from pytz import timezone
import time
from spatical_db_management import SpetialDBManagement

WAITTIME = 5


# DB 사용 준비
test = SpetialDBManagement('admin1', '1234', 'location_data')
now = datetime.now(timezone('Asia/Seoul'))
test.init_database()

# DB에 마켓 정보 추가
test.add_market_data(333,'samsung',"(0 0, 10 0, 0 10, 10 10, 0 0)", 3, 100001, 'electric')

# DB에 상품 정보 추가
test.add_product_data(333, 99231, 3, 4, 'galaxy S22', '1001')

# DB에 사용자 위치 정보 추가
# formatted_data = now.strftime('%Y-%m-%d %H:%M:%S')
# test.add_user_local_data(11022, '(3, 3)', 3, formatted_data)
# test.print_user_local_data(formatted_data)

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


# 사용자가 상품 근처에 WAITTIME 만큼 있을때 클라우드에 업로드
sample_data = {
    'market_id' : 333,
    'user_id' :  99231,
    'x_user' : 3,
    'y_user' : 4,
    'timestemp' : None
}

sample_data['timestemp'] = timestemp = now.strftime('%Y-%m-%d %H:%M:%S')
temp1 = test.user_hold_product(sample_data['market_id'], sample_data['user_id'], sample_data['x_user'], sample_data['y_user'], sample_data['timestemp'])
if (temp1 != -1):
    product_name1 = temp[1]

time.sleep(WAITTIME)

sample_data['timestemp'] = timestemp = now.strftime('%Y-%m-%d %H:%M:%S')
temp2 = test.user_hold_product(sample_data['market_id'], sample_data['user_id'], sample_data['x_user'], sample_data['y_user'], sample_data['timestemp'])
if (temp2 != -1):
    product_name2 = temp[1]
    
if (product_name1 == product_name2):
    temp = 'market ID = {market_id}, product name = {product_name}'.format(market_id = temp2[0], product_name = temp2[1])
    print('->  ' + temp)