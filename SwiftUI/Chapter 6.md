# 6. Controls & User Input

`TextField`, `Button`, `Stepper` 등과 같은 사용자 입력을 위한 control과 리팩토링에 대해 알아본다.

## 6.1 A simple registration form

### A bit of refactoring

재사용성이 높고 코드의 양을 줄이는 리팩토링은 애플이 권장하는 패턴이며, 이 사항에 대한 실습을 진행할 것이다.

### Refactoring the logo image

### Refactoring the welcome message

## 6.2 Creating the registration view

## 6.3 Power to the user: the TextField

> **Note**: UIKit 보다 다형성을 많이 갖으며, `.background` modifier는 `View` 를 채택하는 어떤 타입이든 수용할 수 있다. (`Color` 뿐만 아니라 `Image`, `Shape` 과 같은...)

### Styling the TextField

`RoundedRectangle()` 에 `.stroke()` modifier를 사용하면 내용물은 보이지 않고 border만 남는다.

### Creating a custom text style

### Creating a custom modifier

다른 뷰에도 적용할 수 있기 때문에 custom text style보다는 custom modifier가 선호된다.

`ViewModifier`는 `body` 멤버를 정의하지만 property가 아닌 function이다.

이를 적용하기 위해서 `ModifiedContent` struct를 사용한다.

`View` extension을 활용하면 기타 다른 modifier 사용 방식과 동일하게 사용할 수 있다.

### A peek at TextField's initializer

`TextField` 의 생성자에는 Localized 와 non-localized 버전이 있다.

```swift
public init<S>(
  _ title: S,
  text: Binding<String>,
  onEditingChanged: @escaping (Bool) -> Void = { _ in },
  onCommit: @escaping () -> Void = {}
) where S : StringProtocol
```

- `onEditingChanged`: 편집이 포커싱될 때와 포커싱을 잃을 때 호출된다.
- `onCommit`: 사용자가 commit 액션을 취할때 호출된다. (반환 키 클릭과 같은...) 다음 필드로 자동으로 옮기고자 할 때 활용할 수 있다.

위와 다른 생성자(non-localized version)는 파라미터에 formatter가 추가되어 있다.

```swift
public init<S, T>(
  _ title: S,
  value: Binding<T>,
  formatter: Formatter,
  onEditingChanged: @escaping (Bool) -> Void = { _ in },
  onCommit: @escaping () -> Void = {}
) where S : StringProtocol
```

- `fomatter` 파라미터는 `Foundation` 의 추상 클래스인 `Formatter` 를 상속하는 인스턴스이다. String과 다른 타입(number나 date) 을 편집할 때 사용된다.
- `T` generic parameter는 textfield에 의해 처리되는 실제 타입을 결정한다.

### Showing the keyboard

`@ObservedObject` 속성은 `@State` 속성과 유사하지만 custom class에 적용되었다는 사실에 주목하자. 자세한건 챕터 8에서...

> **Note**: 여러개의 padding modifier를 갖으면, 각 방향에서 padding값을 모두 더한 결과가 적용된다.

## 6.4 Taps and buttons

스유에서의 버튼은 UIKit/AppKit의 버튼보다 더 유연하다. 아래 정의에서 알 수 있듯이, `View` 에 해당하는 모든 것으로 버튼을 구성할 수 있다.

```swift
struct Button<Label> where Label : View	
```

버튼의 생성자는 다음과 같다.

```swift
init(
  action: @escaping () -> Void,
  @ViewBuilder label: () -> Label
)
```

- **action**: the trigger handler
- **label**: the button content

`@ViewBuilder` attribute는 `label` 파라미터에 적용되어 해당 클로저가 여러개의 자식 뷰들을 반환할 수 있게 해준다.

> **Note**: tap handler 파라미터는 **tap** 이나 **tapAction** 보다는 **action** 으로 불려진다. 문서를 보면 **tap handler** 가 아닌, **trigger handler** 로 불린다. 
>
> 그 이유는, iOS에서는 tap, macOS에서는 마우스 클릭, watchOS에서는 Digital Crown press 이기 때문이다.

### Submitting the form

Inline closure를 추가할 수 있지만, 뷰의 선언부를 지저분하게 만드는 것은 피하는 것이 좋다. 따라서 instance method를 대신 사용하여 trigger event를 처리한다.

`UserManager` 는 `ObservableObject` 를 채택한다. 해당 클래스를 뷰내부에서 사용할 수 있게 해주는 protocol이고, instance state가 변경될 때 뷰를 갱신한다. 내부에는 `@Published` attribute로 표시된 두 속성이 있다. 이 것이 뷰 갱신을 유발하는 상태를 식별한다. 

`@EnvironmentObject` attribute 를 표시하여 선언하는 이유는, 해당 앱 전반에 걸쳐 한번만 인스턴스를 주입할 것이고, 그것이 필요한 어떤 환경에서든 읽을 수 있도록 하기 위함이다. 9 챕터에서 더 자세히... 

### Styling the button

### Reacting to input: validation

### Reacting to input: counting characters

## 6.5 Toggle Control

## 6.6 Other controls

### Slider

### Stepper

### SecureField

## 6.7 Key points

- Refactoring 과 reusing view는 지나쳐서는 안되는 중요한 부분이다.
- `ViewModifier` 를 이용하여 커스텀 modifier를 생성할 수 있다.
- 사용자 입력을 처리하기 위해서 `TextField` 를 사용할 수 있고, 민감한 정보는 `SecureField` 를 사용할 수 있다.
- 키보드가 보여질 때, `TextField` 를 가리지 않도록 주의해야 한다. 이를 위해서 Notification Center와 키보드 높이를 활용할 수 있다.
- UIKit/AppKit 의 버튼과 비교하여 스유의 버튼은 컨텐츠를 구성하는 데 더 자유롭다.
- 입력 검증이 더 쉽다. 규칙을 정하기만 하면 스유에서 상태가 변할 때 그 규칙을 알아서 처리하기 때문이다.
- Toggle, slider, stepper와 같은, 사용자 입력을 처리하기 위한 여러 컨드롤들이 있다.