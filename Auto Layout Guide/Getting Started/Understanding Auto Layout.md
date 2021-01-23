# Understanding Auto Layout

auto layout은 동적으로 view hierarchy에 있는 모든 view들의 size와 position을 각각의 constraint를 기반으로 하여 계산한다. 예를 들어, 버튼에 제약을 주어 image view의 수평선 상의 가운데 위치하게 하고, button의 top edge를 image의 bottom으로부터 8 point 간격을 갖게 할 수 있다. 만약, image view의 크기나 위치가 변경된다면, button의 위치도 그에 상응하여 자동으로 바뀌게 된다.

이러한 제약 기반(constraint-based)의 접근법은 내,외부 변화에 따라서 동적으로 UI를 디자인 할 수 있게 해준다.



## External Changes

외부 변화는 superview의 size나 shape이 바뀔 때 발생한다. 각각의 변화에 대해서, 가능한 공간을 잘 활용하기 위해 view hierarchy의 layout을 변경해야 한다. 다음은 위부 변화를 유발하는 요소들이다.

- 유저가 window의 크기를 변경한다.(OS X)
- 유저가 iPad에서 Split View에 들어가거나 나온다.(iOS)
- 장치가 회전한다.(iOS)
- (다음 본문 참조)

위의 대부분 변화는 runtime에 발생하며, 앱으로부터 동적인 응답을 필요로한다. 

## Internal Changes

내부 변화는 UI에서 view나 control의 크기가 변할 때 발생한다. 다음은 내부 변화의 몇몇 일반적인 source이다.

- 앱에 의해 보여지는 내용이 변한다.
- 앱이 internationalization(다양한 언어, 지역, 문화를 수용)을 지원한다.
- 앱이 dynamic type을 지원한다.(iOS)

앱의 content가 변화하면, 새로운 content는 다른 layout을 필요로 할 것이다. 앱에서 text나 image를 보여줄 때 흔히 발생한다. 예를 들어, news 앱은 article 각각의 크기에 따라 layout을 적용해야한다. 유사하게 photo collage는 image 크기의 넓은 범위와 화면비(aspect ratio)를 다룰 수 있어야 한다.

internattionalization은 다른 언어, 지역, 문화를 수용하여 앱을 만들 수 있도록하는 process이다. Internationalized 앱의 layout은 이러한 차이를 고려해야 하며, 앱이 지원하는 모든 언어와 지역에 대해 정확하게 표시돼야 한다.

3가지 영향에 대한 내용은 나중에...

마지막으로, iOS앱이 dynamic type을 지원한다면, 유저는 앱에 사용된 font size를 변경할 수 있다. 따라서, UI에서 문자 요소의 너비와 높이를 변경시킬 수 있다. 만약 앱이 실행중일 때 font size를 변경한다면, font와 layout이 적합하게 되어야 한다.



## Auto Layout Versus Frame-Based Layout

UI를 배치하는 데 3가지 접근법이 있다. UI를 직접 배치할 수 있고, 외부 변화에 자동으로 응답할 수 있도록 autoresizing mask를 사용할 수 있고, auto layout을 사용할 수 있다.

전통적으로, 뷰 계층에 있는 각각의 뷰에 대해서 frame을 설정하여 UI 배치를 해왔다. frame은 superview 좌표계에서 뷰의 origin, height, width로 정의했다.

<img src="https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/AutolayoutPG/Art/layout_views_2x.png" width=300/>

UI를 배치하기 위해, 뷰 계층 내부의 모든 뷰의 크기와 위치를 계산해야 했다. 그리고 변화가 발생하면 영향을 받는 뷰의 frame을 다시 계산했다.

코드로 뷰의 frame을 정의하는 것은 많은 방면에서 유연성과 power를 제공한다. 변화가 발생하면, 정확히 원하는 어떠한 변화를 만들어낼 수 있다. 그러나 모든 변화를 관리해야 하기 때문에, 단순한 UI를 배치하는 데에도 디자인, 디버그, 유지에 있어서 많으 노력이 필요하다. 

이러한 노력을 완화하기 위해 autoresizing mask를 사용할 수 있다. autoresizing mask는 superview frame이 변할 때, view frame이 얼마나 변할지 정의한다. 이것은 외부 변화를 수용하는 layout을 생성하기 쉽게 만든다.

그러나, autoresizing mask는 상대적으로 적은 양의 layout만을 지원한다. 복잡한 UI의 경우, autoresizing mask를 늘려야 한다. 게다가, autoresizing mask는 외부 변화에만 대응할 수 있다.

비록 autoresizing mask는 반복된 향상의 결과였지만, auto layout은 완전히 새로운 paradigm이다. view의 frame을 생각하는 대신에, 그 관계를 생각한다.

auto layout은 일련의 constraint를 사용하여 UI를 정의한다. constraint는 일반적으로 두 view 간의 관계를 나타낸다. auto layout은 이 제약을 기반으로 각 view의 크기와 위치를 계산한다. 이러한 방식으로 내,외부 변화에 동적으로 반응할 수 있는 것이다.

<img src="https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/AutolayoutPG/Art/layout_constraints_2x.png" width=300/>

제약 집합을 디자인하는데 사용된 logic은 절차적 또는 객체 지향 코드를 작성하는데 사용된 로직과 매우 상이하다. 그러나 다른 언어를 익히는 것과 auto layout을 습득하는 것을 크게 다르지 않다. 두가지 기본 단계가 있다. 먼저 constraint-based layout 의 로직을 이해해야 한다. 그리고 API를 배운다. 언어 학습도 이와 같이 해왔고, auto layout도 예외는 없다.

