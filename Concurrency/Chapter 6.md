# 6. Operation

GCD와 Operation은 둘 다 코드 덩어리를 보내어 분리된 쓰레드에서 수행할 수 있게 한다. operation은 보내진 task에 대해 더 많은 제어를 할 수 있다.

operation은 GCD를 기반으로 하여 만들어 졌고, 다른 operation들에 대한 의존, 실행중인 operation을 취소, 객체 지향 모델과 같은 추가 기능을 제공한다.

## 6.1 Reusability

`Operation` 을 사용하는 이유중 하나는 재활용성이다. 

`Operation` 은 실제 Swift 객체이다. 즉, task를 구성하기 위해 전달할 수 있고, helper method를 구현할 수 있다. 

## 6.2 Operation states

operation은 lifecycle을 표현하기 위한 state machine이 있다.

- 인스턴스화 되고 실행할 준비가 되어 있다면 `isReady` 상태로 전환한다.
- `start` method를 호출하게 되는 경우, `isExecuting` 상태로 전환된다.
- 앱이 `cancel` method를 호출하면, `isFinished` 상태로 전환되기 전에  `isCancelled` 상태로 전환된다.
- 최소되지 않았다면, `isExecuting` 에서 `isFinished` 로 바로 전환된다.

이 상태들은 `Operation` class의 read-only Boolean 속성이다. `Operation` class가 전환 처리를 하게 되며, 직접 영향을 줄 수 있는 속성은 `isExecuting` 상태와 `isCancelled` 상태이다. 각각, operation을 시작할 때, `cancel` method를 호출할 때 전환된다.

## 6.3 BlockOperation

`BlockOperation` class를 사용하여 코드 블락으로 `Operation` 을 빠르게 생성할 수 있다. 단순히 클로저를 생성자에 넘겨주게 된다.

```swift
let operation = BlockOperation {
  print("2 + 3 = \(2 + 3)")
}
```

`BlockOperation` 은 기본 전역 큐에서 하나 이상의 클로저를 비동기로 실행하는 것을 관리한다. 이미 `OperationQueue`를 사용하는 앱에 객체 지향 래퍼를 제공하여 별도의 `DispatchQueue` 를 생성할 필요가 없다.

KVO 알림, dependency 와 같은 `Operation` 이 제공하는 것들을 이용할 수 있다.

클로저 그룹을 관리할 수도 있으며, dispatch group 처럼 모든 클로저들의 종료 시점을 확인할 수 있다.

> **Note:** `BlockOperation` 의 작업은 병렬로 수행된다. 만약, 직렬로 수행하기 위해서는 `DispatchQueue` 에 전달하거나 dependency를 설정하면 된다.

### Multiple block operations

`BlockOperation`은 `DispatchGroup` 과 유사하게 동작한다. 즉, 모든 작업이 끝난 시점을 쉽게 알 수 있다.

`completionBlock` 클로저를 전달하여 block operation에 추가된 모든 클로저가 종료되었을 때 수행할 코드 블럭을 실행할 수 있다.

## 6.4 Subclassing operation

`BlockOperation` class는 단순한 task에 적합하지만, 더 복잡한 작업이나 재활용 가능한 요소를 원한다면 `Operation` 을 서브클래스화 해야 한다.

### Tilt shift the wrong way

### Tile shift almost correctly
