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

Publish subject가 `completed` 나 `error` 이벤트(stop 이벤트)를 받으면, 새로운 subscriber에게는 next 이벤트를 방출하지 않고, stop 이벤트를 재방출한다. 따라서, 구독을 할 때 종료되었다는 것을 알리는 처리(stop 이벤트에 대한 처리)를 하는 것이 사소한 버그를 유발시키지 않는다.

## 3.4 Working with bahavior subjects

Behavior subject는 publish subject와 유사하게 작동한다. 다만, 가장 최근 next 이벤트를 새로운 subscriber에게 전달한다는 점이 다르다.

behavior subject는 가장 최근 데이터로 뷰를 미리 생산하기 원할 때 유용하다. 예를 들어, 사용자 프로필 화면의 컨트롤을 behavior subject와 연결할 수 있는데, 앱이 새로운 데이터를 가져올 동안 화면을 구성할 수가 있다.

bahavior subject는 가장 최근 값을 새로운 subscriber에게 전달하기 때문에, "요청이 로딩중이다" 혹은 "시간이 9:41 이다" 와 같은 상태를 모델링할 때 좋은 선택지가 될 것이다.

가장 최근 값 뿐만 아니라 더 많은 값을 보여주기 위할 때에는, 가장 최근 검색어 5개와 같은, replay subject를 사용하자.

## 3.5 Working with replay subjects

replay subject는 최근 방출한 요소들을 설정한 크기만큼 임시 저장하고 있다.  그리고는 새로운 subscriber에게 버퍼를 전달한다.

이미지나 배열을 replay subject의 요소로 구성하기에는 많은 메모리 사용에 주의해야 한다.

 현재 값을 가져오기 위해서는 relay를 사용하자.

## 3.6 Working with relays

relay는 replay 행위를 유지하는 subject를 감싼 것이다. 다른 subject와 다르게 accept 메소드를 사용하여 값을 추가한다. 다른 말로는 onNext를 사용하지 않는다. 왜냐하면 relay는 값만 허용하며 error나 completed 이벤트를 추가할 수 없기 때문이다.

PublishRelay는 PublishSubject를 BehaviorRelay는 BehaviorSubject를 감싼다. 감싸진 subject와 relay를 구분하는 것은 relay는 종료되지 않음을 보장한다는 점이다.

Behavior relay는 현재 값을 언제든지 읽을 수 있다는 점에서 imperative 세계와 reactive 세계를 연결해준다.

