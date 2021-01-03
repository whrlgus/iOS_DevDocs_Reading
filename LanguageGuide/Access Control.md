# Access Control

access control은 다른 파일이나 모듈에 있는 코드에서 특정 코드 부분의 접근을 제한한다. 이 특징은 코드의 세부 구현사항을 숨기고, 접근하거나 사용할 수 있는 코드에 interface로서 명시할 수 있게 해준다.

class, structure, enumeration 과 같은 개별 타입에 특정 접근 레벨을 할당할 수 있으며, 또한 그 타입에 속한 property, method, initializer, subscript에도 할당할 수 있다. 

swift에서 명시적으로 접근 레벨을 표시할 필요는 없다.



## Modules and Source Files

swift의 access control 모델은 모듈과 소스 파일의 개념에 근거한다.

module은 framework나 앱으로서 다른 모듈로 들여와(import) 사용할 수 있는 코드 배포의 단위이다. 

swift에서, app bundle이나 framework와 같은 각 빌드 타겟은 다른 모듈로 다뤄진다. 

source file은 module 내의 swift source code file 을 말한다. 



## Access Levels

swift는 entity에 대한 5가지의 접근 레벨을 제공한다. 이 접근 레벨은 entity가 정의된 소스파일이나, 그 소스파일이 속한 모듈과 관련있다.

- Open access와 public access는 모듈 내의 모든 소스파일이나 정의된 모듈을 import하는 다른 모듈의 소스파일에서, 개체를 사용 가능하게 해준다. 전형적으로 framework의 public interface를 명시할 때 사용한다.
- Internal access는 모듈 내의 모든 소스파일에서 개체를 사용가능하게 해준다. 하지만, 모듈 밖의 소스파일에서는 사용할 수 없다. 전형적으로 앱이나 framework의 내부 구조체를 정의할 때 사용한다.
- File-private access는 개체가 정의된 소스파일 내부로 접근을 제한한다. 파일 전체에서만 사용되는 구현 세부 사항을 숨기기 위해 사용한다.
- Private access는 정의부에서만 개체에 접근할 수 있게 제한한다. 또한 동일한 파일에 존재하는 선언의 extension에서만 접근할 수 있다. 단일 선언부 내에서만 사용되는 구현 세부 사항을 숨길 때 사용한다.

Open access가 가장 높은 접근 레벨이고, private이 가장 낮은 접근 레벨이다.

Open access는 class나 class member에만 적용가능하다. 모듈 밖의 코드에서 subclass나 override가 가능하게 해준다는 점에서 public access와 차이가 있다. class를 open으로 마킹하는 것은 다른 모듈에서 superclass로 사용하기 위함이란 점을 명시하는 것이다. 

### Guiding Principle of Access Levels

접근 레벨은 전반적인 가이드 원칙을 따른다. *entity의 접근 레벨은 다른 entity의 접근 레벨보다 높을 수 없다.*

예를 들어:

- public variable은 internal, file-private, private 타입에서 정의될 수 없다. 왜냐하면, public 변수가 사용되는 곳에서 해당 type이 불가능하기 때문이다. 
- function은 parameter type이나 return type보다 높은 접근 레벨을 가질 수 없다. 왜냐하면, 구성하는 type이 둘러싸인 코드에서 사용할 수 없는 경우가 있기 때문이다.

### Default Access Levels

거의 모든 개체는 명시되지 않으면 internal 접근 레벨을 갖는다.

### Access Levels for Single-Target Apps

간단한 단일 타겟 앱을 만들 때, 앱의 코드는 self-contained(자급식의, 그것만으로 완비된)하며, 앱 외부 모듈에서 접근가능하게 할 필요가 없다. 그러므로 custom 접근 레벨을 부여할 필요가 없다. 그러나 앱 모듈 내의 다른 코드에 세부 구현 사항을 숨기기 위한 경우에 file-private 이나 private은 사용하자.

### Access Levels for Frameworks

framework를 개발할 때, open 이나 public로서 public-facing interface를 정의하여, 해당 framework를 import 하여 사용하는 외부 모듈에서 접근할 수 있게 하자. 이 public-facing interface는 framework의 API(application programming interface)이다.

> framework의 내부 구현 사항은 default 접근 레벨인 internal이나 private, file-private으로 지정하여 사용해도 된다. 단, framework의 API로 사용하고 싶다면 open 이나 public으로 표시하자.

### Access Levels for Unit Test Targets

유닛 테스트가 있는 앱을 만들 때, 앱의 코드는 테스트하기 위해 접근 가능하도록 만들어야 한다. 기본적으로, open 이나 public으로 표시된 개체의 경우만 다른 모듈에서 접근할 수 있다. 하지만 unit test target은 `@testable` 속성과 함께 product 모듈을 import 하고, product 모듈을 테스트 가능하도록 컴파일 한다면, internal 개체에 접근할 수 있다. 

## Custom Types

custom type 역시 동일한 방식으로 type의 접근 레벨을 지정할 수 있다. 새로운 type은 접근 레벨이 허용하는 한에서 사용이 가능하다. 예를 들어, file-private class를 정의했다면, 정의된 파일 내에서 해당 class를 property, function parameter 또는 return type으로 사용할 수 있다.

type의 접근 제어 레벨은 type member(property, method, initializer, subscript) 의 defualt 접근 레벨에도 영향을 미친다. private 이나 file-private으로 선언된 type은, 그 member 또한 private 혹은 file-private 레벨을 갖는다. internal 이나 public type의 경우는 그 member의 기본 접근 레벨이 internal이 된다.

> public type member의 default 접근 레벨은 public이 아닌 internal이다. public으로 하기 위해선 명시적으로 표시해줘야한다. 이 요구사항은 type의 public-facing API는 명시적으로 표시해야되며, 실수로 노출시키는 경우를 방지하기 위함이다.

```swift
public class SomePublicClass {                  // explicitly public class
    public var somePublicProperty = 0            // explicitly public class member
    var someInternalProperty = 0                 // implicitly internal class member
    fileprivate func someFilePrivateMethod() {}  // explicitly file-private class member
    private func somePrivateMethod() {}          // explicitly private class member
}

class SomeInternalClass {                       // implicitly internal class
    var someInternalProperty = 0                 // implicitly internal class member
    fileprivate func someFilePrivateMethod() {}  // explicitly file-private class member
    private func somePrivateMethod() {}          // explicitly private class member
}

fileprivate class SomeFilePrivateClass {        // explicitly file-private class
    func someFilePrivateMethod() {}              // implicitly file-private class member
    private func somePrivateMethod() {}          // explicitly private class member
}

private class SomePrivateClass {                // explicitly private class
    func somePrivateMethod() {}                  // implicitly private class member
}
```

### Tuple Types

tuple type의 접근 레벨은 내부의 모든 type 중 가장 제한적인 접근 레벨을 갖게된다. 예를 들어, 두 개의 다른 type을 tuple로 사용하고, 각각 internal 과 private 접근 레벨을 갖는다면, tuple type의 접근 레벨은 private이 된다.

> tuple type은 class, structure, enumeration, function과 다르게 독립적인 정의를 가질 수 없다. tuple type의 접근 레벨은 구성 요소에 의해 자동으로 결정되며, 따로 명시할 수 없다.

### Function Types

function type의 기본 접근 레벨은 parameter와 return type 중 가장 제한적인 접근 레벨로 계산된다. 그러나 문맥상 맞지 않는 경우 따로 명시해 줘야한다.

아래 예시는 global function을 명시적인 접근 레벨 변경자(modifier) 없이 정의한 예제이다. 아래 함수의 default 접근 레벨은 internal이 아닌 private이고, 이 경우 private이나 file-private으로 명시해줘야한다. 그렇지 않으면 compile error가 발생한다.

```swift
func someFunction() -> (SomeInternalClass, SomePrivateClass) {} // compile error
private func someFunction() -> (SomeInternalClass, SomePrivateClass) {}
```

### Enumeration Types

Enumeration 의 각각의 case는 type과 동일한 접근 레벨을 갖으며, 따로 명시할 수 없다. 

#### Raw Values and Associated Values

raw value나 associated value의 접근 레벨은 type의 접근 레벨 이상이어야 한다.

### Nested Types

nested type의 접근 레벨은 containing type이 public이 아닌 한, 동일한 접근 레벨을 갖는다. public type 내부에 정의된 nested type은 자동적으로 internal이다. 그러나 명시함으로서 public으로 지정할 수도 있다.

## Subclassing

현재 접근 context에서 접근할 수 있는 class를 subclass화 할 수 있다. 그리고 그 subclass는 같은 모듈에 정의한다. 또한, 다른 모듈에 정의된 open class를 subclass화 할 수 있다. subclass는 superclass보다 높은 접근 레벨을 가질 수 없다. 예를 들어, internal superclass의 public subclass를 정의할 수 없다.

게다가, 같은 모듈내에 정의된 class들에 대해, 특정 접근 context에서 보이는 모든 class member(method, property, initiailizer, subscript)를 override 할 수 있다. 다른 모듈에 정의된 class에 대해, open class member를 override할 수 있다.

override는 물려 받은 class member의 접근성을 superclass 에서의 접근성보다 확장되게 할 수 있다. 

```swift
public class A {
    fileprivate func someMethod() {}
}

internal class B: A {
    override internal func someMethod() {}
}
```

또한, subclass member의 접근 레벨보다 낮은 superclass member를 호출할 수 있다. 단 superclass member 호출이 가능한 접근 레벨 context여야한다. 즉, file-private member 호출의 경우 superclass와 같은 소스 파일에 있어야하고, internal member 호출의 경우 superclass와 같은 모듈 내에 존재해야 한다.

```swift
public class A {
    fileprivate func someMethod() {}
}

internal class B: A {
    override internal func someMethod() {
        super.someMethod()
    }
}
```

## Constants, Variables, Properties, and Subscripts

Constant, variable, property 모두 해당 type보다 public하게 설정할 수 없다. 예를 들어, private type을 public property로 지정할 수 없다. 유사하게, subscript도 index type이나 return type보다 public하게 설정할 수 없다.

```swift
private var privateInstance = SomePrivateClass()
```

### Getters and Setters

이들의 getter와 setter는 동일한 접근 레벨을 갖는다. setter의 접근 레벨을 getter 보다 낮게 설정할 수 있는데, 이는 읽기 쓰기 권한에 차이를 두기 위함이다. `private(set)` `internal(set)` `fileprivate(set)` 을 `var` 나 `subscript` 앞에 적으면 된다.

야래 예제는 string property가 몇번이나 변경되었는지 추적하는 구조체를 보여준다.

```swift
struct TrackedString {
    private(set) var numberOfEdits = 0
    var value: String = "" {
        didSet {
            numberOfEdits += 1
        }
    }
}
```

두개의 저장 property가 있다. `value` property의 `didset` property observer로 변경을 추적할 수 있고 변경될 때마다 개수를 저장하는 property의 값을 변경해준다.

구조체와 `value` property는 접근 레벨 변경자를 명시하지 않았기 때문에 internal로 설정된다. 그러나 `numOfEdits` property는 setter의 접근 레벨을 private으로 한정하여 getter는 기본 레벨인 internal에 머무르지만 setter는 더 제한적으로 설정하여 구조체 내부에서만 접근할 수 있다.

아래와 같이 `public` 과 `private(set)` 을 조합하여 setter에도 접근 레벨을 부여할 수 있다. 

```swift
public struct TrackedString {
    public private(set) var numberOfEdits = 0
    public var value: String = "" {
        didSet {
            numberOfEdits += 1
        }
    }
    public init() {}
}
```

## Initializers

custom initializer의 접근 레벨은 type의 접근 레벨 이하로 설정할 수 있다. 예외로, required initializer는 class의 레벨과 같아야 한다. 

function과 method parameter 처럼, initializer parameter는 initializer의 접근 레벨보다 더 private할 수 없다.

### Default Initializers

swift는 structure나 class가 별도의 initializer가 정의되지 않고, 모든 property가 default 값을 가지고 있다면 어떠한 인자도 없는 default initializer를 제공한다.

type이 public이 아닌이상, default initializer의 접근 레벨은 type과 동일하다. 기본적으로 internal 접근 레벨에 해당하는 것은 명시적으로 public하게 설정할 수 있다.

### Default Memberwise Initializers for Structure Types

structure의 모든 저장 property가 private이라면 default memberwise initializer역시 private으로 설정된다. 동일하게, 만약 모든 저장 property가 file private이라면 생성자도 file private이다. 이외에는 internal 접근 레벨을 갖는다.

이 생성자도 public으로 설정 가능하다.



## Protocols

protocol을 선언할 때, 명시적인 접근 레벨을 할당하여 특정 접근 context에서 채택 가능한 protocol을 생성할 수 있다.

protocol의 각 요구사항(requirement)의 접근 레벨은 자동적으로 protocol의 접근 레벨과 동일하게 설정된다. protocol과 다른 접근 레벨을 요구사항에 설정할 수는 없는데, 이는 해당 protocol을 채택하는 type에서 protocol의 모든 요구사항을 볼 수 있게 하기 위함이다.

> 만약 public protocol을 정의한다면, 그 protocol의 요구사항도 public 접근 레벨을 필요로 한다. 이것은 다른 public type과는 다른 동작인데, 다른 public type은 type member에 대해 기본적으로 internal 접근 레벨을 부여한다.

### Protocol Inheritance

만약 존재하는 protocol을 상속하는 새로운 protocol을 정의한다면, 새로운 protocol의 접근 레벨은 기껏해야 상속한 protocol의 접근 레벨이다. 예를 들어, internal protocol을 상속 받는 public protocol은 정의할 수 없다.

### Protocol Conformance

한 type은 자신의 access level보다 낮은 level의 protocol을 채택할 수 있다. 예를 들어, internal protocol을 채택하는 public type을 정의할 수 있다. 하지만, protocol의 구현사항은 internal module에서만 사용가능하다. 또, 그게 가능하도록 접근 레벨을 부여해야한다.



## Extensions

Class, structure, enumeration의 가능한 접근 context 에서는 각각 확장가능하다. extension에 추가되는 member는 기본적으로 원본 type의 접근 레벨을 따른다. 

extension에도 명시적으로 접근 레벨을 지정할 수 있고, 추가된 type member는 해당 레벨을 따르게된다. 

만약 extension이 protocol을 채택한다면 명시적 접근 레벨을 지정할 수 없다. 대신에, protocol의 접근 레벨이 protocol requirement에 적용된다.

### Private Members in Extensions

동일한 파일에 정의한 extension은 원본 type의 선언과 동일하게 취급한다. 

- extension에서 원본 선언부의 Private member에 접근할 수 있다.
- 한 extension에서 선언한 private member에 다른 extension에서 접근 가능하다.
- extension에 정의한 private member에 원본 선언부에서 접근할 수 있다.

```swift
protocol SomeProtocol {
    func doSomething()
}

struct SomeStruct {
    private var privateVariable = 12
}

extension SomeStruct: SomeProtocol {
    func doSomething() {
        print(privateVariable)
    }
}
```



## Generics

generic type과 generic function의 접근 레벨은 type 제약중 최소 레벨이 적용된다.

## Type Aliases

tuple과 비슷하게 적용된다.