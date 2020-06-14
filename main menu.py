import urllib.request
import json,pprint
import urllib.parse
import subprocess

from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from glob import glob

def translate():
    # 번역할 txt파일 내용 불러와서 읽기
    with open('source.txt', 'r', encoding='utf8') as memo:
        text = memo.read()

    # 번역할 내용을 txt파일로 읽어서 받아옴
    encText = urllib.parse.quote(text)
    # 한영번역
    # data = "source=ko&target=en&text=" + encText
    # 영한번역
    data = "source=en&target=ko&text=" + encText

    # 개발자센터에서 발급받은 값
    client_id = "uucszwBYG7Kx3m68gu8Y"
    client_secret = "ARQJd5IcAh"

    ##번역시작코드
    # 웹요청
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    # 결과 받아오는 부분
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))

    # 응답이 성공적일때
    rescode = response.getcode()
    # 성공
    if (rescode == 200):
        response_body = response.read()
        txt = response_body.decode('utf-8')
        # 응답데이터 형 변환, 딕셔너리화
        txt = json.loads(txt)
        # pprint 이용해서 출력 변경
        pprint.pprint(txt)

        # 수정 후 메모장 파일 생성
        with open('translate.txt', 'w', encoding='utf8') as memo:
            memo.write(txt['message']['result']['translatedText'])

        messagebox.showinfo("번역", txt['message']['result']['translatedText'])
    # 실패
    else:
        print("Error Code:" + rescode)

def crawling():
    
    with open('source.txt', 'r', encoding='utf8') as f:
        date = f.read()

    plusUrl = urllib.parse.quote_plus(date)

    pageNum = 1
    count = 1

    i = 1 #1페이지로 고정

    sys.stdout = open('output.txt', 'a', encoding='UTF-8')

    lastPage = int(i) * 10 - 9
    while pageNum < lastPage + 1:
        url = f'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query={plusUrl}&sm=tab_pge&srchby=all&st=sim&where=post&start={pageNum}'

        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find_all(class_='sh_blog_title')

        print(f'-----{plusUrl}의 {count}페이지 결과 입니다.-----')
        for i in title:
            print(i.attrs['title'])
            print(i.attrs['href'])

        pageNum += 10
        count += 1
        messagebox.showinfo("크롤링",title)

def calendar():
    filelist = glob("Calendar.py")

    for file in filelist:
        subprocess.call(['python', file])

def campusmap():
    filelist = glob("CampusMap.py")

    for file in filelist:
        subprocess.call(['python', file])

def close():
    messagebox.showinfo("종료","프로그램을 종료합니다.")
    quit()

def main():
    window = Tk()
    window.title("메뉴선택")#GUI창 이름변경
    window.geometry("640x400+100+100")#크기 설정
    window.resizable(0,0)
    photo = PhotoImage(file="CBNU.png");
    labe2 = Label(window, image=photo);
    labe3 = Label(window, text='글씨 인식 프로그램', font=(30))

    # 호출
    b1 = Button(window, text="1. 번역", width=15,height=5,compound="c",command=translate)
    b2 = Button(window, text="2. 웹 크롤링",width=15,height=5,compound="c", command=crawling)
    b3 = Button(window, text="3. 학교 위치 정보", width=15,height=5, compound="c", command=campusmap)
    b4 = Button(window, text="4. 캘린더", width=15,height=5, compound="c", command=calendar)
    b5 = Button(window, text="5. 종료",width=15,height=5,compound="c", command=close)

    labe2.pack()
    labe3.pack()
    b1.pack(side=LEFT, padx=10)
    b2.pack(side=LEFT, padx=10)
    b3.pack(side=LEFT, padx=10)
    b4.pack(side=LEFT, padx=10)
    b5.pack(side=LEFT, padx=10)

    window.mainloop()

main()
