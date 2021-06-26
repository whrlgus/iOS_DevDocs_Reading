# Chapter 1. Hello, RxSwift!

RxSwift는 observable sequence와 함수형 스타일의 operator를 사용하여(이로써 스케줄러를 통해 parameterized execution이 가능), 비동기와 이벤트 기반 코드를 구성하는 라이브러리이다. (Parameterized excution은 준비된 statement에 파라미터 즉, 변수만 넘기면 실행되는 것을 말한다.)

본질적으로, RxSwift는 우리의 코드를 새로운 데이터에 반응하게 하고 순차적, 독립적으로 처리할 수 있게 하여, 비동기 프로그램 개발을 단순화한다.

일단은 Deterministic(같은 input -> 같은 output) asynchronous 코드를 작성하는데 도움이 된다!!

## 1.1 Introduction to asynchrounous programming

## 1.2 Foundation of RxSwift

### Observables

`Observable<Element>` 는 Rx 코드의 기반을 제공한다: `Element` 타입에 해당하는 불변의 스냅샷 데이터를 운반할 수 있는, 이벤트 시퀀스를 비동기적으로 생산. 간단하게 말해서, 소비자가 다른 객체에서 발생한 이벤트 혹은 값을 구독할 수 있게 해준다.

이 `Observable` class는 하나 이상의 observer가 실시간으로 어떠한 이벤트에도 반응할 수 있게 해주고 앱의 UI를 갱신할 수 있게 해준다. 또는 새로운 데이터를 처리하고 이용할 수 있게 해준다.

`ObservableType` protocol(`Observable`이 채택하는) 은 단순하다. `Observable` 은 세가지 유형의 이벤트만 방출할 수 있다.(다르게 말해서 observer는 세가지 유형의 이벤트만 받을 수 있다)

- **A `next` event**: latest(또는 next) 데이터 값을 운반하는 이벤트. observer들이 값들을 받게 되는 방식이다. `Observable` 은 종료하는 이벤트가 방출되기 전까지, 이러한 값들을 무한정 방출할 수 있다.
- **A `completed` event**: 이 이벤트는 event sequence를 성공적으로 마무리한다. 즉, `Observable` 은 자신의 lifecyle을 성공적으로 완료하고, 더이상의 이벤트를 내보내지 않는 것을 의미한다.
- **An `error` event**: `Observable` 은 error와 함께 종료되며, 더이상의 이벤트를 내보내지 않는다.

실 사용의 예를 확인하기 위해, finite 과 infinite, 두 유형의 observable sequence를 확인해보자.

#### Finite observable sequences

어떤 observable sequence들은 하나 이상의 값을 방출하거나 아무 값도 방출하지 않으며, 나중에는 성공적으로 종료되거나 에러와 함께 종료된다.

iOS 앱에서, 인터넷에서 파일을 다운로드 받는 코드를 고려해보자:

- 우선, 다운로드를 시작하고 인입되는 데이터를 관측하기 시작한다.
- 그리고 파일의 일부분이 도착하면, 계속하여 데이터 덩어리를 받는다.
- 네트워크 연결에 문제가 생기면, 다운로드는 중단되어 연결은 에러와 함께 종료된다.
- 반대로, 파일의 모든 데이터를 다운로드 받는다면, 성공적으로 종료된다.

이러한 작업흐름은 전형적인 observable의 lifecycle을 정확히 묘사한다.

```swift
API.download(file: "http://www...")
   .subscribe(
     onNext: { data in
      // Append data to temporary file
     },
     onError: { error in
       // Display error to user
     },
     onCompleted: {
       // Use downloaded file
     }
   )
```

`API.download(file:)` 은 네트워크로부터 가져온 데이터 덩어리에 해당하는 `Data` 값을 방출하는 `Observable<Data>` instance를 반환한다. 

`onNext` closure를 제공하여 `next` event를 구독한다. 다운로드 예제에서, 디스크에 저장되는 임시 파일에 데이터를 추가한다.

`onError` closure를 제공하여 `error` 를 구독한다. 이 closure에서, `error.localizedDescription` 을 alert box에 보여주거나 다른 방식으로 에러를 처리한다.

마지막으로 `completed` event를 처리하기 위해, `onCompleted` closure를 제공하여, 다운로드된 파일을 보여주기 위한 로직을 수행할 수 있다.

#### Infinite observable sequences

자연적으로나 강제적으로 종료되는 상황과 다르게, UI event와 같은 무한정 observable sequence도 존재한다.

예를 들어, 앱에서 기기의 방향 변화에 반응해야 하는 코드를 고려해보자:

- 특정 class를  `NotificationCenter` 로부터 `UIDeviceOrientationDidChange` 알림의 observer로 추가한다.
- 그리고 방향 변화를 처리하기 위한 method callback을 제공한다. 현재 방향을 가지고 있어야 하며, 최신 값에 따라 반응해야 한다.

이러한 방향 변화에 대한 sequence(차례? 연속?)는 자연적인 끝이 없다. 게다가 이 sequence는 사실상 무한하고 상태 보존적이므로, 관측을 시작할 때에 항상 초기 값을 갖게 된다.

```swift
UIDevice.rx.orientation
  .subscribe(onNext: { current in
    switch current {
    case .landscape:
      // Re-arrange UI for landscape
    case .portrait:
      // Re-arrange UI for portrait
    }
  })
```

`UIDevice.rx.orientation`은 `Observable<Orientation>`을 제공하는 가상의 control property이다. 이것을 구독하여 현재 방향에 따라 앱 UI를 갱신한다. `onError`와 `onCompleted` 인자는 사용하지 않는다.(관련 이벤트는 방출하지 않기 때문)

### Operators

`ObservableType` 과 `Observable` class의 구현은 별개의 비동기 작업과 이벤트 조작을 추상화하는 여러 method를 포함한다. 그리고 이들을 조합하여 더 복잡한 로직을 구현할 수 있다. 이들은 결합도가 낮고 조합이 가능하기 때문에 **operator**라고 불리기도 한다.

이 operator들은 비동기 입력을 포함하며 side effect를 유발하지 않는 출력을 생산하기 때문에, 퍼즐 조각들과 같이 서로 쉽게 어울려 큰 그림을 만들어 낼 수 있다. 

 

### Schedulers

scheduler는 dispatch queue나 operation queue와 동등한 것이다.  이것이 특정 작업의 execution context(배경, 상황)를 정의할 수 있게 해준다.



## 1.3 App architecture

RxSwift와 MVVM은 특히 잘 어울린다. 그 이유는 뷰모델은 `Observable` 프로퍼티를 노출시키며, 뷰컨 glue code의 UIKit 컨트롤에 바로 결합할 수 있기 때문이다. 이는 모델 데이터를 UI에 결합시키는 것을 간단하게 표현할 수 있게 한다.
