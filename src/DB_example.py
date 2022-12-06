from datetime import datetime
from pytz import timezone

from spatial_db_management import SpetialDBManagement

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


temp = test.user_hold_product(333, 99231, 3, 4, formatted_data)
if (temp != -1):
    temp = 'market ID = {market_id}, product name = {product_name}'.format(market_id = temp[0], product_name = temp[1])
    print('->  ' + temp)