# Initialization

initialization(초기 내용 설정)은 class, struct, enumeration의 인스턴스를 사용할 수 있도록 준비하는 절차이다. 이 절차는 인스턴스에 있는 각 stored property의 초기값을 설정하고, 필요한 setup을 수행하거나, 새로운 인스턴스를 사용할 준비를 하기 전에 필요한 initialization하는 것을 포함한다.

특정 타입의 새로운 인스턴스를 생성할 때 호출할 수 있는 메소드인, initializer를 정의하여 초기 내용 설정 절차를 구현하게 된다. Objective-C initializer와는 다르게 Swift initializer는 값을 반환하지 않는다. 생성자의 주요 역할은 새로운 인스턴스가 처음으로 사용되기 전에 올바르게 초기화하는 것이다.

또한, 클래스 타입의 인스턴스는 deinitializer를 구현할 수 있다. 이 것은 해당 클래스 인스턴스가 해제되기 바로 전에 정리하는 로직을 수행한다. 



## Setting Initial Values for Stored Properties

## Customizing Initialization

## Default Initializers

Swift는 구조체나 클래스가 모든 프로퍼티에 기본 값을 제공하고, 다른 생성자를 제공하지 않을 때, 기본 생성자를 제공한다. 기본 생성자는 단순히 기본 값으로 설정된 프로퍼티들로 새로운 인스턴스를 생성한다.

이 예제는 ShoppingListItem 클래스를 정의하고, 항목의 이름, 개수, 구매 상태를 캡슐화하고 있다:

```swift
class ShoppingListItem {
  var name: String?
  var quantity = 1
  var purchased = false
}
var item = ShoppingListItem()
```

모든 프로퍼티가 기본 값을 갖고 있고 슈퍼클래스가 없는 기본 클래스이기 때문에, 자동적으로 기본 값으로 새로운 인스턴스를 생성할 수 있는 기본 생성자 구현을 갖게된다. 해당 클래스의 기본 생성자를 사용하여 인스턴스를 생성하고 item 변수에 인스턴스를 할당한다.

### Memberwise Initializers for Structure Types

구조체 타입은 커스텀 생성자가 없다면, 자동적으로 memberwise 생성자를 갖는다. 기본 생성자와는 다르게 기본 값이 없는 저장 프로퍼티가 있어도, 구조체는 memberwise 생성자를 갖는다.

Memberwise 생성자는 새로운 구조체 인스턴스의 멤버 프로퍼티를 초기화할 수 있는 편리한 방법이다. 초기값은 이름으로 생성자에 전달할 수 있다.

아래 예제는 width, height 프로퍼티를 갖는 Size 구조체를 정의한 것이다. 두 프로퍼티는 0.0 의 기본 값을 항당받아 Double 타입으로 추론될 수 있다. 

이 구조체는 자동적으로 `init(width:height:)` memberwise 생성자를 갖고, 새로운 인스턴스 생성시에 사용할 수 있다.

```swift
struct Size {
  var width = 0.0, height = 0.0
}
let twoByTwo = Size(width: 2.0, height: 2.0)
```

memberwise 생성자를 호출할 때, 기본 값이 있는 프로퍼티는 생략할 수 있다. 위 예제에서 두 프로퍼티는 기본 값을 갖는다. 생성자 호출 시, 둘 중 하나를 빼거나 둘 모두를 뺄 수 있다.

```swift
let zeroByTwo = Size(height: 2.0)
print(zeroByTwo.width, zeroByTwo.height)
// Prints "0.0 2.0"

let zeroByZero = Size()
print(zeroByZero.width, zeroByZero.height)
// Prints "0.0 0.0"
```



## Initializer Delegation for Value Types

생성자는 인스턴스의 초기 설정의 한 부분으로서 다른 생성자를 호출할 수 있다. 이 절차는 생성자 위임(initializer delegation)이라고 하며, 여러 생성자에 같은 코드를 생성하지 않도록 해준다. 

생성자 위임이 어떻게 동작하는지, 어떠한 위임 형태가 허용되는지에 대한 규칙은 값 타입과 클래스 타입이 서로 다르다. 값 타입(structure and enumeration)은 상속을 지원하지 않기에, 제공하는 것만 다른 생성자로 위임하면 돼서, 생성자 위임 절차는 상대적으로 간단하다. 반면, 클래스는 다른 클래스를 상속할 수 있다. 즉, 상속한 저장 프로퍼티에 적절한 값이 할당될 수 있게 해야하는 추가적인 책임을 가지고 있는 것이다. 이 책임은 아래 Class Inheritance and Initialization에 설명되어 있다.

커스텀 생성자를 작성할 때, 값 타입에는 `self.init` 을 사용하여 내부의 다른 생성자를 참조할 수 있다. `self.init`을 호출하는 것은 생성자 내부에서만 가능하다.

값 타입의 커스텀 생성자를 정의할 때 주의할 점은, 더이상 기본 생성자(또는 structure일 경우, memberwise 생성자)에 접근할 수 없다는 것이다. 이 제약은 더 복잡한 생성자에서 추가적으로 필요한 셋업이, 자동적인 생성자 중 하나를 사용하는 누군가에 의해 누락되는 것을 방지한다. 

> NOTE
>
> 만약 기본 생성자와 memberwise 생성자와 함께 커스텀 생성자로 초기화 가능한 커스텀 값 타입을 만들고 싶다면, 생성자를 값 타입의 기본 구현체에 일부에 만들기보다는 extension에 만들자. 

아래 직사각형을 나타내는 `Rect` 구조체를 정의했다.  `Size` 와 `Point` 라는 구조체가 필요하며 기본 값은 0.0으로 설정한다.

```Swift
struct Size {
  var width = 0.0, height = 0.0
}
struct Point {
  var x = 0.0, y = 0.0
}
```

`Rect` 구조체를 다음 중 하나의 방법으로 초기화할 수 있다: 0으로 초기화된 `origin`과 `size` 의 기본 값을 사용하거나, 구체적인 원점과 크기를 제공하거나, 중점과 크기를 제공. 이 초기화 옵션은 세개의 커스텀 생성자로 아래와 같이 정의되어 있다.

```Swift
struct Rect {
  var origin = Point()
  var size = Size()
  init() {}
  init(origin: Point, size: Size) {
    self.origin = origin
    self.size = size  
  }
  init(center: Point, size: Size) {
    let originX = center.x - (size.width / 2)
    let originY = center.y - (size.height / 2)
    self.init(origin: Point(x: originX, y: originY), size: size)
  }
}
```

첫번째 생성자 `init()` 는 커스텀 생성자를 제공하지 않을 경우 사용할 수 있는 기본 생성자와 기능적으로 동일하다. 

```swift
let basicRect = Rect()
```

두번째 생성자 `init(origin:size)` 는 커스텀 생성자를 제공하지 않을 경우 사용할 수 있는 memberwise 생성자와 기능적으로 동일하다.

```swift
let originRect = Rect(origin: Point(x: 2.0, y: 2.0),
                      size: Size(width: 5.0, height: 5.0))
```

세번째 생성자 `init(center:size:)` 는 약간 복잡하다. 중점과 크기를 기반으로 적절한 원점을 계산하는 것으로 시작된다. 그리고 새로운 원점과 크기 값을 사용하여 `init(origin:size)` 생성자를 호출(혹은 생성자로 위임) 한다. 

```swift
let centerRect = Rect(center: Point(x: 4.0, y: 4.0),
                      size: Size(width: 3.0, height: 3.0))
```

`init(center:size:)` 생성자는 `origin` 과 `size` 에 새로운 값을 할당할 수 있다. 그러나 기능적으로 동일한 기존에 구현된 생성자를 활용하는 것이 더 편리하고 의도가 명확하다.

> NOTE
>
> `init()` 과 `init(origin:size:)`를 정의하지 않고 위 예제를 구현할 수 있는 방법으로 extension을 사용하는 것이 있다.

## Class Inheritance and Initialization

클래스의 모든 저장 프로퍼티(부모클래스로부터 상속한 프로퍼티를 포함하여)는 초기화 과정에서 반드시 초기 값이 할당되어야 한다.

Swift는 이를 위해 클래스 타입에 두 유형의 생성자를 정의한다: designated 생성자와 convenience 생성자.

### Designated Initializers and Convenience Initializers

designated 생성자는 클래스의 주요한 생성자이다. 이 생성자는 클래스에 있는 모든 프로퍼티를 전부 초기화하고 슈퍼클래스에서도 이 절차를 수행하도록 슈퍼클래스의 적절한 생성자를 호출한다.

클래스는 적은 수의 designated 생성자를 갖는 경향이 있고, 한개만 갖는 것이 일반적이다. 이 생성자는 초기화가 일어나는 지점이며 이 통로로 초기화 절차가 슈퍼클래스 체인을 타고 수행되게 된다.

모든 클래스는 적어도 하나의 designated 생성자를 갖는다. 몇몇 클래스에서는 이 요구사항이 슈퍼클래스로부터 하나 이상의 지정 생성자를 상속함으로써 충족된다.

Convenience 생성자는 클래스의 생성자를 보조한다. 같은 타입 내부의 지정 생성자를 호출하는 편의 생성자를 정의하여 지정 생성자의 일부 파라미터를 기본 값으로 설정할 수 있다. You can also define a convenience initializer to create an instance of that class for a specific use case or **input value type**(??).

필요하지 않다면 convenience 생성자를 제공할 필요가 없다. 공통적인 초기화 패턴을 줄이는 것이 시간을 절약하고 의도를 명확히 해준다면 사용하자.

### Syntax for Designated and Convenience Initializers

클래스의 지정 생성자는 값 타입의 생성자와 같은 방식으로 작성한다:

편의 생성자는 convenience 수식어를 init 키워드 앞에 붙여서 작성한다.

### Initializer Delegation for Class Types

지정 생성자와 편의 생성자 간의 관계를 단순화하기 위해, Swift는 생성자간 위임 호출을 위한 세가지 규칙을 적용한다.

- **Rule 1**

  지정 생성자는 바로 상위에 있는 슈퍼클래스의 지정 생성자를 호출해야 한다.

- **Rule 2**

  편의 생성자는 같은 클래스의 다른 생성자를 호출해야 한다.

- **Rule 3**

  편의 생성자는 궁극적으로 지정생성자를 호출해야 한다.

이를 기억하기 위한 간단한 방법은 다음과 같다:

- 지정 생성자는 상위로 위임해야 한다.
- 편의 생성자는 가로로 위임해야 한다.

이 규칙을 도식화 하면 아래와 같다:

<img src = "https://docs.swift.org/swift-book/_images/initializerDelegation01_2x.png" width = 70%/>

여기서, 슈퍼클래스는 하나의 지정 생성자를 갖고 두개의 편의 생성자를 갖는다. 한 편의 생성자는 다른 편의 생성자를 호출하고, 이어서 지정 생성자를 호출한다. 이는 위 규칙 2와 3을 만족한다. 슈퍼 클래스는 상위의 슈퍼클래스를 갖지 않으며, 규칙 1은 적용되지 않는다.

서브클래스는 두개의 지정 생성자와 하나의 편의 생성자를 갖는다. 이 편의 생성자는 같은 클래스의 다른 생성자를 호출해야하기 때문에, 반드시 두 지정 생성자 중 하나를 호출해야 한다. 이는 규칙 2와 3을 만족한다. 두 지정 생성자는 규칙 1을 만족하기 위해, 반드시 슈퍼클래스의 지정 생성자를 호출해야 한다.

> NOTE
>
> 이 규칙들은 클래스의 사용자가 각 클래스의 인스턴스를 어떻게 생성할 지에 영향을 주지 않는다. 위 그림에서 모든 생성자는 속해있는 클래스의 인스턴스를 완전히 초기화할 수 있고, 이 규칙들은 클래스의 생성자를 구현할 때 어떻게 작성해야 하는지에만 영향을 미친다.

아래 그림은 더 복잡한 클래스 계층을 나타낸다. 이 그림은 계층 내의 지정 생성자가 클래스 초기화에 어떻게 funnel 지점 역할을 하는지 보여주며, 체인에서 클래스간 관계를 단순화 한다.

<img src = "https://docs.swift.org/swift-book/_images/initializerDelegation02_2x.png" width = 70%/>



### Two-Phase Initialization

Swift에서 클래스 초기화는 두 단계 절차를 거친다. 첫 단계에서, 각 저장 프로퍼티는 초기 값을 할당받는다. 모든 저장 프로퍼티의 초기 상태가 결정되면, 두번째 단계가 시작되고, 각 클래스는 새로운 인스턴스가 사용되기 전에 저장 프로퍼티를 커스텀할 수 있는 기회가 생긴다.

두 단계의 초기화 절차는 초기화를 안전하게 해주며, 클래스 계층에 있는 클래스들에게 완전한 유연성을 제공한다. 그리고 프로퍼티 값이 초기화되기 전에 접근되는 것을 방지하고, 의도치않게 다른 생성자에 의해 다른 값이 할당되는 것을 방지한다.

> NOTE
>
> Swift의 두 단계 초기화 절차는 Objective-C의 초기화와 유사하다. 주요한 차이는 단계 1에서 Objective-C는 0이나 null 값을 모든 프로퍼티에 할당한다. Swift의 초기화 흐름은 커스텀 초기값을 할당하고, 기본 값이 0이나 nil일 수 없는 타입에 대처할 수 있어 더 유연하다.

Swift의 컴파일러는 두 단계 초기화가 에러없이 완료될 수 있도록 네 가지의 안전 검증을 수행한다:

- **Safety check 1**

  지정 생성자는 슈퍼클래스 생성자로 위임하기 전에 클래스 내의 모든 프로퍼티가 초기화되도록 해야 한다.

  위에 언급한 바와 같이, 객체의 메모리는 모든 저장 프로퍼티의 초기 상태가 인지된 이후에야 완전히 초기화된 것으로 여겨진다. 이 규칙이 만족되기 위해서는, 지정 생성자는 반드시 체인의 상위로 위임하기 전에 모든 프로퍼티를 초기화해야 한다.

- **Safety check 2**

  지정 생성자는 상속된 프로퍼티에 값을 할당하기 전에 슈퍼클래스 생성자로 역할을 위임해야 한다. 그렇지 않으면, 지정 생성자가 할당하는 새로운 값은 슈퍼클래스의 초기화 과정에서 덮어 쓰여질 것이다.

- **Safety check 3**

  편의 생성자는 프로퍼티에 값을 할당하기 전에 다른 생성자로 위임해야 한다. 그렇지 않으면, 편의 생성자가 할당하는 새로운 값은 같은 클래스의 지정 생성자에 의해 덮어 쓰여질 것이다.

- **Safety check 4**

  생성자는 초기화 첫 단계가 완료되기 전까지, 인스턴스 메소드를 호출하거나, 인스턴스 프로퍼티의 값을 읽거나, self를 참조하면 안된다.

  클래스 인스턴스는 첫 단계가 끝난 이후에야 완전히 유효하다. 클래스 인스턴스가 첫 단계 이후에 유효하다고 판별되면, 프로퍼티는 접근 가능하고, 메소드는 호출 가능해진다.

위 네가지의 안전 검증을 기반으로 두 단계 초기화가 어떻게 이뤄지는지는 다음과 같다:

- **Phase 1**
  - 지정 또는 편의 생성자는 클래스에서 호출된다.
  - 클래스의 새로운 인스턴스를 위한 메모리가 할당된다. 이 메모리는 아직 초기화되지 않았다.
  - 클래스의 지정 생성자는 모든 저장 프로퍼티가 값을 갖는지 확인한다. 이 저장 프로퍼티들을 위한 메모리는 이제 초기화된다.
  - 지정 생성자는 슈퍼클래스의 생성자에게 같은 작업을 하도록 한다.
  - 클래스 상속 체인을 거슬러 올라가 끝에 도달할 때까지 반복한다.
  - 체인의 최상위에 도달하여, 저장 프로퍼티가 값을 갖게되는 것이 확인되면, 이 인스턴스의 메모리는 완전히 초기화되며 phase 1은 완료된다.
- **Phase 2**
  - 체인의 최상위에서 다시 하위로 가며, 각 지정 생성자는 인스턴스를 커스터마이즈할 수 있게 된다. 생성자는 self에 접근하여 그 프로퍼티를 변경할 수 있고 인스턴스 메소드를 호출할 수 있다.
  - 편의 생성자 동일

다음은 가상의 서브클래스와 슈퍼클래스에서 단계 1에 해당하는 초기화 호출을 보여준다:

<img src = "https://docs.swift.org/swift-book/_images/twoPhaseInitialization01_2x.png" width = 70%/>

이 예제에서, 초기화는 서브클래스의 편의 생성자를 호출하는 것으로부터 시작한다. 이 편의 생성자는 아직 어떠한 프로퍼티도 변경할 수 없다. 바로 같은 클래스 내의 지정 생성자에게 위임한다. 

이 지정 생성자는 서브클래스의 모든 프로퍼티가 값을 가질 수 있게 해야한다. 그러고 나서 체인의 초기화를 계속할 수 있도록 슈퍼클래스의 지정 생성자를 호출한다.

슈퍼클래스의 지정 생성자는 내부의 모든 프로퍼티가 값을 가질 수 있게 해야 한다. 상위에 슈퍼클래스가 존재하지 않으므로, 더이상의 위임은 필요가 없다.

슈퍼클래스의 모든 프로퍼티가 값을 가진 후에, 메모리는 완전히 초기화 되었고, 단계 1은 완료된다.

단계 2:

<img src = "https://docs.swift.org/swift-book/_images/twoPhaseInitialization02_2x.png" width = 70%/>

슈퍼클래스의 지정 생성자는 인스턴스를 커스텀할 수 있게 되었다. 슈퍼클래스의 지정 생성자가 마무리되면, 서브클래스의 지정 생성자는 추가적인 커스텀 작업을 할 수 있게 된다. 마지막으로, 편의 생성자에게 그 차례가 온다.

### Initializer Inheritance and Overriding

Objective-C의 서브클래스와는 다르게, Swift 서브클래스는 기본적으로 슈퍼클래스의 생성자를 상속하지 않는다. 이 접근은 슈퍼클래스의 단순한 생성자가 더 구체적인 서브클래스에 의해 상속되어, 완전히 초기화 되지 않은 서브클래스 인스턴스를 생성하는 상황은 방지하기 위함이다.

> NOTE
>
> 슈퍼클래스 생성자는 안전하고 적절한 특정 상황에서만 상속된다. 

만약, 커스텀 서브클래스가 슈퍼클래스의 생성자와 동일한 생성자를 갖도록 하려면, 서브클래스에 커스텀 생성자를 구현하면 된다.

슈퍼클래스의 지정 생성자와 대등한 서브클래스 생성자를 작성할 때, 그 지정 생성자를 오버라이드하여 제공한다. 그러므로, 서브클래스 생성자 정의 앞에 override 지정자를 붙여야 한다. 자동적으로 제공되는 기본 생성자를 오버라이딩할 때도 동일하다. 

오버라이드된 프로퍼티, 메소드 또는 subscript에 대해, override 지정자의 존재는 Swift로 하여금 슈퍼클래스가 대등한 지정 생성자를 갖고, 파라미터가 타당한지 검사하게 한다.

> NOTE
>
> 서브클래스 생성자의 구현이 편의 생성자라 할지라도, 슈퍼클래스의 지정 생성자를 오버라이딩하는 경우엔 override 지정자를 반드시 표시해야 한다.

반대로, 슈퍼클래스의 편의 생성자와 대등한 서브클래스 생성자를 작성한다면, 슈퍼클래스 편의 생성자는 서브클래스에 의해 호출되지 않는다. 그러므로, 서브클래스는 슈퍼클래스 생성자의 재정의를 제공하지 않는다. 결과적으로, override 지정자를 붙이지 않는다.

아래 예제는 Vehicle 이라는 기본 클래스를 정의한다. 이 기본 클래스는 numberOfWheels 프로퍼티를 선언하고 기본 Int 값으로 0을 할당했다. 이 프로퍼티는 description이라는 연산 프로퍼티에 의해 사용된다.

```swift
class Vehicle {
  var numberOfWheels = 0
  var description: String {
    return "\(numberOfWheels) wheel(s)"
  }
}
```

이 클래스는 저장 프로퍼티에 기본 값을 제공하고 커스텀 생성자가 없다. 따라서, 자동적으로 기본 생성자를 갖게된다. 이 기본 생성자는 항상 지정 생성자가 되며, numberOfWheels가 0인 새로운 Vehicle 인스턴스를 생성한다.

```swift
let vehicle = Vehicle()
print("Vehicle: \(vehicle.description)")
```

다음 예제는 Vehicle의 서브클래스인 Bicycle을 정의한다:

```swift
class Bicycle: Vehicle {
  override init() {
    super.init()
    numberOfWheels = 2
  }
}
```

이 서브클래스는 커스텀 지정 생성자를 정의한다. 이 생성자는 슈퍼클래스의 지정생성자와 대등하고, 따라서 override 지정자를 표시한다.

Bicycle의 `init()` 생성자는 `super.init()`을 호출하는 것으로 시작된다. 상속한 numberOfWheels 프로퍼티를 Bicycle이 변경할 기회를 얻기 전에 Vehicle에 의해 초기화한다. `super.init()` 호출한 후, numberOfWheels의 기본 값이 2로 변경된다.

만약, Bicycle 인스턴스를 생성하면, numberOfWheels 프로퍼티가 갱신된 것을 확인하기 위해, 상속한 description 연산 프로퍼티를 호출할 수 있다.

```swift
let bicycle = Bicycle()
print("Bicycle: \(bicycle.description)")
```

만약, 서브클래스 생성자가 초기화 절차의 단계 2에서 커스텀을 수행하지 않고, 슈퍼클래스가 인자 없는 지정 생성자를 갖으면, 서브클래스의 모든 저장 프로퍼티를 초기화하고 나서 `super.init()` 호출을 생략할 수 있다. 

다음 예제는 Vehicle의 다른 서브클래스인 Hoverboard를 정의한다. 생성자에서, color 프로퍼티만 설정한다. `super.init()` 호출을 명시하는 대신, 암묵적인 호출에 의존한다. 

```swift
class Hoverboard: Vehicle {
  var color: String
  init(color: String) {
    self.color = color
    // super.init() implicitly called here
  }
  override var description: String {
    return "\(super.description) in a beautiful \(color)"
  }
}
```

Hoverboard 인스턴스는 Vehicle 생성자에 의해 제공되는 기본 바퀴 수를 사용한다.

```swift
let hoverboard = Hoverboard(color: "silver")
print("Hoverboard: \(hoverboard.description)")
```

> 서브클래스는 초기화 중에 상속한 변수 프로퍼티를 변경할 수 있지만, 상수 프로퍼티는 변경이 불가능하다.

### Automatic Initializer Inheritance

위에 언급된 것처럼, 서브클래스는 기본적으로 슈퍼클래스의 생성자를 상속하지 않는다. 그러나, 만약에 특정 조건에 부합한다면, 슈퍼클래스의 생성자를 자동적으로 상속한다. 즉, 많은 공통 시나리오에서 생성자 오버라이드를 하지 않아도 되며, 슈퍼 클래스의 생성자를 쉽게 상속할 수 있다.

서브클래스의 모든 프로퍼티에 기본 값을 제공한다고 가정할 때 다음 규칙이 적용된다:

- **Rule 1**

  만약 서브클래스에 지정 생성자가 정의되지 않았다면, 자동적으로 슈퍼클래스의 모든 **지정 생성자**를 상속한다.

- **Rule 2**

  만약 서브클래스가 슈퍼클래스 모든 지정 생성자의 구현을 제공한다면(rule 1이 적용되었거나, 커스텀 구현을 한 경우), 자동적으로 슈퍼클래스의 **편의 생성자**를 상속한다.

이 규칙은 서브클래스가 추가적인 편의 생성자를 구현해도 적용된다.

> NOTE
>
> 서브클래스는 규칙 2를 만족시키기 위해 편의 생성자로서 슈퍼클래스의 지정 생성자를 구현할 수 있다.



### Designated and Convenience Initializers in Action

아래 예제는 지정 생성자, 편의 생성자, 자동 생성자 상속이 동작하는 것을 보여준다. Food, RecipeIngredient, ShoppingListItem 이름을 갖는 세개의 클래스 계층을 정의하고, 생성자가 어떻게 상호작용하는지 보여준다.

계층의 기본 클래스는 Food로 음식의 이름을 캡슐화한다. 이 클래스는 name이라는 String 프로퍼티를 갖고  두개의 생성자를 제공한다.

```swift
class Food {
  var name: String
  init(name: String) {
    self.name = name
  }
  convenience init() {
    self.init(name: "[Unnamed]")
  }
}
```

아래 그림은 생성자 체인을 보여준다:

<img src = "https://docs.swift.org/swift-book/_images/initializersExample01_2x.png" width = 70%/>

클래스는 기본 memberwise 생성자를 갖지 않기 때문에, name이라는 하나의 인자를 갖는 지정 생성자를 정의하였다. 이 생성자는 특정 이름으로 Food 인스턴스를 생성하는데 사용될 수 있다.

```swift
let namedMeat = Food(name: "Bacon")
// namedMeat's name is "Bacon"
```

`init(name: String)` 생성자는 지정 생성자로 제공된다. 왜냐하면 모든 프로퍼티가 완전히 초기화될 수 있도록 하기 때문이다. 슈퍼클래스를 갖지 않으며, 이 생성자에서 초기화를 완료하기 위해 `super.init()` 을 호출할 필요가 없다.

또한, 인자가 없는 편의 생성자를 갖는다. [Unnamed] 라는 값으로 init(name: String) 으로 위임할 수 있는 기본 이름을 제공한다.

```swift
let mysteryMeat = Food()
// mysteryMeat's name is "[Unnamed]"
```

계층 내의 두번째 클래스는 RecipeIngredient로 Food 의 서브클래스이다. 이 클래스는 요리 레시피의 재료를 형성한다. quantity라는 이름의 Int 프로퍼티를 갖고, 두개의 생성자를 정의한다.

```swift
class RecipeIngredient: Food {
  var quantity: Int
  init(name: String, quantity: Int) {
    self.quantity = quantity
    super.init(name: name)
  }
  override convenience init(name: String) {
    self.init(name: name, quantity: 1)
  }
}
```

이 클래스의 생성자 체인은 다음 그림과 같다:

<img src = "https://docs.swift.org/swift-book/_images/initializersExample02_2x.png" width = 70%/>

하나의 지정 클래스를 갖고, 새로운 인스턴스의 모든 프로퍼티를 형성할 수 있다. 이 생성자는 quantity 프로퍼티에 전달받은 값을 할당하는 것으로 시작된다. 이후에, 이 생성자는 Food 클래스의 `init(name: String)` 에게 위임한다. 이 절차는 위 내용의 Two-Phase Initialization에서 safety check 1 을 만족한다.

RecipeIngredient는 편의 생성자도 정의한다. 이 편의 생성자는 양을 명시하지 않고 생성하며 1개라고 가정한다. 이 정의는 RecipeIngredient 인스턴스를 빠르고 편리하게 생성해주며, 양이 1인 인스턴스 생성시에 코드 중복을 없애준다. 이 편의 생성자는 단순히 같은 클래스의 지정 생성자로 위임하고 quantity의 값으로 1을 전달한다.

RecipeIngredient의 편의 생성자는 Food의 지정생성자와 같은 파라미터를 취한다. 이 편의 생성자는 슈퍼클래스로부터 지정생성자를 오버라이드하기 때문에 override 지정자를 반드시 붙여준다.

RecipeIngredient가 `init(name: String)` 을 편의 생성자로서 제공하지만, 슈퍼클래스의 모든 지정 생성자를 제공한 것이다. 그러므로, 자동적으로 슈퍼클래스의 편의 생성자를 모두 상속한다.

상속한 init() 함수는 슈퍼클래스와 동작이 동일하며, 다만 Food로 위임하는 것이 아닌 RecipeIngredient로 위임한다.

이 세가지 생성자는 모두 RecipeIngredient 인스턴스를 생성하는데 사용될 수 있다:

```swift
let oneMysteryItem = RecipeIngredient()
let oneBacon = RecipeIngredient(name: "Bacon")
let sixEggs = RecipeIngredient(name: "Eggs", quantity: 6)
```

계층에서 세번째이고 마지막 클래스인 ShoppingListItem은 RecipeIngredient의 서브클래스이다. 이 클래스는 쇼핑 목록으로 표현되는 요리 재료를 모델링한다.

쇼핑 목록의 모든 항목은 미구매 상태로 시작한다. 연산 프로퍼티로 인스턴스의 설명을 제공한다.

```swift
class ShoppingListItem: RecipeIngredient {
  var purchased = false
  var description: String {
    var output = "\(quantity) x \(name)"
    output += purchased ? " ✔" : " ✘"
    return output
  }
}
```

ShoppingListItem에서 purchased는 미구매 상태로 시작하기 때문에 이를 초기화하는 생성자를 정의하지 않는다. 이 클래스는 자동적으로 슈퍼클래스의 모든 지정 생성자와 편의 생성자를 상속한다.

아래 그림은 세 클래스의 최종적인 생성자 체인을 보여준다:

<img src = "https://docs.swift.org/swift-book/_images/initializersExample03_2x.png" width = 70%/>

ShoppingListItem 인스턴스를 생성하기 위해 이 세가지 생성자를 사용할 수 있다:

```swift
var breakfastList = [
    ShoppingListItem(),
    ShoppingListItem(name: "Bacon"),
    ShoppingListItem(name: "Eggs", quantity: 6),
]
breakfastList[0].name = "Orange juice"
breakfastList[0].purchased = true
for item in breakfastList {
    print(item.description)
}
// 1 x Orange juice ✔
// 1 x Bacon ✘
// 6 x Eggs ✘
```



## Failable Initializers

## Required Initializers

## Setting a Default Property Value with a Closure or Function



