# 12. Thread Sanitizer

## 12.1 Why the sanitizer?

TSan으로 불리는 Thread Sanitizer는 애플이 LLVM 컴파일러의 일부로 제공하는 툴이다. TSan은 다수의 쓰레드가 적절한 접근 동기화 작업 없이 동일한 메모리에 접근하려하는 것을 식별할 수 있다.

## 12.4 It's not code analysis

runtime 시에만 분석할 수 있다. 즉, 실행시점에 문제가 발견되지 않으면 이슈를 확인할 수 없다.

## 12.5 Xcode keeps getting smarter

Thread Sanitizer사용 없이도 runtime시에 error를 감지하여 알려주기도 한다.