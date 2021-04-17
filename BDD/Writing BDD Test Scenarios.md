# Writing BDD Test Scenarios

BDD 시나리오가 어떻게 테스트를 좀 더 사람답게 만들 수 있는지

[링크](https://www.departmentofproduct.com/blog/writing-bdd-test-scenarios/)



### The difference between BDD and TDD

BDD (*behaviour driven development*) 와 TDD (*test driven development*) 는 소프트웨어 개발 방식을 가리킨다. 



#### Test driven development

TDD는 구체적인 코드의 unit을 테스트하는 unit testing과 관련되어 있다. 앱은 구체적인 부분을 담당하는 작은 units of code로 구성되어 있고, 이러한 units of code 각각을 테스트하는 것을 'unit testing' 이라고 부른다.

![](https://www.departmentofproduct.com/wp-content/uploads/2017/06/TDD.001.png)



TDD에는 여러가지 단계와 원칙이 있다:

1. 모든 테스트의 작성은 코드 작성보다 먼저 한다.
2. 테스트를 작성한다.
3. 모든 테스트를 실행하여 작성한 테스트가 실패하는 것을 확인한다.
4. 코드를 작성한다.
5. 테스트를 다시 실행한다.
6. 필요하다면 코드를 수정한다.
7. 데스트를 다시 실행한다.



```
Benefits of TDD
1. Short debugging time/effort - 단위 테스트가 실패하면, 구체적으로 어떤 것 때문인지 정확하게 알 수 있다.
2. Safety net - 팀을 위한 안전망 역할을 한다. 팀원간 사기를 높이고, 팀내 자신감을 키워줄 수 있다.
3. Less bugs - 결함의 수를 줄여준다.
```

그러나, 코드 자체에만 집중하는 것은 앱의 사용자나 그의 행동을 무시하는 것이다.



#### Behavior driven development

BDD의 주요 목적은 business(PM을 포함한), 개발자, 기계 사이의 의사소통 문제를 해결하는 것이다. 

![](https://www.departmentofproduct.com/wp-content/uploads/2017/06/Lesson-2-testing-and-devops.001.jpeg)

새로운 기능 개발을 할때, 배포까지 여러 단계를 거쳐 가공되었을 것이다. BDD의 목표는 이러한 cost of translation 을 줄이는 것이다.



**<u>Principles of BDD</u>**

1. ubiquitous languages 라 불리는 단순한 언어를 사용한다.
2. 쉽고 간단한 언어로 작성하여, business person이 읽을 수 있고 무엇을 테스트 하는지 알 수 있다.
3. 소비자 관점에서 작성된다. 제품을 사용하는 사용자에 초점을 둔다.



**<u>Benefits of BDD</u>**

1. **Simple language** - 직관적인 언어의 사용으로 domain expert 뿐만 아니라 팀 내 모든 구성원이 사용하고 이해할 수 있다.
2. **Focus** - 개개의 단위로 분리된 기술적 구현에 집중하는 것이 아닌, 제품의 동작에 집중할 수 있다. 즉, 제품이 취해야할 행동에 모두가 집중하게 된다.
3. **Using Scenarios** - 개발 절차의 속도를 높이기 위해 고안되었다. 개발에 참여하는 모두가 같은 시나리오에 의존한다. 시나리오는 요구사항, 허용 기준(acceptance criteria), 테스트 케이스, 테스트 설명 모두를 포함한다. 
4. **Efficiency** - BDD framework는 시나리오를 쉽게 자동화된 테스트로 만들어 준다. 시나리오에 의해 여러 절차는 정해져 있고, 개발자는 각 단계의 동작을 수행하기 위한 method/function만 작성하면 된다.



### How to write BDD scenarios

BDD 시나리오는 여러 유저 관점에서 제품의 행동을 설명한다. 시나리오는 번역에 사용되는 비용을 줄여주고, 앤지니어가 요구사항을 이해하기 쉽게 해주며, QA가 적절하게 테스트 할 수 있게 해준다. 

BDD 시나리오를 사용하는 것은 요구사항과 테스트를 하나의 사항으로 결합할 수 있음을 의미한다. 특정 경우에서, 이는 자동화된 테스트로 전환될 수 있다. BDD 시나리오는 특정 형식을 따른다. 이 형식은 직관적이며, 약간의 노력으로도 작성할 수 있다. 

다음은 LinkedIn signup 절차를 설명하는 기본적인 BDD 시나리오이다.

```
Scenario 1: User successfully creates a LinkedIn Account
- GIVEN John은 현재 LinkedIn 등록 페이지에 있다. 
- WHEN 그는 모든 등록 항목을 입력했다.
- THEN LinkedIn 계정이 생성된다.
```

첫 번째로 확인되는 부분은 header이다. 모든 BDD 시나리오는 관심을 두고 있는 시나리오를 정확하게 설명하는 header를 포함해야 한다. 지저분할 수 있는 몇몇 경우에는 없이 작성하기도 한다.

두 번째는 3개의 단어이다. BDD 시나리오에는 가장 단순한 형식으로 다음 3개의 핵심 요소가 존재한다.

```
GIVEN (describing the context)
WHEN (describing the action)
THEN (describing the outcome)
```

이 세가지의 요소는 문맥(전후관계 or 배경), 행동, 결과 를 사용하여 시스템의 행동을 설명하는 데 도움을 준다. 만약 더 필요한 정보가 있다면, AND를 추가할 수 있다.

#### 

#### Using ANDs

시나리오에 더 많은 정보가 필요하다면, descriptor 뒤에 AND를 추가할 수 있다.

```
GIVEN (context)
AND (further context)
WHEN (action/event)
AND (further action/event)
THEN (outcome)
AND (further outcome)
```



LinkedIn 등록 시나리오를 ANDs를 사용하여 다음과 같이 상세하게 표현할 수 있다.

```
GIVEN 존은 LinkedIn 등록 페이지에 있다.
WHEN 그가 모든 등록 정보를 입력했다.
AND 그는 'join now'를 클릭한다.
THEN 그의 계정이 생성된다.
AND 프로필 생성 페이지로 이동된다.
AND 확인 메일이 전송된다.
```





#### How do BDD scenarios work with user stories?

BDD 시나리오는 하나의 상세를 형성해야 한다. 이는 user story와 시나리오를 포함한다. 그래서 만약 Jira와 같은 backlog 관리 도구에 user story를 작성한다면, 다음과 같은 순서로 상세를 작성할 수 있다.

1. User story - 사용자 관점에서 요구사항을 설명하는 user story로부터 시작한다.
2. BDD scenarios - 다음으로 테스트에 도움을 주는 시스템 행동을 설명하는 scenrio를 포함한다.



User story는 BDD와 조금은 다른 구조를 갖는다. 

```
As an X
I can / want Y
So that Z
```

LinkedIn 예제를 사용하면:

```
As a 새로운 사용자, I can 홈페이지에 새로운 계정을 등록 so that LinkedIn에 접속할 수 있다.
```



#### When should BDD scenarios be used?

BDD 시나리오는 제품의 모든 명세 사항에 필요하진 않다. 오해할 소지가 있는 요구사항이나 철저한 테스트 접근이 필요한 경우에 적합하다. 사소한 색상 변경, 텍스트 변경, 혹은 기술적 잡업이나 버그 같은 경우, BDD 시나리오에 적합한 케이스가 없을 것이다.

새로운 주요 기능 전부에 대한 것을 적거나 명세 사항 일부에 집중할 수 있을 것이다. 궁극적으로 BDD 시나리오는 개발 절차에 도움을 주는 요소이므로, 팀이나 개인이 적합하게 결정해야 할 것이다.