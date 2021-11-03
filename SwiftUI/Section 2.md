# 2. Getting Started

SwiftUI는 애플이 2014년 Swift를 발표한 이후로 가장 흥미로은 뉴스 중 하나라고 한다. 모두가 코딩하는 애플의 목표에 한발짝 거대한 진보를 했다는데... 스유는 기초를 단순화해서 유저를 기쁘게 할 수 있는 커스텀 기능들에 더 많은 시간을 할애할 수 있게 만들어 줬다고 한다.

이 챕터는 스유 앱을 만드는 기반에 대해 편안함을 느낄 수 있게 해주는 것이 목표이며, 우리는 Xcode에서 실시간 미리보기도 활용할 수 있게 될 것이다. 

이 챕터에서 우리는 색조합 게임을 만들 것이다. 앱의 목표는 랜덤하게 생성된 색과 매칭시키는 것이다. 

이 챕터에서 우리는 다음을 다룰 것이다:

- 코드 각각에 해당하는 UI 를 생성하기 위해 Xcode canvas를 어떻게 사용하는 지 배울 것이다. 코드와 UI는 동기화를 유지할 것이고, 이처럼 한쪽의 변화가 다른 한쪽을 변화시키는 것을 확인할 것이다.
- 이미지에서 보이는 slider를 위한 재사용 가능한 뷰를 생성할 것이다.
- `@State` 프로퍼티를 배울 것이고 상태값이 변할때마다 UI를 갱신하기 위해 이 프로퍼티를 사용할 것이다.
- 유저의 점수를 보여주기 위해 alert를 화면에 띄울 것이다. 

## 2.1 Getting started

**UIKit/RGBullsEye** 앱은 rgb 값으로 랜덤하게 생성된 목표 색을 보여준다. 유저는 슬라이더를 움직여 목표색과 매칭시켜야 한다. 이런 앱을 더욱 스위프트스럽게(Swiftly) 만들거라고 하네.

### Exploring the SwiftUI starter project

project navigator에서 RGBullsEye 그룹에 보면, RGBullsEyeApp.swift 파일이 보일 것이다. (스유 이전에 대게 AppDelegate.Swift 였던 것이다.) 이 파일의 객체는 `ContentView()` 로부터 앱의  `WindowGroup` 을 생성한다.

```swift
@main
struct RGBullsEyeApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
  }
}
```

**`@main` attribute는 이 구조체가 앱의 entry point를 지니고 있다는 의미이다.** `App` 프로토콜은 실제 실행되는 static `main` 함수를 생성하는 데 관여한다. 앱이 시작되면 `ContentView` 의 인스턴스를 보여주며, 이는 ContentView.swift 파일에 정의돼 있다. 이 구조체는 `View` 프로토콜을 채택하고 있다.

```swift
struct ContentView: View {
  var body: some View {
    Text("Hello, world!")
      .padding()
  }
}
```

이것은 스유가 `Text` 뷰를 포함하는 `ContentView` 의 `body` 를 선언하는 방법이다. `padding()` modifier는 텍스트에 10 포인트 패딩을 추가한다.

### Previewing your ContentView

ContentView.swift에서 `ContentView_Previews` 는 `ContentView` 의 인스턴스를 포함하는 뷰를 가지고 있다.

```swift
struct ContentView_Previews : PreviewProvider {
  static var previews: some View {
    ContentView()
  }
}
```

preview를 위한 샘플 데이터를 명시할 수 있는 곳이며, 다른 화면과 폰트 크기를 비교할 수 있다. 



## 2.2 Creating your UI

스유 앱은 storyboard나 view controller가 없다. ContentView.swift가 이들의 역할을 대신한다. UI를 생성하기 위해 코드와 Object library로부터 드래그하는 기능을 조합할 수가 있다. 

스유는 선언적(declarative)이다: UI가 어떻게 보일지 선언하면, 스유는 선언문을 효율적인 코드로 바꿔 우리의 일을 대신해준다. Apple은 우리의 코드를 읽기 쉽도록 유지할 수 있는 양의 view를 생성하는 것을 권장한다. 파라미터화된 재사용 가능한 뷰를 특히 권장한다. 

이 챕터에서는 Interface Builder(IB)에서 UI를 배치한 방식과 유사하게 canvas를 활용할 것이다. 

### Some SwiftUI Vocabulary

뷰를 생성하기 전에 알고넘어가야 할 용어들이 있다.

- **Canvas and Minimap**: 코드 에디터 옆에서 canvas로 앱의 뷰를 미리보기할 수있다. 
- **Modifiers**: UIKit 객체의 속성을 설정하는 대신에 색, 폰트 패딩 등을 위해 modifier method를 활용할 수 있다.
- **Container views**: H, V, ZStack과 Group이 이에 해당한다.

### Creating the target color view

`body` 는 computed property로 단일 `View` 만을 반환한다. 따라서 두개 이상의 뷰를 조합하기 위해서는 container view를 활용해야 한다. 

- canvas의 `Text` 뷰를 **Command-click**하면 코드가 강조되면서 Action 창이 보여진다. 
- **Control-Option-click** 하면 SwiftUI **inspector**가 canvas에 보여진다.
- toolbar에서 + 버튼을 클릭해서 library를 열 수 있다. 캔버스로 드래그하면 하단에 hint 메시지도 확인할 수 있다.
- 스유의 Embed 명령은 단일 객체에서만 수행할 수 있다. IB는 여러 뷰를 선택해서 할 수 있는뎁...

### Creating the button and slider

- Library를 계속 열어두고 싶으면 **Option-click**으로 + 버튼을 누르자.
- 뷰 드래그해서 코드위에 잠시 머무르면 공간 하나 마련해주네 ㅎ
- **Option-Command-P** 는 Resume 버튼 클릭의 단축키다.
- Slider의 값은 `.constant(0.5)` 로 채운다. 그냥 0.5가 아닌 이유는 나중에 알려준대

## 2.3 Updating the UI

view의 property 값이 변할 때 UI를 갱신하도록 하려면 `@State` 프로퍼티로 지정해야한다. `@State` property는 값이 변할 때 뷰가 자신의 외양을 무효화하고 body를 다시 계산한다.

## 2.4 Making reusable views

slider는 기본적으로 동일하기 때문에 하나의 slider view를 정의하고 다른 두 slider를 위해 그것을 재활용하면 된다. 이것이 Apple이 권장하는 바이다.

### Maing the red slider

- slider에 `accentColor(_:Color?)` modifier를 추가하면 `minimumTrackTintColor` 를 설정할 수 있다.

### Bindings

- `$`를 사용하여 read-only 값을 read-write binding 할 수 있다.

### Extracting subviews

- `@State` 과 `@Binding`는 해당 데이터를 소유하냐 소유하지 않냐의 차이로 사용된다.

### Live Preview

UIKit 앱은 slider 액션에 모든 코드를 집어넣는다. 반면 스유는 `State` property를 사용하여 뷰가 일련의 이벤트가 아닌 상태에 의존하게 만든다.

## 2.8 Key Points

- Xcode canvas는 코드와 나란히 놓고 UI를 생성할 수 있게 해준다. 코드와 캔버스간 동기화를 스스로 유지하고 있다.
- 수평 수직 스택을 사용하여 뷰 객체를 구성할 수 있다.
- **Preview**는 다양한 초기 데이터로 앱을 살펴볼 수 있다. **Live Preview**는 시뮬레이터 실행 없이 앱을 볼 수 있게 해준다.
- 재사용가능한 뷰를 생성하는 것을 목표로 해야한다. Xcode의 **Extract Subview** 툴로 이를 쉽게 할 수 있다.
- 스유는 `State` property의 값이 변할 때마다 UI를 갱신한다. `Binding` 으로 subview에 참조를 넘겨 `State` property에 read-write 접근을 가능하게 할 수 있다.

















