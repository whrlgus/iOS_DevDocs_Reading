# 8. State & Data Flow - Part1

## 8.1 MVC: The Mammoth View Controller

**View**는 UI, **Model**은 데이터, **Controller**는 model과 view의 동기화를 담당. controller에서 자동으로 동기화가 처리되지 않아, 일일이 연결해줘야한다.

이러한 동기화 작업의 필요성으로 view와 controller는 더이상 분리된 개체가 아닌 형태로 변질되었다.

스유 이전에는...

- Massive view controller 문제
- model과 UI 동기화 작업을 수동으로 처리
- UI와 상태가 항상 동기화되진 않음
- view와 subview 사이에서 상태와 데이터를 갱신해줘야 함
- 에러/버그 유발 가능성이 높음

## 8.2 A functional user interface

실용적인 UI: 중간 상태가 없다. 따라서, 상태 변경에 따라 수동으로 처리할 일이 없다

순환 참조 문제를 고려하지 않아도 된다: view는 참조 타입이 아닌 값 타입이므로, capture시에 참조가 아닌 복사를 한다.

스유의 주요 장점

- **Declarative**: UI 구현을 하지 않아도 된다. 그냥 선언만...
- **Functional**: 같은 상태가 주어지면, 같은 UI가 만들어진다. 다르게 표현하면 UI는 상태를 입력으로 하는 함수다.
- **Reactive**: 상태가 변하면 스유는 자동으로 UI를 갱신한다.

## 8.3 State

### Embedding the state into a struct

struct는 값 타입이고 이런 뷰의 내부 상태를 변경하는 시도는 허용되지 않는다.

### Embedding the state into a class

model은 변경되지만, UI는 갱신되지 않는다.

### Wrap to class, embed to struct

### The real State

> `State` 는 값을 읽고 쓸 수 있는 property wrapper type으로 스유에 의해 관리된다.

> 스유는 state로 선언된 모든 property의 저장소를 관리한다. State 값이 갱신되면, view는 body를 다시 구성한다. 이런 상태는 single source of truth 로서 사용해야 한다.

`@State` attribute로 선언한 프로퍼티는 property wrapper이며, 컴파일러가 `State<Value>` 타입의 실제 구현(underscore를 접미사로 하는)을 생성해준다.

### Not everything is reactive

필요한 경우만 상태 값으로 관리하자

## 8.4 Using binding for two-way reactions

### How binding is (not) handled in UIKit

값의 변화를 감지하기 위해서 delegate을 사용하거나 notification을 subscribe

### Owning the reference, not the data

데이터를 소유하지 않고 다른 곳에 저장된 데이터를 참조하기 때문에, 모델이 변경될 때 UI를 자동으로 갱신할 수 있다. 스유는 어떤 요소가 모델을 참조하는지 알기 때문에, UI의 어떤 부분을 갱신해야 할 지 구분할 수 있다.

이 동작이 가능하게 하기 위해서 binding이라는 정교한 방식의 참조 핸들링을 사용한다.

> **binding** 은 property(데이터 저장)와 view(데이터를 보여주고 갱신) 사이의 양방향 연결이다. binding은 데이터를 직접 저장하는 대신에, property를 어딘가에 저장된 *source of truth* 에 연결한다.

State property는 `projectedValue` 에 binding을 포함한다.

### Defining the single source of truth

데이터는 단일 개체에 의해 소유되어야 한다. 그리고 다른 개체는 동일한 데이터에 접근해야 하며, 복사해서는 안된다.

State property는 각자의 실제 상태를 가지고 있다. 이들을 single source of truth 상태로 유지하기 위해서는 binding을 이용하여 참조값 복사를 통해 단일 저장소를 공유해야 한다.

## 8.5 Key points

- `@State` 을 사용하여 프로퍼티를 선언하면, 선언된 뷰가 그 데이터를 소유하게 된다. 이 property 값이 변경되면, 이 property를 사용하는 UI 는 자동적으로 다시 그려지게 된다.
- `@Binding` 로는 state property와 유사한 property를 생성할 수 있다. 하지만, 그 데이터는 다른 곳에 저장되며 다른 곳에서 소유하게 된다.