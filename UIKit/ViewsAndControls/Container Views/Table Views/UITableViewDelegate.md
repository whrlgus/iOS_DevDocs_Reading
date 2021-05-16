[링크](https://developer.apple.com/documentation/uikit/uitableviewdelegate)

# UITableViewDelegate

테이블 뷰에서 선택 행위을 관리하고, 섹션 해더와 푸터를 구성하고, 삭제와 셀의 재정렬, 기타 다른 액션을 수행하기 위한 메소드들이 정의되어 있다.

## Overview

이 프로토콜의 메소드를 통해 다음 기능들을 제어할 수 있다.

- 커스텀 해더와 푸터 뷰를 생성 및 관리
- 행, 해더, 푸터의 커스텀 높이 조정
- 더 나은 스크롤링을 위한 높이 예상치 제공 (더 낫다?????????????)
- 행의 컨텐츠 들여쓰기(indent)
- 행 선택 액션 처리
- 행의 스와이프 및 다른 액션 처리 (어떤 다른??????????????)
- 테이블 컨텐츠 편집 지원

테이블 뷰는 [NSIndexPath](https://developer.apple.com/documentation/foundation/nsindexpath) 객체를 사용하여 행과 섹션의 위치를 지정한다. 



## Instance Mathods

### Configuring Rows for the Table View

- #### tableView(_:willDisplay:forRowAt:)

  델리게이트에게 테이블 뷰가 특정 행에 셀을 그릴 것이라고 말해준다.

  ##### Discussion

  테이블 뷰는 셀을 사용하여 행을 그리기 바로 전에 델리게이트에게 이 메시지를 전달한다. 따라서, 델리게이트가 셀이 보여지기 전에 커스터마이즈할 수 있도록 한다. 이 메소드는 델리게이트가, 이전의 테이블 뷰에 의해 설정된 상태 기반 프로퍼티들을 오버라이드할 기회를 준다. 예를 들면, 선택(selection)과 배경 색이 있다. 델리게이트가 대답(return)하면, 테이블 뷰는 alpha나 frame 프로퍼티의 값만 설정한다. 이 역시도 행이 silde in 또는 out 애니메이션을 수행할 때 뿐이다.

- #### tableView(_:indentationLevelForRowAt:)

  델리게이트에게 주어진 위치에 해당하는 행의 들여쓰기 수준을 반환하도록 요구한다.

  Indentation amount는 indentation level에 indentation width를 곱한 값이다. Indentation width의 기본 값은 10이다.

- #### tableView(_:shouldSpringLoadRowAt:with:)

  이 메소드는 호출되어 테이블 행의 Spring-loading 행위를 조절할 수 있도록 한다.

### Responding to Row Selections

- #### tableView(_:willSelectRowAt:)

  델리게이트에게 행이 곧 선택될 것을 말해준다.

  ##### Return Value

  선택된 행을 확정할지 바꿀지에 따른 index path. 다른 셀이 선택되도록 바꾸고 싶다면 다른 index path를 반환하자. 선택되지 않게 하기 위해서는 nil을 반환하자.

  ##### Discussion

  시스템은 유저가 손가락을 들어올리면 이 메소드를 호출한다; 첫 터치에 행은 강조되지만, 터치가 끝나야 선택되는 것이다. UITableViewCell.SelectionStyle.none을 사용하여 첫 터치에 셀 강조 외양을 비활성화할 수 있다. 행 선택이 가능하지 않게되면, 이 메소드는 호출되지 않는다.

- #### tableView(_:didSelectRowAt:)

  델리게이트에게 행이 선택되었다고 말해준다.

  ##### Discussion

  델리게이트는 이 메소드에서 선택을 처리한다.

- #### tableView(_:willDeselectRowAt:)

  델리게이트에게 행이 선택 해제될 것을 말해준다.

  ##### Discussion

  이 메소드는 유저가 다른 행을 선택할 때 이미 선택한 것이 존재할 때 호출된다.

- #### tableView(_:didDeselectRowAt:)

  델리게이트에게 행이 선택해제 되었음을 말해준다.

  ##### Discussion

  델리게이트는 이 메소드에서 행 선택 해제를 처리한다. 예를 들어 행과 관련된 체크마크 이미지를 제거할 수 있다.

### Providing Custom Header and Footer Views

- #### tableView(_:viewForHeaderInSection:)

  델리게이트에게 테이블 뷰의 섹션 해더에서 보여질 뷰를 요구한다.

  ##### Return Value

  섹션의 상단에 보여질 UILabel, UIImageView, 또는 커스텀 뷰.

  ##### Discussion

  이 메소드를 구현하고 tableView(_:heightForHeaderInSection:) 메소드는 구현하지 않는다면, 테이블 뷰는 그 높이를 자동적으로 계산하거나, sectionHeaderHeight 값이 설정되어 있다면 이 값을 사용한다.

- #### tableView(_:viewForFooterInSection)

  위와 유사

- #### tableView(_:willDisplayHeaderView:forSection:)

  델리게이트에게 해더 뷰가 보일 것임을 말해준다.

- #### tableView(_:willDisplayFooterView:forSection)

  위와 유사

### Providing Header, Footer, and Row Height

- #### tableView(_:heightForRowAt:)

  델리게이트에게 특정 위치에 있는 행의 높이를 요청한다.

  ##### Discussion

  테이블의 행 높이가 모두 같지 않다면 오버라이드하자. 만약 모두 같다면 이 메소드를 오버라이드하지 말고, UITableView의 프로퍼티인 rowHeight에 값을 할당하자. 이 메소드에 의해 반환되는 값은 rowHeight 프로퍼티 값보다 우선순위가 높다.

  화면에 나타나기 전에, 테이블 뷰는 보여지는 부분의 항목에 대해 이 메소드를 호출한다. 화면에 보여질 때마다 호출된다.

- #### tableView(_:heightForHeaderInSection:)

  델리게이트에게 특정 섹션에 있는 해더의 높이를 요청한다.

  ##### Discussion

  tableView(_:viewForHeaderInSection:) 메소드에 의해 반환되는 커스텀 뷰의 높이를 명시할 때 이 메소드를 사용하자.

- #### tableView(_:heightForFooterInSection:)

  위와 유사

- #### automaticDimension

  주어진 길이에 대한 기본 값을 나타내는 상수

  ##### Discussion

  테이블 뷰가 주어진 길이에 대해 기본 값을 선택하길 원하면 델리게이트 메소드에 해당 값을 반환하자. 예를 들어, tableView(_:heightForHeaderInSection:) 에서 이 상수를 반환하면, 테이블 뷰는 tableView(\_:titleForHeaderInSection:) 의 반환 값에 맞는 높이를 사용한다.

### Estimating Heights for the Table's Content

- #### tableView(_:estimatedHeightForRowAt:)

  델리게이트에게 지정된 위치에 있는 행의 예상 높이를 요청한다.
  
  ##### Return Value
  
  행 높이의 추정치로 음이 아닌 실수 값. 추청 값이 없다면 automaticDimension을 반환하자.
  
  ##### Discussion
  
  테이블 뷰가 로딩됐을 때, 사용자 경험을 향상시킬 수 있는 행의 높이 예측값을 제공한다. 만약 테이블이 다양한 행 높이를 갖는다면, 모든 높이를 계산하는 것은 비용이 높고 로드 시간이 길어진다. 예측을 사용하여 로드 시간부터 스크롤 시간까지 연산의 비용을 지연할 수 있다.
  
- #### tableView(_:estimatedHeightForHeaderInSection:)

  위와 유사

- #### tableView(_:estimatedHeightForFooterInSection:)

  위와 유사

### Managing Accessory views

- #### tableView(_:accessoryButtonTappedForRowWith:)

  델리게이트에게 유저가 특정 행의상세 버튼을 탭했다는 것을 말해준다.

  ##### Discussion

  행의 상세 버튼 액세서리 뷰에서 탭 행위에 응답하는 메소드이다. 테이블 뷰는 다른 유형의 액세서리 뷰에는 이 메소드를 호출하지 않는다.

### Responding to Row Actions

- #### tableView(_:leadingSwipeActionsConfigurationForRowAt:)

  행의 선두 모서리에 보여줄 스와이프 액션을 반환하자.

- #### tableView(_:trailingSwipeActionsConfigurationForRowAt:)

  위와 유사

### Managing Table View Highlights

- #### tableView(_:shouldHighlightRowAt:)

  델리게이트에게 지정된 행이 하이라이트되어야 하는지 묻는다.

  ##### Discussion

  터치 이벤트가 도착하면, 테이블 뷰는 유저가 행들을 선택할 것을 예상하여 그것들을 강조한다. 이러한 터치 이벤트들을 처리할 때, 테이블 뷰는 델리게이트에게 주어진 셀이 강조되어야 하는지 묻기 위해 이 메소드를 호출한다. 다른 행이 이미 선택되었거나 다른 관련된 행위가 일어날 때 이러한 강조를 방지하기 위해 이 메소드를 구현할 수 있다.

  이 메소드를 구현하지 않는다면, 기본 반환 값은 true이다.

- #### tableView(:didHighlightRowAt:)

  델리게이트에게 지정된 행이 강조되었다고 알려준다.

- #### tableView(:didUnHighlightRowAt:)

  델리게이트에게 지정된 위치의 행으로부터 강조가 제거되었다고 알려준다.

### Editing Table Rows

- #### tableView(_:willBeginEditingRowAt:)

  델리게이트에게 데이블 뷰가 편집 모드로 전환될 것이라고 말해준다.

  ##### Discussion

  이 메소드는 유저가 행의 수평으로 스와이프할 때 호출된다; 결과적으로, 테이블 뷰는 isEditing 프로퍼티를 true로 설정하고 삭제 버튼을 보여준다. 이러한 swipe to delete 모드에서 테이블 뷰는 다른 삽입, 삭제, 재정렬 컨트롤을 보여주지 않는다. 이 메소드는 델리게이트가 UI를 편집모드로 조정할 기회를 준다. 테이블이 편집모드에서 나갈 때, 테이블 뷰는 tableView(_:didEndEditingRowAt:) 메소드를 호출한다.

  > Note
  >
  > 셀의 스와이프 모션은 데이터소스가 tableView(_:commit:forRowAt:) 메소드를 구현하지 않으면 삭제 버튼을 보여주지 않는다.

- #### tableView(_:didEndEditingRowAt:)

  델리게이트에게 테이블 뷰가 편집 모드에서 벗어났음을 알린다.

- #### tableView(_:editingStyleForRowAt:)

  델리게이트에게 테이블 뷰에서 특정 위치에 있는 행의 편집 스타일을 요청한다.

  ##### Discussion

  이 메소드는 델리게이트가 셀의 편집 스타일을 커스터마이즈할 수 있게 해준다. 만약 이 메소드를 구현하지 않고 UITableViewCell 객체가 편집가능하다면(isEditing 프로퍼티가 true), UITableViewCell.EditingStyle.delete 가 기본 값으로 설정된다.

- #### tableView(_:titleForDeleteConfirmationButtonForRowAt:)

  삭제 확인 버튼의 기본 타이틀을 변경한다.

  ##### Discussion

  셀의 우측에 보여지는 삭제 확인 버튼은 기본적으로 Delete 라는 타이틀을 갖는다. 유저가 행을 스와이프하거나 편집모드에서 빨간 마이너스 아이콘을 탭하여 행을 삭제하려할 때, 테이블 뷰는 이 버튼을 보여준다. 이 메소드를 구현하여 대체할 수 있는 타이틀을 반환할 수 있으며, localized 되어야 한다.

- #### tableView(_:shouldIndentWhileEditingRowAt:)

  델리게이트에게 테이블 뷰가 편집 모드일 때, 지정된 행의 배경이 들여쓰기 되어야 하는지 묻는다.

  ##### Discussion

  기본 값은 true이며, tableView(_:indentationLevelForRowAt:) 메소드와 관련이 없다.

### Reordering Table Rows

- #### tableView(_:targetIndexPathForMoveFromRowAt:toProposedIndexPath:)

  델리게이트에게 행의 제안된 이동에 대한 새로운 index path를 반환하도록 요구한다.

  ##### Return Value

  이동 동작에 대한 바람직한 행 목적지의 위치에 해당하는 index path. proposedDestinationIndexPath의 위치가 적절하다면 이 값은 반환하자.

  ##### Discussion

  이 메소드는 테이블 뷰 내에서 특정 행의 상하 이동에 대한 목적지 위치를 커스터마이즈할 수 있게 해준다. 드래그하는 행이 다른 행을 떠다닐 때, 목적지의 행은 재정렬을 위한 공간을 만들기 위해 아래로 슬라이드된다; 이 위치가 proposedDestinationIndexPath이다.

### Tracking the Removal of Views

- #### tableView(_:didEndDisplaying:forRowAt:)

  델리게이트에게 테이블에서 셀이 제거되었을을 알린다.

  ##### Discussion

  뷰가 나타났는지 사라졌는지 감시하기보다, 테이블 뷰에서 셀이 제거될 때를 탐지하기 위한 목적으로 이 메소드를 사용하자.

- #### tableView(_:didEndDisplayingHeaderView:forSection:)

  위와 유사

- #### tableView(_:didEndDisplayingFooterView:forSection:)

  위와 유사



