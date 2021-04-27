# Table Views

하나의 열에 커스터마이즈 가능한 행들을 두어 데이터를 보여준다.



### Overview

테이블 뷰는 수직 스크롤이 가능한 하나의 열(column)에, 행(row)과 섹션(section)으로 컨텐츠를 구분하여 보여준다. 테이블 뷰의 각 행은 앱에 연관된 정보들 중의 하나를 보여준다. 예를 들어, 연락처 앱은 이름 목록을 보여주기 위해 테이블 뷰를 사용한다.

![](https://docs-assets.developer.apple.com/published/6c67362d82/eb067a17-54f7-415f-ac37-25681879911f.png)

테이블 뷰는 다음과 같은 다양한 객체들을 조합하여 사용된다.

- Cells.

  셀을 통해 컨텐츠를 시각적으로 표현하게 된다. 앱의 니즈에 맞게 default 셀을 사용하거나, 커스텀 셀을 정의하여 사용할 수 있다.

- Table view controller.

  보통 테이블 뷰를 관리하기 위해 [UITableViewController](https://developer.apple.com/documentation/uikit/uitableviewcontroller) 객체를 사용한다. 다른 종류의 뷰 컨트롤러를 사용하여 관리할 수 있다.

- Data source object.

  이 객체는 [UITableViewDataSource](https://developer.apple.com/documentation/uikit/uitableviewdatasource) 프로토콜을 채택하며, 테이블에 데이터를 제공한다.

- Delegate object.

  이 객체는 [UITableViewDelegate](https://developer.apple.com/documentation/uikit/uitableviewdelegate) 프로토콜을 채택하며, 테이블의 컨텐츠에 대한 사용자 인터랙션을 관리한다.