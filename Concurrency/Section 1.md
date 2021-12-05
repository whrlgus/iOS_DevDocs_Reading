# 1. Introduction

## 1.1 What is concurrency?

위키피디아에 따르면, 프로그램, 알고리즘, 문제를 순서에 상관없이 혹은 부분적으로 정렬된 요소로 분해할 수 있는 속성이라고 한다. 즉, 앱의 로직에서 어떤 부분을 순서에 상관없이 혹은 동시에 수행하더라도 그 결과는 기대한 대로 도출된다.

현대 기기들을 하나 이상의 CPU를 가지고 있으며 이는 동시에 여러 일을 수행할 수 있음을 의미한다. 앱을 논리적인 코드 덩어리로 나눔으로써, 프로그램의 여러 부분을 동시에 수행할 수 있고 결과적으로 성능이 향상된다.

## 1.2 why use concurrency?

앱의 동작을 매끄럽게 만들고 아주 작은 시간 마저 줄이는 것이, 곧 사용자로 하여금 불편함을 없앨 수 있는 방법이다.

concurrency를 활용하면, 자연스레 작은 단위의, 더 관리하기 용이한 method를 동시에 수행할 수 있도록 만들게 될 것이다.

## 1.3 How to use concurrency

- Grand Central Dispatch
- `Operation` class

# 2. GCD vs. Operations

## 2.1 Grand Central Dispatch

GCD는 C의 **libdispatch** 라이브러리 구현체이다. 가용 자원에 따라서 병렬적으로 수행할 수 있는 method나 closure인 **task** 를 줄세우는 것이 그 목적이다. 

### Synchronous and asynchronous tasks

큐에 있는 작업은 동기 혹은 비동기로 실행될 수 있다. 작업이 동기적으로 수행되면, 앱은 작업 수행이 완료될 때까지 현재 run loop를 멈추며 기다린다. 반면에 작업이 비동기적으로 수행되면, 즉시 실행을 반환한다.

> **Note:** 큐가 FIFO란 것은 시작 시점에만 해당될 뿐, 완료 시점과는 별개이다. 

### Serial and concurrent queues

작업을 수행할 큐는 **serial** 또는 **concurrent** 로 구분된다. Serial 큐는 단일 쓰레드만 사용하며, 주어진 시간에 하나의 테스크만 수행된다. 반면에 Concurrent 큐는 시스템이 허용하는 만큼의 쓰레드를 활용할 수 있다. 쓰레드는 Concurrent 큐에서 필요한 만큼 생성되고 사용된다.

> **Note:** iOS 장치의 가용 리소스 상황에 따라서 concurrent 큐라도 한번에 한 작업만 수행하게될 수도 있다.

### Asynchronous doesn't mean concurrent

**동기**냐 **비동기**냐는 큐가 다음 작업으로 이행하기 전에 작업이 완수되기를 기다리는지 그렇지 않은 지로 구분할 수 있다. 반면에 **직렬** 이냐 **병렬** 이냐는 큐가 단일 쓰레드를 사용하는지 여러 쓰레드를 사용하는지를 구분할 수 있다. 다른 말로 동기/비동기는 테스크의 출발지, 직렬/병렬은 테스크의 목적지와 연결지을 수 있다.

## 2.2 Operations

GCD는 백그라운드에서 한번 수행할 일반적인 테스크에 사용하기 좋다. 이미지 편집 작업과 같은 여러번 수행될 수 있는 기능을 설계할 때에는 `Operation` 의 서브클래스로 캡슐화할 수 있다.

### Operation subclassing

`Operation` 은 완전히 기능적인 클래스로 `OperationQueue` 에 전달될 수 있다. 마치 GCD에서 작업 클로저를 `DispatchQueue` 에 전달하는 것과 같다. 클래스이며 변수를 포함하기 때문에, 특정 시점에 작업의 상태를 확인할 수 있다.

Operation은 다음 상태중 하나에 해당될 수 있다.

- `isReady`
- `isExecuting`
- `isCancelled`
- `isFinished`

GCD와 다르게 operation은 기본적으로 동기적으로 수행된다. 비동기로 수행되도록 하려면 추가 작업이 필요하다.

### Bonus features

테스크를 취소할 수 있고, 상태를 알릴 수 있으며, 비동기 작업을 감싸 다양한 테스크들 사이의 의존성을 특정할 수 있다.

### BlockOperation

GCD와 같이 작업을 단순화하기 위해 `DispatchQueue` 를 생성하지 않고 `BlockOperation` 클래스를 활용할 수 있다.

`Operation` 의 서브클래스인 `BlockOperation` 은 하나 이상의 클로저를 기본적으로 전역 큐에서 병렬적으로 수행한다.

> **Note:** Block operation은 병렬적으로 수행된다. 직렬적으로 수행하기 위해서는 dispatch queue를 사용해야 한다.

## 2.3 Which should you use?

단순한 작업에는 GCD를, 테스크 관리의 필요성이 있다면 Operation을 사용할 수 있다.

다만, 여러 사람들은 높은 수준의 추상화가 이뤄진 것을 사용하라는 애플의 가이드에 따라 GCD 를 기반으로 구성된 Operation을 사용하기를 권장한다.

궁극적으로는 장기적으로 유지보수에 용이한 것을 택하여 사용하는 것이 좋다.