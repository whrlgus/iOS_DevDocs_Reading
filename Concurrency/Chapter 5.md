# 5. Concurrency Problems

dispatch queue에 의해 제공되는 이점들은 모든 성능 이슈에 만병통치약은 아니다. 주의하지 않으면 맞닥뜨릴 수 있는 3가지 문제가 있다.

## 5.1 Race conditions

동일한 process를 공유하는 thread들은 동일한 address space를 공유하는 것이다. 즉, 동일한 shared resource에서 읽고 쓰는 작업을 하게된다. 만약 주의하지 않는다면, 여러 쓰레드가 동시에 동일한 변수로 값을 쓰려하는 **race conditions**을 겪게 될 것이다. 

컴퓨터는 **clock cycle**  주기로 동작하며 매 순간 하나의 operation만 실행한다. (읽고 쓰는 작업은 분리된 operation이다.)

> **Note:** iPhone XS는 2.49 GHz processor를 가지고 있다. 즉, 매초 2,490,000,000 clock cycles을 수행한다.

공유 자원에 대한 접근을 동시에 하지 못하도록 다음과 같은 직렬 큐를 사용하여 해결 할 수 있다.

```swift
private let threadSafeCountQueue = DispatchQueue(label: "...")
private var _count = 0
public var count: Int {
  get {
    return threadSafeCountQueue.sync { 
      _count
    }
  }
  set {
    threadSafeCountQueue.sync { 
      _count = newValue
    }
  }
}
```

**각 getter setter로의 동시 접근은 불가하더라도 변경 작업은 의도대로 되지 않음...**



### Thread barrier

공유자원에 대한 변경 로직이 더 복잡한 경우에는 GCD의 **dispatch barrier** 를 사용할 수 있다.

```swift
private let threadSafeCountQueue = DispatchQueue(label: "...",
                                                 attributes: .concurrent)
private var _count = 0
public var count: Int {
  get {
    return threadSafeCountQueue.sync {
      return _count
    }
  }
  set {
    threadSafeCountQueue.async(flags: .barrier) { [unowned self] in
      self._count = newValue
    }
  }
}
```

barrier task는 앞선 모든 읽기 작업이 끝나기 전까지 실행되지 않는다. barrier task가 시작되면 큐는 직렬 큐로 동작하여 하나의 barrier task만 수행된다. 완료 후에는 다시 병렬적으로 동작한다.

## 5.2 Deadlock

두 개의 작업이 서로 다른 작업이 끝나길 기다리는 상황을 말한다. 

세마포어로 여러개의 자원을 제어할 때, 그 순서에 주의해야 한다. 

## 5.3 Priority inversion

- 우선순위 역전 현상은 낮은 qos의 큐에 높은 qos의 큐보다 높은 우선순위가 부여되면 발생한다. 
  - -> 다른 큐를 사용하여 해결
- 또한, 우선 순위가 다른 두 큐가 하나의 공유자원을 사용하는 경우 발생한다.