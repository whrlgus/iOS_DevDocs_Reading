# Extensions

Extension은 class, struct, enum, protocol 타입에 새로운 기능을 추가하기 위해 사용한다. 원래의 소스 코드에 접근할 수 없는 경우를 위한 타입 확장도 가능해진다(소급 모델링, retroactive modeling). extension은 Objective-C에서 category와 유사하다. (반면, category와 다르게 extension은 이름이 없다.)

extension은 다음과 같은 것들을 가능하게 해준다:

- 연산 인스턴스 프로퍼티와 연산 타입 프로퍼티를 추가할 수 있다.
- 인스턴스 메소드와 타입 메소드를 정의할 수 있다.
- 새로운 초기화 함수를 제공할 수 있다.
- 서브스크립트를 정의할 수 있다.
- 새로운 중첩 타입을 정의하고 사용할 수 있다.
- 현재 타입이 프로토콜을 채택하도록 할 수 있다.

또한, 프로토콜을 확장하여 구현체를 제공하거나, 추가 기능을 제공할 수도 있다. 

> NOTE
>
> extension은 타입에 새로운 기능을 제공할 수 있지만, 현재 기능을 재정의할 수는 없다.

## Extension Syntax

`extension` 키워드로 extension을 선언한다.

```swift
extension SomeType {
	// SomeType에 추가할 새로운 기능
}
```

extension은 현재 타입이 하나 이상의 protocol을 채택하도록 확장할 수 있다. class 나 struct에 작성하는 방식으로 Protocol 을 따르도록 하면 된다.

```swift
extension SomeType: SomeProtocol, AnotherProtocol {
	// protocol 요구의 구현
}
```

> NOTE
>
> 새로운 기능을 현재 타입에 추가하기 위해 extension을 정의하면, 그 타입의 extension이 정의되기 이전에 타입이 정의되었다 하더라도, 새 기능은 그 타입의 현재한 모든 인스턴스에서 접근 가능하다.

## Computed Properties

extension는 현재 타입에 연산 인스턴스 프로퍼티와 연산 타입 프로퍼티를 추가할 수 있다. 이 예제는 거리 단위 작업을 위한 기본 지원을 제공하기 위해, Swift 내장 Double 타입에 5개의 연산 인스턴스 프로퍼티를 추가한 것을 보여준다. 

```swift
extension Double {
	var km: Double { return self * 1_000.0 }
	var m: Double { return self }
	var cm: Double { return self / 100.0 }
	var mm: Double { return self / 1_000.0 }
	var ft: Double { return self / 3.28084 }
}
let oneInch = 25.4.mm
// 0.0254
let threeFeet = 3.ft
// 0.914399970739201
```

이 연산 프로퍼티는 Double값이 특정 길이 단위로 간주되어야 함을 나타낸다. 비록 연산 프로퍼티로 구현되었지만, 길이 변환을 수행하기 위한 방법으로 이 프로퍼티의 이름을 부동소수점 값에 이어 붙일 수 있다.

이 예제에서 `1.0`값은 "1미터"로 표현된다. 그래서 `m` 연산 프로퍼티가 `self`를 반환한 것이다. `1.m` 표현은 `1.0` 값으로 연산된다.

다른 단위는 미터로 측정된 값을 표현하기 위해 약간의 변환이 필요하다. 1킬로미터는 1,000 미터와 같기 때문에, `km` 프로퍼티는 미터로 변환하기 위해 그 값을 `1_000.0` 로 곱한다. 

이러한 프로퍼티들은 읽기만 가능한 연산 프로퍼티이며, 간결함을 위해 `get` 키워드 없이 표현된다. 그 반환값은 `Double`이며 `Double`이 허용되는 모든 연산에 사용될 수 있다.

```swift
let aMarathon = 42.km + 195.m
// 42195.0
```

> NOTE
>
> extension은 새로운 연산 프로퍼티를 추가할 수 있지만, 저장 프로퍼티는 불가하며, 현재하는 프로퍼티에 프로퍼티 옵저버를 추가하는 것도 불가능하다.

## Initializers

extension은 현재 타입에 새로운 생성자를 추가할 수 있다. 다른 타입을 확장하여 생성자 매개변수로 커스텀 타입을 수용할 수 있도록 하거나, 본래 구현에 없는 추가적인 초기화 옵션을 제공할 수 있다.

extension은 클래스에 새로운 편의 생성자를 추가할 수 있지만, 지정 생성자나 소멸자를 추가할 수는 없다. 지정 생성자와 소멸자는 본래 클래스 구현에 추가되어야 한다.

만약 모든 저장 프로퍼티에 디폴트 값을 제공하는 값 타입에 생성자를 추가하는데 extension을 사용하고 어떠한 커스텀 생성자를 정의하지 않는다면, extension 생성자에서 값 타입을 위한 디폴트 생성자와 memberwise 생성자를 호출할 수 있다.  값 타입의 본래 구현에 생성자를 작성한 경우에는 해당되지 않는다.

다른 모듈에 선언된 구조체에 생성자를 추가하기 위해 extension을 사용했다면, 정의하는 모듈에서 생성자가 호출된 이후에야 새로운 생성자에 접근할 수 있다.

아래 예제는 사각형을 표현하기 위한 커스텀 `Rect` 구조체이다. 또한, 모든 프로퍼티에 디폴트 값을 제공하는 `Size`와 `Point` 라고 불리는 보조 구조체도 정의한다. 

```swift
struct Size {
	var width = 0.0, height = 0.0
}
struct Point {
	var x = 0.0, y = 0.0
}
struct Rect {
	var origin = Point()
	var size = Size()
}
```

`Rect` 구조체는 모든 프로퍼티에 디폴트 값을 제공하므로, 자동적으로 기본 생성자와 멤버와이즈 생성자를 제공받는다. 이 생성자들은 새로운 `Rect` 인스턴스를 생성하는데 사용될 수 있다:

```swift
let defaultRect = Rect()
let memberwiseRect = Rect(origin: Point(x: 2.0, y: 2.0), size: Size(width: 5.0, height: 5.0))
```

특정 중앙점과 크기를 갖는 초가적인 생성자를 제공하기 위해 `Rect` 구조체를 확장할 수 있다.

```swift
extension Rect {
	init(center: Point, size: Size) {
		let originX = center.x - (size.width / 2)
		let originY = center.y - (size.height / 2)
		self.init(origin: Point(x: originX, y: originY), size: size)
	}
}
```

이 새로운 생성자는 주어진 `center` 와 `size` 값에 근거하여 적절한 원점을 계산하는 것으로부터 시작된다. 그리고 새로운 원점과 크기를 저장하는, 자동적인 멤버와이즈 생성자 `init(origin:size:)` 를 호출한다.

```swift
let centerRect = Rect(center: Point(x: 4.0, y: 4.0), size: Size(width: 3.0, height: 3.0))
// centerRect의 원점은 (2.5, 2.5), 크기는 (3.0, 3.0)
```

> NOTE
>
> 만약 extension에 새로운 생성자를 제공한다고 해도, 여전히 그 생성자의 완료시점에  각 인스턴스가 완전히 초기화 되도록 해야한다.

## Methods

extension은 현재 타입에 새로운 인스턴스 메소드와 타입 메소드를 추가할 수 있다. 다음 예제는 `Int`타입에 `repetitions` 이라고 불리는 새로운 인스턴스 메소드를 추가했다:

```swift
extention Int {
	func repetitions(task: () -> Void) {
		for _ in 0..<self {
			task()
		}
	}
}
```

`repetitions(task:)` 메소드는 매개변수와 반환값이 없는 함수를 나타내는 `() -> Void` 타입의 단일 인자를 받는다.

extension을 정의한 후에 여러차례 작업을 수행할 수 있도록 어떠한 정수에 `repetitions(task:)` 메소드를 호출할 수 있다.

```swift
3.repetitions {
	print("Hello!")
}
// Hello!
// Hello!
// Hello!
```

### Mutating Instance Methods

extension에 추가된 인스턴스 메소드는 인스턴스 자체를 수정할 수 있다. `self` 나 그 프로퍼티를 수정하는 struct와 enum 메소드는, 본래 구현에 있는 method처럼 반드시 `mutating` 로 인스턴스 메소드를 표시해야 한다.

아래 예제는 `Int` 타입에 원래 값을 제곱하는 `square` 메소드를 추가한다.

```swift
extension Int {
	mutating func square() {
		self = self * self
	}
}
var someInt = 3
someInt.square()
// someInt is now 9
```

## Subscripts

extension은 현재 타입에 새로운 서브스크립트를 추가할 수 있다. 이 예제는 Swift 내장 `Int` 타입에 정수 서브스크립트를 추가한다. 이 서브스크립트 `[n]`은 숫자 오른쪽으로부터 `n`위치에 있는 10진수 한자리를 반환한다.

- `123456789[0]`은 `9` 를 반환한다.
- `123456789[1]`은 `8` 를 반환한다.

```swift
extension Int {
	subscript(digitIndex: Int) -> Int {
		var decimalBase = 1
		for _ in 0..<digitIndex {
			decimalBase *= 10
		}
		return (self / decimalBase) % 10
	}
}
```

만약 `Int` 값이 요청된 인덱스 만큼의 수가 부족하다면, 왼쪽에 0을 붙인 수에서와 같이, 서브스크립트 구현은 `0`을 반환한다.

```swift
746381295[9]
// 아래의 요청과 같이 0을 반환
0746381295[9]
```

## Nested Types
extension은 class, struct, enum에 중첩 타입을 추가할 수 있다.

```swift
extension Int {
	enum Kind {
		case negative, zero, positive
	}
	var kind: Kind {
		switch self {
		case 0:
			return .zero
    case let x where x > 0:
			return .positive
		default:
			return .negative
		}
	}
}
```

이 예제는 `Int`에 새로운 중첩 enum을 추가하였다. 이 enum은 특정 정수가 표현하는 수의 종류를 나타낸다. 구체적으로 음수, 0, 양수를 표현한다.

이 예제는 또한 그 정수에 적절한 `Kind` enum 케이스를 반환하는 새로운 인스턴스 프로퍼티를 추가한다.

중첩 enum은 어떠한 `Int` 값에나 사용할 수 있다:

```swift
func printIntegerKinds(_ numbers: [Int]) {
	for number in numbers {
		switch number.kind {
		case .negative:
			print("- ", terminator: "")
		case .zero:
			print("0 ", terminator: "")
    case .positive:
    	print("+ ", terminator: "")
		}
	}
	print("")
}
printIntegerKinds([3, 19, -27, 0, -6, 0, 7])
// "+ + - 0 - 0 + "
```

이 `printIntegerKinds(_:)` 함수는 `Int` 배열을 입력으로 하고 차례대로 반복한다. 배열의 각 정수에 대해서, 이 함수는 정수의 `kind`  연산 프로퍼티를 확인하여 적절한 설명을 출력한다.

> NOTE
>
> `number.kind`는 `Int.Kind` 타입으로 알려진다. 때문에 모든 `Int.Kind` 케이스의 값은 `switch` 구문에서 `Int.Kind.negative`가 아닌 `.negative`와 같은 약어로 작성될 수 있다.