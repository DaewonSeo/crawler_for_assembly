from bs4 import BeautifulSoup
import requests
import re
import csv

def main():

    url = 'http://www.assembly.go.kr/assm/memact/congressman/memCond/memCondListAjax.do?currentPage=1&rowPerPage=300'

    """
    국회의원 현황 페이지의 경우 javascript 기반으로 작동되고 있다. selenium으로 접근 가능하지만, 좀 더 쉬운 방법으로 
    http://www.assembly.go.kr/assm/memact/congressman/memCond/memCond.do 페이지를 크롬 개발자 도구 Network를 
    보면 요청시 렌더링 되는 값들을 확인할 수 있는데 이 페이지에서는 ajax 방식을 통해 
    http://www.assembly.go.kr/assm/memact/congressman/memCond/memCondListAjax.do의 url로 데이터를 주고 받고 있다 .
    
    그리고 이 url의 페이지 소스를 보면 하단부분에 currentPage와 rowPerPage라는 파라미터가 존재하는데, 
    이를 통해 ajax 결과값을 조정하는 것을 확인할 수 있다. 
    결과적으로 rowPerPage의 값이 현재 페이지에서 보여주는 데이터들을 정의함으로, 국회의원 299명을 전체 한페이지로 불러오기 위해 
    rowPerPage 값을 300으로 정의하였다. 
    
    """
    req = requests.get(url)
    html = req.content # 요청 보낸 데이터를 받아오기

    soup = BeautifulSoup(html, 'lxml') # lxml를 파서로 사용하고, BeautifulSoup에 담기

    
    
    
    member_list = soup.select('.memberna_list dl dt a') # select 메소드는 css selector 방식읕 통해서 특정 문단을 가져올 수 있는 방법

    """
    css selector는 css 문법을 기반으로 작동한다.
    css에서는 클래스 태그의 경우 .tagname
    일반 태그의 경우 tagname으로 작동.

    그래서 위 예제에서도 각 의원들의 값을 구글 검사 기능으로 확인해보면 
    <div class='memberna_list'>
        <dl>
        <dt>
            <strong>
                <a href="javascript:jsMemPop('9770276')" title="강길부의원정보 새창에서 열림">강길부</a>
            </strong>
        </dt>
        </dl>
    </div>
    다음과 같이 되어있기 때문에 class 태그인 memberna_list는 .memberna_list로 접근 그 안의 dl은 일반태그 이기 때문에 dl 그리고 다른 태그의 경우 일반
    태그 이기 때문에 태그명으로만 접근이 가능하다. 
    그래서 select 안의 css selector 문법과 일치하는 모든 경우를 리스트 값으로 반환해준다. 

    참고 : id 태그의 경우에는 #tagname으로 접근 가능. 

    """
    
    with open('member_list.csv', 'w') as f:
        csv_writer = csv.writer(f)    
        for member in member_list:
            name = member.text # 이름값 가져오기
            id_href = member['href'] #href 값으로 접근

            pattern = re.search(r'\d+', id_href) # 문자열에서 특정 패턴의 문자들만 가져오기 (매칭되는 결과가 있으면 True, 없으면 False 반환) 예) javascript:jsMemPop('9770933') 9770933 값만 가져오기

            if pattern:
                mem_id = pattern.group(0) # 매칭되는 값 가져오기

            else:
                mem_id = None # 매칭되는 값이 없는경우 None 값 선언
            
            f = open('photo/{}.jpg'.format(mem_id), 'wb') # 파일명 지정 국회의원번호.jpg (해당 경로에 photo 라는 디렉토리 생성해야함.)
            request_photo = requests.get('http://www.assembly.go.kr/photo/{}.jpg'.format(mem_id)).content # 사진 url로 요청보내고 그 결과값 가져오기 크롬 개발자도구로 사진 url 확인가능
            f.write(request_photo) # 사진 데이터 저장해주기

            
            csv_writer.writerow([name, mem_id]) # 파일 작성해주기

        

    

    
    
    














if __name__ == "__main__":
    main()