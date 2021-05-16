[링크](https://developer.apple.com/documentation/uikit/uitableviewdelegate/handling_row_selection_in_a_table_view)

# Handling Row Selection in a Table View

유저가 테이블 뷰 셀을 탭할 때를 감지하여 앱이 다음 액션을 취할 수 있도록 한다.

## Overview

유저가 테이블 뷰의 행을 탭할 때, 특정 행위가 뒤따른다. 또 다른 뷰가 미끄러져 온다든가, 행에 체크마크 표시를 한다든가 하는 것들이 있다. 이러한 액션을 수행하기 위해, 유저가 언제 행을 탭하는지 알아야 하며 그것에 알맞게 반응할 수 있어야 한다.

## Configure Row Selection Behavior

다음 프로퍼티들을 히용해 테이블 뷰에서 행 선택 행위를 어떻게 할 지 구성할 수 있다.

- allowsSelection

  테이블이 편집 모드가 아닐 때 행을 선택할 수 있는지 결정. defualt는 true.

- allowsMultipleSelection

  편집 모드가 아닐 때, 두 개 이상의 행을 선택할 수 있는지를 결정. default는 false.

- allowsSelectionDuringEditing

  편집 모드에서 행 선택을 할 수 있는지를 결정. default는 false.

- allowsMultipleSelectionDuringEditing

  편집 모드에서 두 개 이상의 행을 선택할 수 있는지를 결정. default는 false.

## Respond to Row Selections

유저가 행을 탭하면, 테이블 뷰는 델리게이트 메소드인 `tableView(_:didSelectRowAt:)`을 호출한다. 이 시점에, 앱은 행동을 취한다.

만약 셀 선택에 대한 반응으로 새로운 뷰컨을 네비게이션 스택에 푸시했다면, 스택에서 팝을 할 때 선택 해제를 하자. 만약 UITableViewController를 사용한다면, clearsSelectionOnViewWillAppear 프로퍼티를 true로 설정하면 된다. 그렇지 않으면, 뷰컨의 viewWillAppear(_:) 메소드에서 선택을 해제할 수 있다.

만약 행이 상세 버튼 액세서리 뷰를 보여주며 이 뷰를 탭한다면, 테이블 뷰는 tableView(\_:didSelectRowAt:) 메소드 대신에 tableView(_:accessoryButtonTappedForRowWith:) 메소드를 호출한다.

## Select a Row Programmatically

선택은 테이블 뷰에서의 탭으로 이뤄지지 않고 앱 자체에서 이뤄진다. 예를 들어, 주소록에 새로운 사람을 추가하고 연락처 목록으로 돌아가는 상황이 있다. 이때, 새로 추가된 사람의 행으로 스크롤하는데, 이 상황에서 사용되는 메소드가 selectRow(at:animated:scrollPosition:) 이다. 

> Note
>
> 코드로 행을 선택하면 tableView(\_:willSelectRowAt:) 이나 tableView(\_:didSelectRowAt:) 메소드가 호출되지 않으며, 옵저버에게 selectionDidChangeNotification 노티를 보내지도 않는다.

## Manage Selection Lists

셀 선택을 통해 선택된 항목들의 inclusive 나 exclusive 목록을 구성할 수도 있다. Inclusive 목록은 하나 이상의 선택된 항목들을 가질 수 있는 반면, exclusive 목록은 하나 이하의 항목을 가질 수 있다.

앱에서 선택 목록을 제공할 때, 셀의 선택된 상태로 항목의 선택 여부를 보여주지 말자. 대신에 액세서리 뷰의 체크마크를 보여주자. 이를 위해서, tableView(_:didSelectRowAt:) 델리게이트 메소드를 구현하고, deselectRow(at:animated:) 메소드로 선택 해제 후, 셀의 accessoryType 프로퍼티를 UITableViewCell.AccessoryType.checkmark로 설정한다.

Exclusive 목록을 관리하는 것도 위와 비슷하다. 행을 선택 해제하고 체크마크를 보여주거나, 액세서리 뷰에 선택된 상태를 표시할 수 있다. 그러나 inclusive 목록과는 다르게 한번에 최대 하나로 제한한다.

