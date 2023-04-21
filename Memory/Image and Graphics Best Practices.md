# Image and Graphics Best Practices

## UIImage and UIIMageView

### Buffers

버퍼는 메모리의 인접한 영역(contiguous region)이다.

### Image Buffers

어떤 이미지의 in-memory representation을 저장하는 버퍼를 말한다. 이 버퍼의 각 요소는 이미지의 단일 픽셀에 대한 색과 투명도를 표현한다. 결과적으로, 메모리 버퍼의 크기는 이미지의 크기에 비례한다.

#### The frame buffer

앱의 실제 만들어진 출력값을 가지고 있는 것이 frame buffer이다. 앱이 뷰 계층을 갱신하면 UIKit은 앱의 window와 모든 subview들을 frame buffer로 만들어낸다. 이 frame buffer는 픽셀당 색 정보를 제공하며, 디스플레이 하드웨어는 화면에 그 픽셀을 비추기 위해 그 정보를 읽는다. 마지막 과정은 고정된 간격으로 두며 이루어 진다. 보통 60 fps로 화면이 갱신되며, 앱에서 아무런 변화가 없다면 디스플레이 하드웨어는 frame buffer의 동일한 데이터를 가져올 것이다. 그러나 새로운 이미지를 할당하는 것과 같이 변화가 생기면, UIKit은 앱의 window를 frame buffer로 다시 만들어낸다. 그리고 다음 인터벌에는 해당 내용이 보여지게 된다.

#### Data Buffers

일련의 바이트 정보를 포함하는 버퍼이다. 이미지 파일을 포함하는 데이터 버퍼는 해당 이미지의 크기를 표현하는 메타데이터로 시작된다. 그리고 JPEG이나 PNG 와 같은 형태의 인코딩된 이미지 데이터 정보를 가지고 있다. 이 말인 즉슨, 메타데이타 이후의 바이트들은 이미지의 픽셀 정보를 표현하지 않는다.

따라서, data buffer를 사용하여 픽셀당 데이터로 frame buffer를 채워야 한다. 이를 위해서 UIImage는 data buffer에 포함된 이미지 크기만큼의 image buffer를 할당한다. 그리고 인코딩 이미지를 픽셀당 이미지 정보로 전환하기 위한 디코딩 과정을 수행한다. UIKit이 이미지 뷰에게 이미지를 렌더링하라고 하면, frame buffer에 복사할 때, 이미지 뷰는 content mode에 따라 image buffer의 이미지 데이터를 복사하여 크기를 조정한다. 

### Decoding Concerns

이미지 디코딩 단계는 CPU 가 많이 소요되는 작업이 수행되기 때문에, UIKit이 이미지 뷰에게 렌더링 하라고 할 때마다 이 작업을 수행하는 것이 아니고, 한번만 수행하여 UIImage이 해당 image buffer를 가지고 있는다. 결과적으로 디코딩되는 모든 이미지에 대해 영구적인 메모리 할당을 하게 될 것이다. 이 할당은 Frame buffer에 렌더링된 이미지 뷰의 크기가 아닌, input image의 크기에 비례한다. 결과적으로 성능에 안 좋은 영향을 미친다.

### Consequences of Excessive Memory Usage

앱 주소 공간에 있는 거대한 할당은 참조하려는 내용이 아닌 다른 연관된 내용을 침범할 수 있다. 이것이 바로 fragmentation이다. 앱의 메모리 사용량이 많아지면, OS가 개입하여 물리 메모리의 내용을 압축하려고 할 것이다. 이 작업에 CPU가 개입할 것이고, 통제할 수 없는 CPU 사용량이 늘어나게 되는 것이다.

### Proactively Saving Memory

#### Downsampling



## Custom drawing with UIKit

## Advanced CPU and GPU techniques