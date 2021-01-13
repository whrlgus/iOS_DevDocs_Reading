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
- vertical stack view에서는 순서에 따른 첫번째 혹은 마지막 arranged view로 사용한다.

> Note
>
> baseline alignment는 높이가 intrinsic content size의 높이와 일치하는 경우에만 바르게 동작한다.

### Common Stack View Layouts

**Define the position only.** stack view의 인접 모서리 두개만 super view에 고정하는 걸로 stack view를 정의할 수 있다. 이 경우에 stack view의 크기는 arranged view에 의해 두 방향으로 증가한다. 이 접근법은 stack view의 content를 해당 intrinsic size에 따라 보여지게 하고 싶은 경우와 다른 UI 요소를 stack view에 연과 지어 정렬하고 싶은 경우에 유용하다.

<img src="https://docs-assets.developer.apple.com/published/f8e8e88004/786347a6-3c16-480d-949e-8319ebcc68f7.png" width=600/>

**Define the stack's size along its axis.** 이 경우에, stack 의 축에 따라 양 끝 모서리를 super view에 고정하자. 그리고 위치를 정의하기 위해 남은 모서리 중 하나를 고정해야 한다. stack view는 정의된 공간을 채우기 위해 content의 크기와 위치를 결정하게 된다. 하지만, 고정되지 않은 모서리는 가장 큰 arranged view에 의해 움직여질 것이다.

<img src="https://docs-assets.developer.apple.com/published/19ba11ed1c/0b922694-dbfc-4123-b3d6-02f70ac60a6c.png" width=600/>

**Define the stack's size perpendicular to its axis.** 이 접근은 이전과 유사하다. 그러나 stack view 축의 직각 방향의 양 끝 모서리를 고정하고, 축 방향의 두 모서리 중 하나만 고정한다. stack view가 arranged view를 추가하거나 삭제함에 따라 축 방향으로 view의 크기가 변하게 된다. fillEquallly distribution이 아니라면 arranged view의 크기는 intrinsic content size에 의해 결정될 것이다. 축의 직각 방향으로는 stack viewdml alignment 속성에 따라 크기가 결정된다.

<img src="https://docs-assets.developer.apple.com/published/cc6e21faab/651cc05e-4df4-493a-8113-41fed7da7d3f.png" width=600/>

**Define the size and position of the stack view.** 이 경우는 4개의 모든 모서리를 고정하여 content를 제한된 공간에 놓는다. 

## Managing the Stack View's Appearance

stack view는 arranged view의 위치와 크기를 관리한다. 다음 property들은 stack view가 content를 어떻게 배치하는지 결정하는 요소이다.

- **axis** property는 수직이나 수평으로 stack의 방향을 결정한다.
- **distribution** 은 stack의 축 방향으로 arranged view의 배치(layout)를 결정한다.
- **alignment** 는 축의 수직 방향으로 arranged view의 배치를 결정한다.
- **spacing** 은 arranged view들 사이의 최소 공간을 결정한다.
- **isBaselineRelativeArrangement** 는 vertical spacing이 baseline에 의해 결정될지 말지를 결정한다.
- **isLayoutMarginsRelativeArrangement** 는 arranged view를 layout margin에 따라 배치할지를 결정한다.

## Maintaining Consistency Between the Arranged Views and Subviews

stack view의 `arrangedSubviews` property는 항상 `subviews` property의 부분집합이다. 특히, stack view는 다음 규칙을 따른다.

- `arrangedSubviews` 에 view를 추가하면, `subview` 에도 추가된다. (단, 이미 존재하는 경우가 아니라면)
- subview가 제거되면 arrangedSubviews 배열에서도 제거된다.
- arrangedSubviews에서 view를 제거해도 subview에서 제거되진 않는다. Stack view가 더이상 해당 view의 크기와 위치를 관리하지 않지만, 여전히 view hierarchy에 일부이며, visible 하다면 화면에 나타난다.

비록 arrangedSubviews가 subviews의 부분집합을 포함한다해도, 그 순서는 독립적이다.

- arrangedSubviews의 순서는 stack에서 view가 나타나는 순서를 나타낸다. 
- subviews의 순서는 Z-order를 나타낸다. 낮은 index의 view 는 높은 index의 view 뒤(아래)에 나타난다.

## Dynamically Changing the Stack View's Content

Stack view는 arrangedSubviews에 view가 추가, 삭제, 삽입될 때, 또는 arranged subview의 isHidden 속성이 변할 때마다 자동적으로 layout을 갱신한다. 

또한, stack view의 어떠한 property의 변화에도 자동적으로 반응한다. 예를 들어, 동적응로 stack의 방향을 바꿀 수 있다.

interface builder에서 stack view의 size class 변화에 따른 여러 property 값을 정의할 수 있다.

