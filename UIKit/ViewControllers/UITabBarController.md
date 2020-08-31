# UITabBarController

**Container** view controller 로서, multiselection 인터페이스를 관리하며, 각 selection은 어떤 child view controller를 화면에 보여줄지 결정한다.

## Overview

tab bar 인터페이스는 화면 하단에 보여지며, 여러 mode 중에 선택을 할 수 있고, 해당 view를 화면에 보여준다. view에 해당하는 class는 대게 `-is` 형태로 사용되지만, 간혹 subclass화 되기도 한다.

tab bar controller 인터페이스의 각 tab은 **custom** view controller와 연관이있다. user가 특정 tab을 선택한다면, tab bar controller는 이전 view를 대체하여 해당 view controller의 root view를 화면에 보여준다. (이미 선택된 tab을 포함한 어떤 tab을 클릭하든, 항상 해당 tab의 root view를 보여준다.) tab bar 인터페이스는 일반적으로 다음 두 가지 중 하나의 형태로 사용한다. 하나는, 정보의 다른 타입을 표현하는 것이고, 다른 하나는 같은 정보를 완전히 다른 style의 인터페이스로 표현하는 것이다. 아래 그림은 시계 앱으로 time 기반의 정보를 다른 형태로 제공한다.

<img src = "https://docs-assets.developer.apple.com/published/6ffdd16259/a4c30adf-176b-4020-ae69-f228edb9e621.png">



Tab bar controller의 tab bar view에 직접적으로 접근하면 안된다. tab bar controller의 tabs를 구성하기 위해 각 tab의 root view를 위한 view controller를 `viewControllers` property에 할당해야 한다. 할당된 view controller 들은 순서대로 tab bar에서 보여질 것이다. 

Tab bar item 들은 응당하는 view controller로 구성된다. Tab bar item과 view controller를 연결하기 위해선, UITabBarItem class 객체를 생성하고 `tabBarItem` property에 할당한다. 만약, view controller를 위한 **custom** tab bar item을 설정하지 않으면 default 로 이미지 없이 view controller의 `title` property로 item을 생성하게 된다.

Tab bar 인터페이스와 user가 interact하기 위해서, tab bar controller 객체는 interaction에 관한 notification을 내부의 delegate로 보낸다. 이 delegate는  `UITabBarControllerDelegate` protocol을 준수하는 조건하에 어떠한 object든지 상관이 없다. 이러한 delegate는 특정 tab bar item이 선택되는 것을 막고 tab이 선택 됐을 때 추가적인 task를 수행하도록 하기 위해 사용될 수 있다. 또한 **More navigation controller** 에 의한 tab bar의 변화를 monitor하는데 사용될 수도 있다.

## The Views of a Tab Bar Controller

UITabBarController는 UIViewController의 파생 class로, 접근이 가능한 `view` property를 가지고 있다. 이 `view` 는 tab bar view를 위한 container이고, custom content를 포함하는 view이다. (아래 그림에서 가운데 view에 해당하는 것 같다.) 해당 view는 한개 이상의 tab bar item을 포함하여 selection control을 제공한다. tab bar 와 toolbar view의 item들은 변할 수 있으나 item들을 관리하는 tab bar view는 변하지 않고, 딱 하나, custom content view만 tab의 선택에 따라 변한다.

<img src = "https://docs-assets.developer.apple.com/published/a0fd9e66d5/1bc595c9-a817-4057-b8b9-ecaa4e8647de.png" width = "600">

위의 그림처럼 navigation controller 혹은 custom view controller를 tab에 해당하는 **root** view controller로 사용할 수 있다. 만약, navigation controller를 root view controller로 사용하는 경우에는, tab bar controller에서 navigation content를 보여주기 위해 크기를 조정하여 tab bar에 겹쳐지지 않도록 한다. 이와 같은 상황에 대비해, tab bar 인터페이스를 보여주는 view는 크기 재조정을 위한 `autoresizingMask` property를 가지고 있어야 한다.

## The More Navigation Controller

Tab bar는 custom item을 표시할 공간의 제약이 있기 때문에 6개 이상의 item을 갖는 경우 첫 4개와 standard More item을 tab bar에 표시한다. More item을 tap하면 나머지 item을 선택할 수 있는 standard 인터페이스가 보여진다.

standard More item을 위한 인터페이스는 **Edit button** 을 포함하여, user가 tab bar를 재구성할 수 있게 한다. 기본적으로, user가 재정렬할 수 있도록 되어있고, 그것을 막기 위해서는 `customizableViewControllers` property에 있는 해당 view controller를 제거해야 한다.

## State Preservation

View controller의 `restorationIdentifier` property에 값을 할당하면 상태를 보존하여, restore time에 같은 view controller를 보이게 할 수 있다. 



https://developer.apple.com/documentation/uikit/uitabbarcontroller