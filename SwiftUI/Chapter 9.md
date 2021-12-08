# 9. State & Data Flow - Part 2

## 9.1 The art of observation

struct 로 선언된 인스턴스는 내부 property가 변경되면 전체 인스턴스를 복사하여 갱신하게 된다. 따라서, 일부의 변경으로 그 인스턴스를 참조하는 모든 곳에서 비효율적으로 갱신이 이뤄지게 된다.

model을 참조 타입으로 구현한다면, 새로운 참조를 할당할 때에 변형될 것이고, 그 때만 UI를 갱신하게 될 것이다.

### Making an Object Observable

앞선 내용에 따르면, 커스텀 모델은

- 참조 타입이어야 하고, 
- 어떤 property가 UI를 갱신할 지 구분할 수 있어야 한다.

이에 세가지 새로운 타입이 필요하다:

- **class**를 관측가능하게 선언할 수 있는 타입. 이 타입은 state property와 유사하게 사용할 수 있게 할 수 있다.
- **class property**를 관측가능하게 선언할 수 있는 타입.
- **관측가능한 class 타입의 instance인 property**를 관측되도록 하는 타입. 이 타입은 뷰에서 observable class를 observed property로 사용할 수 있게 할 수 있다.

Class 를 관측가능하게 만들기 위해서 `ObservableObject` 를 채택하도록 해야한다. 이 class는 **publisher** 가 된다. 이 protocol은 단 하나의 `objectWillChange`  property를 정의하고 있다.

`ObservableObject`  의 property를 `@Published` attribute를 이용하여 선언하면, 뷰에서 state property로 동작하게 된다. 그리고 state property와 동일하게 published property에도 아래 사항이 적용된다.

- Published property는 값 타입이어야 한다.
- struct에 많은 property를 포함하면 안된다.

### Observing an Object

Published property는 state property와 유사하다.

- Single source of truth를 정의하고
- binding을 가지고 있으며,
- 값이 갱신될 때마다 그 값을 참조하는 UI를 갱신한다.

## 9.2 sharing in the environment

Singleton 방식으로 문제를 해결하기 좋은 경우가 있다. 다만, 사용하기 좋은 패턴은 아니다. 불필요한 의존성을 형성하며 의존 주입과 같은 다른 패턴을 사용하는 것을 피하게 된다.

### Environment and Objects

객체를 가방에 넣어두고 필요할 때 꺼내 쓰는 방식이며, 가방은 **environment** 객체는 **environment object** 에 해당한다.

이 패턴은 두가지의 흔한 스유 방식을 이용하게 된다: modifier와 attribute

- `environmentObject(_:)` 를 사용하여 object를 environment에 주입한다.
- `@EnvironmentObject`를 사용하여 environment에서 object(참조)를 꺼내 property에 저장한다.

> Note: environment에 이름 없이 instance를 주입한다. `@EnvironmentObject` 를 사용하여 꺼낼 때에는 instance type을 명시해야 한다. environment에는 타입 별로 하나의 instance만 주입할 수 있다. 다른 instance를 주입하면, 첫번째 것으로 대체된다.

### Environment and duplicates (to avoid)



## 9.3 Object Ownership

## 9.4 Understanding environment properties

## 9.5 Key points