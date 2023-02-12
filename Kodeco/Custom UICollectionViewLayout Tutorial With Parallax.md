*본문: https://www.kodeco.com/527-custom-uicollectionviewlayout-tutorial-with-parallax*

iOS 6에 소개되어 iOS 10에 새로운 기능으로 개선된 `UICollectionView` 는, iOS 앱에서 데이터 콜랙션 표현을 커스터마이즈하고 애니메이션을 적용하기 위한 최고의 선택지이다.

`UICollectionView` 에 연관된 핵심 독립체는 `UICollectionViewLayout` 이다. 이 객체는 셀, 보조 뷰, 장식 뷰와 같은 모든 콜렉션 뷰 요소들의 속성을 정의하는 책임을 지고 있다.

`UIKit` 은 `UICollectionViewFlowLayout` 으로 불리는 `UICollectionViewLayout` 의 기본 구현체를 제공한다. 이 클래스는 간단한 커스텀으로 격자 배치를 구성할 수 있게 해준다.

이번 튜토리얼은 `UICollectionViewLayout` 을 서브클래스화하고 커스터마이즈하는 방법을 가르쳐 줄 것이다. 또한, 콜랙션 뷰에 커스텀 보조 뷰, 늘림, 고정, 시차 효과를 추가하는 방법도 보여줄 것이다.

## Getting Started
이 앱은 정글 축구 컵 2017에 참가하는 부엉이 팀의 선수들을 보여주고 있다. 섹션 헤더는 팀에서 그들의 역할을 보여주며, 푸터는 각 집합의 힘을 보여준다.

**JungleCupCollectionViewController.swift** 파일에는 `UICollectionViewDataSource` 를 채택하는 `UICollectionViewController` 의 서브클래스 구현체가 있다. 이 것은 보조 뷰를 추가하는데 필요한 메소드와 옵셔널 메소드를 구현하고 있다. 또한, 콜랙션 뷰가 데이터 소스를 대체할 수 있게  `MenuViewDelegate` 를 채택하고 있다.

**Reusable Views** 폴더에는 셀을 위한 `UICollectionViewCell`, 섹션 헤더와 푸터 뷰를 위한 `UICollectionReusableView` 의 서브클래스가 있다. 각각 **Main.storyboard** 파일에 디자인 된 뷰에 연결되어 있다.

`CustomLayout` 이 필요로 하는 커스텀 보조 뷰도 있다. `HeaderView` 와 `MenuView` 클래스는 `UICollectionReusableView`의 서브클래스이다. 각각 **.xib** 파일에 연결되어 있다.

**MockDataManager.swift** 파일은 모든 팀을 위한 데이터 구조를 들고 있다. 편의를 위해, Xcode 프로젝트는 필요한 에셋을 내장하고 있다.

## Layout Settings
`Custom Layout` 폴더에는 다음 두가지 중요한 파일이 있어 주목할 필요가 있다:
- **CustomLayoutSettings.swift**
- **CustomLayoutAttributes.swift**

**CustomLayoutSettings.swift** 는 배치 설정을 갖고 있는 구조체를 구현하고 있다. 그 첫 그룹은 콜랙션 뷰의 요소 크기를 다루는 설정이고, 두번째 그룹은 배치 행동, 세번째는 배치 간격을 정의하고 있다.

## Layout Attributes
**CustomLayoutAttributes.swift** 파일에서 `UICollectionViewLayoutAttributes` 서브클래스를 구현하고 있다. 이 클래스는 콜랙션 뷰의 요소를 보여주기 전에 이를 구성하기 위해 필요한 모든 정보를 저장하고 있다.

이 클래스는 슈퍼 클래스로부터 `frame`, `transform`, `transform3D`, `alpha` 와 `zIndex` 같은 기본 속성을 상속받는다.

또한, 다음과 같은 새로운 커스텀 속성을 추가한다:
```swift
var parallax: CGAffineTransform = .identity
var initialOrigin: CGPoint = .zero
var headerOverlayAlpha = CGFloat(0)
```

`parallax`, `initialOrigin` 과 `headerOverlayAlpha` 는 늘림, 고정 효과의 구현을 위해 나중에 사용할 커스텀 속성이다.

> **Note:** 배치 속성(layout attributes) 객체는 콜랙션 뷰에 의해 복사될 수 있다. 그러므로, `UICollectionViewLayoutAttributes` 를 서브클래스화할 때, 새로운 인스턴스로 커스텀 속성을 복사하기 위한 적합한 메소드를 구현하여, `NSCopying`을 준수해야 한다. 
> 만약, 커스텀 배치 속성을 구현하면, 속성들의 값을 비교하기 위해, 상속한 `isEqual` 메소드를 재정의해야 한다. iOS 7 부터 배치 속성들이 변하지 않으면, 콜랙션 뷰는 배치 속성들을 적용하지 않는다.


## The Role of UICollectionViewLayout
`UICollectionViewLayout` 객체의 주목적은 `UICollectionView` 내의 모든 요소들의 위치와 시각적인 상태에 대한 정보를 제공하는 것이다. 이 객체가 셀이나 보조 뷰의 생성에 대한 책임을 지고 있지 않다는 점을 명심하자. 이 객체의 업무는 셀이나 보조 뷰에게 올바른 속성을 제공하는 것이다.

커스텀 `UICollectionViewLayout` 을 생성하는 것은 세가지 절차를 거친다:
1. 추상 클래스 `UICollectionViewLayout` 을 서브클래스화 하고 레이아웃 연산을 수행하는데 필요한 모든 속성을 정의하자.
2. 콜랙션 뷰의 모든 요소에 올바른 속성을 제공하기 위해 필요한 연산을 수행하자. `CollectionViewLayout` 를 스크래치 부터 구현할 것이기 때문에 가장 복잡한 단계가 될 것이다.
3. 콜랙션 뷰가 `CustomLayout` 클래스를 채택하도록 만든다.

## Step 1: Subclassing the UICollectionViewLayout Class
```swift
import UIKit

final class CustomLayout: UICollectionViewLayout {
  
  // 1
  enum Element: String {
    case header
    case menu
    case sectionHeader
    case sectionFooter
    case cell
    
    var id: String {
      return self.rawValue
    }
    
    var kind: String {
      return "Kind\(self.rawValue.capitalized)"
    }
  }
  
  // 2
  override public class var layoutAttributesClass: AnyClass {
    return CustomLayoutAttributes.self
  }
  
  // 3
  override public var collectionViewContentSize: CGSize {
    return CGSize(width: collectionViewWidth, height: contentHeight)
  }

  // 4
  var settings = CustomLayoutSettings()
  private var oldBounds = CGRect.zero
  private var contentHeight = CGFloat()
  private var cache = [Element: [IndexPath: CustomLayoutAttributes]]()
  private var visibleLayoutAttributes = [CustomLayoutAttributes]()
  private var zIndex = 0
  
  // 5
  private var collectionViewHeight: CGFloat {
    return collectionView!.frame.height
  }

  private var collectionViewWidth: CGFloat {
    return collectionView!.frame.width
  }

  private var cellHeight: CGFloat {
    guard let itemSize = settings.itemSize else {
      return collectionViewHeight
    }

    return itemSize.height
  }

  private var cellWidth: CGFloat {
    guard let itemSize = settings.itemSize else {
      return collectionViewWidth
    }

    return itemSize.width
  }

  private var headerSize: CGSize {
    guard let headerSize = settings.headerSize else {
      return .zero
    }

    return headerSize
  }

  private var menuSize: CGSize {
    guard let menuSize = settings.menuSize else {
      return .zero
    }

    return menuSize
  }

  private var sectionsHeaderSize: CGSize {
    guard let sectionsHeaderSize = settings.sectionsHeaderSize else {
      return .zero
    }

    return sectionsHeaderSize
  }

  private var sectionsFooterSize: CGSize {
    guard let sectionsFooterSize = settings.sectionsFooterSize else {
      return .zero
    }

    return sectionsFooterSize
  }

  private var contentOffset: CGPoint {
    return collectionView!.contentOffset
  }
}
```
1. `enum` 은 `CustomLayout` 의 모든 요소를 정의하기에 좋은 선택지이다. 문자열 사용을 하지 않아도 된다. No strings = no typos.
2. `layoutAttributesClass` 연산 프로퍼티는 속성 인스턴스가 사용할 클래스를 제공한다. `CustomLayoutAttributes` 타입의 클래스를 반환해야 한다: 스타터 프로젝트에서 찾을 수 있다.
3. `UICollectionViewLayout` 의 서브클래스는 `collectionViewContentSize` 연산 프로퍼티를 반드시 오버라이드 해야 한다.
4. `CustomLayout` 은 속성들(attributes)을 준비하기 위해 이 프로퍼티들이 필요하다. `settings`는 외부 객체에 의해서 구성될 수 있기 때문에, `settings`를 제외한 모든 것들이 `private` 이다. 
5. 이후 장황한 반복을 피하기 위해 신택틱 슈가를 사용한 연산 프로퍼티들이다. 어디가??


## Step 2: Implementing the CollectionViewLayout Core Process

콜랙션 뷰는 `CustomLayout` 객체와 직접적으로 동작하여 전체 레이아웃 프로세스를 관리한다. 예를 들어, 콜랙션 뷰는 처음 보여지거나 리사이즈 될 때 레이아웃 정보를 요청한다.

레이아웃 프로세스 동안에, 콜랙션 뷰는 `CustomLayout` 객체의 필요한 메소드를 호출한다. 다른 옵셔널 메소드는 특정 상황하에 호출 될 수도 있다. 이러한 메소드들은 아이템들의 위치를 계산하고 콜랙션 뷰에게 필요한 정보를 제공할 기회이다.

오버라이드할 필요한 처음 두가지 메소드들은:
- `prepare()`
- `shouldInvalidateLayout(forBoundsChange:)`

`prepare()`은 레이아웃에서 요소들의 위치를 결정하기 위해 필요한 모든 계산을 수행할 수 있는 기회이다. `shouldInvalidateLayout(forBoundsChange:)` 는 `CustomLayout` 객체가 핵심 프로세스를 언제 다시 수행할 지 정의하기 위한 곳이다.

`prepare()` 구현부터 살펴보자.
```swift
// MARK: - LAYOUT CORE PROCESS
extension CustomLayout {

  override public func prepare() {
    
    // 1
    guard let collectionView = collectionView,
      cache.isEmpty else {
      return
    }
    // 2
    prepareCache()
    contentHeight = 0
    zIndex = 0
    oldBounds = collectionView.bounds
    let itemSize = CGSize(width: cellWidth, height: cellHeight)
    
    // 3
    let headerAttributes = CustomLayoutAttributes(
      forSupplementaryViewOfKind: Element.header.kind,
      with: IndexPath(item: 0, section: 0)
    )
    prepareElement(size: headerSize, type: .header, attributes: headerAttributes)
    
    // 4
    let menuAttributes = CustomLayoutAttributes(
      forSupplementaryViewOfKind: Element.menu.kind,
      with: IndexPath(item: 0, section: 0))
    prepareElement(size: menuSize, type: .menu, attributes: menuAttributes)
    
    // 5
    for section in 0 ..< collectionView.numberOfSections {

      let sectionHeaderAttributes = CustomLayoutAttributes(
        forSupplementaryViewOfKind: UICollectionElementKindSectionHeader,
        with: IndexPath(item: 0, section: section))
      prepareElement(
        size: sectionsHeaderSize,
        type: .sectionHeader,
        attributes: sectionHeaderAttributes)

      for item in 0 ..< collectionView.numberOfItems(inSection: section) {
        let cellIndexPath = IndexPath(item: item, section: section)
        let attributes = CustomLayoutAttributes(forCellWith: cellIndexPath)
        let lineInterSpace = settings.minimumLineSpacing
        attributes.frame = CGRect(
          x: 0 + settings.minimumInteritemSpacing,
          y: contentHeight + lineInterSpace,
          width: itemSize.width,
          height: itemSize.height
        )
        attributes.zIndex = zIndex
        contentHeight = attributes.frame.maxY
        cache[.cell]?[cellIndexPath] = attributes
        zIndex += 1
      }

      let sectionFooterAttributes = CustomLayoutAttributes(
        forSupplementaryViewOfKind: UICollectionElementKindSectionFooter,
        with: IndexPath(item: 1, section: section))
      prepareElement(
        size: sectionsFooterSize,
        type: .sectionFooter,
        attributes: sectionFooterAttributes)
    }
    
    // 6
    updateZIndexes()
  }
}
```
1. 준비 동작은 자원 집약적이며 성능에 영향을 미칠 수 있다. 이러한 이유로, 생성시에 계산한 속성을 캐싱한다. 실행 전에 `cache` 딕셔너리가 비어있는지 확인해야 한다. 오래된 것과 새로운 `attributes` 인스턴스를 엉망으로 만들지 않도록 하는 것은 중요하다.
2. `cache` 딕셔너리가 비어있다면, 그것을 적절히 초기화해야한다. `prepareCache()` 를 호출하여 이를 수행한다. 이 구현은 설명 이후에 추가할 것이다.
3. 늘어나는 헤더는 콜랙션 뷰의 첫번째 요소이다. 따라서, 이 헤더의 `attributes`를 처음으로 고려해야 한다. `CustomLayoutAttributes` 클래스의 인스턴스를 생성하고 `prepareElement(size:type:attributes)` 에 전달한다. 이 메소드 또한 곧 구현할 것이다. 커스텀 요소를 생성할 때마다 `attributes`를 정확히 캐시하기 위해 이 메소드를 호출한다는 점만 기억하다.
4. 스티키 메뉴는 콜랙션 뷰의 두번째 요소이다. 전과 같이 이것의 `attributes` 를 계산한다.
5. 이 루프는 핵심 레이아웃 프로세스에서 가장 중요하다. 모든 `section`의 모든 `item` 에 대해서:
	1. 섹션 헤더의 `attributes` 를 생성하고 준비한다.
	2. `items`의 `attributes` 를 생성한다.
	3. 이들을 특정 `indexPath` 에 연관짓는다.
	4. 아이템들의 `frame` 과 `zIndex` 를 계산하고 설정한다.
	5. `UICollectionView` 의 `contentHeight` 를 갱신한다.
	6. 새롭게 생성된 속성을 `cache` 딕셔너리에 `type`(여기에서는 셀) 과 `indexPath` 를 키로하여 저장한다.
	7. 마지막으로, 섹션 푸터의 `attributes` 를 생성하고 준비한다.
6. 마지막에는, 모든 `zIndex`  값을 갱신하기 위한 메소드를 호출한다. 곧 세부 내용을 다룰 것이며 이것이 왜 중요한지 배울 것이다.

다음으로 아래 메소드를 추가하자:
```Swift
override public func shouldInvalidateLayout(forBoundsChange newBounds: CGRect) -> Bool {
  if oldBounds.size != newBounds.size {
    cache.removeAll(keepingCapacity: true)
  }
  return true
}
```

`shouldInvalidateLayout(forBoundsChange:)` 내부에서, `prepare()` 에서 수행한 계산들을 어떻게 그리고 언제 무효화해야 하는지 정의해야 한다. 콜랙션 뷰는 `bounds` 속성이 변할 때마다 이 메소드를 호출한다. 콜랙션 뷰의 `bounds` 는 사용자가 스크롤 할 때마다 변하게 되는 것에 주목하자.

바운즈의 `size` 가 변한다면 항상 `true` 를 반환하며, 이 것은 콜랙션 뷰가 `portrait` 에서 `landscape` 모드로 혹은 반대로 전환되었음을 의미한다. 그리고 `cache` 딕셔너리는 비운다.

기기의 오리엔테이션 변화는 콜랙션 뷰의 `frame` 을 다시 그리게 하기 때문에, 캐시 정화는 필수적이다. 결과적으로 저장된 모든 속성들은 새로운 콜랙션 뷰 프레임에 맞지 않는다.

다음으로, `prepare()` 에서 호출되는 모든 메소드들을 구현할 것이다.

다음을 추가하자:
```swift
private func prepareCache() {
  cache.removeAll(keepingCapacity: true)
  cache[.header] = [IndexPath: CustomLayoutAttributes]()
  cache[.menu] = [IndexPath: CustomLayoutAttributes]()
  cache[.sectionHeader] = [IndexPath: CustomLayoutAttributes]()
  cache[.sectionFooter] = [IndexPath: CustomLayoutAttributes]()
  cache[.cell] = [IndexPath: CustomLayoutAttributes]()
}
```

이 메소드가 하는 첫번째는 `cache` 딕셔너리를 비우는 것이다. 다음으로, 기본키로서 요소의 `type`을 사용하여 내포된 모든 딕셔너리들을 재설정한다. `indexPath` 는 캐싱된 속성을 식별하기 위해 사용되는 보조키이다.

다음으로 `prepareElement(size:type:attributes:)` 를 구현하자.

```Swift
private func prepareElement(size: CGSize, type: Element, attributes: CustomLayoutAttributes) {
  //1
  guard size != .zero else {
    return
  }
  //2
  attributes.initialOrigin = CGPoint(x:0, y: contentHeight)
  attributes.frame = CGRect(origin: attributes.initialOrigin, size: size)
  // 3
  attributes.zIndex = zIndex
  zIndex += 1
  // 4
  contentHeight = attributes.frame.maxY
  // 5
  cache[type]?[attributes.indexPath] = attributes
}
```
1. 요소가 타당한 `size` 를 가지고 있는지 검사한다. 만약 크기가 없다면 `attributes` 를 캐싱할 이유가 없다.
2. 다음으로, 속성의 `initialOrigin` 프로퍼티에 프레임의 `origin` 값을 할당한다.
3. 그리고, 다른 요소들과 겹치지 않기 위해 `zIndex` 값을 할당한다.
4. 필요한 정보를 생성하고 저장했다면, 새로운 요소를 `UICollectionView` 에 추가했기 때문에 콜랙션 뷰의 `contentHeight` 를 갱신한다.
5. 마지막으로 요소 `type` 과 `indexPath`를 유일 키로 사용하여 속성을 `cache` 딕셔너리에 추가한다.

마침내 `updateZIndexes()` 를 구현할 때이다:

```swift
private func updateZIndexes(){
  guard let sectionHeaders = cache[.sectionHeader] else {
    return
  }
  var sectionHeadersZIndex = zIndex
  for (_, attributes) in sectionHeaders {
    attributes.zIndex = sectionHeadersZIndex
    sectionHeadersZIndex += 1
  }
  cache[.menu]?.first?.value.zIndex = sectionHeadersZIndex
}
```
이 메소드는 섹션 헤더에 계속 증가하는 `zIndex` 값을 할당한다. 카운트는 셀에 할당된 마지만 `zIndex` 값부터 시작한다. 가장 큰 `zIndex` 값은 메뉴의 `attributes` 에 할당된다. 이러한 재할당은 스티키 행동의 일관성을 위해 필요하다. 이 메소드가 호출되지 않는다면, 주어진 섹션의 셀들은 섹션의 헤더보다 큰 `zIndex` 값을 갖게 될 것이다. 그러면 스크롤 중에 괴상한 오버랩 효과를 보게될 것이다.

`CustomLayout` 클래스를 완료하고 레이아웃 핵심 프로세스를 올바르게 동작하기 위해서, 다음 필요한 메소드들을 구현해야 한다:
- `layoutAttributesForSupplementaryView(ofKind:at:)`
- `layoutAttributesForItem(at:)`
- `layoutAttributesForElements(in:)`

이 메소드들의 목적은 적시에 올바른 요소에 올바른 속성을 제공하기 위함이다. 더 구체적으로, 첫 두 메소드들은 콜랙션 뷰에 특정 보조 뷰나 특정 셀에 속성을 제공한다. 세번째는 주어진 순간에 보여지는 요소에 레이아웃 속성을 반환한다.

```swift
//MARK: - PROVIDING ATTRIBUTES TO THE COLLECTIONVIEW
extension CustomLayout {
  
  //1
  public override func layoutAttributesForSupplementaryView(
    ofKind elementKind: String,
    at indexPath: IndexPath) -> UICollectionViewLayoutAttributes? {
    
  switch elementKind {
    case UICollectionElementKindSectionHeader:
      return cache[.sectionHeader]?[indexPath]
      
    case UICollectionElementKindSectionFooter:
      return cache[.sectionFooter]?[indexPath]
      
    case Element.header.kind:
      return cache[.header]?[indexPath]
      
    default:
      return cache[.menu]?[indexPath]
    }
  }
  
  //2
  override public func layoutAttributesForItem(
    at indexPath: IndexPath) -> UICollectionViewLayoutAttributes? {
      return cache[.cell]?[indexPath]
  }

  //3
  override public func layoutAttributesForElements(
    in rect: CGRect) -> [UICollectionViewLayoutAttributes]? {
      visibleLayoutAttributes.removeAll(keepingCapacity: true)
      for (_, elementInfos) in cache {
        for (_, attributes) in elementInfos where attributes.frame.intersects(rect) {
          visibleLayoutAttributes.append(attributes)
        }
      }
      return visibleLayoutAttributes
  }
}
```
1. `layoutAttributesForSupplementaryView(ofKind:at:)`내부에서 `kind` 프로퍼티를 전환하여 `kind` 와 `indexPath` 에 해당하는 캐싱된 속성을 반환한다.
2. 동일하게 셀 속성을 반환한다.
3. `visibleLayoutAttributes` 배열을 비우고, 캐싱된 속성을 순회하며 보이는 요소들을 다시 담아 반환하다.

## Step 3: Adopting the CustomLayout


## Adding Stretchy, Sticky and Parallax Effects
이 튜토리얼의 마지막 섹션에서는 다음 시각적인 효과를 추가할 것이다:
1. 헤더를 늘리고 튕긴다
2. 메뉴와 섹션 헤더에 스티키 효과를 추가한다.
3. 사용자 경험을 더 매력적으로 만들기 위해 부드러운 시차 효과를 구현한다.

### Affine Transforms
`Core Graphics` `CGAffineTransform` API 는 `UICollectionView` 의 요소에 시각적 효과를 주기에 좋은 방법이다.

아핀 변환은 다양한 이유에서 매우 유용하다:
1. 이전, 크기 변환 그리고 회전 혹은 이 세가지를 결합하는 것과 같은 복잡한 시각적인 효과를 매우 짧은 코드로 생성할 수 있다.
2. `UIKit` 구성요소와 `AutoLayout` 에 결함없이 동작하게 할 수 있다.
3. 복잡한 시나리오에서도 성능 최적화를 유지할 수 있게 해준다.

### Transforming Visible Attributes
```swift
override public func layoutAttributesForElements(
  in rect: CGRect) -> [UICollectionViewLayoutAttributes]? {

    guard let collectionView = collectionView else {
      return nil
    }
    visibleLayoutAttributes.removeAll(keepingCapacity: true)
    // 1
    let halfHeight = collectionViewHeight * 0.5
    let halfCellHeight = cellHeight * 0.5
    // 2
    for (type, elementInfos) in cache {
      for (indexPath, attributes) in elementInfos {
        // 3
        attributes.parallax = .identity
        attributes.transform = .identity
        // 4
        updateSupplementaryViews(
          type,
          attributes: attributes,
          collectionView: collectionView,
          indexPath: indexPath)
        if attributes.frame.intersects(rect) {
          // 5
          if type == .cell,
            settings.isParallaxOnCellsEnabled {
              updateCells(attributes, halfHeight: halfHeight, halfCellHeight: halfCellHeight)
          }
          visibleLayoutAttributes.append(attributes)
        }
      }
    }
    return visibleLayoutAttributes
}
```

1. 특정 유용한 값들을 저장하여 루프에서 계산을 피한다.
2. 이전 버전과 동일한 루프이다. 캐싱된 모든 속성들을 순회한다.
3. `parallax` 변환 값과 `transform` 요소 속성 값을 디폴트 값으로 재설정한다.
4. 다른 종류의 보조 뷰를 갱신하기 위해 메소드를 호출한다. 
5. 현재 속성이 셀에 속해있는지 확인한다. 만약 시차 효과가 레이아웃 설정에서 활성화 되어 있다면, 그 속성을 갱신하는 메소드를 호출한다. 

다음으로, 위 루프에서 호출되는 두 메소드를 구현할 때이다:
- `updateSupplementaryViews(_:attributes:collectionView:indexPath:)`
- `updateCells(_:halfHeight: halfCellHeight:)`

```swift
private func updateSupplementaryViews(_ type: Element,
                                      attributes: CustomLayoutAttributes, 
                                      collectionView: UICollectionView,
                                      indexPath: IndexPath) {
    // 1
    if type == .sectionHeader,
      settings.isSectionHeadersSticky {
        let upperLimit = 
           CGFloat(collectionView.numberOfItems(inSection: indexPath.section))
           * (cellHeight + settings.minimumLineSpacing)
        let menuOffset = settings.isMenuSticky ? menuSize.height : 0
        attributes.transform =  CGAffineTransform(
          translationX: 0,
          y: min(upperLimit,
          max(0, contentOffset.y - attributes.initialOrigin.y + menuOffset)))
    }
    // 2
    else if type == .header,
      settings.isHeaderStretchy {
        let updatedHeight = min(
          collectionView.frame.height,
          max(headerSize.height, headerSize.height - contentOffset.y))
        let scaleFactor = updatedHeight / headerSize.height
        let delta = (updatedHeight - headerSize.height) / 2
        let scale = CGAffineTransform(scaleX: scaleFactor, y: scaleFactor)
        let translation = CGAffineTransform(
          translationX: 0,
          y: min(contentOffset.y, headerSize.height) + delta)
        attributes.transform = scale.concatenating(translation)
        if settings.isAlphaOnHeaderActive {
          attributes.headerOverlayAlpha = min(
            settings.headerOverlayMaxAlphaValue,
            contentOffset.y / headerSize.height)
        }
    }
    // 3
    else if type == .menu,
      settings.isMenuSticky {
        attributes.transform = CGAffineTransform(
          translationX: 0,
          y: max(attributes.initialOrigin.y, contentOffset.y) - headerSize.height)
    }
  }
```

1. 현재 요소가 섹션 헤더인지 확인한다. 레이아웃 설정에서 스티키 행위가 활성화되어 있다면, `transform` 을 계산한다.
2. 위와 동일한 절차이지만, 이번에는 요소가 상위 헤더인지를 검사한다. 늘림 효과가 활성화되어 있다면, 변환 계산을 수행한다.
3. 다시 동일한 절차이다. 스티키 메뉴에 대한 변환 계산을 수행한다.

이제는 콜랙션 뷰 셀을 변환할 차례이다:
```swift
  
private func updateCells(_ attributes: CustomLayoutAttributes,
                         halfHeight: CGFloat,
                         halfCellHeight: CGFloat) {
  // 1
  let cellDistanceFromCenter = attributes.center.y - contentOffset.y - halfHeight
    
  // 2
  let parallaxOffset = -(settings.maxParallaxOffset * cellDistanceFromCenter)
    / (halfHeight + halfCellHeight)
  // 3 
  let boundedParallaxOffset = min(
    max(-settings.maxParallaxOffset, parallaxOffset),
    settings.maxParallaxOffset)
  // 4
  attributes.parallax = CGAffineTransform(translationX: 0, y: boundedParallaxOffset)
}
```

1. 콜랙션 뷰의 `center` 로부터 셀의 거리를 계산한다.
2. `parallax`  최대값의 중앙에서 떨어진 거리에 비례하여 매핑한다.
3. 시각적인 글리치를 피하기위해 `parallaxOffset` 을 제한한다.
4. 계산된 `parallax` 값으로 `CAAffineTransform` 전환을 생성한다. 마지막으로, 속성의 `transform`  프로퍼티에 할당한다.

시차 효과를 주기위해서는 이미지의 프레임의 상하 인셋이 음수 값이어야 한다.
