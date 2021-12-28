# 11. Core Data

## 11.1 NSManagedObjectContext is not thread safe

`Appdelegate` 에서 `NSPersistentContainer` 의 일부로 생성된 `NSObjectedContext` 는 main thread에 연결되어 있다. 즉, main UI thread에서만 이 context를 사용할 수 있다는 의미이다. 하지만, 그렇게 된다면, 사용자 경험에 악영향을 미칠 것이다.

`NSManagedObjectContext` class에 concurrency를 가능하게 해주는 두가지의 method가 있다:

- `perform(_:)`
- `performAndWait(_:)`

두가지 method는 closure로 전달된 어떤 action이든지 context를 생성한 동일한 queue에서 실행됨을 보장한다. Main thread가 아님이 주목해야 하는데, 다른 큐에서 context를 생성할 수 있고, 항상 적절한 thread에서 실행됨을 보장하여 runtime에 crash 를 발생시키지 않게된다.

첫번째는 비동기 method이고, 두번째는 동기 method라는 차이점이 있다. 두 메소드 모두 사용시 안전성을 제공해준다.

## 11.2 Importing data

서버에 접근하여 데이터를 다운받고, 비교하여 불러오는 작업이 일반적이다. 이 모든 작업을 `Operation`으로 처리하지 않아도 된다. Core Data의 `NSPersistentContainer` 는 `performBackgroundTask(_:)` 를 제공한다.

closure의 인자로 private queue에 새로운 context를 생성된 `NSManagedObjectContext` 가 주어진다. 

## 11.3 NSAsynchronousFetchRequest

Core Data에 질의하기 위해 `NSFetchRequest`를 사용하는데, 이 작업은 동기적으로 동작한다. 단일 객체 하나를 가져오기위한 작업에 적합하며, 시간이 오래 소요되는 질의를 수행하기 위해서는 `NSAsynchronousFetchRequest`를 사용하여 비동기적으로 동작시켜야 한다.

## 11.4 Sharing an NSManagedObject

`NSManagedObject` 나 그 서브클래스는 thread간 공유할 수 없다. 

만약 분리된 thread에서 동일 객체에 접근해야 하면, 실제 `NSManagedObject` 대신에 `NSManagedObjectId`를 전달하면 된다. 

### Using ConcurrencyDebug

Core data method를 잘못된 thread에서 실행했는지 확인하기 위해 project scheme에서 runtime debug flag를 설정할 수 있다.