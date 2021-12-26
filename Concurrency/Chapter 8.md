# 8. Asynchronous Operations

operation이 동기적으로 수행되는 경우 `Operation` class 의 state machine은 알맞게 동작한다. Operation 이 `isReady` 상태로 전환되면, 시스템은 가용 쓰레드를 검색할 수 있게된다. 스케쥴러가 operation을 실행할 thread를 발견하면, operation의 상태는 `isExecuting`으로 변경되며, 코드가 실행되고 완료되어 상태는 `isFinished` 로 변경된다.

<img src="https://assets.alexandria.raywenderlich.com/books/con/images/1e68ebd765a99ec051fab5838f8d2a5f59d8ea394d984df065b850d6f14874a3/original.png" width=400/>

하지만 비동기 operation의 경우는 `main` method가 실행되면 비동기 작업으로 동작하여 `main` 에서 바로 반환된다. 비동기 메소드가 언제 끝날 지 알 수 없기 때문에 operation 상태는 `isFinished` 로 자동으로 전환될 수가 없다.

<img src="https://assets.alexandria.raywenderlich.com/books/con/images/8934bd7f60663dcd929b6f82076773cfeb3a4a65e113ad4da07e96952eba1b3c/original.png" width=400/>

## 8.1 Asynchronous operations

비동기 메소드를 operation으로 감싸는 방법이 있다. Read-only인 상태 속성을 수동으로 변경해야 하지만, 추상 클래스로 정의하여 이를 상속하면 더 이상의 작업은 필요없게 된다.

### AsyncOperation

#### State tracking

상태를 다음과 같이 정의했다.

```swift
extension AsyncOperation {
  enum State: String {
    case ready, executing, finished

    fileprivate var keyPath: String {
      return "is\(rawValue.capitalized)"
    }
  }
}
```

이 경우에 `Operation` class가 사용하는 KVO notification이 제대로 동작하게 하기 위해서 아래와 같이 4번의 명령문을 실행해야 한다.

```swift
var state = State.ready {
  willSet {
    willChangeValue(forKey: newValue.keyPath)
    willChangeValue(forKey: state.keyPath)
  }
  didSet {
    didChangeValue(forKey: oldValue.keyPath)
    didChangeValue(forKey: state.keyPath)
  }
}
```

#### Base properties

> **Note:** 스케쥴러가 쓰레드에서 실행할 operation을 찾아 준비시키는 과정까지 모든 것을 알 수 없기 때문에 `isReady`를 override 할 때에는 base class의 `isReady` 를 참조해야한다.

`isAsynchronous` 가 false 면 현재 쓰레드에서 동기적으로 operation을 수행하며, main method가 반환되면 상태는 완료가 된다. true인 경우는 다른 쓰레드에서 작업을 수행하여 상태 처리를 따로 해줄 필요가 있다.

다만, start 메소드를 직접 호출하지 않고, OperationQueue를 이용하는 경우에는 무조건 다른 쓰레드에서 작업을 수행하게 된다.

#### Starting the operation

operation을 수동으로 실행하거나, operation queue에 의해 실행할 때 가장 먼저 불리는 method는 `start` method이다. 그리고 이 method는 `main` 을 호출해야 하는 책임이 있다.

### Math is fun!

비동기 작업이 완료되면 상태를 반드시 갱신해 줘야 한다. 그렇지 않으면, 무한 루프에 빠질 수 있다.

## 8.2 Networked TiltShift

### NetworkImageOperation

### Using NetworkImageFilter