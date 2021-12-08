# 4. Groups & Semaphores

단지 하나의 job을 큐에 넘기는 것 이외에, job들을 그룹화하는 작업이 필요할 수 있다. 개개의 작업이 동시에 시작할 필요는 없으나, 언제 끝나는지는 알아야 할 필요가 있는데, 이 때 **Dispatch Groups** 을 사용하면 된다.

## 4.1 DispatchGroup

`DispatchGroup` class는 task 그룹의 완료 여부를 추적하기 위해 사용할 수 있다.

```swift
let group = DispatchGroup()

someQueue.async(group: group) { ... your work ... } 
someQueue.async(group: group) { ... more work .... }
someOtherQueue.async(group: group) { ... other work ... } 

group.notify(queue: DispatchQueue.main) { [weak self] in
  self?.textLabel.text = "All jobs have completed"
}
```

`async` method의 인자로 group을 전달한다. 그룹은 하나의 dispatch queue에만 사용될 필요가 없고, 여러 큐에 job을 보내어 작업의 우선순위에 따라 수행하도록 할 수 있다. `DispatchGroup`은 `notify(queue:)` method를 제공하며, 모든 job이 끝날 때 호출된다.

> **Note:** 알림 자체는 비동기로 동작하기 때문에, 이전 작업이 끝나기 전에는 notify 메소드 호출 이후에도 job을 group에 전달할 수 있다.

### Synchronous waiting

그룹의 완료 알림을 비동기적으로 반응할 수 없는 경우에 사용할 수 있는 method는 `wait` 이다. 

```swift
let group = DispatchGroup()

someQueue.async(group: group) { ... }
someQueue.async(group: group) { ... }
someOtherQueue.async(group: group) { ... } 

if group.wait(timeout: .now() + 60) == .timedOut {
  print("The jobs didn’t finish in 60 seconds")
}
```

동기적으로 모든 job이 완료될 때까지 현재 큐를 block하며, method 인자에 optional로 wait time을 지정할 수 있다. 

> **Note: ** 현재 큐를 block하기 때문데, main queue에서 `wait` 을 사용하지 말자.

### Wrapping asynchronous methods

```swift
queue.dispatch(group: group) {
  // count is 1
  group.enter()
  // count is 2
  someAsyncMethod { 
    defer { group.leave() }
    
    // Perform your work here,
    // count goes back to 1 once complete
  }
}
```

closure 내부에 비동기 작업이 있다면, 해당 closure가 아직 끝나지 않았음을 알리는 무언가가 필요하다. `DispatchGroup` 의 `enter` method 가 그 역할을 한다. `enter` 는 반드시 `leave` 와 쌍을 이뤄야 하며, `defer` statement를 활용하면 빼먹는 실수를 줄일 수 있다.

### Downloading images



## 4.2 Semaphores

얼마나 많은 쓰레드가 하나의 공유자원에 접근할 수 있는지 제어할 필요가 있다. 
