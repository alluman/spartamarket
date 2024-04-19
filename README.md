# Django 기초과제 (이시문, AI_6기)

회원가입 및 로그인, 상품등록 사이트 제작


![erd](https://github.com/alluman/spartamarket/assets/160446710/dfdda3c7-355e-464a-a4fe-aad0d3644c23)

사용한 기술

Python, Django

기능

product CRUD

좌측 상단 [청순 수연] 버튼으로 list page로 이동

글에 대한 좋아요 여부에 따라 좋아요 숫자 변경

글 접속 및 새로고침시 조회수 변경

최신순, 좋아요순으로 정렬 가능하고, 좋아요 개수에 따른 정렬 가능(동일한 개수라면 최신순으로 정렬)

글 작성시 내용 및 해시태그 입력란에 #hashtag 형태로 해시태그를 넣을 수 있고, 글 조회시 해시태그 항목에 별도로 표시, 해시태그에 특수문자 배제

글에 이미지를 넣을 수 있고, 이미지를 넣지 않을 경우 기본 이미지 표시

게시글 검색 기능(title, content, author, hashtag)

user CRUD

회원가입 가능(username, password, email, profile_image) + email 중복일 경우 errormessage, image 등록하지 않을 경우 기본image 제공

로그인 여부에 따라 글 작성, 좋아요, 팔로우에 제한이 생기며 비 로그인 상태로 실행한 경우 로그인 페이지로 이동

유저 정보 수정 가능(password, email, profile_image), 변경할 password가 기존의 password와 같으면 errormessage

profile_page에서 해당 유저의 정보 조회가능(가입일자, 팔로우/팔로워 숫자, 작성글, 좋아요 누른 글)

유저의 팔로우 여부에 따라 팔로워, 팔로잉 숫자 변경
