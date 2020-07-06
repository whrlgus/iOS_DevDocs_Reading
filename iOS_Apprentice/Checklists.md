### 9. Table views

Xcode의 basic app은 기본적으로 ViewController.swift라는 소스 코드 파일과 Main.storyboard 안에 user interface design을 포함하고 있다. storyboard 에서 각 view controller는 scene이라고 부른다. controller의 view type과 scene type은 맞춰줘야 한다. table에는 plain-style table과 grouped table 두가지가 있다. UITableView는 row만 존재하기때문에 리스트와 같다. row와 column까지 사용할 수 있는 뷰는 UICollectionView다.

storyboard에서 view를 추가할 때에는 항상 warning이 발생한다. 이는 constraints를 설정하지 않아서 발생하는 것으로 view의 layout에 대한 제약사항을 추가해서 해결하자.

### 10. The Data Model

model-view-controller pattern은 delegation, target-action과 함께 iOS의 필수적인 세 가지의 디자인 패턴이다.

- model object는 data와 data에 관련된 기능을 포함한다. 게임에서 data는 캐릭터의 레벨, 점수가 될 수 있고, 기능은 data model object가 수행하는 것으로 business rule 혹은 domain logic으로 불린다.
- view object는 앱의 시각적인 부분을 구성하는 image, button, label, text field, table view cell과 같은 것들이다. 앱의 로직에는 관여하지 않는다.
- controller object는 data model object와 view를 연결한다. 뷰에 탭 동작이 발생하는지 주시하면서, 반응으로 data model object를 수정하여 그 결과를 view에 반영한다.

### 11. Navigation Controllers

table view에서 데이터를 모델에 추가하고 뷰에 추가하려고 할 때, tableView의 insertRows(at:with:) method를 호출하면 tableView(*:cellFroRowAt:) method가 자동으로 호출된다. data model과 view는 이와 같은 방식으로 sync를 맞출 수 있다. row를 지우는 과정도 동일한 절차로 수행된다. data model에서 데이터를 지우고, deleteRow(at:with:) method를 이용해서 table view에서 일치하는 row를 지우면 된다. 신기한 부분은 tableView(*:commit:forRowAt:) method를 수행하면 안되던 스와이프 기능이 활성화 되는 것이었다. 검색 결과 iOS(컴파일러??) 가 해당 메소드의 존재 유무를 확인하여 제스쳐 기능을 활성화하는 것이라고 한다. 주의할 점은 데이터를 지울 때 순서를 지켜야 한다는 점이다. 데이터 소스에서 먼저 row 데이터를 지운 뒤에 deleteRows(at:with:) method를 수행해야한다. iOS가 delete 동작 전후의 row개수를 계산하여 지워진 데이터의 개수와 비교해 보는 작업을 수행하기 때문이다.

segue types

- S**how**: 새로운 view controller를 navigation stack에 push하는 것이다. 이전 view controller로 돌아가는 버튼이 자동으로 제공된다. 만약 navigation controller에 내장되지 않았다면, 해당 view controller는 modal 형태로 화면에 나타난다.
- P**resent Modally**: 새로운 view controller가 이전 view controller를 덮는 형태로 나타난다.

navigation controller는 일명 content controller라고 할 수 있는 view controller들을 포함하는 container controller이다. navigation bar를 포함하며 한 스크린에서 다른 스크린으로 쉽게 이동가능하다.

### 12. Add Item Screen

### 13. Delegates & Protocols

screen A에서 screen B를 화면에 띄운 상황에서 두 화면이, 즉 두개의 view controller가 통신을 해야할 수가 있다. 이때, screen B가 screen A의 존재를 알도록 하는 참조 변수를 사용하는 방식은 좋지 못하다. 그렇게 된다면 screen B는 screen A와만 통신할 수 있는 controller가 되기 때문이다. 좋은 방법은 delegate를 사용하는 방법이다.

UIStroyboardSegue 객체의 destination에서 화면에 보여질 view controller에 접근할 수 있다. 이 view controller의 타입은 UIViewController로서, subclass 타입으로 force downcast할 필요가 있는데, 그때 as! 키워드를 사용한다.

IBOutlet의 weak 키워드는 reference cycle의 형성을 막기 위한 것은 아니고, view controller가 해당 view의 소유권을 완전히 가지고 있지 않음을 나타내기 위함이다.

### 14. Edit Items

view 들의 layout constraints를 설정하는데 하나의 뷰에 고정 width가 필요한 경우가 있다. swift에는 variable shadowing이라는 것이 있다. optional variable을 unwrap하여 사용할 경우에 쓰는 방식으로 같은 이름의 constant 변수에 unwrap한 값을 넣을 수 있다.

textField 뷰의 텍스트가 편집되었는지 확인이 필요할 때가 있다. 그럴 때는 UITextFieldDelegate를 채택하여 protocol의 메소드를 구현하면 된다. 그리고 connection inspector에서 textField의 delegate를 해당 controller에 연결해준다. 간혹 여러개의 textField가 있어 이를 구분하려면 tag나 IBOutlet의 객체를 비교하는 방식으로 하면 된다.

사용자 정의 클래스의 객체를 비교하려고 할때, NSObject를 채택하도록 해야지 비교가 가능하다. 원래 Equatable을 채택하여 비교를 할 수 있도록 필요한 메소드를 구현해야 하지만 간편하게 Equatable을 채택하는 NSObject를 채택하기도 한다.

### 15. Saving & Loading

.plist 파일이란 것이 있다. property list를 뜻하며 XML 파일 형식으로 구조화된 데이터를 저장한다. property list에 data를 저장하기 위해서 swift의 Codable protocol을 사용한다. 이를 통해 구조화된 파일 형식으로 저장될 수 있다. NSCoder의 동작 방식과 유사한데, storyboards가 이를 이용하여 정보를 저장하고 불러온다. 객체를 파일로 변환하고 다시 객체로 불러오는 과정을 serialization이라고 한다.

file에 값을 저장하고자 한다면, binary data로 변환해야 한다. 그리고 나서야 file에 쓸 수 있게된다. 이를 위해서 PropertyListEncoder라는 instance를 생성하고 encode라는 method를 사용하여 Data type의 변수에 저장한다. 그리고 Data 객체의 write method를 사용하여 앱의 Documents 폴더 내의 file에 쓰면 된다. 그리고 이렇게 PropertyListEncoder를 이용하여 encode나 decode되는 객체는 반드시 Codable protocol을 채택해야 한다. Codable은 각 방향으로 serialization 처리에 필요한 Encodeable 과 Decodeable protocol 두가지를 따르는 protocol이다. 그리고 해당 protocol은 method에 대한 default implementation 코드가 존재하므로 표준 Swift 타입에 해당하는 객체에 한해서는 따로 구현할 필요가 없다.

do - catch 문과 같이 catch 블락이 존재한다면 Swift는 자동적으로 error 라는 이름의 지역 변수를 선언하여 에러 발생 시에 해당 변수로 관련된 값을 할당한다. 따라서 catch 블락 내에서는 error 변수를 참조할 수 있게 된다. do 블락에서 try를 이용한 메소드 호출을 하는데, do-catch문을 사용하지 않으려면 try? 를 이용해서 실패 시 nil을 반환하도록 할 수도 있다.

NS object는 Foundation framework에서 제공하는 NS(Next Step)이라는 Mac OS X 이전 버전의 운영체제의 이름을 접두어로 한 객체이다.

init이라는 이름의 생성자는 객체를 만들 때 객체의 property의 값이 모두 설정되어 있음을 보장하기 위한 함수이다. 만약 subclass의 생성자에서 property를 초기화하고 함수를 실행할 경우가 있다면 super.init() 의 호출을 기준으로 이전에는 모든 값들을 세팅하고 이후에 함수를 호출해야 한다. 왜냐하면 super class의 모든 property까지도 값이 전부 설정되어 있어야 간혹 발생할 수 있는 에러를 방지할 수 있기 때문이다.

### 16. Lists

버튼에 action method 연결은 버튼에서 view controller로 control-drag 하면 되고, outlet연결은 반대로 view controller에서 버튼으로 control-drag하면 된다.

### 17. Improved Data Model

### 18. User Defaults

user defaults는 optional을 처리할 수 없다. 두개의 equal signs(==)은 변수의 값이 같은 지를 확인하는 operator 이고, 세 개의 equal signs(===)는 변수가 참조하는 객체가 같은 지를 확인하는 연산자이다.

### 19. UI Improvements

localizedStandardCompare(_:) method는 두개의 string을 비교하는데 현재 locale을 기준으로 한다. locale은 객체로 나라와 언어 규칙에 대한 정보가 있다. sorting in german과 sorting in english는 다르다. 알파벳 정렬할 때의 독일어와 영어를 말하는 것 같다.

### 20. Local Notifications