# Automatic Reference Counting

swift는 ARC를 사용하여 앱의 메모리 사용량을 추적하며 관리한다. 대부분의 경우, 직접 관리할 필요가 없다. ARC는 자동으로 더이상 사용하지 않는 class instance에 의한 메모리를 해제한다. 

그러나 ARC가 앱의 메모리를 관리할 수 있게 하기 위해 필요한 정보가 있고, 그 상황을 설명하겠다. 

참조 카운팅(reference counting)은 class instance에만 적용된다. structure와 enumeration은 value type으로 참조에 의해 저장되거나 전달되지 않는다.

## How ARC Works

class의 instance를 생성할 때마다 ARC는 해당 instance 정보를 저장하기 위한 메모리를 할당한다. 이 메모리는 instance type에 대한 정보를 들고 있고, 그 instance와 연관된 저장 property의 값을 가지고 있다. 

추가적으로, instance가 더이상 필요하지 않다면, ARC는 해당 instance가 사용하던 메모리를 다른 용도로 사용할 수 있도록 해제한다. 따라서, 더이상 필요하지 않다면 class instance는 메모리 공간을 차지하고 있지 않는다.

그러나, 사용되고 있는 instance를 ARC가 해제한다면, 해당 instance property로의 접근이나 method 호출은 불가능하게 되며, 앱은 crash가 발생한다.

여전히 사용중일 때, instance가 사라지지 않음을 보장하기위해, ARC는 얼마나 많은 property, constant, variable 이 각 class instance를 참조하고 있는지 추적한다. ARC는 하나의 참조라도 남아있다면 해제하지 않는다.

이렇게 하기 위해서 class instance를 property, constanct, variable에 할당할 때, instance를 strong reference 하도록 해야한다. 

## ARC in Action

`Person` class가 있고 stored constant property, 생성자, 소멸자가 정의되어 있다.

```swift
class Person {
    let name: String
    init(name: String) {
        self.name = name
        print("\(name) is being initialized")
    }
    deinit {
        print("\(name) is being deinitialized")
    }
}
```

optional person type의 변수 세개를 정의한다. default 값은 nil이다.

```swift
var reference1: Person?
var reference2: Person?
var reference3: Person?
```

첫 변수는 class의 생성자를 통해 instance를 생성하고 참조 값을 할당한다. 나머지는 같은 instance를 참조하도록 한다. 하나의 person instance에는 세개의 참조가 연결되어 있다.

```swift
reference1 = Person(name: "John Appleseed")
// Prints "John Appleseed is being initialized"
reference2 = reference1
reference3 = reference1
```

이 중 처음 두개에 nil을 할당하는 것으로는 instance가 해제되지 않는다. 남은 하나의 강한 참조가 남아있기 때문이고, 이 마저 nil을 할당한다면 메모리에서 해제된다.

```swift
reference1 = nil
reference2 = nil

reference3 = nil
// Prints "John Appleseed is being deinitialized"
```

## Strong Reference Cycles Between Class Instances

위 예시와 같이, ARC는 생성한 class instance로의 참조 개수를 추적할 수 있고, 더이상 필요하지 않을 때 해제할 수 있다.

그러나, class instance가 zero strong reference에 도달하지 못하게 코드를 작성할 수 있다. 두개의 instance가 서로를 강하게 참조하고 있는 경우 발생되며, 이를 strong reference cycle이라고 한다.

strong reference cycle은 class 간 관계를 strong reference 대신에 weak 또는 unowned로 정의하여 해결할 수 있다. 그 전에 이 상황을 먼저 살펴보자.

strong reference cycle이 발생할 수 있는 예시이다. 두 class가 정의되어 있고, 각각은 상대방을 참조할 수 있는 property가 정의되어 있다. 사람은 아파트가 없는 상황이 존재할 수 있고, 아파트는 세입자가 없는 경우가 존재할 수 있기 때문에, optional로 선언하였다.

```swift
class Person {
    let name: String
    init(name: String) { self.name = name }
    var apartment: Apartment?
    deinit { print("\(name) is being deinitialized") }
}

class Apartment {
    let unit: String
    init(unit: String) { self.unit = unit }
    var tenant: Person?
    deinit { print("Apartment \(unit) is being deinitialized") }
}
```

optinal 처리를 할 수 있도록 각 class type의 변수를 정의하고, 값을 할당한다.

```swift
var john: Person?
var unit4A: Apartment?

john = Person(name: "John Appleseed")
unit4A = Apartment(unit: "4A")
```

다음 코드로 이제 서로를 강하게 참조하게 된다.

```swift
john!.apartment = unit4A
unit4A!.tenant = john
```

그리고 두 변수에 nil을 할당하면 strong reference cycle이 발생하게 되며, 메모리에서 해제되지 않아 앱의 memory leak을 유발하게 될 것이다.

```swift
john = nil
unit4A = nil
```

## Resolving Strong Reference Cycles Between Class Instances

class type의 property와 관련된 strong reference cycle을 해결하기 위한 방법으로 weak reference, unowned reference 두가지가 있다. 

이 둘은 reference cycle에서 하나의 instance가 다른 instance를 강하게 참조하지 않는다. 따라서 strong reference cycle을 생성하지 않고 서로를 참조할 수 있다.

weak reference는 다른 instance가 짧은 lifetime을 가질 때 사용하자. 즉, 다른 instance가 먼저 해제될 수 있는 경우이다. 위의 예제에서 아파트는 어느 순간에 세입자가 없는 경우가 생기므로, weak reference를 하는 것이 적합하다고 볼 수 있다. 반면에, 다른 instance가 더 길거나 같은 lifetime을 갖는다면, unowned reference를 사용하자.

### Weak References

weak reference는 참조하는 instance를 강하게 잡고있지 않기 때문에, ARC가 참조된 instance를 해제하는 것을 방해하지 않는다. property나 variable 선언 앞에 weak 키워드를 적어주어 나타낼 수 있다.

weak reference가 참조하고 있더라도, ARC에의해 해당 instance는 해제될 수 있다. ARC는 자동으로 weak reference가 해제된 경우 nil로 설정한다. 그렇기 때문에 weak reference는 optional type이어야 한다.

> Garbage collection 을 사용하는 시스템에서 weak pointer는 단순한 caching mechanism을 구현하는데 사용된다. 그게 가능한 이유는, 메모리 압박이 없을 때, 강한 참조가 없는 객체가 해제되지 않기 때문이다. 그러나 ARC는 마지막 strong reference가 제거되면 값을 해제하기 때문에, weak reference를 GC의 weak pointer 용도로 사용할 수 없다.

### Unowned References

weak reference와 같이 instance를 강하게 참조하지 않는다. 하지만, 다른 instance가 길거나 같은 lifetime을 가질 때에만 사용할 수 있다. unowned 키워드를 property나 variable 선언부 앞에 붙여서 사용한다.

weak reference와 다르게 unowned reference는 값이 항상 있음을 기대한다. 그 결과 unowned로 표시된 값은 optional이 되지 않으며 ARC는 절대 nil로 설정하지 않는다.

> 참조하는 instance가 해제되지 않음을 확신할 수 있는 경우에만 unowned를 사용하자.
>
> 만약, instance가 해제되었는데 unowned reference의 값에 접근하려한다면, runtime errorr가 발생한다.

> Unowned reference는 safe 한 방법이다. swift는 unsafe unowned reference를 제공하는데, 이는 성능상의 이유와 같이 runtime safety check를 비활성화 할 때를 위함이다.
>
> `unowned(unsafe)` 로 선언할 수 있고, 해당 instance가 해제되어도 memory로 접근한다. 즉, dangling pointer로 예상치 못한 결과를 초래할 수 있으며, 사용할 때 이러한 점을 주의해야 한다.

### Unowned Optional References

optional reference 를 unowned 로 선언할 수도 있다. ARC ownership model에서, unowned reference 와 weak reference는 둘다 같은 문맥에서 사용된다. unowned optional reference를 사용할 때의 차이점이라면, 항상 타당한 객체를 참조하고 있는 것을 보장해야하고 그렇지 않으면 nil을 설정해야한다.



### Unowned References and Implicitly Unwrapped Optional Properties

두 property가 항상 값을 가져야 하며, initialization이 완료되면 어떠한 것도 nil이 되면 안되는 상황이 있다. 이 경우 한 class에 unowned property를 사용하고, 다른 class에 implicitly unwrapped optional property를 선언해서 사용하면 된다.

이러면, optional unwrapping 없이, reference cycle도 피하면서 초기화가 완료되면 각 property에 바로 접근할 수 있다. 

아래 예제에는, 두개의 class가 정의돼 있고 서로 다른 class instance를 저장할 수 있는 property가 있다. 

```swift
class Country {
    let name: String
    var capitalCity: City!
    init(name: String, capitalName: String) {
        self.name = name
        self.capitalCity = City(name: capitalName, country: self)
    }
}

class City {
    let name: String
    unowned let country: Country
    init(name: String, country: Country) {
        self.name = name
        self.country = country
    }
}
```

만약, `Country` 의 `capitailCity` property가 implicitly unwrapped optional 이 아니라면, 값이 설정되기 전에 self를 사용할 수 없다. 결과적으로 한줄의 코드로 두 개의 instance를 생성할 수 있게되며, strong reference cycle을 형성하지 않고, property를 사용할 때 unwrap하기 위해 exclamation point를 사용하지 않아도 된다.

```swift
var country = Country(name: "Canada", capitalName: "Ottawa")
print("\(country.name)'s capital city is called \(country.capitalCity.name)")
// Prints "Canada's capital city is called Ottawa"
```



## Strong Reference Cycles for Closures

class의 property로 closure를 할당하고, 그 closure의 body가 instance를 capture하고 있다면, strong reference cycle이 발생할 수 있다. closure의 body에서 `self.someProperty` 와 같이 instance의 다른 property에 접근하거나, `self.someMehtod()` 와 같이 instance의 method를 호출하기 때문에 유발된다. 각각의 경우에서, closure는 self를 capture하여 strong reference cycle을 생성한다.

이러한 이유는 closure 역시 reference type이기 때문이다. 

swift는 *closure capture list* 라는 해결책을 제공한다. 이 해결책에 앞서, self를 참조하는 closure로 인해 strong reference cycle을 생성하는 예제를 보자.

```swift
class HTMLElement {
    let name: String
    let text: String?

    lazy var asHTML: () -> String = {
        if let text = self.text {
            return "<\(self.name)>\(text)</\(self.name)>"
        } else {
            return "<\(self.name) />"
        }
    }

    init(name: String, text: String? = nil) {
        self.name = name
        self.text = text
    }

    deinit {
        print("\(name) is being deinitialized")
    }
}
```

다음과 같이 사용할 수 있으며, paragraph variable에 nil을 할당하여 strong reference 끊어도, instance와 closure는 해제되지 않는다.

```swift
var paragraph: HTMLElement? = HTMLElement(name: "p", text: "hello, world")
print(paragraph!.asHTML())
// Prints "<p>hello, world</p>"

paragraph = nil
```



## Resolving Strong Reference Cycles for Closures

closure 정의의 일부로 capture list를 정의하면 이러한 strong reference cycle을 해결할 수 있다. capture list는 closure body에서 하나 이상의 reference type을 capture할 때의 규칙이다. 

> swift는 closure에서 self의 member를 참조할 때, someProperty 나 someMethod() 대신에 self.someProperty 나 self.someMethod() 형식으로 작성하도록 요구한다. 이는 self를 capture하고 있다는 것을 자각시키기 위함이다.

### Defining a Capture List

capture list의 각 item은 weak 이나 unowned와 참조하는 class instance 의 쌍, 혹은 어떤 값으로 초기화된 변수가 되며, 대괄호 내부에 컴마로 구분한다.

closure parameter와 return type 앞에 위치시킨다. 만약, 추론 가능하여 return type이 없고 parameter도 없다면 in 앞에 위치시킨다.

```swift
lazy var someClosure = {
    [unowned self, weak delegate = self.delegate]
    (index: Int, stringToProcess: String) -> String in
    // closure body goes here
}

lazy var someClosure = {
    [unowned self, weak delegate = self.delegate] in
    // closure body goes here
}
```



### Weak and Unowned References

closure와 capture하는 Instance가 항상 서로를 참조하고있고, 동시에 해제된다면 closure에서 capture를 unowned reference로 정의하자.

대조적으로, capture한 reference가 어느 순간에 nil이 될 수 있다면 weak reference로 정의하자. 

> 만약 capture된 reference가 nil이 될 여지가 없다면 weak이 아닌 unowned로 정의해야한다.

