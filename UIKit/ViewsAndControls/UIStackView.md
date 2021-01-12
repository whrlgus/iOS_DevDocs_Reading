[본문](https://developer.apple.com/documentation/uikit/uistackview)

# UIStackView

행이나 열로 view들의 집합을 놓기 위한 streamlined(능률적인, 최신식의) interface

## Declaration

```swift
class UIStackView: UIView
```



## Overview

auto layout은 device의 orientation, screen size, 허용 공간 내의 어떠한 변화에 동적으로 반응할 수 있는 user interface를 생성할 수 있게 해준다. stack view를 사용하면 이러한 auto layout의 기능을 이용할 수 있게 된다. stack view는 arrangedSubviews property에 있는 모든 view의 layout(배치)을 관리한다. 이 view들은 stack view의 axis를 따라 정렬되어 있다. stack view의 **axis**, **distribution**, **alignment**, **spacing**, 그리고 다른 property에 따라 view를 다양하게 배치할 수 있다.

<img src = "https://docs-assets.developer.apple.com/published/82128953f6/uistack_hero_2x_04e50947-5aa0-4403-825b-26ba4c1662bd.png" width = 500/>

IB에서의 활용법은 [본문](https://developer.apple.com/documentation/uikit/uistackview) 참조

## Stack View and Auto Layout

stack view는 arranged view의 위치와 크기를 결정하기 위해 auto layout를 사용한다. stack view는 arranged view의 첫번 째와 마지막 view를 axis에 따른 edge에 일치시킨다. horizontal stack 에서, 첫 view의 leading edge를 stack view의 leading edge에 고정하고, 마지막 view의 trailing edge를 stack view의 trailing edge에 고정한다는 의미이다. (vertical stack에서는 각각 top과 bottom.) 만약, `isLayoutMarginsRelativeArrangement` property를 true로 설정한다면, stack view는 content를 bounds가 아닌 연관된 margin에 고정한다. 

UIStackView.Distribution.fillEqually 이외의 모든 distribution에서는 stack view가 축을 따르는 자신의 크기를 정할 때, 각 arranged view의 intrinsicContentSize를 사용한다. fillEqually는 축에 따라 stackview의 arranged subview를 같은 크기로 조정하여 채운다. 

UIStackView.Alignment.fill 을 제외한 모든 alignment에서 stack view는 축의 직각에 해당하는 크기를 계산할 때, 각 arranged view의 intrinsic content size를 사용한다. fill은 stack view의 직각으로 모든 arranged view의 크기를 조정하여 채운다.

### Positioning and Sizing the Stack View

비록 stack view가 auto layout을 직접적으로 사용하지 않고도 content를 배치할 수 있지만, stack view 자체를 위치시키기 위한 auto layout은 필요하다. 일반적으로, 적어도 두개, 위치를 정의하기 위한 stack view의 인접 edge를 고정해야한다. 추가적인 제약이 없으면, system은 content에 따라 stack view의 크기를 결정한다.

- stack view의 축 방향에 해당하는 fitting 크기는 arranged view의 크기와 view간 간격의 합이다.
- 직각 방향에 해당하는 fitting 크기는 가장 큰 arranged view의 크기이다.
- 만약, `isLayoutMarginsRelativeArrangement` property가 true라면, stack view의 fitting size는 margin 공간을 포함하여 증가한다.

stack view의 너비와 높이에 대한 추가적인 제약을 정의할 수 있다. 이 경우, stack view는 arranged view를 정의된 공간에 채우기 위해 배치와 크기를 조절한다. stack view의 property인 distribution과 alignment에 따라 배치가 다르며 여유 공간과 불충분한 공간에 대한 처리도 다르다.

stack view를 first 나 last baseline에 따라 위치시킬 수도 있다. stack view의 fitting size와 동일하게, content로 baseline이 결정된다.

- horizontal stack view에서 forFirstBaselineLayout과 forLastBaselineLayout은 높이가 가장 큰 view이다. 만약 해당 view가 stack view라면 재귀적으로 forFirstBaselineLayout이나 forLastBaselineLayout을 사용한다.
- vertical stack view에서는 첫번째 arranged view로 사용한다.

> Note
>
> baseline alignment는 높이가 intrinsic content size의 높이와 일치하는 경우에만 바르게 동작한다.

### Common Stack View Layouts

