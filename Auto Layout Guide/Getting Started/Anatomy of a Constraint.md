# Anatomy of a Constraint

뷰 계층의 layout은 일련의 일차 방정식(linear equation)들로 정의된다. 각 제약은 하나의 방정식을 나타낸다. 

다음은 예시이다.

<img src="https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/AutolayoutPG/Art/view_formula_2x.png" width=500/>

- **Item1.** 방정식의 첫번째 item이다. view 또는 layout guide이어야 한다.
- **Attribute 1.** 첫번째 item에서 제약을 가할 속성을 나타낸다. 
- **Relationship.** 좌변과 우변 사이의 관계이다. equal, greater than or equal, less than equal 중 하나의 값을 가질 수 있다.
- **Multiplier.** attribute 2의 값은 해당 실수로 곱해진다. 
- **Item2.** 방정식의 두번째 item이다. 첫번째 item과는 다르게 공백으로 둘 수가 있다.
- **Attribute2.** 두번째 item이 공백이라면 `Not An Attribute` 이어야 한다.
- **Constant.** 실수 offset 값이다.

대부분의 제약은 UI에서 두개의 item 사이 관계를 정의한다. view나 layout guide가 될 수 있다. 또한, 단일 item의 두 속성간의 관계일 수도 있다. 예를 들어, 너비와 높이 사이의 화면비. 그리고 item의 높이나 너비에 상수 값을 할당할 수도 있다. 상수 값으로 처리할 때 두번째 item이 없다면, 두번째 attribute는 `Not An Attribute` 여야하고, multiplier는 0.0으로 설정해야 한다. 

## Auto Layout Attrributes

auto layout에서 속성은 제약을 가할 수 있는 특징이다. 일반적으로 네개의 edge와 너비, 높이, 수직/수평 center가 있다. Text item은 하나 이상의 baseline 속성이 더 있다. NSLayoutAttribute enum에는 더 많은 속성들이 있으니 확인해 보자.

## Sample Equations

두가지 속성 타입(size, location)으로 나뉜다. 그리고 다음의 규칙이 있다.

- Size 속성은 location 속성에 제약을 가할 수 없다.
- Location 속성에 상수 값을 할당할 수 없다.
- location 속성과 nonidentity multiplier(1.0을 제외한)를 사용할 수 없다.
- location 속성에서, Vertical 속성과 horizontal 속성의 관계를 맺을 수 없다.
- 또한, leading이나 trailing은 left 나 right 속성과 관계할 수 없다.



## Equality, Not Assignment

방정식의 두 항은 관계를 나타내는 것이지 할당을 의미하는 것이 아니다. 따라서 순서를 바꿔서 정의할 수도 있다.

다만 다음과 같은 일반적으로 선호되는 스타일이 있다.

- 실수 multiplier보다 정수 형태가 선호된다.
- 음수형 constant보다 양수형이 선호된다.
- 가능하면 leading to trailing, top to bottom의 순서로 표현하자.



## Intrinsic Content Size

특정 뷰는 현재 content에 주어진 본연의 크기가 있다. 예를 들어, button의 intrinsic content size는 그 title의 크기와 margin의 합이다. 

| View                                       | Intrinsic content size |
| ------------------------------------------ | ---------------------- |
| UIView and NSView                          | 없음                   |
| Sliders                                    | width만 정의(iOS)      |
| Labels, buttons, switches, and text fields | 너비 높이 둘다 정의    |
| Text views and image views                 | 다양?                  |

intrinsic content size는 view의 현재 content를 기반으로 한다. label이나 button은 보이는 text와 font를 기반으로 정해진다. 다른 뷰들은 더 복잡하다. 예를 들어, 비어있는 image view는 intrinsic content size를 갖지 않는다. image가 설정되면, 해당 image의 크기로 intrinsic content size가 결정된다.

Text view는 내용, 스크롤 가능 여부, 적용된 제약에 따라 content size가 다양하다. 예를 들어, 스크롤이 가능한 경우 ics는 없다. 스크롤이 안되면, ...필요할 때 정리하자.

auto layout은 각 차원마다 한 쌍의 제약을 사용하여 ics를 표현한다. Content hugging은 view를 content쪽으로 당겨 딱 맞게 한다. Compression resistance는 view를 바깥으로 밀어내 content가 잘리지 않도록 한다.

이 제약은 inequality 방정식으로 정의된다.

각각의 제약은 priority가 다르며 기본적으로 chp은 250, crp은 750이다. 그러므로, 줄어드는 것보다 늘리는 것이 쉽다. 

가능한 ics를 이용해서 layout을 잡자. Content 변화에 따라 동적으로 적합하게 만들어 준다. 불명확하고, 충돌없는 layout을 위해 필요한 많은 제약을 줄여줄 수도 있다. 하지만 chcr priority를 관리해야 한다. 다음은 ics를 다루기 위한 몇몇 가이드 라인이다.

- 공간을 채우기 위해 일련의 뷰를 늘릴 때, 만약 모든 뷰가 동일한 chp를 갖는다면, layout은 모호해진다. auto layout은 어떤 뷰를 늘릴지 알수가 없다.
- (당장은 너무 특정 케이스에 한정되므로 필요할 때 정리하자)

