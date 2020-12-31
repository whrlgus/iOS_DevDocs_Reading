# Structures and Classes

structure와 class(이하 SC)는 프로그램 코드의 building block을 형성한다. property와 method로 SC에 기능을 추가하게 된다. 이때 constant, variable, function을 정의하는데 사용하는 syntax는 동일하다.

custom SC를 생성할 때, 다른 프로그래밍 언어와 다르게 swift는 interface와 implementation 파일을 분리하여 생성할 필요가 없다. swift에서는 SC를 단일 파일에 정의하면 해당 SC에 대한 외부 interface는 자동으로 사용이 가능하다.



## Comparing Structures and Classes

swift에서 SC는 공통적인 부분이 여럿 존재하며, SC는 다음과 같은 것을 할 수 있다.

- 값을 저장하기 위한 **property**를 정의
- 기능을 제공하기 위한 **method**를 정의
- Subscript syntax를 사용하여 그 값에 접근 가능하게 하는 **subscript**를 정의
- 초기 상태를 구성하기 위한 **initializer**를 정의
- defult implementation 이외에 **extension**으로 기능을 확장
- 특정 유형의 표중 기능을 제공하기 위해 **protocol**을 준수

class의 추가적인 capability(능력) 은 다음과 같다.

- inheritance는 하나의 class가 다른 class의 특징을 상속할 수 있게(물려 받을 수 있게) 해준다.
- type casting은 runtime에 class instance의 type을 검사하고 해석할 수 있게 해준다.
- deinitializer에서 class instance가 내부에 할당된 자원을 해제할 수 있다.
- 하나 이상의 class instance에 대한 reference counting을 할 수 있다.

class의 추가적인 능력은 복잡도가 증가한다는 단점이 있다. 일반적인 가이드라인은, 쉽게 그 구조를 추론하기 쉬운 struct를 사용하는 것이고, 필요성 혹은 합당한 이유가 있을 때 class를 사용하는 것이다. 대부분의 custom data type은 structure나 enumeration으로 정의하는 것이 좋다. 

### Definition Syntax

SC는 비슷한 정의 syntax를 갖는다. 각각 `struct` 나 `class` 키워드로 시작을 하며, 전체 정의 부분은 괄호 쌍안에 위치한다.

```swift
struct SomeStructure {

}
class SomeClass {

}
```

> SC의 type 이름은 UpperCamelCase 로 작성하여 표준 swift type(String, Int, and Bool)과 capitalization을 일치하는 것이 좋다. property나 method의 이름은 lowerCamelCase로 작성하여 type 이름과 구별하는 것이 좋다.

다음은 struct와 class의 정의부이다.

```swift
struct Resolution {
    var width = 0
    var height = 0
}
class VideoMode {
    var resolution = Resolution()
    var interlaced = false
    var frameRate = 0.0
    var name: String?
}
```

`Resolution` structure는 두개의 stored property로 구성되어 있다. stored property는 constant나 variable이며, SC 내부에서 값을 저장하고 있다. 초기화 값을 통해 property의 type을 추론할 수 있다. 예제에서는 0으로 초기화 하였기 때문에, type은 `Int` 가 된다.

`VideoMode` class는 4개의 variable stored property로 구성돼 있다. `name` 은 optional String 타입으로 default 값은 `nil` 이다.

### Structure and Class Instances

위 SC의 정의부는 단순히 어떻게 구성돼 있는지를 표현한 것이고, 구체적인 대상을 표현하기 위해서는 instance를 생성해야 한다. 

```swift
let someResolution = Resolution()
let someVideoMode = VideoMode()
```

둘은 유사한 syntax의 initializer를 사용해서 새로운 instance를 생성한다. 가장 단순한 형태의 initializer로서, type 이름 뒤에 빈 소괄호(parenthesis) 쌍이  붙는다. 그러면 둘의 instance는 default 값으로 초기화된다. 

### Accessing Properties

instance의 property에 접근하기 위해서 dot syntax를 사용하여, 값을 읽고 쓸 수 있다.

```swift
print("\(someResolution.width)")
print(someVideoMode.resolution.width)
someVideoMode.resolution.width = 1280
```

### Memberwise Initializers for Structure Types

structure는 자동적으로 memberwise initializer를 생성한다.

```swift
let vga = Resolution(width: 640, height: 480)
```



## Structures and Enumerations Are Value Types

value type은 variable 이나 constant에 할당될 때, 혹은 function으로 전달될 때 값이 복사된다. 

swift의 기본 type인 integers, floating-point numbers, booleans, strings, arrays 그리고 dictionaries는 모두 value type이며, struct로 구현돼 있다.

> Array, dictionary, string과 같은 표준 library에 정의된 collection은 값을 복사하는데 드는 비용을 줄이기 위한 최적화 방식을 사용한다. collection은 바로 복사하지 않고, 원본 instance와 복사본 사이에 elements 가 저장된 메모리 공간을 공유한다. 만약, 복사본이 변경된다면, 변경되기 이전에 elements를 모두 복사한다. 이는 마치 복사가 즉시 이뤄지는 것처럼 느끼게 한다.



다음 예제를 보자. 

```swift
let hd = Resolution(width: 1920, height: 1080)
var cinema = hd
```

`hd` instance의 값을 `cinema` 로 복사하는 코드이다. 두 개의 독립적인 instance가 생성되었기 때문에, `cinema`의 property를 변경하는 행위는 `hd`에 아무런 영향을 주지 않는다.

 enumeration에서도 동일한 행동이 이뤄진다.

```swift
enum CompassPoint {
    case north, south, east, west
    mutating func turnNorth() {
        self = .north
    }
}
var currentDirection = CompassPoint.west
let rememberedDirection = currentDirection
currentDirection.turnNorth()

print("The current direction is \(currentDirection)")
print("The remembered direction is \(rememberedDirection)")
// Prints "The current direction is north"
// Prints "The remembered direction is west"
```



## Classes Are Reference Types

value type과 다르게, reference type은 variable 이나 constant에 값이 할당될 때, 혹은 function에 값을 전달할 때 복사하지 않는다. 복사 대신에 존재하는 instance에 대한 참조를 하게 된다.

```swift
let tenEighty = VideoMode()
tenEighty.resolution = hd
tenEighty.interlaced = true
tenEighty.name = "1080i"
tenEighty.frameRate = 25.0
```

`tenEighty` constant를 선언하고 `VideoMode` instance 를 참조하도록 한다. 그리고 내부 property의 값을 변경한다.

```swift
let alsoTenEighty = tenEighty
alsoTenEighty.frameRate = 30.0
```

`alsoTenEighty` constant가 동일한 instance를 참조하도록 하고 내부 property를 또 변경한다. instance 값이 복사되는 것이 아니고, 동일한 instance를 참조하기 때문에, 한 constant가 내부 값을 변경하면 다른 constant의 값도 달라지는 것이다. 

이러한 점이 추론하기 어려운 부분이다.(This example also shows how reference types can be harder to reason about.) `tenEighty`를 사용할 때마다, `alsoTenEighty` 를 사용하는 코드를 고려해야 한다. 대조적으로, value type은 독립성이 보장되므로, easy to reason about 하다로 표현할 수 있다.

주목할 부분은 `tenEighty`  와 `alsoTheEighty` 가 variable이 아닌 constant라는 점이다. 둘은 참조하고 있는 instance가 달라지지 않고, 그 instance의 variable로 선언된 property를 변경하는 것이기에 가능한 코드이다.

### Identity Operators

class는 reference type이기 때문에, 여러개의 constant 와 variable이 하나의 instance를 참조하는 것이 가능하다. 따라서, 동일한 instance를 참조하는 지 확인할 수 있는 방법이 필요하고 다음과 같은 identity operator를 사용하여 구분할 수 있다.

- Identical to (===)
- Not identical to (!==)

주목할 점은 identical to(===) 와 equal to(==) 는 동일하지 않다는 점이다. equal to 는 두 instance의 값이 동일하다는 의미이며, identical to 는 동일한 instance라는 의미이다.

