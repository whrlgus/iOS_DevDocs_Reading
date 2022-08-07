## Declaration Attributes

### propertyWrapper

Class, structure, enumeration 선언부에 이 attribute을 적용하여 그 타입을 property wrapper로 사용할 수 있다. 타입에 이 attribute을 적용하면, 그 타입과 같은 이름의 커스텀 attribute이 생성되는 것이다. 이 attribute을 class, structure, enumeration의 property에 적용하여 wrapper type의 인스턴스로 그 속성으로의 접근을 감쌀 수 있다; 동일한 방식으로 local stored variable 선언부에 적용하여 그 변수로의 접근을 감쌀 수 있다. 연산 변수, 전역 변수, 상수에는 property wrapper를 사용할 수 없다.

이 wrapper는 `wrappedValue` 라는 인스턴스 프로퍼티를 반드시 정의해야 한다. property의 *wrapped value* 는 이 property의 getter 와 setter가 노출하는 값이다. 대부분의 경우에, `wrappedValue` 는 computed value이지만, stored value일 수도 있다. wrapper는 감싸진 값에 의해 필요한 저장소를 정의하고 관리한다. 컴파일러는 wrapped property의 이름에 underscore(_) 를 prefix로 하여 wrapper 타입의 인스턴스 저장소를 통합한다 - 예를 들어, `someProperty` 는 `_someProperty` 로 저장된다. 통합된 저장소는 접근 제어 레벨이 `private` 이다. 

property wrapper로 사용되는 property는 `willSet` 과 `didSet` 블락을 포함할 수 있지만, `get`, `set` 블락은 override할 수 없다.

Swift는 property wrapper의 초기화를 위한 두가지 형태의 syntactic sugar를 제공한다. 값을 할당하는 assignment syntax를 사용하여 property wrapper의 생성자 파라미터인 `wrappedValue`의 인자로 전달할 수 있다. 또한, attribute를 property에 적용할 때 attribute에 인자를 제공할 수 있고, 그 인자들은 property wrapper의 생성자에 전달된다.  



projected value는 추가적인 기능을 노출하기 위해 사용할 수 있는 두번째 값이다. 

property wrapper로부터 값을 투영하기 위해, `projectedValue`  인스턴스 프로퍼티를 wrapper type에 정의해야 한다. 컴파일러는 이 값을 위한 식별자를 dollar sign($) 을 이름의 서두에 위치시켜서 통합할 것이다. 이 `projectedValue`의 접근 제어 레벨은 기존 프로퍼티와 동일하다. 

# Properties

## Property Wrappers

property wrapper는 property를 정의하는 부분과 property가 어떻게 저장되는지 관리하는 부분 사이를 분리하는 레이어이다. 예를 들어, property의 thread-safety 확인을 해야하거나 그 값을 데이터베이스에 저장해야 한다면, 관련된 코드를 모든 프로퍼티에 작성해야 한다. property wrapper를 사용하면, wrapper를 정의할 때 관리하기 위한 코드를 한번만 적고, 여러개의 프로퍼티에 적용하여 재활용할 수 있는 장점이 있다.

property wrapper를 정의하기 위해, 타입(structure, enumeration, class)에 `wrappedValue` 프로퍼티를 정의해야 한다. 아래 코드에서, `TwelveOrLess` 구조체는 감싸고 있는 값이 항상 12 이하임을 보장한다. 

```swift
@propertyWrapper
struct TwelveOrLess {
    private var number = 0
    var wrappedValue: Int {
        get { return number }
        set { number = min(newValue, 12) }
    }
}
```



wrapper를 property적용하기 위해서 wrapper의 이름으로 된 attribute를 property에 부여하게 된다. 아래 예제는 `TwelveOrLess` property wrapper를 사용하여 사각형을 저장하는 구조체가 그 치수를 12 이하로 보장하는 코드이다.

```swift
struct SmallRectangle {
    @TwelveOrLess var height: Int
    @TwelveOrLess var width: Int
}

var rectangle = SmallRectangle()
print(rectangle.height)
// Prints "0"

rectangle.height = 10
print(rectangle.height)
// Prints "10"

rectangle.height = 24
print(rectangle.height)
// Prints "12"
```



wrapper를 property에 적용할 때, 컴파일러는 wrapper의 저장소를 제공하는 코드와 그 wrapper를 통한 property의 접근 코드를 통합한다. Attribute syntax를 이용하지 않고 Property wrapper의 동작을 사용하는 코드를 작성할 수도 있다. 예를 들어, 아래와 같이 `@TwelveOrLess` 를 attribute로 사용하는 대신에 아래와 같이 사용할 수도 있다.

```swift
struct SmallRectangle {
    private var _height = TwelveOrLess()
    private var _width = TwelveOrLess()
    var height: Int {
        get { return _height.wrappedValue }
        set { _height.wrappedValue = newValue }
    }
    var width: Int {
        get { return _width.wrappedValue }
        set { _width.wrappedValue = newValue }
    }
}
```

`_height`와 `_width` property에 property wrapper 인스턴스를 저장하고, `height`와 `width`의 getter 와 setter로 `wrappedValue` property로의 접근을 감싼다.

### Setting Initial Values for Wrapped Properties

위 예제에서는 `TwelveOrLess` 선언부에서 `number` 에 초기값을 할당하여 감싸진 property의 초기값을 설정하였다. 이 property wrapper를 사용하는 코드는 `TwelveOrLess` 에 의해 감싸진 property를 위한 다른 초기값을 설정할 수가 없다 - 예를 들어, `SmallRectangle` 의 정의는 `height` 와 `width` 에 초기값을 할당할 수 없다. 초기값 할당 혹은 다른 커스텀 구현을 지원하기위해서, property wrapper에 생성자를 구현해야 한다. 아래는 `SmallNumber` 라는 이름의 `TwelveOrLess` 확장판이다. 

```swift
@propertyWrapper
struct SmallNumber {
    private var maximum: Int
    private var number: Int

    var wrappedValue: Int {
        get { return number }
        set { number = min(newValue, maximum) }
    }

    init() {
        maximum = 12
        number = 0
    }
    init(wrappedValue: Int) {
        maximum = 12
        number = min(wrappedValue, maximum)
    }
    init(wrappedValue: Int, maximum: Int) {
        self.maximum = maximum
        number = min(wrappedValue, maximum)
    }
}
```

wrapper를 property에 적용하고 초기값을 지정하지 않으면, Swift는 wrapper를 구성하기 위해서 `init()` 생성자를 사용한다.

```swift
struct ZeroRectangle {
    @SmallNumber var height: Int
    @SmallNumber var width: Int
}

var zeroRectangle = ZeroRectangle()
print(zeroRectangle.height, zeroRectangle.width)
// Prints "0 0"
```

`height` 와 `width` 를 감싸는 `SmallNumber` 의 인스턴스는 `SmallNumber()` 의 호출로 생성된다. 

property에 초기 값을 지정할 때, Swift는 `init(wrappedValue:)` 생성자를 사용한다. 

```swift
struct UnitRectangle {
    @SmallNumber var height: Int = 1
    @SmallNumber var width: Int = 1
}

var unitRectangle = UnitRectangle()
print(unitRectangle.height, unitRectangle.width)
// Prints "1 1"
```



커스텀 attribute 다음 괄호안에 인자들을 적으면, Swift는 wrapper를 구성하기 위해 적힌 인자들을 허용하는 생성자를 호출한다. 

```swift
struct NarrowRectangle {
    @SmallNumber(wrappedValue: 2, maximum: 5) var height: Int
    @SmallNumber(wrappedValue: 3, maximum: 4) var width: Int
}

var narrowRectangle = NarrowRectangle()
print(narrowRectangle.height, narrowRectangle.width)
// Prints "2 3"

narrowRectangle.height = 100
narrowRectangle.width = 100
print(narrowRectangle.height, narrowRectangle.width)
// Prints "5 4"
```

property wrapper에 인자를 포함하므로써, wrapper의 초기 상태를 구성할 수 있다. Property wrapper를 사용하는 가장 일반적인 syntax이다. 

property wrapper에 인자를 포함하고 초기값 할당을 할 수도 있다. Swift는 이 할당을 wrappedValue 인자로 다루며, 알맞은 생성자를 호출하게 된다.

```swift
struct MixedRectangle {
    @SmallNumber var height: Int = 1
    @SmallNumber(maximum: 9) var width: Int = 2
}

var mixedRectangle = MixedRectangle()
print(mixedRectangle.height)
// Prints "1"

mixedRectangle.height = 20
print(mixedRectangle.height)
// Prints "12"
```

### 

### Projecting a Value From a Property Wrapper

wrapped value에 더해, property wrapper는 projected value를 정의하여 추가적인 기능을 제공할 수 있다 - 예를 들어, 데이터베이스로의 접근을 관리하는 property wrapper는 `flushDatabaseConnection()` 메소드를 projected value로 표현할 수 있다. projected value는 달러 기호($)로 시작한다는 점이 wrapped value와 다르다. 

```swift
@propertyWrapper
struct SmallNumber {
    private var number: Int
    private(set) var projectedValue: Bool

    var wrappedValue: Int {
        get { return number }
        set {
            if newValue > 12 {
                number = 12
                projectedValue = true
            } else {
                number = newValue
                projectedValue = false
            }
        }
    }

    init() {
        self.number = 0
        self.projectedValue = false
    }
}
struct SomeStructure {
    @SmallNumber var someNumber: Int
}
var someStructure = SomeStructure()

someStructure.someNumber = 4
print(someStructure.$someNumber)
// Prints "false"

someStructure.someNumber = 55
print(someStructure.$someNumber)
// Prints "true"
```

`someStructure.$someNumber` 는 wrapper의 projected value로 접근한다. 

property wrapper는 projected value를 이용하여 어떠한 타입이라도 반환할 수 있다.

타입의 일부인 코드에서 projected value에 접근할 때, getter 나 인스턴스 method 처럼, `self.`를 생략할 수 있다. 







## Property Wrapper

- Property Wrapper는 코드 재사용성을 높이기 위한 방안으로 설계되었다. 
- property 구현상 반복적인 접근 패턴으로 코드가 작성될 수 있다. wrapper에 패턴에 해당하는 코드를 구현하고 이를 property에 적용하면, 이러한 반복적인 패턴을 줄일 수 있다.

### 예제

- WWDC 19, UserDefaults
- docs.swift.org
  - @propertyWrapper 라는 attribute를 타입에 적용하여 custom attribute를 정의할 수 있다.
  - wrappedValue 라는 이름의 property는 반드시 정의해야 한다. 
    - Stored/computed property 다 가능하다.
  - attribute syntax를 사용하지 않고도 wrapper 특성을 지니게 할 수 있다.
  - property wrapper가 적용된 property는 `willSet` `didSet` 블락을 사용할 수 있지만, `get` `set` 블락은 사용할 수 없다.

### 초기화

초기화하기 위한 두 가지 형태의 syntax를 제공한다.

- assignment syntax
- attribute 적용부에 argument 전달

### Projected value

추가적인 기능을 제공하기 위한 목적으로 사용된다. 

- 특정 의미가 아니기에, use case에 따라 다른 의미로 정의할 수 있다.
- SwiftUI에서는 binding api 사용시에 활용되며 projectedValue 에 PropertyWrapper instance 자체를 저장하고 있다.

### Use Cases

- Clamping
- Trimmed



