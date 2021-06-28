# Chapter 2. Observables

## 2.2 What is an observable?

Observable은 Rx의 핵심이다. Rx에서 "observable", "observable sequence", "sequence" 라는 용어들을 같은 의미로 사용하는 것을 보았을 것이다. 그리고 "stream" 이라는 용어를 언젠가, 특히 다른 reactive programming 환경에서 RxSwift로 온 개발자들로 부터 들었을 것이다. "Stream" 또한 같은 것을 지칭하지만, RxSwift에서는 sequence로 통한다.

비동기라는 중요한 요소를 가지고 있는 `Observable` 은 sequence이다. 이는 이벤트를 특정 시간 동안 생성한다. 이것을 **emitting**이라고 일컷는다. 이벤트는 커스텀 타입, 탭과 같은 제스쳐를 식별할 수 있는 인스턴스 혹은 숫자와 같은 값들을 포함할 수 있다. 



## 2.3 Lifecycle of an observable

observable이 한 인자를 방출할 때, **next** 이벤트로 알려진 것을 통해 이 동작이 이뤄진다.

특정 개수의 이벤트를 방출하고, 끝내기 위해서는 **completed** 이벤트를 방출한다. 그리고 더이상 이벤트를 방출하지 않는다.

무언가 잘못되었을 때, **error** 이벤트를 방출할 수 있다. Completed 이벤트와 동일하게 observable이 종료되며 더이상의 이벤트 방출은 이뤄지지 않는다.

정리하자면:

- observable은 인자를 포함하는 **next** 이벤트를 방출한다.
- 이 동작은 **error** 나 **completed** 이벤트와 같이 **종료 이벤트** 를 방출하기 전까지 계속될 수 있다.
- observable이 끝나게되면, 더이상의 이벤트 방출은 없다.



Event는 enumeration case들로서 표현된다. 아래는 실제 RxSwift 소스 코드의 구현부이다.

```swift
/// Represents a sequence event.
///
/// Sequence grammar:
/// **next\* (error | completed)**
public enum Event<Element> {
    /// Next element is produced.
    case next(Element)

    /// Sequence terminated with an error.
    case error(Swift.Error)

    /// Sequence completed successfully.
    case completed
}
```

`next` 이벤트는 특정 `Element` 인스턴스를 포함하고 있는 것을 확인할 수 있다. `error` 이벤트는 `Swift.Error` 인스턴트를 포함하고, `completed` 이벤트는 단순한 정지 이벤트로 어떠한 데이터도 포함하지 않는다.



## 2.4 Creating observables

```swift
example(of: "just, of, from") {
  // 1
  let one = 1
  let two = 2
  let three = 3

  // 2
  let observable = Observable<Int>.just(one)
}
```

위 코드에서:

1. 뒤이은 예제들에서 사용할 integer 상수들을 정의한다.
2. `one` integer 상수를 인자로 하는 `just` 메소드를 사용하여 `Int` 타입의 observable sequence를 생성한다.

`just` 메소드의 이름은 적절하다. 왜냐하면 이 메소드가 하는 일은 *just* 단일 인자를 포함하는 observable sequence를 생성하는 것이 전부다. 이 메소드는 `Observable`의 정적 메소드이다. 그러나 Rx에서는 method를 "operator" 로 부른다. 



```swift
let observable2 = Observable.of(one, two, three)
```

`of` operator는 **variadic**(가변인자) 파라미터를 갖기때문에 위 observable 인자의 타입은 `[Int]` 배열이 아닌 `Int` 이다.



```swift
let observable4 = Observable.from([one, two, three])
```

`from` operator는 인자 타입의 배열로부터 인스턴스를 생성할 수 있게 해준다.



## 2.5 Subscribing to observables

다음은 `UIKeyboardDidChangeFrame` 알림의 observer 이다. 

```swift
let observer = NotificationCenter.default.addObserver(
  forName: UIResponder.keyboardDidChangeFrameNotification,
  object: nil,
  queue: nil) { notification in
  // Handle receiving notification
}
```

RxSwift observable을 구독하는 것은 이와 유사하다; 우리는 observable을 관측하는 것을, 그것을 구독하는 것이라고 표현한다. 그래서 `addObserver()` 대신에, `subscribe()` 를 사용한다. 개발자들이 전형적으로 `.default` 싱글톤 인스턴스만을 사용하는  `NotificationCenter` 와는 다르게, Rx에서 각각의 observable은 다르다. 

더 중요하게 observable은 구독자를 갖기 전까지는, 이벤트를 보내지도, 어떠한 작업을 수행하지도 않을 것이다.

observable은 sequence(일련의 순서, 연속) 정의부에 지나지 않는다. 그리고 observable을 구독하는 것은 Swift 표준 라이브러리의 `Iterator` 에서 `next()` 를 호출하는 것과 다르지 않다.

```swift
let sequence = 0..<3
var iterator = sequence.makeIterator()
while let n = iterator.next() {
  print(n)
}
/* Prints:
 0
 1
 2
 */
```

observable을 구독하는 것은 훨씬 streamlined(단순하지만 효율적이고 효과적)이다. 

```swift
let one = 1
let two = 2
let three = 3

let observable = Observable.of(one, two, three)
observable.subscribe { event in
	print(event)
}
```

`subscribe` 를 Option-click으로 확인해보면, `Int` 타입의 `Event` 를 받고 아무것도 반환하지 않는 closure 파라미터가 있다. 그리고 `Disposable` 을 반환한다.

이 구독은 `observable` 에 의해 방출되는 각 이벤트를 출력한다. 각 요소의 `next` 이벤트를 방출하고, `completed` 이벤트 방출 이후에 종료된다. 

`Event` 는 `element` 프로퍼티를 가지고 있다. `next` 이벤트만이 인자를 갖기 때문에, 이  프로퍼티를 옵셔널 값이다. 그래서 optional binding을 통해 `nil` 이 아닌 element를 unwrap하게 된다. 



## 2.6 Disposing and terminating

observable은 구독을 받기 전까지 아무 동작도 하지 않는다. observable을 작동시키는 트리거는 구독이며, `error` 나 `completed` 이벤트가 observable을 종료하기 전까지 새로운 값을 방출하게 한다. 그러나, 직접 구독을 취소하여 observable을 종료시킬 수 있다.

```swift
example(of: "dispose") {
  let observable = Observable.of("A", "B", "C")
  let subscription = observable.subscribe { event in
    print(event)
  }
  subscription.dispose()
}
```

명시적으로 구독을 취소하고 싶다면, disposable 인스턴스의 `dispose()` 를 호출하자. 구독이 취소되면, 혹은 제거하면, observable은 이벤트 방출하는 것을 멈출 것이다.

각각의 구독을 관리하는 것은 귀찮은 일이기 때문에, RxSwift는 `DisposeBag` 타입을 포함한다. dispose bag은 disposable 인스턴스들을 가지고 있다가 해제되기 직전에 각 인스턴스의 `dispose()` 를 호출한다.

만약, 구독을 완료했거나 다른 이유로 observable이 득정 시점에 종료됐을 때, 구독을 dispose bag에 넣거나, 직접 `dispose()` 호출하는 것을 잊는다면, 메모리 누수가 발생할 것이다.

```swift
example(of: "create") {
  let disposeBag = DisposeBag()
  Observable<String>.create { observer in

  }
}
```

`create` operator를 사용하는 것은 observable이 subscriber에게 방출할 수 있는 모든 이벤트를 구체화 하는 다른 방법이다.

`create` operator는 `subscribe` 라는 이름의 단일 파라미터를 취한다. 이것의 일은 observable의 `subscribe` 호출 구현부를 제공하는 것이다.

`subscribe` 파라미터는 `AnyObserver`를 취하고 `Disposable` 을 반환하는 escaping closure이다. `AnyObserver` 는 observable sequence에 값(결과적으로 subscriber에게 방출하는 값) 추가를 수월하게 해주는 generic 타입이다.

```swift
Observable<String>.create { observer in
  // 1
  observer.onNext("1")
  // 2
  observer.onCompleted()
  // 3
  observer.onNext("?")
  // 4
  return Disposables.create()
}
```

1. `next` 이벤트를 observer에게 추가한다. `onNext(_:)` 는 `on(.next(_:))` 의 convenience method이다. 
2. `completed` 이벤트를 observer에 추가한다. 
3. 또 다른 `next` 이벤트를 observer에 추가한다.
4. disposable을 반환한다. observable이 종료되거나 제거될 때 어떤 것을 수행할 지 정의하는 것이다; 이 경우에는 정리할 것이 없기 때문에 빈 disposable을 반환한다.

```swift
example(of: "create") {
  enum MyError: Error {
    case anError
  }

  let disposeBag = DisposeBag()

  Observable<String>.create { observer in
    // 1
    observer.onNext("1")
//    observer.onError(MyError.anError)
    // 2
//    observer.onCompleted()
    // 3
    observer.onNext("?")
    // 4
    return Disposables.create()
  }
  .subscribe(
    onNext: { print($0) },
    onError: { print($0) },
    onCompleted: { print("Completed") },
    onDisposed: { print("Disposed") }
  )
//  .disposed(by: disposeBag)
}
```

`completed` 이벤트를 추가하는 줄이나, 구독을 `disposeBag` 에 추가하는 줄의 주석을 제거하면, 메모리 누수를 사라지게 할 수 있다. (Complete 이벤트로도 제거할 수 있구나...)



## 2.7 Creating observable factories

subscriber를 기다리는 observable을 생성하는 것 이외에, 새로운 observable을 각 subscriber에게 제공하는 observable factory를 생성하는 것도 가능하다.

```swift
example(of: "deferred") {
  let disposeBag = DisposeBag()
  // 1
  var flip = false
  // 2
  let factory: Observable<Int> = Observable.deferred {
    // 3
    flip.toggle()
    // 4
    if flip {
      return Observable.of(1, 2, 3)
    } else {
      return Observable.of(4, 5, 6)
    }
  }
}
```

1. observable이 반환할, 뒤짚기 위한 `Bool` 플래그를 생성한다.
2. `deferred` operator를 사용하는 `Int` observable factory를 생성한다. 
3. `factory`를 구독하면 `flip`을 전환한다.
4. `flip` 의 값에 따라 다른 observable을 반환한다.



## 2.8 Using Traits

trait은 일반 observable보다 좁은 행동 집합을 갖는 observable이다. 이것의 목적은 우리의 의도를 코드를 읽는 사람 혹은 API를 사용하는 사람에게 더 분명하게 전달하는 것이다. trait을 사용함으로써 암시되는 문맥은 코드를 더욱 직관적으로 만들어 준다.

RxSwift에는 세가지 종류의 trait이 있다: `Single`, `Maybe`, `Completable`. 

- `Single` 은 `success(value)` 나 `error(error)` 이벤트만을 방출한다. 사실 `success(value)` 는 `next` 와 `completed` 이벤트를 조합한 것이다. 이 trait은 데이터를 다운로딩하거나 디스크로부터 로딩할 때와 같이, 성공하여 값을 전달하거나 실패하는 일회성 프로세스에 사용하기 유용하다.
- `Completable` 은 `completed` 나 `error(error)` 이벤트만을 방출한다. 이 trait은 어떠한 값도 방출하지 않는다. 파일 쓰기와 같이 작업이 성공적으로 완료되거나 실패하는 것을 다루기에 유용하다.
- `Maybe` 는 `Single` 과 `Completable` 의 조합이다. `success(value)`, `completed`, `error(error)` 를 방출할 수 있다. 작업이 성공 혹은 실패할 수 있고, 선택적으로 성공하는 경우에 값을 반환한다면 이 trait을 사용하자.

