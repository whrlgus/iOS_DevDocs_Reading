# Generics

## Extending a Generic Type

제네릭 타입을 확장할 때 익스텐션 정의의 일부로 타입 파라미터 목록을 제공하지 않는다. 대신에 익스텐션에서 본래 타입 정의에 있는 타입 파라미터 목록을 이용한다.

아래 예제는 읽기 전용 연산 프로퍼티 `topItem` 을 추가하기 위해, 제네릭 `Stack` 타입을 확장하였다.

```swift
extension Stack {
	var topItem: Element? {
		return items.isEmpty ? nil : items[items.count - 1]
	}
}
```

`topItem` 프로퍼티는 `Element` 타입의 옵셔널 값을 반환한다. 만약 스택이 비었다면 `topItem` 은 `nil` 을 반환한다: 그렇지 않으면 `items` 배열의 마지막 항목을 반환한다.

타입 파라미터 목록을 정의하지 않았다는 것을 주목하자. 대신에 `Stack` 타입의 존재하는 타입 파라미터 이름인 `Element` 가 사용된다. 

`topItem` 연산 프로퍼티는 이제 `Stack` 인스턴스에 접근해 상위 항목을 반환한다.

```swift
if let topItem = stackOfStrings.topItem {
	topItem // tres
}
```

제네릭 타입의 익스텐션은 새로운 기능을 얻기 위해 확장된 타입의 인스턴스가 만족해야 할 요구사항을 포함할 수 있다.



## Extensions with a Generic Where Clause

익스텐션의 일부로 제네릭 `where` 절을 사용할 수 있다. 아래 예제는 제네릭 `Stack` 구조체를 확장하여 `isTop(_:)` 메소드를 추가하였다.

```swift
extension Stack where Element: Equatable {
	func isTop(_ item: Element) -> Bool {
		guard let topItem = items.last else {
			return false
		}
		return topItem == item
	}
}
```

`isTop(_:)` 메소드는 우선 스택이 비어있는지 확인하고, 상위 항목과 주어진 항목을 비교한다. 제네릭 `where` 절이 없다면 문제가 발생한다: 구현부에는 `==` 연산자를 사용하는데, `Stack` 정의는 항목이 동일시되어야 한다는 요구조건을 만족하지 않아서 컴파일 에러가 발생한다. 제네릭 `where` 절 사용은 익스텐션에 새로운 요구사항을 추가할 수 있게 해주어, 스택의 항목이 동일시할 수 있을 때, `isTop(_:)` 메소드를 추가한다.

제네릭 `where` 절은 프로토콜 익스텐션에도 사용할 수 있다. 

```swift
extension Container where Item: Equatable {
	func startsWith(_ item: Item) -> Bool {
		return count >= 1 && self[0] == item
	}
}
```

익스텐션의 일부로 제네릭 `where`절에서 여러 요구사항을 포함할 수 있다. 목록의 각 요구사항은 컴마로 구분하자.