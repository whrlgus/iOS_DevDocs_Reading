## Navigation Bars

Navigation bar는 status bar 아래의 앱화면 상단에 나타나며 hierarchical screens에서 어디에 있는지 알 수 있다. 새로운 화면이 나타나면 back button이 대게의 경우 labeled 형태로 같이 navigation bar 좌측에 보여진다. 우측은 Edit or Done과 같은 조작기능을 하는 버튼들로 구성될 수 있다. 불투명한 형태로 background tint로 색을 표현하며 키보드를 띄우는 상황이나, gesture가 발생하는 경우에 navigation bar를 숨기도록 구성할 수 있다. 대게 **full-screen content를 보여주고자 하는 경우**에 tap gesture를 이용해 bar를 숨기고 나타내자.

#### Navigation Bar Titles

- current view의 title은 필요한 경우에만 표시한다. 메모 앱 같은 경우 content view 상단에 메모라는 내용이 있기 때문에 navigaton bar의 title을 표시하지 않았다.
- later~



#### Navigation Bar Controls

- navigation bar에 많은 control을 포함시키지 말자. 만약, segmented control을 사용하고자 한다면 다른 control과 title을 없애도록 하자.
- later~



## Tab Bars

앱 화면 하단에 위치하여 앱의 다른 section간의 전환을 가능케 해준다. 여러개의 텝을 포함할 수 있으며 화면 크기 때문에 다 표시되지 않는 경우에는 마지막 텝이 More 텝으로 활용되어 나머지 텝들을 표시한다.

- app level에서 정보를 구성할 때 사용하자. 주로 앱의 category 정보를 담아 사용하며 flat navigation style에 적합하다.
- Tab bar button은 action 수행해 사용하지 말고 navigation 용도로만 사용하자. action 수행에 적합한 것은 **Toolbar**이다.
- later~

#### Tip

Tab bar는 앱에서 여러 section을 구분하기 위한 용도로 사용되고, Toolbar는 여러 action을 수행하기 위한 용도로 사용된다. 같은 뷰에서 Tab bar와 Toolbar를 함께 사용하진 말자.



## Toolbars

toolbar는 앱의 하단에 나타아며 action 수행을 위한 버튼들을 포함하고 있다. 적절하게 숨겼다 나타냈다 하자.

