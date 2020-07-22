## Modality

modality는 사용자에게 보여주던 뷰와 다른 어떠한 임시적인 형태로 content를 보여주는 디자인 기술이다. Self-contained task에 집중하게 만들고 critical information를 받거나 행동을 취할 수 있게 한다.

- **Sheet** presentation style은 card의 형태로 나타나서 아래에 있는 content의 일부를 가리고 나머지 부분은 어둡게 보이게 한다. modaless와는 modal view를 띄운 view는 조작할 수 없게 된다. 하지만 parent view나 previous card의 일부분을 보이게 하여서, 어떤 작업을 하다가 넘어왔는지 기억하기 쉽다. 복잡한 작업이 필요 없는 nonimmersive content를 보여줄 때 사용한다.
- **Fullscreen** presentation style은 전체 화면을 가리게 된다. 따라서 Sheet와 반대로, full-screen이 이점으로 작용하는 복잡한 작업을 수행할 때나 immersive content를 보여줄 때 사용한다.



## Navigation

- **Hierachical Navigation**은 목적지에 도달할 때까지 하나의 화면을 선택해 나가는 스타일이다. iOS의 Settings와 Mail 앱에서 이런 스타일을 볼 수 있다.
- **Flat Navigation**은 여러 content category에서 전환을 하는 스타일로 App Store나 Music 앱의 스타일이다.
- **Content-Driven or Experience-Driven Navigation**은 content 간에 자유롭게 화면을 전환하는 스타일로 Games, books같은 앱에서 볼 수 있다.

대게 여러 스타일을 결합하여 앱의 navigation style을 구성한다. 예를 들어, flat navigation의 각 category를 hierarchical navigation 으로 구현할 수 있다.



