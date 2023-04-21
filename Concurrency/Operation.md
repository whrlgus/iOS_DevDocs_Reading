# Operation

단일 작업에 연관된 코드와 데이터를 표현하는 추상 클래스

## Declaration

```swift
class Operation : NSObject
```

## Overview

`Operation` 은 추상 클래스이므로 실제 테스크를 수행하기 위해 서브클래스화 하여 사용하거나, 시스템 정의 서브클래스([NSInvocationOperation]() or [BlockOperation]())를 사용해야 한다. 기본 Operation은 추상화 되어 있음에도, 그 구현에는 작업 수행의 안전성을 위한 몇몇 로직이 포함되어 있다. 이러한 내장 로직의 존재로 작업과 관련된 실제 구현에만 집중할 수 있다.

operation 객체는 single-shot 객체로서, 한번 수행하면 재수행이 불가능하다. operation은 대게 [OperationQueue]() class의 인스턴스에 추가하여 실행하게 된다. operation queue는 작업을 다른 쓰레드에서 직접적으로 수행하거나, libdispatch 라이브러리를 사용하여 간접적으로 수행한다. 큐가 작업을 어떻게 수행하는지 자세한 정보는 [OperationQueue](https://developer.apple.com/documentation/foundation/operationqueue) 참조.

operation queue를 사용하길 원하지 않으면, 코드에서 start() method를 호출하여 작업을 수행할 수 있다. 준비상태가 아닌 작업을 시작하는 것은 예외를 유발하므로, 수동으로 작업을 수행하는 것은 부담이 될 수 있다. isReady 속성이 작업의 준비를 알린다. 

### Operation Dependencies

종속 관계는 특정 순서로 작업을 수행하기 위한 편리한 방법이다. `addDependency(_:)` 와 `removeDependency(_:)` 로 의존 관계를 형성하고 제거할 수 있다. 기본적으로 의존하는 작업들이 모두 끝나고 나서야 operation은 준비상태가 되며 실행할 수 있게 된다. 

의존 관계는 의존하는 작업이 성공적으로 끝났는지 여부를 구분하지는 않는다. (즉, 작업을 취소하는 것도 끝났다고 표시한다.) 의존하는 작업이 취소되었거나 성공적으로 작업을 완수하지 않은 경우에 대한 처리는 직접 결정해야 한다. 이것은 필요에 따라 operation 객체에 에러를 추적할 수 있는 로직을 추가해야 됨을 말한다.

### KVO-Compliant Properties

NSOperation 클래스는 몇몇 속성들을 위해 KVC와 KVO를 준수한다. 필요하다면 앱의 다른 부분을 제어하기 위해 이러한 속성들을 관측할 수 있다. 아래와 같은 key path를 사용하면 된다:

- isCancelled - read-only
- isAsynchronous - read-only
- isExecuting - read-only
- isFinished - read-only
- isReady - read-only
- dependencies - read-only
- queuePriority - readable and writable
- completionBlock - readable and writable

이러한 속성에 observer를 붙여도 되지만, UI 요소와 속성을 묶기 위해 Cocoa binding을 사용하는 것은 안된다. Main thread에서 수행해야 하는 UI 관련 코드는 어떤 thread에서 수행될 수 있는 operation코드로 인한 문제가 발생하기 때문이다.

앞선 속성들의 커스텀 구현을 제공하고자 한다면, KVC와 KVO를 준수하는 구현을 포함시켜야 할 것이다. NSOperation 객체에 추가되는 속성들도 이를 준수하도록 하는 것이 권장된다. [Key-Value Coding Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueCoding/index.html#//apple_ref/doc/uid/10000107i) 와 [Key-Value Observing Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/KeyValueObserving.html#//apple_ref/doc/uid/10000177i) 참조.

### Multicore Considerations

NSOperation 객체의 method를 호출하는 데, 객체 접근을 동기화 하기 위한 추가적인 lock을 생성하지 않고도 안전하게 처리할 수 있다. operation을 생성하고 관찰하는 thread와 분리된 thread에서 수행되기 때문에 이러한 안전성이 보장되어야 하기 때문이다. 

NSOperation을 서브클래스화 할 때, override 하는 method가 여러 thread에서 안전하게 호출될 수 있게 해야 한다. [Threading Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/Introduction/Introduction.html#//apple_ref/doc/uid/10000057i) 참조.

### Asynchronous Versus Synchronous Operations

작업을 큐에 추가하지 않고 수동으로 실행하고자 한다면, 동기 혹은 비동기 방식으로 디자인할 수 있다. 기본적으로 동기적으로 동작하는데, operation 객체는 실행시 별도의 thread를 생성하지 않는다. 동기 작업의 start method를 호출하면 즉시 현재 thread에서 수행한다. Start method가 caller에게 제어권을 반환할 때가, 그 작업이 끝날 때이다. 

비동기 작업의 start method를 호출하면, 일을 완수하기 이전에 반환된다. 비동기 작업 객체는 별도의 thread에서 작업을 스케줄링한다. 새로운 thread를 직접 시작하거나, 비동기 method를 호출하거나, block을 dispatch queue에 전달하여 이를 수행한다. 제어권이 caller에게 반환될 때, 작업이 진행되는지는 중요하지 않다.

큐를 사용할 때는, 동기적으로 수행하도록 정의하는 것이 더 간단하다. 비동기 작업을 정의하는 것은 작업의 상태를 KVO notification으로 관리해야 하기 때문에 더 복잡하다. 하지만, 호출하는 thread를 block하지 않기 위할 때 유용하다. 

작업 큐에 작업을 추가할 때, 큐는 작업의 asynchronous 속성을 무시하며 항상 별도의 thread에서 start method를 호출한다. 그러므로, 항상 큐를 사용하여 작업을 수행하고자 하면, 작업을 비동기로 구성할 필요가 전혀 없다.

동기와 비동기 작업을 어떻게 정의하는지에 대한 정보는 subclassing notes를 확인하자.

### Subclassing Notes

NSOperation 클래스는 작업의 실행 상태를 추적하기 위한 기본 로직을 제공한다. 하지만, 실제 작업을 위해서는 서브클래스화 해야한다. 어떻게 subclass를 생성해야 하는지는 작업이 병렬적으로 수행되도록 디자인되었는지 여부에 따라 다르다.

#### Methods to Override

non-concurrent 작업의 경우, 대게 단 하나의 method만 override한다:

- [main](https://developer.apple.com/documentation/foundation/nsoperation/1407732-main?language=objc)

이 method에는 주어진 task를 수행하기 위한 코드를 작성하게 된다. 물론 커스텀 클래스의 인스턴스를 쉽게 생성하기 위한 커스텀 생성자를 정의해야 한다. 작업으로부터 데이터에 접근하기 위한 getter/setter 정의도 필요할 수 있다. 그러나, getter/setter method 를 정의하면, thread-safe하게 구현해야 한다.

concurrent 작업의 경우 최소한 다음 method와 속성들을 override 해야한다:

- [start]()
- [asynchronous]()
- [executing]()
- [finished]()

병렬 작업에서 start method는 비동기 방식으로 작업을 수행해야 한다. thread를 생성하거나 비동기 함수를 호출하는 것은 이 method에서 해야 한다. 작업을 시작할 때, start method는 작업의 실행 상태를 갱신해야 한다. executing key path로 KVO 알림을 보내어 갱신을 하게 된다. executing 속성은 thread-safe 한 방식으로 상태를 제공해야 한다.

task를 완수하거나 취소할 때, concurrent 작업 객체는 최종 상태 갱신을 위해 isExecuting과 isFinished 두 key path로 KVO 알림을 생성해야 한다. (취소의 경우, task를 완수하지 않더라도 isFinished key path를 갱신하는 것은 중요하다. 큐에 들어간 작업은 제거되기 전에 끝났다는 것을 알려야 한다.) KVO 알림 생성 이외에, executing 과 finished 속성의 override는 작업 상태에 따른 정확한 값을 제공하도록 해야 한다.

concurrent 작업의 가이드와 생성 법은 [Concurrency Programming Guide](https://developer.apple.com/library/archive/documentation/General/Conceptual/ConcurrencyProgrammingGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40008091) 참조.

> **Important**
>
> start method에서 super를 절대 호출하지 말아야 한다. concurrent 작업을 정의할 때, 기본 start method가 제공하는 것들을, task를 시작하고 KVO 알림을 생성하는 것과 같은, 포함시키자. 또한 task 시작 전에 취소 여부를 확인해야 한다. [Responding to the Cancel Command](https://developer.apple.com/documentation/foundation/nsoperation?language=objc#1661262) 참조.

의존 관계의 경우, isReady key path로 KVO 알림만 추가 구현하면 된다.

#### Maintaining Operation Object States

operation 객체는 실행하기 안전한 시점을 결정하기 위해 내부적으로 상태 정보를 유지하고 있고, 작업의 life cycle에 따른 진행 상황을 외부에 알린다. 커스텀 서브클래스에서 이러한 상태 정보를 유지해야 하며 관련 key path는 다음과 같다:

##### isReady

작업이 실행 가능한지를 클라이언트가 알게 한다. ready 속성은 실행 준비가 되었을 때 true 값을 갖고, 의존하는 작업이 끝나지 않았다면 false 값을 갖는다.

대부분의 경우, 이 상태를 관리하지 않아도 된다. 하지만, 의존 객체가 아닌 프로그램의 외부 요소에 따라 준비 여부가 결정되는 작업이라면, ready 속성에 대한 커스텀 구현을 제공할 수 있다. 

macOS 10.6 이상에서, 다른 의존 작업이 끝나길 기다리는 작업을 취소하면, 의존 관계는 무시되고 이 프로퍼티는 지금 즉시 실행가능하다고 변경된다. 이 행동은 큐에서 취소된 작업을 더 빠르게 제거할 수 있게 만든다.

##### isExecuting

이 키패스로 할당된 task가 실행중인지 확인할 수 있다. 

작업 객체의 start method를 교체하면, 반드시 executing 속성도 교체하고 작업 상태 변경에 따른 KVO 알림을 생성해야 한다.

##### isFinished

이 키패스로 task가 성공적으로 끝났거나 취소되었는지를 알 수 있다. operation 객체는 isFinished kay path로 값이 true가 되면 의존 관계를 정리한다. 유사하게, operation queue도 작업을 그 이후에 dequeue한다. 그러므로, 끝났다는 표시를 하는 것은 작업의 진행과 취소에 따른 큐를 유지하는 데 중요하다.

작업 객체의 start method를 교체하면, 반드시 finished 속성도 교체하고 작업이 끝나거나 취소되었을 때 반드시 KVO 알림을 생성해야 한다.

##### isCancelled

이 키패스로 작업 취소 요청이 있었는지를 알 수 있다. 취소를 지원하는 로직은 필수는 아니지만 권장되며, 이 키패스로 KVO 알림을 보내는 것이 꼭 필요한 것은 아니다.

#### Responding to the Cancel Command

작업을 큐에 추가하는 것은 큐에게 그 작업의 스케쥴링 역할을 위임하게 되는 것이다. 그러나, 그 작업의 수행을 원치 않는 경우에는 operation 객체의 cancel() method를 호출하거나 operationqueue 객체의 cancelAllOperations() 를 호출하여 스케쥴링에 간섭할 수 있다.

작업 취소는 하던 일을 즉시 멈추진 않고, 명시적으로 isCancelled 값을 확인하여 필요시 멈춰야 한다. NSOperation의 기본 구현에 이러한 로직이 포함되어 있다. 예를 들어, start() method가 불리기 전에 취소를 하면, start() 메소드는 호출되지만 작업을 시작하지 않고 바로 빠져나오게 된다. 

> **Note** 
>
> macOS 10.6 이상에서, 큐에있지만 끝나지 않은 의존 작업이 있는 작업의 cancel() method를 호출하면, 의존 작업들은 무시된다. 작업은 이미 취소되었기 때문에, 큐가 operation의 start() method를 호출하여 main() method 호출 이전에 제거하게 된다. 큐에 있지 않은 경우에는 즉시 취소 표시를 한다. 각 경우에서 operation을 ready나 finished로 표시하는 것은 KVO notification을 발생시킨다.

이러한 취소 로직을 커스텀 코드에도 적용해야 한다. 특히 main 작업은 isCancelled 속성을 주기적으로 확인해야 한다. 이 값이 true인 것으로 확인되면, operation 객체는 최대한 빨리 정리되어야 한다. 커스텀 start() method는 초기에 이를 체크하여 적절한 처리를 해줘야 한다. 

또한 취소된 작업의 최종 상태 변경도 해줘야 한다. 특히, concurrent operation을 구현하여 isFinished 와 isExecuting 속성을 관리하게 되면, 적절하게 갱신해야 한다. isFinished를 true로, isExecuting을 false로 각각에서 반환되는 값을 변경해야 한다. 실행 시작 전에 작업이 취소 되었더라도 이러한 갱신은 해줘야 한다.