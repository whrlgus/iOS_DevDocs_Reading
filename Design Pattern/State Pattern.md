상태 패턴은 객체가 런타임에 그 상태를 바꿀 수 있도록 허용하는 행동 패턴이다. 여기서 "상태" 는 주어진 객체가 주어진 시간에 어떻게 행동해야 할지를 설명하는 데이터의 집합을 의미한다.

이 패턴은 세 가지 유형들을 포함한다:

<img src="https://assets.alexandria.raywenderlich.com/books/des/images/41864d4b83222c0a696afc673446e202e63bf0596a7685923a0d4f3ccf89df10/original.png" width=400/>

1. **context** 는 현재 상태를 가지고 있는 객체이며 그 행동이 변화한다.
2. **state protocol** 은 필요한 메소드와 속성들을 정의한다. 개발자들은 대게 프로토콜 대신에 **base state class** 를 사용한다. 이렇게 하면, 베이스에 저장 속성을 정의할 수 있지만, 프로토콜을 사용할 수 없다. 베이스 클래스가 사용되더라도 직접 초기화되는 것을 의도하지는 않고, 상속될 목적으로 정의된다. 다른 언어에서 이것은 `abstract class` 이다. 스위프트는 `abstract` 클래스가 없어서 이 클래스는 컨벤션에 의해서만 초기화되지 않을 뿐이다.
3. **concrete states** 는 상태 프로토콜을 따르거나, 베이스 클래스를 사용한 경우에는 베이스의 서브클래스이다. 컨택스트는 현재 상태를 유지하지만, 구체 상태의 타입을 알지는 못한다. 대신에 컨택스트는 다형성을 사용하여 행동을 바꾼다: 구체 상태는 컨택스트가 어떻게 행동해야 하는지 정의한다. 만약 새로운 행동이 필요하면 새로운 구체 상태를 정의하면 된다.

하지만 중요한 질문이 남아있다: 컨택스트의 현재 상태를 바꾸기 위해 실제로 코드를 어디에 두어야 할까? 컨택스트 내부에, 구체 상태 혹은 다른 곳에?

상태 패턴은 상태를 바꾸기 위한 로직을 어디에 둘 지 정해주지 않는다. 대신에 우리가 결정해야 한다. 이 부분은 이 패턴의 강점이자 약점이다: 유연하게 설계할 수 있지만 동시에 완전한 지침을 제공하지 않는다.

이 챕터에서 각각의 위치에 두는 두가지 방법을 살펴볼 것이다.

## When should you use it?
두개 이상의 상태가 일생동안 변경되는 시스템을 생성하기 위해 상태 패턴을 사용하자. 상태들은 수의 제한이 있을 수(a "closed" set)도 있고 없을 수(an "open" set)도 있다. 예를 들어, 신호등은 신호의 상태를 닫힌 집합으로 정의할 수 있다. 가장 단순한 경우에, 초록에서 노랑, 빨강, 다시 초록으로 진행한다.

애니메이션 엔진은 애니메이션 상태의 열린 집합으로 정의될 수 있다. 제한 없이 회전, 이동 할 수 있고, 일생동안에 진행되는 다른 애니메이션을 가질 수도 있다.

열린 집합과 닫힌 집합의 두 상태 패턴 구현은 행동을 바꾸기 위해 다형성을 이용한다. 결과적으로, 종종 `switch` 와 `if` - `else` 문을 없앨 수 있다.

컨택스트에서 복잡한 상태를 추적하는 대신에, 현재 상태로의 호출을 거치게 된다; 예제를 통해 살펴볼 것이다. 만약 `switch` 와 `if` - `else` 문이 많은 클래스를 가지고 있다면, 대신에 상태 패턴을 사용하여 정의해보자. 결과적으로 더 유연하고 유지하기 쉬운 시스템을 생성하게 될 것이다.

## Playground example


## What should you be careful about?
컨텍스트와 구체 상태들 간에 강한 결합을 형성하는 것에 주의하자. 다른 컨텍스트에서 상태를 재사용하기 원한다면, 특정 컨텍스트에서 구체 상태가 메소드를 호출하게 하는 대신, 구체 상태와 컨텍스트 사이에 프로토콜을 두자.

상태 변화 로직을 상태들에 두게 된다면, 한 상태에서 다른 상태로의 강한 결합에 주의하자.

상태에서 다른 상태로 전환을 원한다면 생성자나 속성을 통해 다음 상태를 넘겨주자.

## Tutorial project


## Key points
- 상태 패턴은 런타임에 객체가 그 행동을 변경하도록 허용한다. 세가지 타입으로 구성된다: 컨텍스트, 상태 프로토콜, 구체 상태.
- **컨택스트(context)** 는 현재 상태를 가지고 있는 객체이다; **상태 프로토콜(state protocol)** 은 필요한 메소드와 속성들을 정의한다; 그리고 **구체 상태(concrete state)** 는 상태 프로토콜과 런타임에 변하는 실제 행동을 구현한다
- 상태 패턴은 전환 로직을 상태들 사이 중 어느 곳에 둘 지 알려주지 않는다. 대신에 우리에게 결정하도록 한다: 우리는 이 로직을 컨택스트나 구체 상태에 둘 수 있다.