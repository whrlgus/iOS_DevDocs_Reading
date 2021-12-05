# 3. Queue & Threads

## 3.1 Threads

앱의 작업을 멀티쓰레드로 분리할 때의 장점은 다음과 같다:

- **Faster execution:** 작업들을 여러 쓰레드에서 수행하면, 동시에 수행할 수 있고, 직렬적으로 수행하는 것에 비해서 빠르게 완료된다.
- **Responsiveness:** 사용자가 보게되는 작업만을 main UI thread에서 수행하고 다른 작업을 다른 쓰레드에서 수행한다면, 사용자는 앱이 느리다거나 멈춤 현상이 일어나는 것을 알 수 없을 것이다.
- **Optimized resource consumption:** 쓰레드는 OS에 의해 최적화되어 있다.

쓰레드를 관리할 수 있는 API를 제공하지만, 직접 관리는 권장하지 않는다.

## 3.2 Dispatch queues

쓰레드 관리는 `DispatchQueue` 를 사용하여 간접적으로 할 수가 있다. 우리가 큐를 생성하면 OS는 해당 큐에 하나 이상의 쓰레드를 생성하여 할당한다. 만약, 존재하는 쓰레드가 사용가능하다면, 이것을 재활용한다. 그렇지 않다면, OS에 의해 필요시 생성된다.

```swift
let label = "com.raywenderlich.mycoolapp.networking"
let queue = DispatchQueue(label: label)
```

Label 인자는 유일한 값이어야 한다. UUID를 사용할 수도 있지만, 디버깅 시에 확인하게 될 값이기 때문에 reverse-DNS style로 의미있게 명명하는 것이 좋다.

### The main queue

앱이 시작하면, `main` dispatch queue는 자동으로 생성된다. 이것은 UI를 위한 직렬 큐이다. 자주 사용되므로 `DispatchQueue.main` 으로 접근할 수 있는 클래스 변수로 만들어진다. Main 큐에서 UI 와 관련없는 특정 작업을 동기적으로 수행하면 앱 성능이 저하될 것이다.

dispatch queue에는 두가지 유형, serial 과 concurrent가 있다. 기본 생성자를 사용하면 직렬 큐가 생성되며 다음 작업이 수행되기 위해서는 이전 작업이 완료되어야 한다.

```swift
let label = "com.raywenderlich.mycoolapp.networking"
let queue = DispatchQueue(label: label, attributes: .concurrent)
```

병렬 큐를 생성하기 위해서는 단순히 `.concurrent` 를 속성으로 전달하면 된다. 병렬 큐는 큐가 반드시 가져야 하는 **Quality of service (QoS)** 에 따라서 6가지의 global concurrent queue가 있다.

### Quality of service

Concurrent dispatch queue를 사용할 때, iOS에 작업의 중요도를 알려야 하며, 그렇게 함으로써 다른 작업에 비해 적절히 우선시 될 수 있다. 높은 우선순위를 부여받은 작업은 더 많은 시스템 자원을 취하고 낮은 우선순위 작업보다 많은 에너지를 사용하여 빠르게 완수된다.

관리가 필요없는 concurrent queue를 생성하기 위해서는 `DispatchQueue` 의 `global` class method를 사용하면, 미리 정의된 전역 큐를 생성할 수 있다.

```swift
let queue = DispatchQueue.global(qos: .userInteractive)
```

애플은 다음 여섯 가지의 quality of service 클래스를 제공한다:

#### `.userInteracive`

이 QoS는 사용자와 직접 상호작용하는 작업에 사용을 권장한다. UI 갱신을 위한 연산, 애니메이션 또는 UI 반응을 빠르게 유지하는 작업에 해당한다. 만약 이 작업들이 빨리 끝나지 않는다면 멈춤 현상이 일어날 것이기 때문에, 즉시 끝나는 작업에 해당되어야 한다.

#### `.userInitiated`

이 큐는 사용자가 UI로부터 시작한, 즉시 일어나야하는, 비동기적으로 실행되도 되는 작업에 사용되어야 한다. 예를 들면, 유저가 버튼을 클릭할 때 문서를 열거나 로컬 디비에서 읽는 작업에 해당된다. 수초 이내에 끝날 수 있는 작업에 사용되어야 한다.

#### `.utility`

이 dispatch queue는 긴 연산, I/O, 네트워키, 계속적인 데이터 피드 와 같은 progress indicator가 필요한 작업에 적절하다. 시스템은 에너지 효율면에서 반응성과  성능의 균형을 맞추려고 할 것이다. 작업은 수초 수분 내로 끝나야 한다.

#### `.background`

사용자가 직접 인식할 수 없는 작업에 사용된다. 사용자 인터랙션이 없으며 시간에 민감하지도 않다. Prefetching, database maintenance, 원격 서버 동기화, 성능 지원등이 좋은 예시이다. OS는 속도보다는 에너지 효율에 초점을 둘 것이다. 수 분이상이 소요되는 작업에 사용할 수 있다.

#### `.defualt` and `unspecified`

qos 인자의 기본 값으로 초기화되는 `.default` 는 `.userInitiated` 와 `.utility` 중간에 해당된다.

`.unspecified` 는 legacy API를 지원하기 위해 존재한다는 것만 알면 된다.

> **Note:** global queue는 항상 concurrent이며, FIFO이다.

### Inferring Qos

concurrent dispatch queue를 생성하려할 때, 생성자 인자로 QoS를 전달할 수 있다.

```swift
let queue = DispatchQueue(label: label, 
                          qos: .userInitiated,
                          attributes: .concurrent)
```

OS는 큐로 전달되는 테스크의 유형에 따라 필요시 qos를 변경한다. 만약 큐가 가진 qos보다 높은 qos를 가진 task를 전달하면 큐의 qos는 상향되며 포함된 모든 작업의 우선도도 상향된다.

### Adding task to queues

dispatch queue는 `sync` 와 `async` method를 제공하여 task를 큐에 추가할 수 있게 한다. 예를 들어, 앱이 시작될 때 서버에 접속하여 앱 상태를 갱신해야 한다. 이것은 user initiated가 아니고 즉시 일어나야 하는 것이 아니며, 네트워킹 I/O에 의존한다 . 따라서 global utility queue에 전달해야 한다.

```swift
DispatchQueue.global(qos: .utility).async { [weak self] in
  guard let self = self else { return }

  // Perform your work here
  // ...

  // Switch back to the main queue to
  // update your UI
  DispatchQueue.main.async {
    self.textLabel.text = "New articles available!"
  }
}
```

위 코드에서 주목해야 할 점은 두가지가 있다.

첫번째는, 캡쳐되는 변수를 활용하려는 계획에 따라 strongly 혹은 weakly 로 캡쳐해야 한다. 작업이 끝나면 해제되기 때문에 강한 참조로 인해서 reference cycle이 형성되지는 않지만, `self` 의 lifetime은 연장된다.

두번째는, UI 갱신을 위해 다른 것들 안에서 `main` 큐를 사용하여 `async` 작업을 하는 것은 일반적이다.

> **Note:** UI 갱신은 main 큐아닌 다른 큐에서 수행하면 안된다. 만약 사용하는 라이브러리에 callback 이 어떤 큐를 사용하는지 명시되어 있지 않다면, main 큐에 전달해야 한다.

dispatch queue를 동기적으로 전달할 때는 주의가 필요하다. 

> **Note:** main thread에서 `sync` 를 호출하면 deadlock에 걸리게 된다.

## 3.3 Image loading example

`Data` 생성자로 이미지를 다운로드 받는 것은 적절한 방법이 아니며(https://developer.apple.com/documentation/foundation/nsdata/1407864-init), 네트워크 요청이 필요한 작업은 UI관련 쓰레드와 분리되어야 한다.

속도와 베터리 수명의 적절한 균형을 유지하는 `.utility` 큐가 이에 적절하다.

### Using a global queue

```swift
private func downloadWithGlobalQueue(at indexPath: IndexPath) {
    DispatchQueue.global(qos: .utility).async { [weak self] in
      guard let self = self else {
        return
      }
      
      let url = self.urls[indexPath.item]
      guard let data = try? Data(contentsOf: url),
            let image = UIImage(data: data) else {
        return
      }
      
      DispatchQueue.main.async {
        if let cell = self.collectionView.cellForItem(at: indexPath) as? PhotoCell {
          cell.display(image: image)
        }
      }
    }
  }
```

### Using built-in methods

```swift
private func downloadWithUrlSession(at indexPath: IndexPath) {
    URLSession.shared.dataTask(with: urls[indexPath.item]) {
      [weak self] data, response, error in

      guard let self = self,
            let data = data,
            let image = UIImage(data: data) else {
        return
      }

      DispatchQueue.main.async {
        if let cell = self.collectionView
          .cellForItem(at: indexPath) as? PhotoCell {
          cell.display(image: image)
        }
      }
    }.resume()
  }
```

## 3.4 `DispatchWorkItem`

`DispatchQueue` 에 anonymous closure를 전달하는 것 이외에, `DispatchWorkItem` 클래스를 사용할 수 있다.

```swift
let queue = DispatchQueue(label: "xyz")
queue.async {
  print("The block of code ran!")
}
```

```swift
let queue = DispatchQueue(label: "xyz")
let workItem = DispatchWorkItem {
  print("The block of code ran!")
}
queue.async(execute: workItem)
```

### Canceling a work item

`DispatchWorkItem`을 사용하는 이유는 보통 작업 시작 전, 중에 취소하기 위해서이다. work item에 `cancel()` 을 호출하면 다음 둘 중 하나의 액션이 수행된다:

1. 만약 task가 큐에서 시작되기 전이라면, 제거된다.
2. 만약 실행중이라면, `isCancelled` property가 true로 설정된다.

`isCancelled` property를 주기적으로 확인하여 적절한 액션을 취해야 할 필요가 있다.

### Poor man's dependencies

`DispatchWorkItem` 클래스는 `notify(queue:execute:)` method를 제공하여 현재 work item 이 완료될 때 실행할 `DispatchWorkItem` 을 지정할 수 있게 한다.

