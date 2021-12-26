# 9. Operation Dependencies

operation 간의 의존관계를 형성하면, 상호작용에 다음 두가지 장점을 얻을 수 있다:

1. 의존하는 작업은 선수 작업이 완료되기 이전에 실행되지 않음을 보장한다.
2. 첫번째 작업에서 두번째 작업으로 데이터를 자동으로 전달하는 깔끔한 방식을 제공한다.

GCD 대신에 `Operation`을 사용하는 주요 이유들 중의 하나가 바로 이 dependency이다.

## 9.1 Modular design

네트워크로부터 다운로드하는 작업과 tilt shift 수행하는 작업을 단일 작업으로 생성할 수도 있지만, 이것은 좋지 못한 구조 설계이다.

이상적으로 클래스는 단일 작업만을 수행하여 프로젝트 내외부에서 재활용이 가능해야 한다. tilt shift 작업으로 네트워킹 코드를 작성하면, 번들 이미지를 위한 작업에는 재활용할 수 없게된다. 생성자 파라미터를 늘리는 방법도 있겠지만, 클래스의 몸집만 키우는 격이된다. 유지보수에 오랜 시간이 걸리며 설계해야하는 테스트 케이스도 늘어난다.

## 9.2 Specifying dependencies

`addDependency(_:)`, `removeDependency(_:)` 로 추가 제거할 수 있다. read-only property로 `dependencies` 를 제공하며, 해당 operation가 의존하는 `Operation` 들의 배열을 반환한다.

### Avoiding the pyramid of doom

dependencies는 코드를 읽기 쉽게 해주는 부차적인 장점이 있다. 만약 GCD로 구현하게 된다면 다음과 같은 pseudo-code가 만들어질 것이다.

```swift
let network = NetworkClass()
network.onDownloaded { raw in
  guard let raw = raw else { return }

  let decrypt = DecryptClass(raw)
  decrypt.onDecrypted { decrypted in
    guard let decrypted = decrypted else { return }
    
    let tilt = TiltShiftClass(decrypted)
    tilt.onTiltShifted { tilted in
      guard let tilted = tilted else { return }
    }
  }
}
```

유지보수하기 어렵고, Retain cycle이나 error checking은 전혀 고려되지도 않았다.

## 9.3 Watch out for deadlock

의존관계의 순환 구조가 형성되면 deadlock에 직면하게 되고, 구조를 재설계해야 할 것이다.

## 9.4 Passing data between operations

operation의 이점은 그것이 재공하는 캡슐화와 재활용성이다. 내부 프로퍼티의 이름을 외부에서도 그대로 쓸 것이라는 보장은 없다.

### Using protocols

프로토콜을 이용하여 의존 분리 및 추상화가 가능하다.

### Adding extensions

**Swift Style Guide** 은 클래스 정의를 활용하는 것보단 `extension` 을 이용하는 것을 권장한다.

### Searching for the protocol

## 9.5 Updating the table view controller

### Custom completion handler