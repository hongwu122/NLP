#coding=utf-8
#__author__ = 'LiuYanBao'
# 论文-中关村小米评论爬虫
# HUAWEI MateBook D 14 2022款(i5 1155G7/16GB/512GB/集显)点评
# https://detail.zol.com.cn/1396/1395993/review.shtml
import re
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import time
import time
from urllib.request import urlopen
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import pymysql

# 连接数据库
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    charset='UTF8',
    password='root',
    database='zol_hw'
)

# 获取游标
cursor = connect.cursor()


def getPageUrl():
    listLink = []
    listPepoleLink = []
    # driver = webdriver.PhantomJS(executable_path='D:\\softWare\\python\\pythonTool\\phantomjs-2.1.1-windows\\bin\\phantomjs')  # phantomjs的绝对路径
    driver_path = r"C:\chromedriver\chromedriver108.0.5359.71.exe"  # 调用软件地址
    driver = webdriver.Chrome(executable_path=driver_path)
    wait = ui.WebDriverWait(driver, 10)
    driver.get(r'https://detail.zol.com.cn/1396/1395993/review.shtml')
    # 小米8   http://detail.zol.com.cn/series/57/34645/review_23927.html
    list1 =[]
    try:
        while 1:
            driver.find_element_by_id('_j_view_more_comments').click()
    except:
        print('页面到底了！！！')
        time.sleep(10)
        pass
 
    content_list = driver.find_elements_by_class_name('comments-item')
    print(content_list)
    for each_content in content_list:

        # titleLink = each_content.find_element_by_class_name('title')
        # link = titleLink.find_element_by_css_selector("a").get_attribute('href')
        # listLink.append(link)

        pepoleLink = each_content.find_element_by_class_name('comments-user')
        link2 = pepoleLink.find_element_by_css_selector("a").get_attribute('href')
        listPepoleLink.append(link2)
        # list1.append('|'.join([link]))

    # with open(r'C:\Users\鸿武\Desktop\爬虫\Data\zolReviews_HW_Link.txt', 'w+', encoding='utf-8') as f:
    #     for i in listLink:
    #         f.write(i + '\n')

    with open(r'C:\Users\鸿武\Desktop\爬虫\Data\zolReviews_HW_PersonLink.txt', 'w+', encoding='utf-8') as f:
        for i in listPepoleLink:
            f.write(i + '\n')

    return listLink,listPepoleLink


def getPageDetails(listLink,listPepoleLink):
    resultData = []
    for (simplelink,simplePepolelink) in zip(listLink,listPepoleLink):
        if simplelink.strip()=='':
            continue
        matchObj = re.match('https://t.zol.com.cn.*',simplelink)
        if matchObj:
            html = urlopen(simplelink)
            soup = BeautifulSoup(html)
            text = soup.find("div", class_="article-box").text
            # purchaseTime = soup.select('div.comments-pro p')[1].get_text()
            nowtime = date.today()
            # nowtime = "2019-05-01"
            reviewsTime = soup.find("span", class_="time").text
            reviewsTime = reviewsTime[:10]
            nowtime = time.strptime(nowtime, "%Y-%m-%d")
            reviewsTime = time.strptime(reviewsTime, "%Y-%m-%d")
            nowtime = datetime(nowtime[0], nowtime[1], nowtime[2])
            reviewsTime = datetime(reviewsTime[0], reviewsTime[1], reviewsTime[2])
            reviewsTime = nowtime - reviewsTime
            reviewsTime = reviewsTime.days

            merits = soup.find("div", class_="merits").text
            faults = soup.find("div", class_="faults").text
            voteNum = soup.find("span",class_="_j_vote_num").text
            voteNum = re.findall("\d+", voteNum)[0]
            respondNum = soup.find("div",class_="discuss-btn").text
            respondNum = re.findall("\d+", respondNum)[0]
            totalScore = soup.find("div",class_="total-score").text
            resultData = [text,reviewsTime,merits,faults,voteNum,respondNum,totalScore]

            # 个人信息获取
            if len(simplePepolelink) > 22:
                htmlPepole = urlopen(simplePepolelink)
                soupPepole = BeautifulSoup(htmlPepole)

                postReviewsNum = soupPepole.find("span", class_="record-num first").text
                postReviewsNum = re.sub("[\u4E00-\u9FA5]", "", postReviewsNum)

                friendNum = soupPepole.find("span", class_="friend-num").a.text
                fansNum = soupPepole.find("span", class_="fans-num").a.text
                focusNum = soupPepole.find("span", class_="focus-num").a.text

            # 插入数据
            sql = "INSERT INTO reviews (text,reviewsTime,merits,faults,voteNum,respondNum,totalScore,linkUrl,htmlPepole,postReviewsNum,friendNum,fansNum,focusNum) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            data = (text,reviewsTime,merits,faults,voteNum,respondNum,totalScore,simplelink,htmlPepole,postReviewsNum,friendNum,fansNum,focusNum)
            cursor.execute(sql % data)
            connect.commit()
            print('成功插入', cursor.rowcount, '条数据')


        else:
            print(simplelink)
            html = urlopen(simplelink)
            soup = BeautifulSoup(html)
            text = soup.select('div.comments-content h3')[0].get_text()
            reviewsTime = soup.find("span", class_="comment-date").text
            reviewsTime = re.sub("[\u4E00-\u9FA5]", "", reviewsTime)
            # nowtime = date.today()
            nowtime = "2019-05-01"
            reviewsTime = reviewsTime[1:]
            nowtime = time.strptime(nowtime, "%Y-%m-%d")
            reviewsTime = time.strptime(reviewsTime, "%Y-%m-%d")
            nowtime = datetime(nowtime[0], nowtime[1], nowtime[2])
            reviewsTime = datetime(reviewsTime[0], reviewsTime[1], reviewsTime[2])
            reviewsTime = nowtime - reviewsTime
            reviewsTime = reviewsTime.days

            # merits = soup.find("div", class_="comments-words").text
            # faults = soup.select('div.comments-words')[1].get_text()
            merits = ''
            faults = ''

            tag = soup.find(class_="comments-content")
            print(len(tag))
            if len(soup.find_all("div", class_="comments-words")) == 3:
                merits = soup.find("div", class_="comments-words").text
                faults = soup.select('div.comments-words')[1].get_text()
                commentSum = soup.select('div.comments-words')[2].get_text()
                text = text + commentSum
            elif len(soup.find_all("div", class_="comments-words")) == 2:
                merits = soup.find("div", class_="comments-words").text
                faults = soup.select('div.comments-words')[1].get_text()
            elif len(soup.find_all("div", class_="comments-words")) == 1:
                commentSum = soup.find("div", class_="comments-words").text
                text = text + commentSum

            voteNum = soup.find("a", class_="J_ReviewHelp").text
            if re.findall("\d+", voteNum) != []:
                voteNum = re.findall("\d+", voteNum)[0]
            else:
                voteNum = 0
            respondNum = soup.find("a", class_="comment-num").text
            if re.findall("\d+", respondNum) != []:
                respondNum = re.findall("\d+", respondNum)[0]
            else:
                respondNum = 0
            totalScore = soup.find("div", class_="total-score").text
            resultData.append([text, reviewsTime, merits, faults, voteNum, respondNum, totalScore])
            print(respondNum)

            # 个人信息获取
            if len(simplePepolelink) > 22:
                htmlPepole = urlopen(simplePepolelink)
                soupPepole = BeautifulSoup(htmlPepole)

                postReviewsNum = soupPepole.find("span", class_="record-num first").text
                postReviewsNum = re.sub("[\u4E00-\u9FA5]", "", postReviewsNum)

                friendNum = soupPepole.find("span", class_="friend-num").a.text
                fansNum = soupPepole.find("span", class_="fans-num").a.text
                focusNum = soupPepole.find("span", class_="focus-num").a.text

            # 插入数据
            sql = "INSERT INTO reviews (text,reviewsTime,merits,faults,voteNum,respondNum,totalScore,linkUrl,htmlPepole,postReviewsNum,friendNum,fansNum,focusNum) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            data = (text, reviewsTime, merits, faults, voteNum, respondNum, totalScore,simplelink,htmlPepole,postReviewsNum,friendNum,fansNum,focusNum)
            cursor.execute(sql % data)
            connect.commit()
            print('成功插入', cursor.rowcount, '条数据')
            # print(resultData)
        # return resultData

if __name__ == "__main__":
    [listLink,listPepoleLink] = getPageUrl()
#     listLink = ['http://t.zol.com.cn/57/1173233/evaluation_515.html',
# 'http://t.zol.com.cn/57/1167243/evaluation_474.html',
# 'http://detail.zol.com.cn/1168/1167243/review_0_0_1614031_1.shtml#tagNav',
# 'http://detail.zol.com.cn/1168/1167243/review_0_0_1608331_1.shtml#tagNav']
    print(listLink)
    getPageDetails(listLink,listPepoleLink)
    # print(Data)
    # 关闭连接
    cursor.close()
    connect.close()
