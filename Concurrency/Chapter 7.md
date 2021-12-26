# 7. Operation Queues

Operation을 `OperationQueue` 로 제어할 때 비로소 operation의 장점이 나타난다. GCD의 `DispatchQueue` 처럼, `OperationQueue` class는 `Operation` 의 스케쥴링을 관리하고, 동시에 수행할 operation의 최대 수를 관리할 수 있다.

`OperationQueue` 에는 다음 세가지 방식으로 작업을 추가할 수 있다:

- `Operation` 전달
- 클로저 전달
- `Operation` 배열 전달

operation은 자체적으로는 동기 작업이다. Main thread로부터 분리하기위해 GCD 큐에 비동기적으로 전달할 수 있지만, `OperationQueue` 에 추가하여 operation의 더 큰 concurrency 장점을 얻을 수 있다.

## 7.1 OperationQueue management

operation queue는 **준비된** operation들을, qos나 dependency에 따라 실행한다. `Operation` 을 큐에 추가하자마자, 완료되거나 취소될 때까지 작업을 동작시킨다. 

동일한 `Operation` 은 다른 `OperationQueue` 에 추가할 수 없다. `Operation` 인스턴스는 한번만 수행되는 작업이므로, 여러번 수행할 필요가 있을 때 서브클래스 화하여 선언한다.

### Waiting for completion

`OperationQueue` 의  `waitUntilAllOperationsAreFinished` method는 현재 thread를 block 하기 때문에, main UI thread에서 호출하면 안된다.

필요시에 `DispatchQueue` 를 구성하여 호출하자. 일부 작업들만 기다려야 하는 경우에는 `addOperations(_:waitUntilFinished:)` method를 사용하자.

### Quality of service

`OperationQueue` 는 서로 다른 qos를 갖는 operation을 추가하여 응당하는 우선순위에 따라 작업을 실행할 수 있다는 점에서 `DispatchGroup` 과 유사하다.

기본 qos는 `.backgroud` 이다. operation queue에 직접 `qualityOfService` 를 설정할 수 있지만, 큐에의해 관리되는 operation의 qos가 적용될 수도 있다.

### Pausing the queue

`isSuspended` 프로퍼티를 설정하여 일지 중지할 수 있다. 진행중인 작업이외에 새로 추가되는 작업은 `false` 로 재설정될 때까지 스케쥴링 되지 않는다.

### Maximum number of operations

기본적으로 디바이스가 허용하는 만큼의 작업들을 한번에 처리하지만 그 수를 제한할 수도 있다. `maxConcurrentOperationCount` 를 1로 설정하면 직렬 큐처럼 동작할 것이다.

### Underlying DispachQueue

`underlyingQueue` 에 `DispatchQueue`를 할당할 수 있다. 

> **Note:** main queue를 underlying queue로 설정하면 안된다.
>

## 7.2 Fix the previous project

### UIActivityIndicator

### Updating the table

