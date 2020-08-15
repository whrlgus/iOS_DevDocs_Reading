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

view에는 **Content Compression Resistance Priority** (내용 압축 저항 우선순위?) 라는 것이 있다. 뷰에서 표현하려는 내용이 많은 경우에 옆에 있는 다른 뷰가 압축될 수 있고, 압축이 가능한지 여부를 결정짓는 척도이다. 즉, A 뷰의 priority가 B 뷰의 priority보다 더 높다면, A 뷰는 B 뷰에 의해 압축되는 경우는 없고, 반대의 경우는 가능하다는 말이다. 이 값은 storyboard의 Size inspector에서도 설정할 수 있다.



##### Unwind segue

Unwind segues 는 대게 delegate protocol에 비해 간편하게 controller간 통신을 할 수 있게 해준다. segue를 인자로 받는 IBAction method를 정의하여 이벤트 발생 객체를 storyboard의 Exit에 연결해주면 prepare() method를 거쳐서 정의한 action method의 내용을 실행할 수 있게된다.



### 26. Adding Polish

##### Keyboard activation

`func becomeFirstResponder() -> Bool` 메소드를 사용해서 키보드를 활성화할 view를 반응하게? 만들어 준다.



##### UITapGestureRecognizer

Target-action pattern으로 target에 tap 을 하게되면 action에 해당하는 지정된 method를 호출하게 된다. `var cancelsTouchesInView: Bool { get set }` 이란 property는 default가 true로 view에 gesture가 전달되지 않는다. 이 값을 false로 바꾸면, gesture가 전달되어 반응을 하는 코드를 작성할 수 있게 된다.



##### HUD

Heads-Up Display의 약자로, 일의 진행 상태 혹은, 완료 상태 등을 사용자에게 알려주기 위한 목적으로 사용한다. 



##### Convenience constructor

class method로 작성하여, `let hubView = HudView()` 대신에 `let hudView = HudView.hud(inView: parentView, animated: true)` 와 같이 instance를 생성할 수 있는 구조(?)를 말한다.



##### UIView의 draw() method

UIKit 에서 view를 그릴 때마다 호출되는 함수이다. iOS의 모든 것은 event-driven으로 view는 UIKit이 그리라고 하기 전까지는 스크린에 view를 그리지 않는다. 즉, 직접 `draw()` method를 호출할 일이 없다는 말이다. 만약 view를 직접 다시 그리고 싶다면, view의 `setNeedsDisplay()` method를 호출해서 `draw()` method가 호출되도록 하자.



### 27. Saving Location