# Protocols

## Adding Protocol Conformance with an Extension

현재 타입의 소스 코드에 접근할 수 없다고 해도, 현재 타입이 새로운 프로토콜을 채택하고 따르도록 확장할 수 있다. 익스텐션은 현재 타입에 새로운 프로퍼티, 메소드, 서브스크립트를 추가할 수 있고, 그 프로토콜이 요구하는 어떠한 요구사항이든지 추가할 수 있다. 

예를 들어, `TextRepresentable` 이라고 불리는 프로토콜은 텍스트로 표현할 수 있는 모든 타입에서 구현될 수 있다. 그 자체의 설명이 될 수도 있고, 현재 상태의 텍스트 버전일 수도 있다:

```swift
protocol TextRepresentable {
	var textualDescription: String { get }
}
```

`Dice` 클래스는 `TextRepresentable` 을 채택하고 따르도록 확장될 수 있다.

```swift
extension Dice: TextRepresentable {
	var textualDescription: Strint {
		return "A \(sides)-sided dice"
	}
}
```

이 익스텐션이 새로운 프로토콜을 채택하는 것은, `Dice` 의 본래 구현에서 제공하는 것과 같다. 콜론으로 구분되어 타입의 이름 뒤에 프로토콜 이름을 작성하며, 프로토콜 요구사항의 구현은 익스텐션의 괄호 안에서 제공된다.

`Dice` 인스턴스는 `TextRepresentable` 로 다뤄질 수 있다:

```swift
let d12 = Dice(sides: 12, generator: LinearCongruentialGenerator())
d12.textualDescription // A 12-sided dice
```

유사하게, `SnakesAndLadders` 게임 클래스도 `TextRepresentable` 프로토콜을 채택하고 따르도록 확장될 수 있다.

```swift
extension SnakesAndLadders: TextRepresentable {
	var textualDescription: String {
		return "A game of Snakes and Ladders with \(finalSquare) squares"
	}
}
```

### Conditionally Conforming to a Protocol

제네릭 타입은 특정 조건에서만 프로토콜의 요구사항을 만족할 수 있다. 제네릭 타입을 확장할 때 제약을 나열하여 조건적으로 제네릭 타입이 프로토콜을 따르도록 할 수 있다. 제네릭 `where` 절을 사용하여 프로토콜 이름 뒤에 제약을 작성할 수 있다. 

아래 익스텐션은 `Array` 인스턴스에 저장된 인자타입이 `TextRepresentable` 을 따를 때, 그 인스턴스가 `TextRepresentable` 프로토콜을 따르도록 했다.

```swift
extension Array: TextRepresentable where Element: TextRepresentable {
	var textualDescription: String {
		let itemsAsText = self.map { $0.textualDescription }
		return "[" + itemsAsText.joined(separator: ", ") + "]"
	}
}
let myDice = [d6, d12]
myDice.textualDescription // [A 6-sided dice, A 12-sided dice]
```

### Declaring Protocol Adoption with an Extension

만약 타입이 프로토콜의 모든 요구사항을 따르고 있지만, 프로토콜을 채택한다고 표현되지 않았다면, 빈 익스텐션으로 프로토콜을 채택하도록 할 수도 있다.

```swift
struct Hamster {
	var name: String
	var textualDescription: String {
		return "A hamster named \(name)"
	}
}
extension Hamster: TextRepresentable {}
```

이제 `Hamster` 인스턴스는 `TextRepresentable`이 요구되는 타입인 곳에 사용될 수 있다.

```swift
let simonTheHamster = Hamster(name: "Simon")
let somethingTextRepresentable: TextRepresentable = simonTheHamster
somthingTextRepresentable.textualDescription // A hamster named Simon
```

> NOTE
>
> 타입은 요구사항을 만족했다고 자동적으로 그 프로토콜을 채택하지 않는다. 반드시 명시적으로 프로토콜을 채택한다고 선언해야 한다.

## Protocol Inheritance

프로토콜은 하나 이상의 다른 프로토콜을 상속할 수 있고 그것이 상속하는 요구사항 상위에 추가적인 요구사항을 더할 수 있다. 클래스 상속을 위한 신텍스와 유사하지만, 컴마로 쿠분하여 여러개의 상속된 프로토콜을 나열할 수 있다.

```swift
protocol InheritingProtocol: SomeProtocol, AnotherProtocol {
	// 프로토콜 정의
}
```

`TextRepresentable` 프로토콜을 상속한 프로토콜의 예시이다:

```swift
protocol PrettyTextRepresentable: TextRepresentable {
	var prettyTextualDescription: String { get }
}
```

`PrettyTextRepresentable`을 채택하는 것은 `TextRepresentable`의 요구사항과 `PrettyTextRepresentable`에 의해 강제되는 추가적인 요구사항을 만족한다. 

`SnakesAndLadders` 클래스는 `PrettyTextRepresentable` 을 채택하고 따르기위해 확장될 수 있다:

```swift
extension SnakesAndLadders: PrettyTextRepresentable {
	var prettyTextualDescription: String {
		var output = textualDescription + ":\n"
		for index in 1...finalSqure {
			switch board[index] {
			case let ladder where ladder > 0:
				output += "▲ "
      case let snake where snake < 0:
      	output += "▼ "
     	default:
     		output += "○ "
			}
		}
		return output
	}
}
```

## Protocol Extensions

프로토콜을 확장하여 메소드, 생성자, 서브스크립트, 연산 프로퍼를 순응 타입에 제공할 수 있다. 이 것은 각 타입이나 전역 함수가 아닌 프로토콜 자체에 행동을 정의할 수 있게 해준다.

예를들어, `RandomNumberGenerator` 프로토콜은 `Bool` 타입의 랜덤 값을 반환하기위해 필요한 `random()`의 결과를 사용하는 `randomBool()` 메소드를 확장한다.

```swift
extension RandomNumberGenerator {
	func randomBool() -> Bool {
		return random() > 0.5
	}
}
```

프로토콜에 extension을 생성함으로써, 모든 순응 타입은 자동적으로 추가 변경없이 이 메소드를 갖게된다.

```swift
let generator = LinearCongruentialGenerator()
generator.random() // 0.3746
generator. RandomBool() // true
```

프로토콜 extension은 순응 타입에 구현을 추가할 수 있지만, 프로토콜을 확장하거나 다른 프로토콜로부터 상속받을 수 없다. 프로토콜 상속은 항상 프로토콜 선언 그 자체에 기술된다.

### Providing Default Implementations

프로토콜의 메소드나 연산 프로퍼티 요구사항을 위한 기본 구현을 프로토콜 extension을 통해 제공할 수 있다. 만약 순응 타입이 요구되는 메소드나 프로퍼티의 구현을 제공한다면, 그 구현은 extension에 의해 제공되는 것들 대신 사용될 것이다.

> NOTE
>
> extension에 의해 기본 구현이 제공되는 프로토콜 요구사항은 옵셔널 프로토콜 요구사항과 다르다. 비록 두 경우 모두 순응 타입에 구현할 필요는 없지만, 기본 구현이 제공되는 요구사항은 옵셔널 체이닝 없이 호출될 수 있다.

예를 들어, `TextRepresentable`을 상속하는 `PrettyTextRepresentable` 프로토콜은, 요구되는 `prettyTextualDescription` 프로퍼티의 기본 구현을  `textualDescription` 프로퍼티의 결과를 반환하여 제공할 수 있다.

```swift
extension PrettyTextRepresentable {
	var prettyTextualDescription: String {
		return textualDescription
	}
}
```

### Adding Constraints to Protocol Extensions

프로토콜 익스텐션을 정의할 때, 익스텐션의 메소드나 프로퍼티를 사용하기 위해 순응 타입이 반드시 만족해야하는 제약을 지정할 수 있다. 제네릭 `where` 절을 이용하여 확장하려는 프로토콜 이름 뒤에 제약을 작성할 수 있다. 

예를 들어, 인자가 `Equatable` 프로토콜을 채택하는 모든 집합에 적용되는 `Collection` 프로토콜에 익스텐션을 정의할 수 있다. 집합의 요소가 `Equatable` 타입으로 제한하면, `==` 와 `!=` 연산자를 사용하여 두 요소간 일치와 불일치 여부를 검사할 수 있다.

```swift
extension Collection where Element: Equatable {
	func allEqual() -> Bool {
		for element in self {
			if element != self.first {
				return false
			}
		}
		return true
	}
}
```

두개의 정수 배열이 있고, 하나는 모든 인자가 동일하고, 다른 하나는 그렇지 않다.

```swift
let equalNumbers = [100, 100, 100, 100, 100]
let differentNumbers = [100, 100, 200, 100, 200]
```

배열은 `Collection`을 따르고 정수는 `Equatable`을 따르기 때문에, `equalNumbers`와 `differentNumbers`는 `allEqual()` 메소드를 사용할 수 있다:

```swift
equalNumbers.allEqual() // true
differentNumbers.allEqual() // false
```

> NOTE
>
> 제약있는 여러개의 익스텐션이 같은 메소드나 프로퍼티의 구현을 제공하고, 순응타입이 그 요구사항을 모두 만족한다면, Swift는 가장 특별한 제약에 해당하는 구현을 사용한다.