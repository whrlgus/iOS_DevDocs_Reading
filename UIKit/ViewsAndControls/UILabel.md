# UILabel

한 줄 이상의 정보전달 text 를 보여주기 위한 view이다.



### Declaration

```swift
class UILabel : UIView
```





### Accessing the Text Attributes

```swift
var text: String? { get set }
```

label이 보여주는 text이다. 이 property는 default값이 nil이고, 값을 할당하면 `attributedText` 속성도 같은 값이 할당된다. 

```swift
@NSCopying var attributedText: NSAttributedString? { get set }
```

값의 할당에 있어서 `text` 속성과 같게 생각하면 되고, 표면적으로 그 쓰임을 구별할 수 없어, 정확히 어떤 것이 다른지는 나중에 알아보자.

```swift
var font: UIFont! { get set }
```

text의 전체 혹은 부분 style을 바꿀 수 있다. Default 값으로 UIFont 의 class method인 `systemFont(ofSize:)` 를 이용한 17 points의 system font가 설정되어 있다. 이 값을 nil로 설정한다면 default 값으로 reset 된다.

```swift
var textColor: UIColor! { get set }
```

font와 마찬가지로 text의 부분 혹은 전체 색을 설정할 수 있다. 부분 설정을 위해서 새로운 attributed string을 생성해야 한다.

```swift
var textAlignment: NSTextAlignment { get set }
```

최근 iOS 버전에서는 `NSTextAlignment.natural` 값이 default로 설정되어 있다. 이 값은 arabic과 같은 RTL(right to left) text의 경우 오른쪽 정렬로 적용이 되고, 영어나 한글같은 LTR은 왼쪽 정렬이 된다. 즉, 앱의 current localization 설정에 따라 다르게 적용이 된다.

```swift
var lineBreakMode: NSLineBreakMode { get set }
```

default 값은 `NSLineBreakMode.byTruncatingTail` 이고, `byWordWrapping` 은 단어 단위로 래핑이 발생하여 여러줄에 텍스트를 표현할 경우 단어가 끊기지 않도록 한다.

```swift
var isEnabled: Bool { get set }
```

이 속성은 label의 text가 어떻게 보여질 지 결정한다. default는 true이며, false로 값이 설정되면 텍스트를 흐리게 표현하여 not active 상태임을 간접적으로 표현한다.

```swift
var enablesMarqueeWhenAncestorFocused: Bool { get set }
```

label의 view hierarchy의 any ancestor가 focus되면 text가 scroll 된다. https://developer.apple.com/videos/play/wwdc2018-208/?time=1514



### Sizing the Label's Text

```Swift
var adjustsFontSizeToFitWidth: Bool { get set }
```

label의 bounding rectangle에 text를 딱 맞게 채우기 위해 font size를 줄일 수 있는 설정이다. `minimumScaleFactor` 의 값도 설정돼 있어야 하며, Single-line label에만 적용이 가능하다.

```swift
var allowsDefaultTighteningForTruncation: Bool { get set }
```

font, line width 등과 같은 여러 다른 요소들에 의해 maximum amount of tightening이 결정되어 label text의 intercharacter spacing을 tighten 한다. Single-line label에만 적용된다.

```swift
var baselineAdjustment: UIBaselineAdjustment { get set }
```

font의 크기에 따라 rounding box의 범위가 결정되고, 만약, shirinking이 일어난다면 box의 범위 내에서 위, 중앙, 아래로 크기가 줄어든 text를 정렬할 때 사용하는 옵션인 듯 하다.

```swift
var minimumScaleFactor: CGFloat { get set }
```

`adjustsFontSizeToFitWidth` 의 값이 true일 때 적용할 수 있으며, 가장 작게 줄어드는 크기를 비율로 한정할 수 있다. 만약, 0.5로 설정한다면, 절반 크기 이하로 줄지 않는다.

```swift
var numberOfLines: Int { get set }
```

label의 text를 bounding rectangle에 맞추기 위한 최대 line의 수를 설정할 수 있다. 이상을 넘어가는 text는 line break의 옵션 설정에 따라 처리된다.



### Managing Highlight Values

### Drawing a Shadow

### Drawing and Positioning Overrides

### Getting the Layout Constraints

### Accessing Additional Attributes

### Related Types

### Instance Properties