# Customizing the Behavior of Segue-Based Presentations

### Overview

사용자가 segue를 발동하면, UIKit이 storyboard에서 찾은 option을 사용하여 view controller를 보여준다. UIKit은 동적으로 segue process를 수정할 수 있는 기능을 제공한다. segue가 일어나는 것을 막거나, segue가 일어날 때 추가적인 동작을 할 수 있다.



### Configure the presentation Style of the Transition

segue의 type은 segue를 나타내고 해제할 때 UIKit이 어떤 종류의 animation을 사용할 지 결정한다. segue를 생성할 때 type을 지정할 수 있고, attribute inspector에서 수정도 가능하다.

| Segue type | Behavior                   |
| ---------- | -------------------------- |
| Show(push) | parent view controller에서 |
|            |                            |
|            |                            |
|            |                            |

정리하다보니까 container controller를 공부하고 Segue를 다양하게 사용해 봐야 할 것같다. 설명이 너무 대충 적혀있다.