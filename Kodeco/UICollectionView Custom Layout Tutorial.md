https://www.kodeco.com/4829472-uicollectionview-custom-layout-tutorial-pinterest#toc-anchor-003

`UICollectionView` 는 iOS 6 에 도입되어 iOS 개발자들 사이에서 가장 인기있는 UI 요소 중의 하나가 되었다. 매력적인 부분은 데이터와 프레젠테이션 레이어 사이의 분리인데, 레이아웃을 처리하기 위해 개별 객체에 의존한다. 레이아웃은 뷰의 위치와 시각적인 속성을 결정하는 책임을 갖는다.

UIKit에서 제공하는 레이아웃 클래스인, 디폴트 플로우 레이아웃을 사용해봤을 것이다. 약갼의 커스터마이즈가 가능한 기본적인 그리드 레이아웃이다.

이 `UICollectionView` 커스텀 레이아웃 튜토리얼에서, 인기있는 앱인 핀터레스트의 영감을 받은 레이아웃을 생성해볼 것이다.

다음에 대해서 배울 것이다:
- 커스텀 레이아웃
- 레이아웃 속성을 계산하고 캐싱하는 법
- 동적 크기 셀을 다루는 법

## Getting Started
스타터 프로젝트를 열고 실행하면 다음과 같이 보일것이다:
<img src="https://koenig-media.raywenderlich.com/uploads/2017/08/pinterest-layout-updated-initial.png" width=300/>

이 캘러리는 표준 플로우 레이아웃을 사용하는 콜랙션 뷰로 구현되었다. 레이아웃 디자인은 처음엔 괜찮지만, 개선될 만한 여지가 있다.

사인은 컨텐츠 영역을 완전히 채우지 않는다. 긴 캡션은 잘린다. 모든 셀이 같은 크기이기 때문에 사용자 경험은 지루하고 정적이다.

각 셀은 크기에서 자유로운 커스텀 레이아웃으로 디자인을 개선할 수 있다.

## Creating Custom Collection View Layouts
캘러리를 위한 커스텀 레이아웃 클래스를 생성하여 놀랄만한 콜랙션 뷰를 만들 것이다.

콜랙션 뷰 레이아웃은 추상 클래스인 `UICollectionViewLayout` 의 서브클래스이다. 그 것은 콜랙션 뷰에서 모든 아이템의 시각적인 속성을 정의한다.

각각의 속성은 `UICollectionViewLayoutAttributes` 의 인스턴스이다. 아이템의 `frame` 이나 `transform`  같은속성들을 포함한다.

### Core Layout Process
콜랙션 뷰 레이아웃 프로세스에 대해 생각해보자. 이는 콜랙션 뷰와 레이아웃 객체 사이의 협동이다. 콜랙션 뷰가 레이아웃 정보를 원하면, 레이아웃 객체에 특정 순서로 관련 메소드를 호출하여 정보를 제공 받는다:
<img src="https://koenig-media.raywenderlich.com/uploads/2015/05/layout-lifecycle-667x500.png"/>
레이아웃 서브클래스는 다음 메소드들을 반드시 구현해야 한다:
- **collectionViewContentSize:** 이 메소드는 콜랙션 뷰 컨텐츠의 너비와 높이를 반환한다. 콜랙션 뷰에서 보이는 컨텐츠가 아닌 전체 컨텐츠 영역을 반환하기 위해 반드시 구현해야 한다. 콜랙션 뷰는 스크롤 뷰의 컨텐츠 크기를 구성하기 위해 내부적으로 이 정보를 사용한다.
- **prepare():** 배치 동작이 수행되려고 할 때마다, UIKit은 이 메소드를 호출한다. 콜랙션 뷰의 크기와 아이템의 위치를 결정하는데 필요한 연산을 준비하고 수행할 수 있는 기회이다.
- **layoutAttributesForElements(in:):** 이 메소드에서는 주어진 사각형 내부의 모든 아이템들의 레이아웃 속성을 반환한다. `UICollectionViewLayoutAttributes` 의 배열로 그 속성들을 콜랙션뷰로 반환한다.
- **layoutAttributesForItem(at:):** 이 메소드는 콜랙션 뷰에서 레이아웃 정보를 요청하면 이를 제공한다. 이 메소드를 오버라이드 하여 요청된 `indexPath` 에 위치한 아이템의 레이아웃 속성을 반환할 필요가 있다.


## Calculating Layout Attributes
사진의 높이를 바로 알기 어렵기 때문에 모든 아이템의 높이는 동적으로 계산해야 한다. `PinterestLayout` 이 필요로 할때 정보를 제공할 수 있게 프로토콜을 정의할 것이다.

다음 델리게이트 프로토콜 선언을 추가하자:
```swift
protocol PinterestLayoutDelegate: AnyObject {
  func collectionView(
    _ collectionView: UICollectionView,
    heightForPhotoAtIndexPath indexPath: IndexPath) -> CGFloat
}
```
사진의 높이를 요청하는 메소드를 가지고 있다. `PhotoStreamViewController` 곧 구현할 것이다.

레이아웃 메소드를 구현하기 전에 할 것이 한가지 더 있다. 레이아웃 프로세스에 도움이 되는 속성들을 정의할 필요가 있다.

다음을 `PinterestLayout` 에 추가하자:
```swift
// 1
weak var delegate: PinterestLayoutDelegate?

// 2
private let numberOfColumns = 2
private let cellPadding: CGFloat = 6

// 3
private var cache: [UICollectionViewLayoutAttributes] = []

// 4
private var contentHeight: CGFloat = 0

private var contentWidth: CGFloat {
  guard let collectionView = collectionView else {
    return 0
  }
  let insets = collectionView.contentInset
  return collectionView.bounds.width - (insets.left + insets.right)
}

// 5
override var collectionViewContentSize: CGSize {
  return CGSize(width: contentWidth, height: contentHeight)
}
```

1. 델리게이트로의 참조를 유지한다.
2. 레이아웃을 구성하는 두가지 속성이다.
3. 계산된 속성을 캐싱할 배열이다. `prepare()` 을 호출할 때, 모든 아이템의 속성을 계산하고 이를 캐시에 추가한다. 콜랙션 뷰가 나중에 레이아웃 속성을 요청할 때, 매번 다시 계산하는 대신에 효율적으로 캐시에 질의할 수 있다.
4. 컨텐트 크기를 저장하기 위한 두가지 속성을 정의한다. 사진을 추가할 때 `contentHeight` 를 증가하고 콜랙션 뷰 너비와 컨텐트 인셋에 기반하여 `contentWidth` 를 계산한다.
5. 콜랙션 뷰의 컨텐츠 크기를 반환하며 이전 단계에서의 두 속성을 사용하여 계산한다.

콜랙션 뷰 아이템의 속성을 계산할 준비가 되었다. 지금은 프레임을 구성할 것이다. 어떻게 할 지에 대한 이해를 위해 다음 다이어그램을 살펴보자:
<img src="https://koenig-media.raywenderlich.com/uploads/2015/05/customlayout-calculations1-667x500.png"/>
모든 아이템의 프레임을 계산할 것이고, 각 아이템의 열과 같은 열에서의 이전 아이템에 기반한다. 프레임을 위한 `xOffset` 과 이전 아이템의 위치를 위한 `yOffset` 을 추적할 것이다.

수평 위치를 계산하기 위해 아이템이 속한 열의 X 시작 좌표를 사용할 것이며, 셀 패딩을 더할 것이다. 수직 위치는 같은 열 아이템의 이전 시작 위치에 그 높이를 더한다. 전체 아이템 높이는 이미지 높이와 컨텐트 패딩의 합과 같다.

이를 `prepare()` 에서 할 것이다. 주요 목적은 레이아웃의 모든 아이템에 대해서 `UICollectionViewLayoutAttributes` 인스턴스를 계산하는 것이다.

다음 메소드를 추가하자:
```swift
override func prepare() {
  // 1
  guard 
    cache.isEmpty, 
    let collectionView = collectionView 
    else {
      return
  }
  // 2
  let columnWidth = contentWidth / CGFloat(numberOfColumns)
  var xOffset: [CGFloat] = []
  for column in 0..<numberOfColumns {
    xOffset.append(CGFloat(column) * columnWidth)
  }
  var column = 0
  var yOffset: [CGFloat] = .init(repeating: 0, count: numberOfColumns)
    
  // 3
  for item in 0..<collectionView.numberOfItems(inSection: 0) {
    let indexPath = IndexPath(item: item, section: 0)
      
    // 4
    let photoHeight = delegate?.collectionView(
      collectionView,
      heightForPhotoAtIndexPath: indexPath) ?? 180
    let height = cellPadding * 2 + photoHeight
    let frame = CGRect(x: xOffset[column],
                       y: yOffset[column],
                       width: columnWidth,
                       height: height)
    let insetFrame = frame.insetBy(dx: cellPadding, dy: cellPadding)
      
    // 5
    let attributes = UICollectionViewLayoutAttributes(forCellWith: indexPath)
    attributes.frame = insetFrame
    cache.append(attributes)
      
    // 6
    contentHeight = max(contentHeight, frame.maxY)
    yOffset[column] = yOffset[column] + height
    
    column = column < (numberOfColumns - 1) ? (column + 1) : 0
  }
}
```
1. `cache` 가 비어있고, 콜랙션 뷰가 존재할 때만 레이아웃 속성을 계산한다.
2. 열 너비에 기반한 모든 열의 x 좌표로 `xOffset` 배열을 채우자. `yOffset` 배열은 모든 열의 y 위치를 추적한다. 처음에는 0으로 초기화한다. 
3. 특정 레이아웃은 하나의 섹션만 존재하기 때문에 첫번째 섹션에 있는 모든 아이템을 순회한다.
4. `frame` 계산을 수행하자. `width` 는 이전에 계산된 셀간 패딩을 포함한 값이다. `delegate` 에 사진 높이를 요청하자, 그리고 위 아래의 패딩과 높이에 기반하여 프레임 높이를 계산하자. 만약, 델리게이트 설정이 되지 않았다면, 디폴트 높이를 사용하자. 그리고나서 속성이 사용할 `insetFrame` 을 생성하기 위해 현재 열의 x, y 오프셋을 결합하자.
5. `UICollectionViewLayoutAttributes` 인스턴스를 생성하여, 프레임을 `insetFrame` 으로 설정하고 `cache` 에 속성을 추가하자.
6. 새로이 계산된 아이템의 프레임을 고려하여 `contentHeight` 를 확장한다. 그리고 프레임에 기반하여 형재 컬럼의 `yOffset` 을 증가시킨다. 마지막으로, `column` 을 증가하여 다음 아이템이 다음 컬럼에 위치할 수 있도록 한다.

> **Note:** `prepare()`는 콜랙션 뷰의 레이아웃이 무효해질 때마다 호출되기 때문에, 전형적인 구현에서는 이 메소드에서 속성을 다시 계산해야 하는 많은 상황이 존재한다. 예를 들어, 오리엔테이션이 바뀌면 `UICollectionView` 의 bounds가 변할 것이다. 또한 아이템이 추가되거나 삭제될 때 변할 수도 있다.
> 
> 이러한 유형들은 이번 튜토리얼의 범위를 벗어나지만, 일반적인 구현에서 이를 인지하는 것은 중요하다.

이제 `layoutAttributesForElements(in:)` 를 오버라이드 할 필요가 있다. 콜랙션 뷰는 `prepare()` 이후에 호출하여, 주어진 사각형에서 어떤 아이템들이 보이는지 결정한다.

다음 코드를 추가하자:
```swift
override func layoutAttributesForElements(in rect: CGRect) 
    -> [UICollectionViewLayoutAttributes]? {
  var visibleLayoutAttributes: [UICollectionViewLayoutAttributes] = []
  
  // Loop through the cache and look for items in the rect
  for attributes in cache {
    if attributes.frame.intersects(rect) {
      visibleLayoutAttributes.append(attributes)
    }
  }
  return visibleLayoutAttributes
}
```

여기서, `cache` 에서 속성들을 순회하며 콜랙션 뷰가 제공하는 `rect` 와 이들의 프레임이 교차하는지 확인한다.

교차하는 속성은 메소드에서 반환할 `visibleLayoutAttributes` 에 추가한다.

구현해야하는 마지막 메소드는 `layoutAttributesForItem(at:)` 이다.
```swift
override func layoutAttributesForItem(at indexPath: IndexPath) 
    -> UICollectionViewLayoutAttributes? {
  return cache[indexPath.item]
}
```

여기서, `cache` 로부터 요청된 `indexPath` 에 해당하는 레이아웃 속성을 찾아 반환한다.

## Connecting with UIViewController
레이아웃이 행동하는 것을 보려면, 레이아웃 델리게이트를 구현할 필요가 있다. `PinterestLayout` 은 그것에 의존하여 아이템 프레임의 높이를 계산하기 위해 사진과 캡션 높이를 제공한다.

## Where to Go From Here?

