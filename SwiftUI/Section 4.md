# 4. Testing & Debugging

앱에 테스트를 추가하는 것은 앱이 우리가 예상한 대로 임을 보장하기 위한 통합적이고 자동화된 방식이다. 뿐만 아니라, 미래의 변화가 존재하는 기능을 깨버리지 않게 함을 보장한다.

## 4.1 Different types of tests

앱에 적용할 수있는 세가지의 테스트 유형이 있다. 복잡도 순으로, 유닛 테스트, 통합 테스트, UI 테스트가 그것이다. 

모든 테스트의 기본이 되는 것은 **Unit Test** 이다. 각 unit test는 입력에 따른 예상 출력을 검증하는 것이다. 다량의 unit test가 같은 코드 조각을 테스트할 수 있으나, 각 unit test는 단일의 코드 단위에 집중해야 한다. unit test는 자주 수행될 것이므로, 밀리초 단위로 수행되어야 한다. 

**Integration test**는 코드의 여러 부분들이 서로 잘 맞물려 동작하는지 검증하는 것이다. 외부 API 같은 영역도 포함된다. 통합테스트는 단일 테스트보다 상대적으로 복잡하므로, 오래걸릴 것이고 덜 실행하게 될 것이다.

**UI Test** 는 사용자 행동에 대한 테스트이다. 사용자 인터랙션을 시뮬레이션하며, 행동에 따른 예상 반응을 검증하는 것이다.

이러한 테스트는 복잡도 순으로 앱의 더 넓은 영역을 확인하는 것이다. 

## 4.2 Debugging SwiftUI apps

### Exploring breakpoint control

> Note: 만약 시뮬레이터에서 앱을 실행하여 (lldb) prompt에서 값을 확인하려면, `po self.memory` 가 아닌 `po self._memory._value` 를 입력해야 한다. (수정되어야 할 버그라고 말하넹... 여태 안나오면 print 로 찍어서 봤는데...)

## 4.3 Adding UI tests

앱에서 모든 경우에 대한 테스트를 작성하지 않더라도, 버그를 발견했을 때 테스트를 작성하는 것은 유익하다고 한다. 테스트를 작성하는 것이 곧 버그를 수정했음을 의미한다. 미래에 다시 버그가 재발할 때 알림을 제공하기도 한다.

`XCTest` framework는 Apple의 기본 테스팅 라이브러리를 포함한다. 테스트 클래스는 `XCTestCase` 를 상속한다. 테스트 프로세스는  `setUpWithError()` 는 클래스 내의 각 테스트 method 실행 전에 호출하고, 각 테스트 메소드가 완료될 때 `tearDownWithError()` 를 호출한다.

테스트는 입력에 따른 출력을 검증하는 것으로 `setupWithError()` 에서 각 메소드 실행전에 상태를 갖도록 하고, `tearDownWithError()` 에서 상태를 초기화하여 다음 테스트를 위한 준비를 해야한다.

```swift
continueAgterFaulure = false
```

실패 이후에 테스트 절차를 중지하도록 하는 코드이다. 테스트가 실패할 때 자주 예상치 못한 상태에 맞닥뜨리게 되는데, 이럴 때마다 넘어가지 않고 바로 고치는 것이 좋다.

"UI Test 작성을 시작하기 위해 recording을 사용하라" UI Test를 작성하는 데 많은 시간을 절약해 줄 것이다.

## 4.4 Creating a UI Test

테스트 이름은 무엇을 테스트하는 지, 태스트의 환경은 어떤지, 결과는 어때야 하는지를 알 수 있도록 지어야 한다.

## 4.5 Accessing UI elements

```swift
let memoryButton = app.buttons["M+"]
memoryButton.tap()
```

찾는 버튼을 위와 같이 찾을 수 있고, 액션을 취하게 할 수도 있다.

## 4.6 Reading the user interface

```swift
.accessibility(identifier: "display")
```

위 modifier를 통해 테스트 시 접근할 수 있는 식별자 설정이 가능하게 된다. 이것이 없으면 기본적으로 ui element는 label로 지정된다.

모든 테스팅 assertion은 `XCT` 를 prefix로 시작된다. (옵씨의 네이밍 컨벤션 잔재라고 한다.)

## 4.8 Adding more complex tests

`XCTAssert` 와 다르게 `XCTAssertEqual`은 실패시 메시지를 보여준다.

## 4.9 Simulating user interaction

## 4.10 Testing multiple platforms

## 4.11 Challenge

## 4.12 Key points

### 