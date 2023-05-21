프로토타입 패턴은 객체가 자신을 복사할 수 있도록 하는 생성 패턴이다. 이 패턴은 두가지 타입을 포함한다:
<img src="https://assets.alexandria.raywenderlich.com/books/des/images/1166b1b00b998a0ee455e00ccc7dd172588ae50ad60a40e4e43246628f1051bf/original.png", width=150/>
1. 복사 메소드를 선언하는 **copying** 프로토콜
2. copying 프로토콜을 채택하는 **prototype** 클래스

실제로는 두가지 유형의 복사가 있다: **shallow** 와 **deep**

얕은 복사는 새로운 객체 인스턴스를 생성하지만, 그 속성들은 복사하지 않는다. 참조타입인 속성들은 여전히 동일한 원복 객체를 가리키고 있다. 예를 들어, 구조체인 스위프트 `Array`  를 복사하면, 자동적으로 할당이 되어, 새로운 배열 인스턴스는 생성되지만 그 `element` 는 복제되지 않는다.

깊은 복사는 새로운 객체 인스턴스를 생성하고 각 속성들 또한 복제한다. 예를 들어, 만약 `Array` 를 깊은 복사하면, 각 요소들도 복사된다. 스위프트는 기본적으로 `Array` 의 깊은 복사 메소드를 지원하지 않기 때문에 이 챕터에서 하나 생성할 것이다.

## When should you use it?
객체가 자신을 복사가능하도록 할 경우에 사용하자.

예를 들어, Foundation 은 `NSCopying` 프로토콜을 정의한다. 그러나, 이 프로토콜은 Objective-C 를 위해 고안되었기 때문에, 스위프트에서 잘 동작하지 않는다. 사용할 수는 있지만, 결국 보일러플레이트 코드를 작성하게 될 것이다.

대신에, 이 챕터에서는 `Copying` 프로토콜을 구현할 것이다. 

## Playground example

## What should you be careful about?
위 예제에서 봤듯이, 기본적으로 슈퍼클래스 인스턴스를 서브클래스의 복사 생성자에 전달하는 것이 가능하다. 만약 서브클래스가 슈퍼클래스 인스턴스로부터 완전히 초기화 된다면, 문제가 없다. 하지만, 만약 서브클래스가 다른 새로운 속성을 가지고 있다면, 슈퍼 클래스 인스턴스로 초기화 되는 것은 불가능하다.

이 이슈를 완화하기 위해, 서브클래스의 복사 생성자를 "unavailable" 로 표시할 수 있다. 그 응답으로, 컴파일러가 이 메소드의 직접 호출을 막을 것이다.

`copy()` 를 통한 간접 호출을 가능한다. 하지만, 이 안전장치는 대부분의 유즈케이스를 만족해야 한다.

만약 우리의 유즈케이스에서 이 이슈를 막지 못하면, 어떻게 처리할 지 고민해야 한다. 예를 들어, 에러 메시지를 콘솔에 출력하고 크래시를 발생시키거나, 기본 값을 제공하여 처리할 수도 있다.

## Tutorial project

## Key points
- 프로토타입 패턴은 객체 자신을 복사할 수 있게 한다. 두가지 타입을 포함한다: 복사 프로토콜과 프로토타입
- 복사 프로토콜은 복사 메소드를 선언하고, 프로토타입이 그 프로토콜을 채택한다.
- `Foundation` 은 `NSCopying` 프로토콜을 제공하나, 스위프트에서는 잘 동작하지 않는다. `Foundation` 나 다른 프레임워크로의 의존을 제거할 수 있는 Copying 프로토콜을 등록하는 것은 쉽다.
- `Copying` 프로토콜을 생성하는 것의 핵심은 `init(_ prototype)` 형태의 복사 생성자를 만드는 것이다.