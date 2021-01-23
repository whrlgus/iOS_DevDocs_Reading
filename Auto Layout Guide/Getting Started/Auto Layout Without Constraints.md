# Auto Layout Without Constraints

stack view는 복잡한 제약 없이 auto layout의 장점을 이용할 수 있는 방법을 제공한다. 단일 stack view는 UI 요소의 행이나 열을 정의한다. 다음 property를 이용하여 이러한 요소들을 배치한다.

- `axis` : (UIStackView) stack view의 방향(vertical or horizontal)을 정의한다. 
- `orientation` : (NSStackView) stack view 의 방향을 정의한다.
- `distribution` : 축에 해당하는 뷰들의 배치를 정의한다.
- `alignment` : 축의 수직 방향으로의 뷰 배치를 정의한다.
- `spacing` : 인접 뷰 사이의 공간을 정의한다.

interface builder에서 stack view를 사용하기 위해서는 canvas에 vertical 이나 horizontal stack view를 끌어다 놓고, content를 내부에 끌어 놓으면 된다.

만약 객체가 intrinsic content size를 갖고 있다면, 해당 size로 stack에 나타난다. 없는 경우에는 기본 크기를 제공한다. 객체의 크기를 변경할 수 있고, interface builder는 그 크기를 유지하기 위해 제약을 추가한다.

Stack view는 arranged view들의 content-hugging priority 와 compression-resistance priority를 기반으로 뷰를 배치한다.

일반적으로 가능한 stack view를 사용하여 layout을 구성하고, stack view만으로 불가능한 경우에 제약을 생성하자.