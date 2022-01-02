# Realm Tutorial: Getting Started

https://www.raywenderlich.com/9220-realm-tutorial-getting-started

Realm은 모바일 앱을 위해 고안된 cross-platform mobile database solution이다. Core Data나 SQLite 에 의존하지 않는다. 이 튜토리얼을 통해 **model을 생성**하고 **query를 수행**하며, **record를 갱신**하는 것을 배울 것이다.

## Concepts and Classes Overview

- **Realm:** Realm 인스턴스는 이 프레임워크의 핵심으로 Core Data managed object context 같은 내부 디비로의 접근점이다. `Realm()` 생성자를 통해 인스턴스를 생성한다.
- **Object:** Realm model이다. 모델을 생성하는 것은 디비의 스키마를 정의하는 것이다. 모델 생성을 위해서는 `Object` 를 서브클래스화하여 프로퍼티로 유지하고 싶은 필드를 정의하면 된다.
- **Relationships:** 참조하는 `Object` 타입의 프로퍼티를 선언하여  일대다 관계를 형성할 수 있다. 또한 `List` 타입의 프로퍼티를 통해 다대일 혹은 다대다 관계를 형성할 수도 있다.
- **Write Transactions:** 디비에서 생성, 편집, 삭제와 같은 작업은 `Realm` 인스턴스의 `write(_:)` 를 호출하여 수행해야 한다.
- **Queries:** 디비로부터 객체를 반환하기 위해서 질의하게되는데, 가장 간단한 형태의 쿼리는 `Realm` 인스턴스에서 `objects()` 를 호출하는 것이다. 더 복잡하다면, predicate, 쿼리 체인, 결과 정렬등을 활용할 수 있다.
- **Results:** 쿼리로 부터 얻은 결과는 auto-updating container 타입이다. Subscript syntax가 가능한 `Array` 와 유사한 점이 많다.

## Your First Model

램에서 string 과 같은 특정 타입은 반드시 초기화되어야 한다.

```swift
import Foundation
import RealmSwift

class Specimen: Object {
  @objc dynamic var name = ""
  @objc dynamic var specimenDescription = ""
  @objc dynamic var latitude = 0.0
  @objc dynamic var longitude = 0.0
  @objc dynamic var created = Date()
}
```

아래와 같은 코드로 Specimen과 Category간의 일대다 관계를 형성할 수 있다. Specimen은 단 하나의 Category에 속하며, Category는 여러개의 Specimen을 가질 수 있다.

```swift
class Specimen: Object {
	@objc dynamic var category: Category!
}
```

## Adding Records

object를 가져오기 위해서 아래와 같이 realm 인스턴스를 생성하고 `objects(_:)` 메소드를 호출하여 프로퍼티를 초기화했다.

```swift
let realm = try! Realm()
lazy var categories: Results<Category> = { self.realm.objects(Category.self) }()
```

Default 값 생성을 위한 코드이다.

```swift
private func populateDefaultCategories() {
  if categories.count == 0 { // 1
    try! realm.write() { // 2
      let defaultCategories =
        ["Birds", "Mammals", "Flora", "Reptiles", "Arachnids" ] // 3
      
      for category in defaultCategories { // 4
        let newCategory = Category()
        newCategory.name = category
        
        realm.add(newCategory)
      }
    }
    
    categories = realm.objects(Category.self) // 5
  }
}
```

`write(_:)` method를 통해 램에 추가하는 transaction을 수행할 수 있다. 그리고 `objects(_:)` method를 통해 fetch하여 할당해준다.

## Introducing the Realm Browser

램은 Realm browser 를 제공하여 디비를 읽고 편집할 수 있게 해준다. 

Encryption key를 입력하라는 창이 뜨길래 검색해 봤더니 MongoDB Realm Studio 라는 툴을 사용하라고 한다. https://github.com/realm/realm-swift/issues/6587

## Working With Realm Browser

다음을 수행하면 램 디비의 위치를 확인할 수 있다. 해당 위치에 있는 파일 중 **default.realm** 이 디비 파일이다.

```swift
print(Realm.Configuration.defaultConfiguration.fileURL!)
```

## Adding Categories

## Adding Specimens

```swift
func addNewSpecimen() {
  let realm = try! Realm() // 1
    
  try! realm.write { // 2
    let newSpecimen = Specimen() // 3
      
    newSpecimen.name = nameTextField.text! // 4
    newSpecimen.category = selectedCategory
    newSpecimen.specimenDescription = descriptionTextField.text
    newSpecimen.latitude = selectedAnnotation.coordinate.latitude
    newSpecimen.longitude = selectedAnnotation.coordinate.longitude
      
    realm.add(newSpecimen) // 5
    specimen = newSpecimen // 6
  }
}
```

위에서 카테고리 추가 코드와 다른 점이라면, 프로퍼티 할당에 그냥 Object 인스턴스를 사용한 점이다.

## Retrieving Records

### A Different View

### Fetches With Predicates

```swift
func filterResultsWithSearchString(searchString: String) {
  let predicate = NSPredicate(format: "name BEGINSWITH [c]%@", searchString) // 1
  let scopeIndex = searchController.searchBar.selectedScopeButtonIndex // 2
  let realm = try! Realm()
    
  switch scopeIndex {
  case 0:
    searchResults = realm.objects(Specimen.self)
      .filter(predicate).sorted(byKeyPath: "name", ascending: true) // 3
  case 1:
    searchResults = realm.objects(Specimen.self).filter(predicate)
      .sorted(byKeyPath: "created", ascending: true) // 4
  default:
    searchResults = realm.objects(Specimen.self).filter(predicate) // 5
  }
}
```

`NSPredicate` 으로 디비 조건절을 선언할 수 있다. `name` 이 `searchString`으로 시작하는 record를 찾기 위함이며, `[c]` 는 case insensitive 하게 찾는다는 의미이다. 그리고 이 조건절을 사용하여 `objects(_:)` method로 가져온 결과를 필터링한다.

## Updating Records

편집 또한 `write(_:)` method로 한다.

```swift
func updateSpecimen() {
  let realm = try! Realm()
    
  try! realm.write {
    specimen.name = nameTextField.text!
    specimen.category = selectedCategory
    specimen.specimenDescription = descriptionTextField.text
  }
}
```



## 궁금증

`List` 타입을 사용하여 다대다, 다대일 관계를 형성하는 과정은?

`Result` 타입과 regular `Arrays` 이 어떤 점에서 유사한지?
