# 10. Canceling Operations

operation은 적절하게 작성되었을 때, 실행중인 작업을 취소할 수 있다. 시간이 지날수록 불필요해지는 오래걸리는 작업에 유용하다. 예를 들어, 사용자가 화면을 이탈하거나 테이블 뷰의 셀을 스크롤하여 넘기는 경우가 있다. 이 경우에 결과를 볼 필요가 없다면, 데이터를 로드하거나 복잡한 연산을 계속할 이유가 없다.

## 10.1 The magic of cancel

operation queue로 operation이 관리되면, 더이상 그것을 제어할 수 없다. 다만, `Operation` 의  `cancel` 메소드를 호출하여 제어할 수는 있다.

이 요청을 보내어 작업을 멈추면, `isCancelled` 연산 프로퍼티는 `true` 를 반환할 것 말고는 자동으로 이뤄지는 것은 없다. 

`Operation`의 default `start` 구현체는 `isCancelled` flag가 `true` 인지 확인하고, 그렇다면 즉시 빠져나온다. 

## 10.2 Cancel and cancelAllOperations

특정 `Operation` 을 취소하기 위해선, `cancel` method를 호출하고, operation queue에 있는 모든 작업을 취소하고 싶다면, `OperationQueue` 의 `cancelAllOperations` method를 호출해라.

## 10.3 Updating AsyncOperation

직접 정의한 operation이 취소가능하게 하기 위해선 적절한 위치에서 `isCancelled` 변수를 체크해야 한다. override한 `start` method 처음에 이를 체크하면, 시작 전에 취소할 수 있게 된다.

## 10.4 Canceling a running operation

실행중인 작업의 취소 기능을 지원하기 위해서는 `isCancelled`를 확인하는 코드를 operation 코드 전반에 여러군데 배치해야 한다. 복잡한 작업일 수록 확인하는 코드도 늘어나는 것은 당연하다.

