# URLSession Tutorial: Getting Started

## Introduction

HTTP 요청을 어떻게 생성하는지, 일시정지와 재개할 수 있는 백그라운드 다운로드를 구현하는 방법에 대해 배우게 될 것이다. 

서버로부터 데이터를 가져오거나, 소셜 미디어 상태 갱신 혹은 디스크로 원격 파일을 다운로드하는 것은 네트워크 요청에 의해 이뤄진다. 네트워크 요청을 위해 Apple에서는 컨텐츠를 업로드하고 다운로드 하기 위한 네트워킹 API인, `URLSession` 을 제공한다.

이 튜토리얼에서는, iTunes Search API에 쿼리를 수행하여 노래를 다운 받고, 백그라운드 전송을 가능하게 하여 사용자가 일시정지, 재개, 취소할 수 있는 앱을 만들 것이다.

## URLSession Overview

`URLSession` 은 HTTP(S) 기반 요청을 처리하기 위한 클래스로 구성되어 있다. 

<img src="https://koenig-media.raywenderlich.com/uploads/2019/05/02-URLSession-Diagram.png" width="500"/>

`URLSession` 은 요청을 보내고 받는데 필요한 핵심 객체이다. `URLSessionConfiguration` 을 통해 생성할 수 있고, 다음 세가지 유형이 있다:

- **default**: disk-persisted global cache, credential and cookie storage 객체를 사용하는 기본 구성 객체를 생성.
- **ephemeral**: 기본 구성과 동일하나, session 기반 데이터를 메모리에 저장한다는 점이 다르다. Private session으로 생각할 수 있다. 
- **background**: session이 background에서 업로드와 다운로드를 수행할 수 있게 해준다. Suspend 나 종료 상태에서 전송을 계속할 수 있다.

`URLSessionConfiguration` 은 timeout 값, 캐시 정책과 HTTP 헤더와 같은 session 의 속성을 구성할 수 있게 해준다. [참조 링크](https://developer.apple.com/documentation/foundation/urlsessionconfiguration)

`URLSessionTask` 는 task 객체를 의미하는 추상 클래스이다. session은 데이터를 가져오고 파일을 다운로드/업로드하는 하나 이상의 실제 작업을 수행하는 task를 생성하게된다. 

### Understanding Session Task Types

다음 세가지의 구체적인 session task가 있다:

- **URLSessionDataTask**: 서버에서 메모리로 데이터를 가져오는 GET 요청에 사용.
- **URLSessionUploadTask**: 디스크에서 웹 서비스로 파일을 업로드하는 POST나 PUT 방식에 사용.
- **URLSessionDownloadTask**: 원격 서비스에서 임시 파일 저장소로 파일을 다운로드할 때 사용.

<img src="https://koenig-media.raywenderlich.com/uploads/2019/05/03-Session-Tasks.png" width="500"/>

task를 보류하고, 재개하며 취소할 수도 있다. `URLSessionDownloadTask` 는 나중에 시작하기 위해 일시정지할 수 있는 기능도 제공한다.

일반적으로 `URLSession` 은 다음 두가지 방식으로 데이터를 반환한다:

- task가 완료될 때 completion handler 를 통해
- session을 생성할 때 설정한 delegate에서 method 호출을 통해

## DataTask and DownloadTask

사용자의 검색어를 iTunes Search API에 질의하기 위해 data task를 생성할 것이다.

```swift
let defaultSession = URLSession(configuration: .default)
var dataTask: URLSessionDataTask?
```

1. `URLSession` 을 생성하고, default session configuration으로 초기화 한다.
2. `URLSessionDataTask` 를 선언한다. iTunes Search 웹 서비스에 GET 요청을 할 때 사용하게 된다. 검색어를 검색할 때마다 초기화 될 것이다.

```swift
func getSearchResults(searchTerm: String, completion: @escaping QueryResult) {
  dataTask?.cancel() // 1
  
  // 2
  if var urlComponents = URLComponents(string: "https://itunes.apple.com/search") {
    urlComponents.query = "media=music&entity=song&term=\(searchTerm)"
    guard let url = urlComponents.url else { return }
    // 3
    dataTask = defaultSession.dataTask(with: url) { [weak self] data, response, error in
      defer {
        self?.dataTask = nil
      }
      if let error = error {
        self?.errorMessage += "DataTask error: \(error.localizedDescription)\n"
      } else if
        let data = data,
        let response = response as? HTTPURLResponse,
        response.statusCode == 200 {
        self?.updateSearchResults(data)
        DispatchQueue.main.async {
          completion(self?.tracks, self?.errorMessage ?? "")
        }
      }
    }
  }
  dataTask?.resume() // 4
}
```

1. 새로운 검색어에 대해 동일한 data task를 사용할 것이기 때문에, 이미 존재하는 것은 취소한다.
2. 쿼리 URL에 검색어를 포함하기 위해서, base URL을 사용하여 `URLComponents` 를 생성하고, 쿼리 문자열을 설정한다.
3. session으로부터 `URLSessionDataTask` 를 `url` 과 completion handler를 사용하여 초기화한다.
4. 모든 task는 기본적으로 suspended state이기 때문에, data task를 시작하기 위해서 `resume()` 메소드를 호출한다.

> **Note:** default request method는 GET이다. POST, PUT, DELETE와 같은 data task를 사용하고 싶다면, 우선 `url` 로 `URLRequest` 를 생성하고 `HTTPMethod` 속성을 설정해야한다. 그리고 `URL` 대신 `URLRequest` 로 data task를 생성하면 된다. 



### Downloading Classes

multiple download를 제어하기 위해 가장 먼저 할 일은 활성화된 download의 상태를 저장하기 위한 커스텀 객체를 생성하는 것이다.

```swift
class Download {
  var isDownloading = false
  var progress: Float = 0
  var resumeData: Data?
  var task: URLSessionDownloadTask?
  var track: Track
  
  init(track: Track) {
    self.track = track
  }
}
```

- **resumeData:** 사용자가 download task를 일시정지할 때 생성되는 `Data`를 저장한다. 만약 호스트 서버가 이를 지원한다면,  앱에서 이 데이터를 사용하여 일시정지된 download를 재개할 수 있다.

## URLSession Delegates

[Apple's URLSession documentation](https://developer.apple.com/documentation/foundation/urlsession) 에 나열된 몇몇 delegate protocol이 있다. `URLSessionDownloadDelegate` download task 에 특정한 task-level 이벤트를 처리한다.

`URLSessionDownloadDelegate` 의 유일한 non-optional 메소드는 다운로드가 끝날 때 앱이 호출하는  `urlSession(_:downloadTask:didFinishDownloadingTo:)` 이다. 

### Downloading a Track

### Saving and Playing the Track

download task 가 완료되면, `urlSession(_:downloadTask:didFinishDownloadingTo:)` 는 임시 파일 저장소의 URL을 제공한다. 이 메소드에서는 이 파일을 앱의 sandbox 내의 영구적인 위치로 이동시켜야 한다.

### Pausing, Resuming, and Canceling Downloads

### Canceling Downloads

### Pausing Downloads

### Resuming Downloads

### Showing and Hiding the Pause/Resume and Cancel Buttons

## Showing Download Progress

### Displaying the Download's Progress

## Enabling Background Transfers

background transfer 모드에서는 앱이 background에 있거나 크래시가 나도 download가 계속된다. 

OS는 background transfer task를 관리하기 위해 앱 외부에 분리된 데몬을 동작시킨다. 그리고 download task가 실행함에 따라 앱에 적절한 delegate 메시지를 전송한다. 전송중에 앱이 종료되어도 이 작업은 영향을 받지 않고, background에서 계속된다.

task가 완료되면 데몬은 background에서 앱을 재실행한다. 재실행된 앱은 관련된 completion delegate message를 받고 디스크에 다운로드된 파일을 저장하는 것과 같은 필요한 액션을 수행하기 위해 background session을 재생성한다. 

> **Note:** 만약, app swicher에서 앱이 강제종료되면, 시스템은 모든 session의 background transfer를 취소하고 앱을 재실행하지 않는다.

> **Note:** 하나의 background configuration에 대해 여러개의 session을 생성하면 안된다. 시스템은 세션 관련 작업에 해당 configuration의 identifier를 사용하기 때문이다.

### Relaunching Your App





