from pytube import YouTube
from AdvUpdater import AdvUpdater

billboard = AdvUpdater()

adv_data_updater = AdvUpdater()
adv_data_updater.load_advertisement_data_with_json("advertisement_data.json")
adv_data_updater._upload_to_dynamoDB()


# 빌보드에 출력할 유튜브 영상 url 가져오기 & 다운로드
adv_url = adv_data_updater._search_in_dynamoDB("iPhone14")
download_folder = "../Download"

yt = YouTube(adv_url)
# stream = yt.streams.get_highest_resolution()
# stream.download(download_folder)

# 빌보드에 함께 출력할 수 있는 내용
'''
print("제목 : ", yt.title)
print("길이 : ", yt.length)
print("게시자 : ", yt.author)
print("게시날짜 : ", yt.publish_date)
print("조회수 : ", yt.views)
print("키워드 : ", yt.keywords)
print("설명 : ", yt.description)
print("썸네일 : ", yt.thumbnail_url)
'''