https://suragch.medium.com/frame-vs-bounds-in-ios-107990ad53ee

# Short description
- frame: **부모 뷰의 좌표계**에서 뷰의 위치와 크기
- bounds: **자신의 좌표계**에서 뷰의 위치와 크기

# Details
Frame을 이해하기 위해 벽의 액자를 떠올려보자. 액자는 사진의 경계와 같고, 벽의 원하는 위치에 걸어둘 수 있다. 같은 방식으로, 뷰는 부모 뷰의 아무 위치에나 둘 수 있다. iOS에서 좌표계의 원점은 좌상단이다. 뷰 프레임의 x,y 좌표를 (0,0) 으로 설정하여, 뷰를 부모뷰의 원점에 놓을 수 있다. 

bounds를 이해하기 위해서는 농구장을 떠올려보자. 농구장은 체육관이나 집앞 혹은 어느 곳에나 위치할 수 있다. 농구장에서 드리블 하는 동안에, 농구장이 어디에 있는지 신경쓰지 않는다. 유사한 방식으로 뷰 bounds의 좌표계는 뷰 자신만을 신경쓴다. 부모뷰의 어느 위치에 있는지 신경쓰지 않는다. bounds의 원점은 뷰의 좌상단, 디폴트로 (0,0), 이다.  하위 뷰들은 이 점을 기준으로 놓이게 된다. 

## Frame vs Bounds
좌측 사진에서는 부모뷰의 좌상단에 뷰가 위치해 있다. 노란선은 뷰의 frame을 나타낸다. 우측은 뷰는 있지만 부모뷰는 보이지 않는다. 왜냐하면, bounds는 부모뷰에 대해 알지 못하기 때문이다. 초록선은 뷰의 bounds를 나타낸다. 빨간 점은 frame과 bounds의 원점을 나타낸다.
<img src="https://miro.medium.com/v2/resize:fit:890/format:webp/1*Pc-kxGOiDYXDGPwL8LZMfw.png" width="300"/>
|  | frame | bounds |
|---|---|---|
| origin | (0,0) | (0,0) |
| width | 80 | 80 |
| height | 130 | 130 |


다음은 부모뷰에서 frame의 좌표를 이동한 그림이다. 뷰의 컨텐츠는 동일하며 bounds는 변화를 알지 못한다.

<img src="https://miro.medium.com/v2/resize:fit:890/format:webp/1*ePKL_Wq5lqZ5J8CkyQvhrQ.png" width="300"/>

|  | frame | bounds |
|---|---|---|
| origin | **(40,60)** | (0,0) |
| width | 80 | 80 |
| height | 130 | 130 |


지금까지는 frame과 bounds의 너비와 높이가 동일하였다. 하지만, 뷰를 회전하게 되면 두 속성의 차이가 발생한다. 
<img src="https://miro.medium.com/v2/resize:fit:890/format:webp/1*Nid_PMoniLYLNYHmhHJEjw.png" width="300"/>

|  | frame | bounds |
|---|---|---|
| origin | **(20,52)** | (0,0) |
| width | **118** | 80 |
| height | **187** | 130 |


뷰가 큰 하위뷰를 가지고 있고 한번에 보여주기 어려운 경우를 생각해보자. bounds의 원점을 변경하게 되면 아래와 같을 것이다. 부모뷰에서 frame은 이동하지 않았지만, bounds의 원점이 다른 위치에서 시작했기 때문에 내부 컨텐츠는 바뀌었다.
<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*EIRyN-2Ojr4-IfH_Lp73oQ.png" width="300"/>

|  | frame | bounds |
|---|---|---|
| origin | **(40,60)** | **(280,70)** |
| width | 80 | 80 |
| height | 130 | 130 |


## When to use frame and when to use bounds
`frame` 은 부모뷰에서 뷰의 위치에 연관되어있기 때문에, 너비를 변경하거나 같은 부보뷰 내의 다른 뷰과의 거리를 찾을 때와 같은, 외부의 변화를 만들어낼 때 사용하자.

`bounds`는 뷰 내부에서 하위뷰를 정렬할 때와 같은 내부의 변화를 만들 때 사용한다. 또한 뷰를 변형시켰다면, 그 크기를 확인할 때 사용하자.
