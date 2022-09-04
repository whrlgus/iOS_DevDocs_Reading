# Closures
클로저는 코드 곳곳을 돌아다니며 사용될 수 있는 독립적인 기능 블록이다. 스위프트의 클로저는 C와 Objective-C에서의 블록과 유사하며, 기타 다른 프로그래밍 언어에서의 람다와 유사하다.

클로저는 컨택스트에 정의된 상수와 변수로의 참조를 붙잡아두고 저장할 수 있다. 상수와 변수를 에워싼다고도 하며, 스위프트에서 이를 위한 메모리 관리를 하고 있다.

전역 함수와 중첩 함수는 사실상 클로저의 특별한 유형이다. 클로저는 아래 세가지 형태 중에 하나이다:
- 전역 함수는 이름은 있지만 어떤 값도 붙잡지 않는 클로저이다.
- 중첩 함수는 이름도 있고 둘러싸고 있는 함수의 값을 붙잡을 수 있는 클로저이다.
- 클로저 표현은 주위의 컨텍스트로부터 값을 붙잡을 수 있는 경량의 구문으로 작성된 이름없는 클로져이다.

스위프트의 클로저 표현은 일반적인 시나리오에서 간결하고 깔끔한 구문을 조장하는 최적화를 제공한다.이러한 최적화는 다음을 포함한다:
- 컨택스트로부터 매개변수와 반환 타입을 추론
- 단일 표현식의 클로저인 경우 암묵적인 반환
- 약칭 인자명
- 트레일링 클로저 구문

## Closure Expressions
중첩함수는 큰 함수의 부분으로서 독립적인 코드 블록을 이름 짓고 정의하기위한 편리한 수단이다. 그러나 완전한 선언과 이름이 없는 짧은 버전의 함수같은 구성체를 작성하는 것이 유용할 때가 있다. 특히 함수나 메소드의 인자로 함수를 취하는 경우이다.

클로저 표현식은 인라인 클로저를 간결하고 집중된 구문으로 작성하는 방법이다. 클로저 표현식은 뚜렷함이나 의도를 잃지 않고 짧은 형태의 클로저를 작성하기 위한 몇몇의 구문 최적화를 제공한다. 아래 클로저 표현식의 예제는 동일한 기능을 하는 `sorted(by:)` 메소드 예제를 더 간결한 방법으로 여러차례 개선하며 구문 최적화를 설명한다.

### The Sorted Method

스위프트 표준 라이브러리는 `sorted(by:)` 메소드를 제공한다. 정렬 클로저의 출력 값에 따라 배열 값들을 정렬한다. 정렬이 끝나면 새로운 배열이 반환되며, 기존 배열을 이 메소드에 의해 변경되지 않는다.

아래 클로저 표현식 예제는 `sorted(by:)` 메소드를 사용하여 `String` 배열을 알파벳 역순으로 정렬한다. 정렬하기 위한 초기 배열을 다음과 같다:
```swift
let name = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
```
`sorted(by:)` 메소드는, 배열 요소 타입과 동일한 타입의 두 인자를 취하며, 정렬 후에 첫번째 값이 두번째 값 전/후에 나타나야하는지를 의미하는 값인  `Bool` 을 반환하는 클로저를 허용한다. 첫번째 값이 두번째 값보다 먼저 나타나야 한다면, `true` 를 반환해야 한다.

이 예제는 `String` 배열을 정렬하는 것이므로, 정렬 클로저는 `(String, String) -> Bool` 타입의 함수여야 한다. 

정렬 클로저를 제공하는 한가지 방법은 올바른 타입의 일반적인 함수를 작성하여 `sorted(by:)` 메소드 인자로 전달하는 것이다.

```swift
func backward(_ s1: String, _ s2: String) -> Bool {
	return s1 > s2											   
}
var reveresedNames = names.sorted(by: backward)
// reversedNames is equal to ["Ewa", "Daniella", "Chris", "Barry", "Alex"]
```

`s1` 이 `s2` 보다 크다면, `backward(_:_:)` 함수는 `true` 를 반환하며, 이는 정렬된 배열에서 `s1` 이 `s2` 보다 앞에 위치해야 한다는 것을 의미한다. 

그러나, 이는 단일 표현식 함수를 작성하는데 다소 숨이 차는 방식이다. 이번 예제에서는, 클로저 표현식 구문을 사용하여 정렬 클로저를 인라인으로 작성하는 더 나은 방법을 보여줄 것이다.

### Closure Expression Syntax

클로저 표현 구문은 다음의 일반적인 형태를 갖는다:

	{ (parameters) -> return type in
		statements
	}

클로저 표현 구문에서 *parameters*  는 in-out 매개변수가 될 수 있지만, 디폴트 값은 가질 수 없다. 가변 매개변수를 사용할 수 있고, 매개변수 타입과 반환 타입에 튜플을 사용할 수도 있다.

아래 예제는 클로져 표현식 버전의 `backward(_:_:)` 함수를 보여준다:

```swift
reversedNames = names.sorted(by: { (s1: String, s2: String) -> Bool in
	return s1 > s2
})
```

인라인 클로저의 매개변수와 반환 타입이 `backward(_:_:)` 함수의 그것들과 동일한 것이 주목하자. 두 경우 모두, `(s1: String, s2: String) -> Bool` 로 작성되었다. 그러나 인라인 클로저 표현식에서 중괄호 밖이 아닌 안에 그것들이 작성되었다.

클로저의 몸체는 `in` 키워드로 시작한다. 이 키워드는 클로저의 매개변수와 반환 타입의 정의가 끝났다는 것과 클로저 몸체가 시작됨을 나타낸다.


### Inferring Type From Context
정렬 클로저는 메소드의 인자로 전달되기 때문에, 스위프트는 매개변수와 반환 타입을 추론할 수 있다. 즉, `(String, String)` 과 `Bool` 타입은 클로저 표현식의 정의 일부에 작성되지 않아도 된다. 모든 타입이 추론가능하므로, 반환 화살표 (->) 와 매개변수 명 주위의 소괄호는 생략 가능하다. 

```swift
reversedNames = names.sorted(by: { s1, s2 in return s1 > s2 })
```

클로저를 인라인 클로저 표현식으로서 함수나 메소드에 전달할 때는 항상 매개변수와 반환 타입을 추론할 수 있다. 결과적으로, 함수나 메소드 인자로 사용되는 인라인 클로저는 완전한 형식으로 작성할 필요가 없다. 그럼에도 독자의 모호함을 없애기 위해 여전히 타입을 명시할 수 있다. 

### Implicit Returns from Single-Expression Closures
단일 표현식의 클로저는 다음처럼 선언부에서 `return` 키워드를 생략할 수 있다.
```swift
reversedNames = names.sorted(by: { s1, s2 in s1 > s2} )
```
`sorted(by:)` 메소드 인자의 함수 타입은 그 클로저에서 `Bool` 값이 반환되어야 함이 명확하다. 이 클로저의 본문은 `Bool` 값을 반환하는 단일 표현식을 포함하며, 모호함이 없으므로, `return` 키워드 생략이 가능하다.

### Shorthand Argument Names
스위프트는 인라인 클로저에 자동적으로 인자 명의 약칭을 제공하여, `$0, $1, $2` 등의 이름으로 클로저 인자의 값을 참조할 수 있다.

클로저 표현식에 이와 같은 인자명의 약칭을 사용하면, 그 정의부에서 클로저 인자 목록을 생략할 수 있다. 인자명 약칭의 타입은 기대되는 함수 타입으로부터 추론되며, 인자 약칭의 가장 높은 숫자가 해당 클로저가 취하는 인자의 수를 결정 짓는다. 클로저 표현식이 몸체 전체를 구성하기 때문에 `in`  키워드 또한 생략 가능하다.
```swift
reversedNames = names.sorted(by: { $0 > $1 } )
```
`$0` 과 `$1` 은 클로저의 첫번째와 두번째 `String` 인자를 참조한다. `$1` 은 가장 높은 숫자의 인자 약칭으로, 이 클로저는 두개의 인자를 취하는 것으로 이해된다. 여기서 `sorted(by:)` 함수는 인자가 문자열인 클로저를 기대하므로, 인자 약칭 `$0` 와 `$1` 은 모두 `String` 타입이다.

### Operator Methods
실은 위의 클로저 표현식보다도 짧은 방법이 있다. 스위프트의 `String` 타입은 문자열에서 두개의 `String` 타입의 파라미터를 갖고 `Bool` 을 반환하는 메소드로 이상 연산자 (>) 구현을 정의하고 있다. 이것은 `sorted(by:)` 메소드에 의해 필요한 메소드 타입과 정확히 일치한다. 그러므로 이상 연산자만을 전달해도 되며, 스위프트는 우리가 문자열 특유의 구현체를 사용하고 싶어한다고 이해할 것이다. 
```swift
reversedNames = names.sorted(by: >)
```


## Trailing Closures
클로저 표현식을 함수의 마지막 인자로 전달해야 하고, 그 클로저가 길다면, 후행 클로저를 작성하는 것이 유용할 수 있다. 후행 클로저가 그 함수의 인자일지라도, 함수 호출의 소괄호 뒤에 후행 클로저를 작성하면 된다. 후행 클로저 구문을 사용할 때, 함수 호출 부분에 첫번째 클로저를 위한 인자 레이블을 작성하지 않는다. 함수 호출은 여러개의 후행 클로저를 포함할 수 있다.

```swift
func someFunctionThatTakesAClosure(closure: () -> Void) {
	// 함수 몸체
}

// 후행 클로저를 사용하지 않고 호출
someFunctionThatTakesAClosure(closure: {
	// 클로저 몸체
})

// 후행 클로저 사용하여 호출
someFunctionThatTakesAClosure() {
	// 후행 클로저 몸체
}
```

위 Closure Expression Syntax 섹션에서 문자열 정렬 클로저는 `sorted(by:)` 메소드의 소괄호 밖에 작성할 수 있다:

```swift
reversedNames = names.sorted() { $0 > $1 }
```

만약 클로저 표현식이 함수나 메소드의 인자로만 제공되고, 이를 후행 클로저로 제공한다면, 소괄호 쌍을 생략할 수 있다:

```Swift
reversedNames = names.sorted { $0 > $1 }
```

후행 클로저는 클로저가 충분히 길어 인라인에 한줄로 표현할 수 없는 경우에 가장 유용하다. 예를 들어, 스위프트의 `Array` 타입은 하나의 인자로 클로저 표현식을 취하는  `map(_:)` 메소드를 가지고 있다. 그 클로저는 배열에 있는 각각의 항목을 위해 한번씩 호출되며, 대응되는 값을 반환한다. 

```swift
let digitNames = [
	0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four",
	5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"
]
let numbers = [16, 58, 510]

let strings = numbers.map { (number) -> String in
	var number = number
	var output = ""
	repeat {
		output = digitNames[number % 10]! + output
		number /= 10
	} while number > 0
	return output
}
// strings is inferred to be of type [String]
// its value is ["OneSix", "FiveEight", "FiveOneZero"]
```

입력 파라미터 `number` 의 타입은 매핑될 배열의 값들로 추론할 수 있기 때문에 작성할 필요는 없다.

이 예제에서 변수 `number` 는 클로저의 몸체에서 수정될 수 있도록, 클로저의 `number` 파라미터의 값으로 초기화된다. (함수와 클로저의 파라미터는 항상 상수이다.)

만약, 함수가 여러개의 클로저를 취하면, 첫번째 후행 클로저의 인자 레이블은 생략하고, 나머지 후행 클로저들은 명시하면 된다. 예를 들어, 아래 함수는 사진갤러리의 그림을 로드한다.

```swift
func loadPicture(from server: Server, completion: (Picture) -> Void, onFailure: () -> Void) {
	if let picture = download("photo.jpg", from: server) {
		completion(picture)
	} else {
		onFailure()
	}
}
```

그림을 로드하기 위해 함수를 호출하면, 두개의 클로저를 제공하게 된다. 첫번째는 성공적으로 다운로드될 때 그림을 보여주는 완수 처리기이고, 두번째는 에러를 사용자에게 보여주는 에러 처리기이다.

```swift
loadPicture(from: someServer) { picture in
	someView.currentPicture = picture
} onFailure: {
	print("Couldn't download the next picture.")
}
```

이 예제에서, `loadPicture(from:completion:onFailure:)` 는 네트워크 작업을 백그라운드로 보내고, 작업이 끝날 때 두 클로저 중에 하나를 호출한다. 두가지 상황을 처리하기 위해 단지 하나의 클로저를 사용하는 대신에, 이런 방식으로 함수를 작성하는 것은 코드를 깔끔하게 분리할 수 있도록 해준다.

> NOTE
> 
> 완수 처리기는 여러 중첩 처리기를 사용해야 하는 상황에서 읽기 어려워질 수 있다. 이에 대안으로, 비동기 코드를 사용할 수 있다.

## Capturing Values
클로저는 컨텍스트에 정의된 상수와 변수를 붙잡아둘 수 있다. 그리고 그것들을 정의하는 스콥이 더이상 존재하지 않더라도, 몸체 내부에서 그것을 참조하고 수정할 수 있다. 

스위프트에서 값을 붙잡을 수 있는 가장 단순한 형태의 클로저는 다른 함수의 몸체 내에 작성된 중첩 함수이다. 중첩함수는 외부 함수의 인자들을 붙잡을 수 있고, 외부 함수에 정의된 상수와 변수를 붙잡을 수 있다.
 
 `incrementer` 라는 중첩함수를 포함하는 `makeIncrementer` 라는 함수의 예제가 있다. `incrementer()` 중첩 함수는 주위의 컨텍스트로부터 `runningTotal` 과 `amount` 를 붙잡고 있다. 이 값들을 붙잡은 다음에 `incrementer` 는 `runningTotal` 을 `amount` 만큼 증가하는 클로저로서 `makeIncrementer` 에 의해 반환된다.

```swift
func makeIncrementer(forIncrement amount: Int) -> () -> Int {
	var runningToatal = 0
	func incrementer() -> Int {
		runningToatl += amount
		return runningTotal
	}
	return incrementer
}
```

`makeIncrementer(forIncrement:)` 의 반환 타입은 `() -> Int` 이다. 즉, 단순한 값이 아닌, 함수를 반환한다는 의미이다. 이 함수는 파라미터가 없고, `Int` 값을 반환한다. 

`incrementer()` 함수는 파라미터가 없지만, 함수 몸체에서 `runningTotal` 과 `amount` 를 참조한다. 이들의 참조를 붙잡고 있기 때문에, `makeIncrementer` 의 호출이 끝나도 사라지지 않고 `incrementer` 함수가 호출되는 다음 시점에도 접근 가능하다.

> NOTE
> 
> 최적화로서 스위프트는 값이 클로저에 의해 변경되지 않는다면, 값을 복사하여 붙잡고 저장한다.
> 또한, 스위프트는 더이상 사용되지 않을 때 변수를 처리하는 메모리 관리를 한다.

> NOTE
> 
> 만약 클래스 인스턴스의 속성에 클로저를 할당하고, 그 클로저가 인스턴스를 붙잡고 있으면, 클로저와 인스턴스 사이에 강한 참조 사이클이 형성된다. 그 강한 참조 사이클을 깨기 위해 스위프트는 캡쳐 목록을 사용한다. 

## Closures Are Reference Types
위 예제에서 `incrementBySeven` 과 `incrementByTen` 은 상수지만, 이것이 참조하는 클로저는 그것이 붙잡고 있는 `runningTotal` 을 증가시킬 수 있다. 이것은 함수와 클로저가 참조타입이기 때문이다.

만약에 클로저를 두개의 다른 상수나 변수에 할당하면, 두개는 같은 클로저를 참조하는 것이다. 
```swift
let alsoIncrementByTen = incrementByTen
alsoIncrementByTen() // 50
incrementByTen() // 60
```

## Escaping Closures
클로저가 함수의 인자로 전달되어 함수 반환 이후에 호출된다면, 클로저가 함수를 벗어났다고 말한다. 함수를 정의하고 파라미터 중 하나로 클로저를 취한다면, 그 클로저가 벗어날 수 있음을 나타내기 위해 파라미터 타입 앞에 `@escaping` 를 작성할 수 있다.

클로저가 벗어날 수 있는 한가지 방법은 함수 외부에 정의된 변수에 저장되는 것이다. 예를 들어, 비동기 작업이 시작되는 함수는 완수 처리기로 클로저 인자를 취한다. 그 함수는 작업이 시작된 후에 반환되지만, 클로저는 작업이 완료되어야 호출된다. 이때 클로저는 나중에 호출될 수 있도록 벗어날 수 있어야 한다. 예를 들어:

```swift
var completionHandlers: [() -> Void] = []
func someFunctionWithEscapingClosure(_ completionHandler: @escaping () -> Void) {
	completionHandlers.append(completionHanlder)
}
```

`someFunctionWithEscapingClosure(_:)` 함수는 인자로 클로저를 취하며 외부에 선언된 배열에 이를 추가한다. 만약 이 함수의 파라미터에 `@escaping` 를 표시하지 않는다면, 컴파일 에러가 발생한다.

만약 탈출 클로저가 `self` 를 참조하고 그것이 클래스의 인스턴스라면 특별한 주의가 필요하다. 탈출 클로저에 `self` 를 붙잡는것은 의도치 않게 강한 참조 사이클을 형성할 수 있기 때문이다. 

일반적으로, 클로저는 그 몸체에 변수를 사용하므로써 암묵적으로 붙잡게 되지만, 이 경우에 명시적으로 할 필요가 있다. 만약 `self` 붙잡고 싶다면, 사용할 때 `self` 를 작성하거나, 클로저의 캡처 목록에 포함시키자. 명시화하는 것은 의도를 명확하게 하는 것이고, 참조 사이클이 없다는 것을 확실시 할 수 있다. 예를 들어, 아래 코드에서 `someFunctionWithEscapingClosure(_:)` 로 전달된 클로저는 `self`를 명시적으로 참조한다. 반대로 `someFunctionWithNoneescapingClosure(_:)` 로의 클로저는 비탈출 클로저이며, 즉 `self` 를 암묵적으로 참조할 수 있다.

```swift
func someFunctionWithNoneescapingClosure(closure: () -> Void) {
	closure()
}

class SomeClass {
	var x = 10
	func doSomething() {
		someFunctionWithEscapingClosure { self.x = 100 }
		someFunctionWithNonescapingClosure { x = 200 }
	}
}

let instance = SomeClass()
instance.doSomething()
print(instance.x) // 200

completionHandlers.first?()
print(instance.x) // 100
```

다음은 클로저의 캡처 목록에 `self` 를 포함하여 붙잡아 암묵적으로 참조하는 `doSomething()` 버전을 보여준다.

```Swift
class SomeOtherClass {
	var x = 10
	func doSomething() {
		someFunctionWithEscapingClosure { [self] in x = 100}
		someFunctionWithNonescapingClosure { x = 200 }
	}
}
```

만약 `self` 가 구조체나 열겨형의 인스턴스라면, 항상 `self` 를 암묵적으로 참조할 수 있다. 하지만, 탈출 클로저는 `self` 가 값 타입의 인스턴스인 경우 변형 가능한 참조로서 `self` 를 붙잡을 수 없다. 구조체나 열거형은 공유되는 변형을 허락하지 않는다.

```swift
struct SomeStruct {
	var x = 10
	mutating func doSomething() {
		someFunctionWithNonescapingClosure { x = 200 }// Ok
		someFunctionWithEscapingClosure { x = 100 } // Error
	}
}
```

`someFunctionWithEscapingClosure` 함수 호출은 에러가 발생하며, 변형가능한 메소드 내부에 있어 `self` 가 변형가능하기 때문이다. 이것은 탈출 클로저는 구조체의 변형 가능한 참조를 붙잡을 수 없다는 규칙을 위반한다.

## Autoclosures

자동클로저는 함수에 인자로 전달되는 표현식을 감싸기위해 자동적으로 생성되는 클로저를 말한다. 어떠한 인자도 취하지 않고, 호출될 때 내부에 감싸진 표현식의 값을 반환한다. 구문적 편의성은 명시적인 클로저 대신에 일반적인 표현식을 작성함으로써 함수의 파라미터 주위에 괄호를 생략할 수 있게 해준다.

자동클로저를 취하는 함수를 호출하는 것은 흔하지만, 이런 함수를 구현하는 것은 그렇지 않다. 예를 들어, `assert(condition:message:file:line:)` 함수는 `condition` 과 `message` 파라미터가 자동클로저이다.

```swift
var customersInLine = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
print(customersInLine.count) // 5

let customerProvider = { customersInLine.remove(at: 0) }
print(customersInLine.count) // 5

print("Now serving \(customerProvider())!") // Now serving Chris!
print(customersInLine.count) // 4
```

클로저 내부의 코드로 `customersInLine` 배열의 첫번째 요소가 제거되더라도, 클로저가 호출되기 전에는 제거된 것이 아니다. 만약 클로저가 절대 호출되지 않는다면, 클로저 내부의 표현식은 평가되지 않고, 배열의 요소는 제거되지 않게된다. `customerProvider` 의 타입은 `String` 이 아닌 `() -> String` 임에 주의하자.

함수의 인자로 클로저를 전달할 때에도 평가를 지연시키는 행동을 볼 수 있다.

```Swift
func serve(customer customerProvider: () -> String) {
	print("Now serving \(customerProvider())!")
}
serve(customer: { customerInLine.remove(at: 0) } ) // Now serving Alex!
```

`serve(customer:)` 함수는 고객 명을 반환하는 명시적인 클로저를 취한다. 아래의 `serve(customer:)` 는 동일한 작업을 수행하지만 명시적인 클로저 대신에 `@autoclosure` 속성을 파라미터 타입에 표시하여 자동 클로저를 취한다. 때문에 그 인자는 자동적으로 클로저로 전환된다.

```swift
func serve(customer customerProvider: @autoclosure () -> String) {
	print("Now serving \(customerProvider())!")
}

serve(customer: customersInLine.remove(at: 0)) // Now serving Ewa!
```

> NOTE
> 
> 자동 클로저를 남용하면 코드는 이해하기 어려워진다. 문맥과 함수 이름은 평가가 연기될 수 있다는 것을 분명히 해야 한다.

만약 탈출 가능한 자동클로저를 원한다면, `@autoclosure` 과 `@escaping` 속성을 사용하자. 
```swift
var customerProvider: [() -> String] = []
func collectCustomerProviders(_ customerProvider: @autoclosure @escaping () -> String) {
	customerProviders.append(customerProvider)
}
collectCustomerProviders(customersInLine.remove(at: 0))
collectCustomerProviders(customerInLine.remove(at: 0))

print("Collected \(customerProviders.count) closures.") // Collected 2 closures.
for customerProvider in customerProviders {
	print("Now serving \(customerProvider())!")
}
// Now serving Barry!
// Now serving Daniella!
```
