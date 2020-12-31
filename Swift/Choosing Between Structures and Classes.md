# Choosing Between Structures and Classes

## Overview

structure나 class는 앱에서 데이터를 저장하거나 행동 모형을 만드는 데 사용한다. 그러나 둘의 유사성으로 둘 중 하나를 선택하는데 어려움이 있다.

다음 장려사항을 참조하여 선택하자.

- 기본적으로 structure를 사용하자.
- Objective-C 와 상호 운용할 필요가 있다면 class를 사용하자.
- 설계한 data model의 identity(동일성, 일치)를 제어할 필요가 있다면 class를 사용하자.
- 행동을 채택하기 위해서는 구현사항을 공유하는 protocol과 함께 structure를 사용하자.



## Choose Structures by Default

일반적인 data 유형을 표현하기 위해 structure를 사용하자. 다른 언어에서 class에만 한정된 특징이 swift에는 많은 부분 가능해졌다. stored property, computed property, 그리고 method를 포함할 수 있다. 게다가, protocol을 채택하여 기본 구현을 통해 행동을 정의할 수 있다. swift의 표준 라이브러리와 Foundation은 numbers, strings, arrays, 그리고 dictionaries 타입을 structure로 선언하여 사용한다.

structure를 사용함으로써 앱의 전체 상태를 고려하지 않고도 코드의 부분을 추론하기 쉽도록 해준다. 왜냐하면 structure는 value type으로 지역적인 변화는 의도적으로 외부와 교류하지 않는 한 외부에 보이지 않는다. 결과적으로, 함수 호출을 신경쓰지 않고 코드의 부분만 보고도 instance의 변화를 확신할 수 있다. 



## Use Classes When You Need Objective-C Interoperability

만약, data를 처리하기 위해 Objective-C API를 사용한다면, 혹은 data model을 Objective-C framework에 정의된 class 계층에서 사용한다면 class와 class 상속을 사용해야 한다. 예를 들어, 많은 Objective-C framework는 사용할 때 subclass를 의도하여 설계되었다.



## Use Classes When You Need to Control Identity

swift의 class 는 reference type이기 때문에 동일성에 대한 내장된 개념을 지니고 있다. 즉, 두개의 class instance가 동일한 값의 stored property를 가지고 있다고 해도, 그 둘은 동일성에서 다를 수 있다. 다르게 표현하면, 앱에서 class instance를 공유한다면, instance의 변화는 그 instance를 참조하고 있는 모든 곳에 영향을 주게 된다. 이러한 동일성을 지니게 하고 싶다면 class를 사용하자. 일반적인 용례로는 file handler, network connection, 그리고 CBCentralManager와 같은 shared hardware intermediaries가 있다.

예를 들어, 만약 local database connection을 나타내는 type을 갖는다면, 해당 database로의 접근을 관리하는 코드는 앱에서 보이는 것처럼 database의 상태를 제어할 수 있어야 한다. 이 경우에 class를 사용하는 것이 적합하며, 앱에서 database에 접근 가능한 부분의 제한을 둬야 한다.

> identity는 주의깊게 다뤄야 한다. 앱에서 만연하게 shared class instance를 사용하는 것은 logic error를 유발한다. 많은 곳에서 공유하는 instance의 변화는 결과를 예측하기 어렵고, 수정하는 데 더 많은 작업을 할 수 있다.



## Use Structure When You Don't Control Identity

개체에 대한 identity 정보를 가지고 있는 모델의 경우 structure를 사용하자.

원격 database를 참고하는 앱의 경우, instance의 identity는 외부 개체의 소유이며, identifier에 의해 교류한다. 만약 앱 model의 일관성이 서버에 저장된다면, model을 식별자와 함께 structure로 형성할 수 있다. 



## Use Structures and Protocols to Model Inheritance and Share behavior

structure와 class 둘다 상속의 형태를 지원한다. structure와 protocol은 protocol만 채택할 수 있고, class는 상속하지 못한다. 그러나, class 로 구성하는 상속 계층의 유형은 protocol 상속과 structure 사용으로 구현 가능하다. 

만약 무에서 상속 관계를 형성하고자 할 때, protocol 상속을 사용하자. class 상속은 다른 class와만 가능하지만, protocol은 class, structure, enumeration에 적용 가능하다. data를 어떻게 형성할 지 선택할 때, 우선 protocol 상속을 사용하여 data type의 계층을 구성하고, structure에 해당 protocol을 채택하도록 하자.