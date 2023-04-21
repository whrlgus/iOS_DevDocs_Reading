# Generics
제네릭 코드는 정의한 요구사항을 조건으로하는 어떠한 타입에도 사용할 수 있는 유연하고 재사용가능한 함수와 타입을 작성할 수 있게 해준다. 중복을 피하고 분명하며 추상적인 방식으로 표현하는 코드를 작성할 수도 있다.

스위프트 표준 라이브러리의 많은 부분은 제네릭 코드로 만들어졌다. 예를들어, 스위프트의 `Array` 와 `Dictionary` 타입은 제네릭 콜렉션이다.

## The Problem That Generics Solve
메소드 몸체가 유사하지만 시그니쳐의 파라미터 타입만 다른 여러개의 함수가 구현되는 상황이 생길 수 있다. 

어떠한 타입이든 사용가능한 단일 함수를 작성하는 것이 유용하고 더 유연할 수 있는데, 제네릭 코드가 이러한 함수를 작성할 수 있게 해준다.

## Generic Functions
제네릭 버전의 함수는 실제 타입명(`Int`, `String` 이나 `Double` 과 같은) 대신에 플레이스 홀더 타입명을 사용한다. 실제 타입은 매 함수 호출시에 결정된다.

## Type Parameters
타입 파라미터는 함수명 바로 다음 화살 괄호 안에 작성되며, 플레이스홀더 타입을 구체화하며 이름 짓는다.
타입 파라미터를 명시하고나면, 함수 파라미터, 반환 타입, 몸체의 타입 어노테이션에 사용가능하다. 타입 파라미터는 매 함수 호출시마다 실제 타입으로 대체된다.
컴마로 구분하여 여러개의 타입 파라미터를 제공할 수 있다.

## Naming Type Parameters
타입 파라미터는 제네릭 타입이나 함수와의 관계를 알 수 있도록 기술적인 이름을 갖게 한다. 하지만 의미있는 관계가 없는 경우에는 단일 문자로 표기할 수 있다.
> NOTE
> 값이 아닌 타입의 플레이스홀더임을 나타내기 위해 항상 upper camel case 로 타입 파라미터를 표기하자.

## Generic Types
제네릭 함수에 더불어, 제네릭 타입을 정의할 수도 있다.

## Extending a Generic Type

제네릭 타입을 확장할 때, 타입 파라미터 목록을 익스텐션 정의에 포함하지 않는다. 대신에 익스텐션에서 본래 타입 정의에 있는 타입 파라미터 목록을 이용한다.

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


## Type Constraints

### Type Constraint Syntax

### Type Constraints in Action


## Associated Types

## Generic Where Clauses

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

## Constextual Where Clauses

## Associated Types with a Generic Where Clause

## Generic Subscripts