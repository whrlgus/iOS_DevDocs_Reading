### 21. Swift Review



### 23. Use Location Data

##### Core Location Error의 종류

Core Location error의 종류로 다음과 같은 것들이 있다.

- CLError.locationUnknown - 위치가 현재 알려지지 않은 상태이다. 하지만 Core Location은 계속 위치를 찾는다.
- CLError.denied - 사용자가 앱의 location service 사용 권한을 부여하지 않은 상태이다.
- CLError.network - 네트워크 관련 에러이다.

이외에도 여러가지가 있다. Error 클래스의 subclass인 NSError의 property인 code를 통해 CLError enumeration에 정의된 에러 종류를 판별할 수 있다. 



##### 에러 처리

다음 조건부에서 kCLErrorDomain과 같은지 확인하는 이유는 에러의 종류가 CLError인지를 확인하기 위함이다.

```swift
if errer.domain == kCLErrorDomain && error.code == CLError.denied.rawValue {
...
}
```



CLLocation.horizontalAccuracy는 위치가 타당하지 않을 때 음수 값을 갖는다. 값이 클 수록 부정확하다고 여기면 된다.



##### Reverse geocoding

reverse geocoding은 좌표를 human-readable 주소로 바꾸는 것을 말한다. 반대 과정인 주소를 GPS 좌표로 바꾸는 것은 regular or forward geocoding이라고 한다.