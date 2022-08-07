# Declaration

## Function Declaration

### Methods with Special Names

특별한 이름을 갖는 몇몇 method들은 함수 호출 syntax가 편리하게 구성되어 있다(syntactic sugar). 만약 한 타입이 이러한 method들을 정의하고 있다면, 그 타입의 인스턴스로 함수 호출에 사용될 수 있다. 이런 함수 호출은 그 인스턴스에 특별한 이름으로 정의된 메소드 호출로 이해할 수 있다.

class, structure, enumeration 타입은 `@dynamicCallable` 속성을 적용하거나, call-as-function method를 정의하여 함수 호출 syntax를 지원한다. 만약, call-as-function method를 정의하고 `@dynamicCallable` 속성을 적용하면, 컴파일러는 call-as-function을 우선시 한다.

Call-as-function method의 이름은 `callAsFunction()` 이거나, `callAsFunction(_:_:)` 과 `callAsFunction(something:)` 같이 레이블이 있거나 없는 인자를 추가한 method 명이 될 수도 있다.

```swift
struct CallableStruct {
    var value: Int
    func callAsFunction(_ number: Int, scale: Int) {
        print(scale * (number + value))
    }
}
let callable = CallableStruct(value: 100)
callable(4, scale: 2)
callable.callAsFunction(4, scale: 2)
// Both function calls print 208.
```

Call-as-function method들과 `@dynamicCallable`  속성의 method들은, 타입 시스템에 제공하는 정보의 양과 런타입에 얼마나 많은 동적 동작이 가능할 지 사이에서 서로 다른 절충이 이뤄진다. call-as-function method를 선언할 때, 인자들의 개수, 타입과 레이블을 명시한다. `@dynamicCallable` 속성의 method들은 인자들의 배열을 담고있을 타입만 명시한다.

이 두가지 유형의 타입은 그 인스턴스를 함수 호출을 지나 완전한 함수로 여기며 사용할 수는 없다. 예를 들어:

```swift
let someFunction1: (Int, Int) -> Void = callable(_:scale:)  // Error
let someFunction2: (Int, Int) -> Void = callable.callAsFunction(_:scale:)
```

`@dynamicMemberLookup` 속성을 갖는 타입에서 `subscript(dynamicMember:)` subscript는 멤버 색인을 위한 편리한 문법을 제공한다. 

# Attributes

## Declaration Attributes

### dynamicCallable

Class, structure, enumeration, protocol 에 적용하면 각 타입의 인스턴스를 호출가능한 함수로 다룰 수 있게된다. 이 타입은 `dynamicallyCall(withArguments:)` method나 `dynamicallyCall(withKeywordArguments:)` method, 혹은 두가지 모두를 구현해야 한다. 

동적으로 호출가능한 타입(dynamically callable type)의 인스턴스는 마치 여러개의 인자를 받는 함수를 호출하는 것처럼 호출할 수 있다.

```swift
@dynamicCallable
struct TelephoneExchange {
    func dynamicallyCall(withArguments phoneNumber: [Int]) {
        if phoneNumber == [4, 1, 1] {
            print("Get Swift help on forums.swift.org")
        } else {
            print("Unrecognized number")
        }
    }
}

let dial = TelephoneExchange()

// Use a dynamic method call.
dial(4, 1, 1)
// Prints "Get Swift help on forums.swift.org"

dial(8, 6, 7, 5, 3, 0, 9)
// Prints "Unrecognized number"

// Call the underlying method directly.
dial.dynamicallyCall(withArguments: [4, 1, 1])
```

`dynamicallyCall(withArguments:)` method는 `[Int]` 와 같은 `ExpressibleByArrayLiteral` 프로토콜을 채택하는 매개 변수 하나만 가질 수 있다. 반환 타입은 어떤 것이든 가능하다.

`dynamicallyCall(withKeywordArguments:)` method를 구현하면 동적 method 호출에 label을 추가할 수 있다.

```swift
@dynamicCallable
struct Repeater {
    func dynamicallyCall(withKeywordArguments pairs: KeyValuePairs<String, Int>) -> String {
        return pairs
            .map { label, count in
                repeatElement(label, count: count).joined(separator: " ")
            }
            .joined(separator: "\n")
    }
}

let repeatLabels = Repeater()
print(repeatLabels(a: 1, b: 2, c: 3, b: 2, a: 1))
// a
// b b
// c c c
// b b
// a
```

`dynamicallyCall(withKeywordArguments:)` method의 선언은 `ExpressibleDictionaryLiteral` 프로토콜을 채탁하는 매개 변수 하나만 가질 수 있고, 반환 타입은 어떤 것이든 상관없다. 매개 변수의 `Key` 는 `ExpressibleByStringLiteral` 이어야 한다. 위 예제의 매개 변수 타입은 `KeyValuePairs` 이기 때문에 호출자는 중복 매개 변수 레이블을 가질 수 있다.

만약 두 `dynamicallyCall` method를 구현하면, method 호출에 키워드 인자들이 포함될 때 `dynamicallyCall(withKeywordArguments:)` 이 불린다. 그 이외의 경우는 `dynamicallyCall(withArguments:)` 가 불린다.

동적으로 호출가능한 인스턴스는 `dynamicallyCall` method 구현의 인자와 반환 타입이 일치해야 호출가능하다. 아래 예제는 컴파일 에러를 발생시키는데, `KeyValuePairs<String, String>` 을 인자로 하는 `dynamicallyCall(withArguments:)` 구현이 존재하지 않기 때문이다.

```swift
repeatLabels(a: "four") // Error
```



### dynamicMemberLookup

Class, structure, enumeration, protocol에 이 속성을 적용하면 런타임에 멤버들을 찾을 수 있게 해준다. 이 타입은 `subscript(dynamicMember:)` subscript를 구현해야 한다.

명시적 멤버 표현에서, 만약 이름있는 멤버에 해당하는 선언이 없다면, 그 표현은 그 타입의 `subscript(dynamicMember:)` subscript(멤버 정보를 인자로 전달하는) 호출로 이해하면 된다. 이 subscript는 key path 혹은 member name의 매개 변수를 사용한다; 만약 두가지 모두 구현한다면, key path 인자가 사용되는 subscript를 우선시 한다.

`subscript(dynamicMember:)` 의 구현은 `KeyPath`, `WritableKeyPath`, `ReferenceWritableKeyPath` 타입의 인자를 사용할 수 있다. 또는 `ExpressibleByStringLiteral` protocol을 채택하는 인자 타입을 사용할 수 있다.  subscript의 반환 타입은 어떤 것이든 상관없다.

멤버 이름에 의한 동적 멤버 색인은 컴파일 타임에 타입 검사를 할 수 없는 경우에 활용될 수 있다. 예를 들어, data를 다른 언어에서 Swift로 연결할 때이다:

```swift
@dynamicMemberLookup
struct DynamicStruct {
    let dictionary = ["someDynamicMember": 325,
                      "someOtherMember": 787]
    subscript(dynamicMember member: String) -> Int {
        return dictionary[member] ?? 1054
    }
}
let s = DynamicStruct()

// Use dynamic member lookup.
let dynamic = s.someDynamicMember
print(dynamic)
// Prints "325"

// Call the underlying subscript directly.
let equivalent = s[dynamicMember: "someDynamicMember"]
print(dynamic == equivalent)
// Prints "true"
```

key path에 의한 동적 맴버 색인은 컴파일 타임에 검사가 가능한 방법의 wrapper type 구현에 사용될 수도 있다.

```swift
struct Point { var x, y: Int }

@dynamicMemberLookup
struct PassthroughWrapper<Value> {
    var value: Value
    subscript<T>(dynamicMember member: KeyPath<Value, T>) -> T {
        get { return value[keyPath: member] }
    }
}

let point = Point(x: 381, y: 431)
let wrapper = PassthroughWrapper(value: point)
print(wrapper.x)
```

