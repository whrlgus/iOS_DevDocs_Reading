[링크](https://developer.apple.com/documentation/uikit/uilayoutguide)

# UILayoutGuide 

auto layout과 상호작용이 가능한 직사각형의 영역

## Declaration

```swift
class UILayoutGuide : NSObject
```



## Overview

Layout guide는 user interface에서 inter-view space를 구현하거나 encapsulation을 할 때 사용했었을 dummy view를 대체하기 위해 사용한다. Dummy view가 필요한 auto layout technique이 여럿 존재했었다. dummy view는 자체적으로 어떠한 시각적인 요소를 갖지 않고 단지 view hierarchy의 직사각형의 지역을 정의하기 위해 사용된다. (예시는 링크 본문 참조 ㅎㅎ) dummy view는 크고 복잡한 user interface를 self-contained(독립의)한 modular(조립식) 덩어리로 쪼갤 수 있게 해준다. 적절히 사용한다면, auto layout constraint 로직을 단순화 하는데 매우 효과적이다.

view 계층에 dummy view를 추가하는 것과 관련한 많은 비용이 존재한다. 첫째, view를 생성하고 유지하는 비용이 있다. 둘째, view 계층의 member로서, 계층이 수행하는 모든 일에 overhead를 더한다. 무엇보다도, 다른 뷰를 위한 message를 가로챌 수 있고, 발견하기 매우 어려운 문제가 될 수 있다.

UILayoutGuide class는 이전 dummy view가 수행했던 역할을 대체하기 위해서 고안되었고, 안전하고 효율적인 방식으로 처리할 수 있게 해준다. view 계층에 포함되지 않고, owning view의 coordinate system에서 직사각형의 영역만을 정의하여 auto layout과 상호작용할 수 있게 해준다.



## Creating Layout Guides

Layout guide를 생성하기 위해 다음 단계를 수행하자

1. 새로운 layout guide instance를 생성한다.
2.  `addLayoutGuide(_:)` method를 호출하여 view에 instance를 추가한다.
3. auto layout 을 사용하여 layout guide의 위치와 크기를 정의한다.

아래는 layout guide를 이용하여 view 사이에 equal spacing을 정의하는 예제이다. (코드가 예전 버전이군... )

```swift
let space1 = UILayoutGuide()
view.addLayoutGuide(space1)
 
let space2 = UILayoutGuide()
view.addLayoutGuide(space2)
 
space1.widthAnchor.constraintEqualToAnchor(space2.widthAnchor).active = true
saveButton.trailingAnchor.constraintEqualToAnchor(space1.leadingAnchor).active = true
cancelButton.leadingAnchor.constraintEqualToAnchor(space1.trailingAnchor).active = true
cancelButton.trailingAnchor.constraintEqualToAnchor(space2.leadingAnchor).active = true
clearButton.leadingAnchor.constraintEqualToAnchor(space2.trailingAnchor).active = true
```



Layout guide는 여러 view와 control을 포함하고 있는 black box로서 행동할 수도 있다. view를 캡슐화하고, 조립 가능한 덩어리로 쪼갤 수 있게 해준다. (label의 content hugging priority를 높여주자.. ㅎ)

```swift
let container = UILayoutGuide()
view.addLayoutGuide(container)
 
// Set interior constraints
label.lastBaselineAnchor.constraintEqualToAnchor(textField.lastBaselineAnchor).active = true
label.leadingAnchor.constraintEqualToAnchor(container.leadingAnchor).active = true
textField.leadingAnchor.constraintEqualToAnchor(label.trailingAnchor, constant: 8.0).active = true
textField.trailingAnchor.constraintEqualToAnchor(container.trailingAnchor).active = true
textField.topAnchor.constraintEqualToAnchor(container.topAnchor).active = true
textField.bottomAnchor.constraintEqualToAnchor(container.bottomAnchor).active = true
 
// Set exterior constraints
// The contents of the container can be treated as a black box
let margins = view.layoutMarginsGuide
 
container.leadingAnchor.constraintEqualToAnchor(margins.leadingAnchor).active = true
container.trailingAnchor.constraintEqualToAnchor(margins.trailingAnchor).active = true
container.topAnchor.constraintEqualToAnchor(topLayoutGuide.bottomAnchor, constant: 20.0).active = true
```

> **Note**
>
> Layout guide는 경량화된 방법으로 layout의 부분을 캡슐화한다. 주목할 부분은, 이 기술은 auto layout이 어떻게 캡슐화된 view들과 상호작용하는지에만 영향을 미치며, view 계층에 변화를 주지 않는다는 점이다. 그리고 container view와 container view controller를 사용하면 view의 캡슐화를 더 낫게 처리할 수 있다. 
>
> 추가적으로 layout constraint는 그 contents를 완전히 캡슐화 하지 않는다. system은 여전히 layout guide 내 외부 사이의 priority of optional constraint를 비교하고 있다.