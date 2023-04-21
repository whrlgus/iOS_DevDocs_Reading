# iOS Animation by Tutorials

## Section 2: View Animations

### Chapter 3. Getting Started with View Animations

#### 3.2 Animatable properties

`UIView` 의 animatable property 는 한정되어 있다. 

##### Positions and Size

확대, 축소, 이동을 위해서 아래와 같은 뷰의 position과 frame을 애니메이트할 수 있다:

- bounds: 뷰의 frame 내의 뷰의 content를 reposition하기 위해 사용.
- frame: 뷰를 이동하고 크기를 조정하기 위해 사용.
- center: 이동하기 위해 사용.

`size` 와 `center` 같은 UIKit의 몇몇 property는 변형가능하다. 즉 `center.y` 로 수직축을 기준으로 움직일 수 있고, `frame.size.width` 로 축소할 수 있다.

##### Appearance

background 색을 변경하거나 투명도를 조절할 수 있다.

- backgroundColor: 시간이 지남에 따라 점진적으로 색을 변경하기 위해 사용.
- Alpha: fade-in/out 효과를 위해 사용.

##### Transformation

위와 같은 방식으로 뷰를 변형한다.

- Transform: 회전, 크기/위치 변경을 위해 animation block에서 property를 변경한다.

Affine 변형은 특정 bounds나 center point를 변형하는 대신에 scale factor 나 rotation angle을 정의할 수 있다.

#### 3.3 Animation options

##### Repeating

- `.repeat`: animation을 영원히 반복하기 위해 사용
- `.autoreverse`: `.repeat` 과 함께 사용한다; 기존 애니메이션 다음에 반대 애니메이션을 차례로 반복할 때 사용

##### Animation easing

- `.curveLinear`: 애니메이션의 가/감속을 적용하지 않는다. 
- `.curveEaseIn`: 시작시에 가속을 적용
- `.curveEaseOut`: 종료시에 감속을 적용
- `.curveEaseInOut`: 둘 다 적용

### Chapter 5. Transitions

**컨테이너 뷰**에 애니메이션을 적용. transition은 컨테이너 뷰와 서브 뷰가 추가 될 때 이 서브 뷰에 애니메이션 효과를 적용한다.







