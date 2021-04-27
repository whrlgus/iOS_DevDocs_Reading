[링크](https://developer.apple.com/documentation/uikit/uitableviewdatasource)

# UITableViewDataSource

데이터를 관리하고 테이블 뷰에 셀을 제공하는데 사용되는 메소드들이 정의되어 있다.

## Overview

테이블 뷰는 데이터를 보여주는 것만 관리하며, 데이터 자체는 상관하지 않는다. 데이터를 관리하기 위해서는 Data Source 객체를 사용해야 하며, `UITableViewDataSource` 프로토콜을 구현해야한다. Data source 객체는 테이블의 데이터 관련 요청에 응답한다. 테이블의 데이터를 직접 관리하거나, 앱의 다른 부분과 협력하여 데이터를 관리한다. 다음과 같은 다른 책임들도 포함한다.

- 섹션과 행의 개수를 알려준다.
- 행을 위한 셀을 제공한다.
- 섹션 해더와 푸터에 타이틀을 제공한다.
- 테이블의 색인(index)을 구성한다.
- 내제된 데이터의 변화를 요구하는 user-initiated 나 table-initiated에 응답한다.

이 프로토콜이 반드시 요구하는 메소드는 두개이다.

```swift
override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
  return 0
}

override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
  let cell = tableView.dequeueReusableCell(withIdentifier: "cellTypeIdentifier", for: indexPath)
  cell.textLabel!.text = "Cell text"
  
  return cell
}
```

테이블을 위한 특별한 기능을 활성화하고 싶다면 다른 메소드를 사용하자. 예를 들어, [tableView(_:commit:forRowAt:)](https://developer.apple.com/documentation/uikit/uitableviewdatasource/1614871-tableview) 메소드는 행의 swipe-to-delete 기능을 활성화해준다.

data source 객체를 사용하여, 어떻게 테이블의 셀을 생성하고 구성하는 지에 대한 설명은 [Filling a Table with Data](https://developer.apple.com/documentation/uikit/views_and_controls/table_views/filling_a_table_with_data) 에 나와있다.

## Specifying the Location of Rows and Sections

테이블 뷰는 NSIndexPath 객체의 row 와 section 프로퍼티를 사용하여 셀의 위치를 전달해준다. 행과 섹션의 인덱스는 zero-based이다. 특정한 행을 지칭하기 위해서는 section과 row 값 두가지 다 필요하다.

![](https://docs-assets.developer.apple.com/published/ea4b57d860/95595fc6-198c-415e-82b7-6af8b9edc396.png)



## Instance Methods

### Providing the Number of Rows and Sections

- #### tableView(_:numberOfRowsInSection:)

  테이블 뷰의 주어진 section에서 행들의 개수를 data source에게 전달한다.

- #### numberOfSections(in:)

  data source에게 테이블 뷰의 section 개수를 반환하도록 요구한다.

  ###### Discussion

  만약 이 메소드를 구현하지 않는다면, 테이블은 한개의 섹션으로 구성된다.



### Providing  Cells, Headers, and Footers

- #### tableView(_:cellForRowAt:)

  data source에게 테이블 뷰의 특정 위치에 삽입하기 위한 셀을 요구한다.

  ##### Discussion

  테이블 뷰의 [dequeueReusableCell(withIdentifier:for:)](https://developer.apple.com/documentation/uikit/uitableview/1614878-dequeuereusablecell) 메소드를 사용하여 셀을 생성하거나 재활용하자. 셀을 생성한 후에는, 적합한 데이터 값으로 셀의 프로퍼티를 갱신하자.

  이 메소드를 직접 호출하지 말자. 만약 테이블로부터 셀을 가져오고 싶다면, table view의 [cellForRow(at:)](https://developer.apple.com/documentation/uikit/uitableview/1614983-cellforrow) 메소드를 사용하자.

- #### tableView(_:titleForHeaderInSection:)

  Data source에게 테이블 뷰의 지정된 섹션 해더의 타이틀을 요청한다.

  ##### Return Value

  섹션 헤더로 사용될 string. 만약 nil을 반환하면, 섹션은 타이틀을 갖지 않을 것이다.

  ##### Discussion

  섹션 헤더 타이틀을 위해 고정된 폰트 스타일이 사용된다. 만약 다른 font style을 원한다면 custom view를 반환하는 [tableView(_:viewDorHeaderInSection:)](https://developer.apple.com/documentation/uikit/uitableviewdelegate/1614901-tableview) 메소드를 사용하자.

  이 메소드나 tableView(\_:viewForHeaderInSection:) 메소드를 구현하지 않는다면, 테이블은 섹션 해더를 보여주지 않는다. 만약, 두개의 메소드를 구현한다면, tableView(\_:viewForHeaderInSection:) 메소드가 우선권을 갖는다.

- #### tableView(_:titleForFooterInSection:)

  Data source에게 테이블 뷰의 지정된 섹션의 footer 타이틀을 요청한다.

  *이하 헤더 관련 내용과 유사*



### Inserting or Deleting Table Rows

- #### tableView(_:commit:forRowAt:)

  Data source 에게 리시버의 지정된 행에 대하여 삽입 삭제를 커밋하도록 요구한다.

  ##### Parameters

  ###### editingStyle

  indexPath 로 지정된 행의 삭제나 삽입에 해당하는 셀 편집 스타일. 가능한 편집 스타일은 UITableViewCell.EditingStyle.insert 나 UITableViewCell.EditingStyle.delete 가 있다.

  ##### Discussion

  테이블 뷰에서 UITableViewCell 객체와 연관된 삽입 혹은 삭제 버튼을 탭할 때, 테이블 뷰는 data source에게 해당 변화를 커밋하라는 메시지를 보낸다. (만약 유저가 삭제 컨트롤(red minus)을 탭하면, 테이블 뷰는 확인을 위해 삭제 버튼을 보여준다.) data source는 UITableView의 메소드인 [insertRows(at:with:)](https://developer.apple.com/documentation/uikit/uitableview/1614879-insertrows) 나 [deleteRows(at:with:)](https://developer.apple.com/documentation/uikit/uitableview/1614960-deleterows) 를 적절하게 호출하여 변화를 커밋한다.

  Swipe-to-delete 기능을 활성화하려면, 반드시 이 메소드를 구현해야 한다.

  이 메소드 구현부에서 setEditing(_:animated:) 메소드를 호출해서는 안된다. 만약, 해야하는 상황이라면, perform(\_:with:afterDelay:) 메소드를 사용하여 일정 시간 지연 후에 호출하자.

- #### tableView(_:canEditRowAt:)

  data source에게 주어진 행이 편집가능한지 확인하라고 요구한다.

  ##### Discussion

  이 메소드는 data source 가 개개의 행들을 편집가능하지 않게 다룰 수 있도록 한다. 편집가능한 행들은 셀 내에서 삽입, 삭제 control을 보여준다. 만약 이 메소드가 구현되지 않으면, 모든 행들이 편집가능하다. 편집 불가한 행들은 UITableViewCell 객체의 editingStyle 프로퍼티를 무시하며, 삽입 삭제 컨트롤을 위한 들여쓰기를 하지 않는다. 편집 가능한 행들에 대해서 삽입 삭제 컨트롤을 보여주길 원하지 않는다면, tableView(_:editingStyleForRowAt:) 델리게이트 메소드를 이용해 UITableViewCell.EditingStyle.none을 반환하면 된다.



### Reordering Table Rows

- #### tableView(_:canMoveRowAt:)

  Data source에게 주어진 행이 테이블 뷰의 다른 위치로 이동할 수 있는지를 요구한다.

  ##### Discussion

  이 메소드는 data source가 지정된 행의 재정렬 컨트롤을 보이지 않을 수 있도록 해준다. 기본적으로 data source가 tableView(_:moveRowAt:to:) 메소드를 구현했다면, 재정렬 컨트롤을 보여준다.

- #### tableView(_:moveRowAt:to:)

  data source에게 테이블 뷰에서 특정 위치의 행을 다른 위치로 이동할 것을 말해준다.

  ##### Discussion

  유저가 fromRow에서 재정렬 컨트롤을 누르면, UITableView 객체가 data source에게 이 메시지를 전송한다.



### Configuring an Index

- #### sectionIndexTitles(for:)

  Data source에게 테이블 뷰의 섹션들의 타이틀을 반환하도록 요구한다.

  ##### Return Value

  String 배열은 테이블 뷰 섹션들의 타이틀을 제공하여, 테이블 뷰 우측에 인덱스 목록에 나타난다. 

- #### tableView(_:sectionForSectionIndexTitle:at:)

  data source에게 주어진 타이틀과 섹션 타이틀 인덱스를 갖는 섹션의 인덱스를 요구한다.

  ##### Discussion

  이 메소드는 섹션 인덱스 목록 중 한 항목에서의 인덱스 숫자와 타이틀을 전달하여, 참조되는 섹션의 인덱스를 리턴해야 한다. 여기서 두개의 인덱스 숫자가 있다: sectionIndexTitles(for:) 에 의해 반환되는 배열에서 섹션 인덱스 타이틀에 해당하는 인덱스, 그리고 테이블 뷰의 섹션 인덱스; 전자는 전달되고, 후자는 반환된다.  sectionIndexTitles(for:) 에 의해 반환되는 섹션 타이틀 배열의 개수는 테이블 뷰의 실제 섹션 개수보다 적을 수 있음에 주의하자.





















