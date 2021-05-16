# UITableViewCell

테이블 뷰에서 하나의 행에 대한 시각적 표현

## Overview

UITableViewCell 객체는 단일 테이블 행의 컨텐츠를 관리하는 뷰의 특별할 타입이다. 셀은 주로 앱의 커스텀 컨텐츠를 구성하고 보여주기 위해 사용되며, 테이블과 관련된 다음과 같은 행동을 커스터마이즈할 수 있게 해준다. 

- 셀에 선택 혹은 강조 색을 적용하는 것 
- Detail 또는 disclosure 컨트롤과 같은 표준 액세서리 뷰를 추가하는 것
- 셀을 편집가능한 상테로 두는 것
- 테이블에서 시각적 계층구조를 생성하기 위해 셀의 컨텐츠를 들여쓰기 하는 것

앱 컨텐츠는 셀의 영역(bounds) 대부분을 차지하나, 다른 컨텐츠를 위한 공간을 마련할 수 있다. 셀은 컨텐츠 영역 후미 가장자리에 액세서리 뷰를 보여줄 수 있다. 테이블을 편집모드로 두면, 셀은 선두 가장자리에 삭제 컨트롤을 추가하고, 선택적으로 재정렬 컨트롤을 위한 액세서리 뷰로 교체한다.

![](https://docs-assets.developer.apple.com/published/2128ef91ee/a27538d0-bc9a-4972-aa83-8616889d7959.png)

모든 테이블 뷰는 컨텐츠를 보여주기 위해 적어도 한가지의 셀 타입을 갖는다. 테이블의 data source는 테이블이 화면에 보여지기 전에 셀을 생성하고 구성한다. 

## Configuring Your Cell's Content

Storyboard 파일에서 셀의 컨텐츠와 배치를 구성하자. 테이블은 기본적으로 하나의 셀 타입을 갖지만, 테이블의 prototype cells attribute에서 값을 바꿔 추가할 수 있다. 셀의 컨텐츠를 구성하는 것 이외에, 다음 속성들을 구성하자.

- Identifier. 셀을 생성할 때 이 식별자(reuse identifier라고 하는)를 사용하자.
- Style. 표준 타입 중 하나를 선택하거나 커스텀 셀을 정의하자.
- Class. 커스텀 행위가 정의된 UITableViewCell 서브클래스를 지정하자.

셀의 컨텐츠와 외양을 구성하기 위해 contentConfiguration 과 backgroundConfiguration을 설정할 수 있다.



## Topics

### Creating a Table View Cell

- #### init(style:reuseIdentifier:)

  스타일과 재활용 식별자로 셀을 초기화하여 호출부로 반환한다.

  ##### Discussion

  이 메소드는 클래스의 지정