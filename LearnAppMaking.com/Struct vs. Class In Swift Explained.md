[원문](https://learnappmaking.com/struct-vs-class-swift-how-to/)

class와 struct의 차이는 무엇일까? 기본적으로 struct를 사용하는 것이 좋다. 왜? 그러면 class는 언제 사용해야할까?

이 글에서는 struct와 class에 대해 살펴볼 것이다. 언제 class와 struct를 사용하는지? 둘의 차이점은 무엇인지? 실제 iOS 개발에서 어떤 영향을 끼치는지?

struct는 swift의 강력한 특징 중 하나이다. 코드를 재사용 가능하며, 유연하게 만들고 결합도를 낮춘다. 

글의 순서는 다음과 같다.

1. At A Glance: Classes vs. Structs
2. When Should You Use Structs?
3. When Should You Use Classes?



## At A Glance: Classes vs. Structs

우선 둘의 공통점을 살펴보자.

- 값을 저장하기 위한 property를 정의할 수 있고, function을 정의할 수 있다.
- subscript syntax로 값에 접근할 수 있는 subscript를 정의할 수 있다.
- extension을 이용해 확장가능하다.
- POP(Protocol Oriented Programming)을 지원하기 위해, protocol을 채택할 수 있다.

class만 가지고 있는 특징은 다음과 같다.

- UIViewController를 상속하여 subclass를 만드는 것과 같이, 다른 class를 상속할 수 있다.
- deinitiailizer를 정의할 수 있고, instance가 사라지기 전에 수행할 내용을 내부에 구현할 수 있다.
- class는 reference type이고, struct는 value type이다.

마지막 항목이 중요한데, 해당 내용은 다음과 같다.

- Value Type: value type을 복사(할당, 초기화, 함수 인자로 전달 등에 의한) 하면, 각 instance는 data의 고유한 복사본은 유지한다. 만약, 하나의 instance를 변경해도 다른 instance에는 영향을 주지 않는다.
- Reference Type: reference type은 복사하면, 각 instance는 data를 공유하게 된다. 참조 자체가 복사되는 것이지 참조하는 값이 복사되는 것이 아니다. 하나를 변경하면 다른 하나도 변경되는 것이다.

즉, value type은 값을 복사하고, reference type은 참조를 복사한다. 이 차이가 class와 struct, 둘 중에 어느 것을 고르는 지에 영향을 준다.



## When Should You Use Structs?

기본적으로 struct를 사용하는 것을 장려한다.

- 단순한 data type에 struct를 사용하자. NewsItem, Task, User와 같은 database 객체를 전달하는 것을 생각해보자. 이들은 명확히 정의돼 있고, 객체 간의 관계를 고려할 필요가 없기 때문에, struct를 사용하는 것이 더 간단하다.
- Multi-threaded 환경에서, 서로 다른 thread에 network 연결이 개방돼 있다면, struct를 사용하는 것이 더 안전하다. Race condition 이나 deadlock 과 같은 위험성 없이 한 thread에서 다른 thread로 복사할 수 있다. class는 thread-safe 하게 설계하지 않는 한, 이러한 struct 고유의 안전성을 갖지 않는다. 
- string과 같은 value type의 property가 대부분이라면 이들을 class가 아닌 struct로 감싸는 것이 이치에 맞다. 주의할 점은 struct가 property로 class instance를 갖는 것이다. reference type으로 shared class instance를 참조한다는 사실을 인지하지 못하면 의도치 않은 결과가 발생할 것이다.

struct를 사용하면 추가적인 이점이 있다. 바로, data 변화를 추론하기 쉽다는 점이다. type이 struct라면, 다른 부분에서 이 객체를 참조하고 있지 않다는 것을 확신할 수 있다. 명시적으로 변경하는 코드를 작성하지 않는 한, 코드의 다른 부분에 의한 변경을 이뤄질 수 없다.



## When Should You Use Classes?

만약, class 만이 가지고 있는 특징을 사용할 필요가 있다면, 그땐 class를 사용하자. 

- class는 다른 class를 상속할 수 있다. `class MyViewController: UIViewController` 와 같이 다른 class 를 상속하여 subclass화 할 수 있다. struct는 상속이 불가능하며, protocol을 채택하여 유사한 계층 구조를 만들 수 있다.
- class는 deinit function을 구현할 수 있고, 하나의 instance에 여러 참조를 생성할 수 있다.
- 참조 타입으로서 identity를 확인하기 위한 수단이 존재한다. 같은 객체(variable, constant, property)인지 확인하기 위해서 === 연산자를 사용한다.

만약, Objective-C 와 상호 운용이 가능하게 하려면 class를 사용해야 한다. 예를 들어, `@objc` 나 realm data model에서의 `dynamic` 을 사용하고자 한다면, 해당 model은 반드시 class여야 한다.

identity와 reference 개념을 바탕으로, 다음과 같은 시나리오에서 class를 사용하는 것이 적합하다.

- instance를 복사하는 것이 이치에 맞지 않는 경우. 예를 들어 `Window` 나 `UIViewController` 는 한번에 활성화 되어있는 것이 하나이기 때문에 instance를 복사하는 것은 조리에 맞지 않는다. 하나의 instance를 여러 군데에서 사용하는 경우가 있는데, struct로 구현하게 되면 instance를 복사하게 되어 값의 변경을 처리하여 동기화하기가 까다롭기 때문이다.
- databaseconnection이나 temporaryfile같은 경우도 동일
- `CGContext` 와 같이 외부 상태를 위한 전달자 역할을 하는 경우. 이러한 역할을 위해 helper 나 wrapper class 를 정의하게 된다. 이 class는 값을 전달하는 전달자 역할만 수행하며, 이 instance를 복사하는 것은 이치에 맞지 않다.

요약하자면, 상속, identity, objective-c interoperability과 같이 class 만이 가진 특징을 사용하고자 할 때, 그리고 값을 복사하는 것이 이치에 맞지 않는 경우에 class를 사용하자.

