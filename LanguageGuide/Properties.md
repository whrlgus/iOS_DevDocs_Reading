# Properties

property는 값과 특정 class, structure, enumeration을 연관짓는다. stored property는 instance의 부분으로서, 상수(constant)와 변수(variable) 값을 저장하고, 반면에 computed property는 저장하기 보다는 값을 연산한다. computed property는 class, structure, enumeration에서 제공될 수 있다. stored property는 class와 structure에 의해서만 제공된다.

Stored 와 computed property는 특정 타입의 instance와 연관되어 있다. 그러나, property는 타입 자체와도 관련이 있다. 이러한 property는 type property라고 한다.

Property 값의 변화를 감시하기 위한 property observer를 정의할 수 있어, custom action으로 변화에 반응할 수 있다. property observer는 직접 정의한 stored property에 추가할 수 있고, superclass로부터 상속한 subclass의 property에 추가할 수 있다.

Property wrapper를 사용하여 여러 property의 getter와 setter에 있는 코드를 재활용할 수 있다.



## Stored Properties

가장 간단한 형태로, stored property는 특정 class나 structure instance의 부분인 constant나 variable이다. stored property는 variable stored property나 constant stored property로 나뉜다. 

stored property 정의의 부분으로 default 값을 지정할 수 있다. 초기화 과정에서 stored property의 초기 값을 설정하거나 변경할 수 있다. 초기화할 때 constant stored property는 초기값 할당은 가능하지만, default값 변경은 불가능하다.

### Stored Properties of Constant Structure Instances

structure instance를 생성하고 constant로 할당한다면, variable property라고 할지라도 그 값을 변경하지 못한다. 이러한 점은 structure가 value type이기 때문이다. Value type의 instance가 constant라면 모든 property도 constant인 것이다.

반면에, reference type인 class에는 해당이 안된다. reference type의 instance는 constant로 할당해도 variable property의 값은 변경할 수 있다.

### Lazy Stored Properties

lazy stored property는 처음 사용하기 전까지 초기 값이 계산되지 않는 property이다. lazy modifier(수식어구, 변경자)를 property 선언부 앞에 적어주면된다. 

> NOTE
>
> lazy property는 항상 변수로 선언해야 한다. 왜냐하면, 초기 값이 초기화가 끝난 이후에 사용될 수 있기 때문이다. constant property는 초기화가 완료되기 이전에 항상 값을 가지고 있어야 하기 때문에, lazy로 선언할 수 없다.

instance의 초기화가 끝나기 이전에는 값을 알 수 없는, 초기값이 외부 요소에 종속적인 property에 적용하기에 유용하다. 또한, 필요하지 않은 경우 수행하면 안되는, 복잡하고 무거운 연산을 요구하는 초기값을 갖는 property에도 적용할 수 있다. 

> NOTE
>
> lazy property로 동시에 접근할 수 있는 thread가 여러개 있고, 아직 초기화 되지 않은 상태라면, 단 한번만 초기화 된다고 보장할 수 없다.

### Stored Properties and Instance Variables

Objective c를 경험하지 않아 이해하기 어렵다...



## Computed Properties

class, structure, enumeration에서 값을 저장하지 않는 computed property를 정의할 수 있다. getter와 optional setter를 제공하여 다른 property의 값을 설정하고 가져올 수 있다. 

### Shorthand Setter Declaration

만약 computed property의 setter에 새로 설정될 값의 이름을 정의하지 않았다면, 기본적으로 `newValue` 라는 이름으로 사용할 수 있다. 

#### Shorthand Getter Declaration

만약 getter의 전체 body가 단일 expression이라면, getter는 암묵적으로 그 expression을 반환한다.

### Read-Only Computed Properties

setter는 없고 getter만 있는 computed property는 read-only computed property이다. 다른 값을 설정할 수는 없으며, dot syntax로 접근만 가능하다. 

> NOTE
>
> computed property는 값이 고정되어 있지 않기 때문에 variable로 선언해야 한다. `let` 키워드는 constant property 에만 사용되어, instance 초기화의 부분으로서 한번 값이 설정되면 변경할 수 없음을 의미한다.

간단하게 `get` 키워드를 없애고 read-only computed property를 선언할 수 있다.



## Property Observers

property observer는 property 값의 변경을 감시하여 반응한다. property 값이 설정될 때마다 호출되며, 새로운 값이 현재 값과 동일해도 호출된다.

다음과 같은 장소에 property observer를 추가할 수 있다.

- 정의한 stored property
- 상속한 stored property
- 상속한 computed property

다음 둘 중 하나 혹은 두가지의 observer를 property에 추가할 수 있다.

- `willSet` 은 값이 저장되기 직전에 호출된다.
- `didSet` 은 새로운 값이 저장된 직후에 호출된다.

> NOTE
>
> superclass property의 `willSet` 과 `didSet` observer는 superclass 생성자가 호출된 이후, subclass 생성자에서 property 값이 설정될 때 호출된다. Superclass 생성자가 호출되기 이전에 class의 property를 세팅할 때에는 호출되지 않는다.

> NOTE
>
> observer를 가진 property를 함수의 in-out parameter로 넘긴다면, `willSet` 과 `didSet` observer가 호출된다. 이는 in-out parameter의 copy-in copy-out 메모리 모델때문이다. 함수의 마지막에 항상 property로 값이 쓰여진다.

