# The Clean Architecture

https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

<img src="https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg" width=500/>

오랜기간 동안 시스템 아키텍쳐 관련된 여러 구상이 있어왔다.:

- Hexagonal Architecture
- Onion Architecture
- Screaming Architecture
- DCI
- BCE

이러한 아키텍쳐들은 세부적으로 다를지언정 매우 유사하다. 관리의 분리(separation of concerns)라는 같은 목표를 가지고 있다. 소프트웨어를 여러 층으로 구분하여 목적을 이뤄냈다. 비즈니즈 룰을 위한 최소 하나의 layer와 인터페이스를 위한 layer들로 구성되어 있다.