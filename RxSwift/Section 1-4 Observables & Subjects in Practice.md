# Chapter 4. Observables & Subjects in Practice

이 시점에서, observable과 여러 유형의 subject가 어떻게 동작하는지 이해했을 것이고, Swift playground에서 어떻게 생성하고 시도하는지 배웠다. UI를 데이터 모델에 바인딩하거나, 새로운 컨트롤러를 노출하고 발생한 출력을 가져오는 것과 같이, 실제 사용을 확인하는 것은 어려울 수 있다. 새로 배운 내용을 실제 어떻게 적용하는지 이번에 다룰 것이다.

## 4.7 Challenges

Alert VC 을 노출하는 로직을 reactive하게 구현할 때 Completable을 반환하게 하여, disposables.create에 vc dismiss 코드를 삽입하는 코드가 있다. 확인 버튼을 누르면 completed 이벤트를 전달하게 되고 바로 dispose될텐데 여기에 trait 생성 메소드 클로저의 반환 값을 활용한 부분이 인상적이다.