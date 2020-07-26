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



### 24. Objects vs. Classes

##### Casts

다음과 같은 casting 방식이 존재한다.

- **as?** 는 실패할 수 있는 상황에 사용된다. object가 nil이거나 casting하려는 적합한 type이 없을 때 실패하게 된다. optional type을 반환하며, 사용시 `if let` 과 같은 optional binding을 이용해 unwrap하게 된다.
- **as!** 는 *downcast*라고도 하며, class와 subclass 간의 캐스팅에 사용된다. Implicitly unwrapped optional 과 같이 안전하지 않은 방식으로, 실패하지 않는다는 보장이 있는 경우에만 사용한다.
- **as** 는 전혀 실패하지 않는 경우에 사용된다. Swift는 *NSString*과 *String* 간의 casting은 항상 가능하며 이러한 경우에만 사용한다.



### 25. The Tag Location Screen

##### Create once and re-use

`DateFomatter` 객체와 같이 생성하는 데 상대적으로 오래 걸리는 경우는 global constant로 선언하여 lazy loding 방식으로 값을 초기화 하는 것이 효율적이다. Swift에서 global은 항상 lazy fashion으로 생성된다. 즉,  처음 사용될 때, 생성되고 구성된다.

```swift
private let dateFormatter: DateFormatter = {
	let formatter = DateFormatter()
	formatter.dateStyle = .medium
	formatter.timeStyle = .short
	return formatter
}()
```

위와 같이 closure를 사용한 객체를 사용하면, 사용할 때 한번만 생성되고, 다음에는 재사용할 수 있는 장점이 있다.



##### Content Compression Resistance

view에는 **Content Compression Resistance Priority** 라는 것이 있다. 특정 위치의 고유한 크기의 뷰를 압축가능한 여부의 척도가 되는 값을 나타낸다. 즉, 다른 뷰의 우선도가 더 높다면 다른 뷰에 의해서 압축될 수 있다는 말이다. 이 값은 storyboard의 Size inspector에서도 설정할 수 있다.

