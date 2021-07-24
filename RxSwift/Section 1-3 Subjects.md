# Chapter 3. Subjects

observable의 대한 학습으로, 어떻게 생성하는지, 어떻게 구독하는지, 어떻게 처분하는지 알게 되었음. 본질적으로 읽기만 가능하다. 따라서 observable을 구독하여 생성된 새로운 이벤트에 대한 알림만 받을 수 있다.

보통 앱 개발시에는 런타임에 subscriber로 방출하기 위한 새로운 값을 observable에 수동으로 추가하는 것이다. 그것은 observable과 **observer**로서의 동작을 동시에 할 수 있어야 한다. 이것을 **subject**라고 부른다.

이 챕터에서는 여러 타입의 subject를 배울 것이고, 각 타입을 어떻게 사용하는지, 일반적인 use case에 근거하여 왜 다른 것이 아닌 특정 타입을 사용해야 하는지 배울 것이다. relay는 subject의 wrapper로 이것 또한 다룰 것이다.

PublishSubject는 적절히 이름지어졌다. 이것은 정보를 받고 subscriber에게 전달한다. 단, 현재 subscriber에게만 방출하며, 이벤트 방출 이후에 구독했다면 값을 전달받지 못한다.



## 3.2 What are subjects?

subject는 observable과 observer의 역할을 수행한다. (값을 받고 방출할 수 있음.) RsSwift에는 4가지의 subject가 있다.

- `PublishSubject`: 빈 채로 시작하여 새로운 요소만 subscriber에게 방출한다.
- `BehaviorSubject`: 초기값으로 시작하며, 새로운 subscriber에게 최근 요소만 방출한다.
- `ReplaySubject`: 버퍼 크기와 함께 초기화되어, 크기만큼의 요소를 저장하고 새로운 subscriber에게 방출한다.
- `AsyncSubject`: sequence에서 마지막 `next` 이벤트만 방출하고, subject가 `completed` 이벤트를 받을때만 방출이 이루어 진다. 자주 사용되는 것이 아니라 이 책에서는 다루지 않는다.

RxSwift는 Relay라고 부르는 개념도 제공한다. `PublishRelay` 와 `BehaviorRelay`가 있다. 각각의 subject를 감싸며, `next` 이벤트만을 허용하며 넘겨줄 수 있다. relay에 `completed` 나 `error` 이벤트를 전혀 추가할 수 없다. 때문에, 종료되지 않는 sequence를 형성할 때 사용하기 좋다.



## 3.3 Working with publish subjects

publish subject는 subscriber가 구독하는 시점에 새로운 이벤트에 대한 알림을 받아, subscriber가 구독을 취소하거나, subject가 completed 나 error 이벤트를 방출하여 종료될 때까지 유지하기 원하는 상황에 사용하기 좋다.



 