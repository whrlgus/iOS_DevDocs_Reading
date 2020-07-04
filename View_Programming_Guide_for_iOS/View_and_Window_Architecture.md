## 1. View Architecture Fundamentals

### View Hierarchies and Subview Management

view는 자체적으로 내용을 표현하는 것 이외에도 다른 view를 포함하는 container역할을 한다. 부모-자식 관계가 형성되며, 컨테이너 뷰인 부모 뷰는 자식 뷰들을 배열 형태로 저장하여 최종적으로는 마지막에 저장된 뷰가 최상단에서 보여지게 된다. 만약 투명도가 적용된다면, 아래 뷰와 함께 보인다.

이벤트 발생시 뷰의 관계에 따라 해당 이벤트가 루트 뷰인 application object까지 전달된다. 도중에 view controller와 같은 responder object가 있다면 그 부분에서 이벤트를 처리하게 된다.

### The View Drawing Cycle

### Content Modes

### Stretchable Views

### Built-In animation Support

## 2. View Geometry and Coordinate Systems

### The Relationship of the Frame, Bounds, and Center properties

- frame은 view의 크기와 super view의 좌표계에 의한 view의 위치를 나타낸다.
- bounds는 self view의 좌표계를 기준으로 한다.
- center는 super view의 좌표계를 기준으로 하는 center point를 나타낸다.

center와 frame은 런타임에 현재 뷰의 기하 변환에 사용하자. 예를 들어, 뷰를 이동하려고 한다면 부모 뷰의 center를 기준으로 옮기면 된다.

bounds는 현재 뷰에 그림을 그리는 경우에 사용하자.

각각의 값을 변경하는 경우에 서로가 영향을 받는다.

- frame을 변경하면 bounds의 크기는 따라 변경될 것이고, center또한 frame의 위치 혹은 크기에 영향을 받는다.
- center를 변경하면 frame의 origin 값이 변경된다.
- bounds는 frame의 크기에 영향을 준다.

default로 view의 frame은 super view의 frame에 의해 잘리지 않는다. 그러나 superview에서 event를 처리하고 있고 superview를 벗어나는 부분에서 클릭과 같은 이벤트가 발생하면, 이는 responder로 전달되지 않는다.

### Coordinate System Transformations

### Points Versus Pixels

iOS의 좌표값 및 거리는 points라는 단위의 실수 값으로 표현된다. Point-based measuring system에 user coordinate space라는 것이 있다. 이는 코드로 표현하는 표준 좌표 공간이다. 이 공간의 1 point는 반드시 device의 1 pixel로 맵핑되는 법은 없다는 것을 주의하자. 즉, user coordinate space와 device coordinate space 사이의 매핑 값은 시스템에 따라 상이하다.

## 3. The Runtime Interaction Model for Views

## 4. Tips for Using Views Effectively