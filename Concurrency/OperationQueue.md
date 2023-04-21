# OperationQueue

작업 수행을 관리하는 큐

## Declaration

```swift
class OperationQueue : NSObject
```

## Overview

operation queue 는 줄지어 놓은 큐를 각자의 우선순위와 준비여부에 따라 실행토록 한다. queue에 operation을 추가하면 작업이 끝날 때까지 큐에 남아있게 된다. operation을 queue에 추가하면 직접 제거할 수는 없다.

> **Note**
>
> operation queue는 큐 내부에 작업이 끝날 때까지 유지하며, 큐 자체는 모든 작업이 끝날 때까지 유지된다. 끝나지 않은 작업으로 큐가 유지되면 메모리 누수가 발생할 수 있다.

operation queue에 대한 자세한 설명은 [Concurrency Programming Guide](https://developer.apple.com/library/archive/documentation/General/Conceptual/ConcurrencyProgrammingGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40008091) 참조.

### Determine the Execution Order

operation queue는 operation들을 각각의 준비여부, 우선순위, 의존관계에 따라 구성하고 실행한다. 예를들어, 모든 operation이 같은 [queuePriority]() 를 갖고 [isReady]() 속성이 true이면, 큐는 추가된 순서로 작업을 수행한다. 그 외의 경우는 높은 우선순위의 작업을 준비 여부에 따라 수행한다.

그러나, 특정 실행 순서 보장을 위해 이러한 사실에만 의존하면 안되는데, 작업의 준비 여부 갱신이 실행 순서 결과를 바꿀 수 있기 때문이다. 작업간 의존도는 각기 다른 큐에 있더라도 작업의 절대적인 실행 순서를 보장한다. 의존하는 모든 작업이 끝난 후에야 작업은 준비 상태가 된다.

우선순위와 의존 설정에 대한 자세한 설명은 [Operation](https://developer.apple.com/documentation/foundation/operation?changes=latest_minor) 의 [Managing Dependencies]() 참고.

### Respond to Operation Cancelation

작업이 끝났다는 것이 반드시 그 작업을 완수했다는 것을 의미하진 않는다; 작업은 취소될 수 있다. operation을 취소하면 그 객체를 큐에 남겨두어 최대한 빨리 그 작업이 끝나야 함을 알린다. 따라서, 현재 실행중인 작업에서는 취소 상태를 확인하여 하던 일을 멈추고 끝났다고 표시해야 한다. 큐에 있지만 아직 실행되지 않은 Operation도 start() method는 호출하여 취소 이벤트를 처리하고 종료 상태로 표시할 수 있도록 해야 한다.

> **Note**
>
> operation 취소는 그 것이 가지고 있던 모든 의존을 무시하게 만든다. 이는 큐가 작업의 `start()` method를 가능한 빨리 수행할 수 있게 하기 위함이다. `start()` method는 작업을 종료 상태로 옮겨 큐에서 제거될 수 있게 만든다.

작업 취소에 대한 더 자세한 정보는 [Operation](https://developer.apple.com/documentation/foundation/nsoperation?changes=latest_minor&language=objc)의 [Responding to the Cancel Command](https://developer.apple.com/documentation/foundation/operation?changes=latest_minor#1661262) 참조.

### Observe Operations Using Key-Value Observing

`OperationQueue` class는 key-value coding(KVC)와 key-value observing(KVO)를 준수하고 있다. 앱의 다른 부분을 제어하기 위해 이 속성들을 사용할 수 있고, 관측을 위해선 다음과 같은 key path를 사용하면 된다:

- [operations](https://developer.apple.com/documentation/foundation/nsoperationqueue/1415168-operations?changes=latest_minor&language=objc) - Read-only
- [operationCount](https://developer.apple.com/documentation/foundation/nsoperationqueue/1415115-operationcount?changes=latest_minor&language=objc) - read-only
- [maxConcurrentOperationCount](https://developer.apple.com/documentation/foundation/nsoperationqueue/1414982-maxconcurrentoperationcount?changes=latest_minor&language=objc) - readable and writable
- [isSuspended](https://developer.apple.com/documentation/foundation/nsoperationqueue/1415909-suspended?changes=latest_minor&language=objc) - readable and writable
- [name](https://developer.apple.com/documentation/foundation/nsoperationqueue/1418063-name?changes=latest_minor&language=objc) - readable and writable

이러한 속성들에 observer를 붙일 수 있지만, Cocoa binding을 사용하여 앱 UI의 요소와 이 속성들을 묶으면 안된다. UI 관련 코드는 대게 앱의 main thread에서 동작하도록 되어있지만, operation queue에 연관된 KVO 알림은 어떠한 thread에서도 동작할 수 있기 때문이다.

KVO에 대한 자세한 설명과 객체에 observer를 붙이는 방법은 [Key-Value Observing Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/KeyValueObserving.html#//apple_ref/doc/uid/10000177i) 참조.

### Plan for Thread Safety

 여러 thread에서 하나의 `OperationQueue` 객체를 별도 동기화 작업 없이 안전하게 사용할 수 있다.

operation queue는 작업들의 실행을 관리하기 위해 [Dispatch](https://developer.apple.com/documentation/dispatch?changes=latest_minor) framwork를 사용한다. 그 결과, 작업의 동기/비동기 여부에 상관없이, 큐는 항상 별도의 thread에서 동작한다.