# UITabBar

앱에서 Tab bar에 하나 이상의 버튼을 보여주며, 각 버튼을 통해 서로 다른 subtask, view, or mode를 선택할 수 있도록 하는 control이다.

## Overview

대게, tab bar는 `UITabBarController` 객체와 함께 사용하지만, 앱에서 standalone control로 사용하기도 한다. 힝싱 화면 하단에 보여지며, 하나 이상의 `UITabBarItem` object의 content를 보여준다. tab bar의 appearance는 커스터마이징이 가능하고 item을 tap하면 해당 item이 highlight된다. 그리고 응당하는 mode를 활성화할 수 있다.

> **Note**
>
> UITabBar class는 UIToolbar class와 외양적으로 비슷하나 용도가 다르다. **Tab bar**는 앱의 mode를 전달하고 바꾸는데 사용하고, **toolbar는** 현재 보여지는 content와 관련된 일련의 action들을 보여주는데 사용된다.

Tab bar는 selection과 user customization(item의 추가, 삭제, 재정렬)을 객체 내부의 delegate object에 알린다. 

## 

## Responding to Tab Selections

tab bar를 Tab bar controller와 함께 사용하면, controller에서 자동적으로 selection을 관리하고 적합한 view controller를 화면에 표시한다. Tab bar를 단독으로 사용할 경우에만 저런 것들을 직접 관리하면 된다. Tab bar는 selection을 delegate method인 `tabBar(_:didSelect:)` 에 전달하고 이 method를 통해 selection에 따른 필요한 조치를 할 수 있다.