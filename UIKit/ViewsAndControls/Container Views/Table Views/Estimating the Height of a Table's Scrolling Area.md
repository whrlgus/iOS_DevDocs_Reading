# Estimating the Height of a Table's Scrolling Area

테이블 뷰의 헤더, 푸터, 행의 높이 예측치를 제공하여 스크롤링이 컨텐츠의 크기를 정확히 반영하도록 하자.

## Overview

가능하다면, 테이블 뷰는 셀, 헤더, 푸터의 높이 예측치를 사용하여 성능과 스크롤링 행위를 향상시킨다. 테이블 뷰가 화면에 나타나기 전에, 스크롤링과 관련된 파마미터들을 구성하기 위한 정보가 필요하기 때문에 컨텐츠 뷰의 높이를 계산한다. 이 항목들에 대한 높이 예측치를 제공하지 않으면, 테이블 뷰는 항목들의 실제 높이를 계산해야하며, 이는 비용이 많이 든다.

> Important
>
> 만약 테이블 뷰가 self-sizing 셀, 헤더, 푸터를 포함한다면 반드시 예측된 높이를 제공해야한다.

테이블 뷰는 표준 헤더, 푸터, 행 스타일에 근거하여 각 항목들에 대한 기본 높이 예측치를 제공한다. 만약 테이블의 항목들이 기본값과 상당한 차이가 있다면, estimated[Row|SectionHeader|SectionFooter]Height 프로퍼티에 커스텀 측정치를 할당할 수 있다. 만약 각각 상이하다면, 다음 델리게이트 객체의 메소드를 통해 제공할 수 있다.

- tableView(_:estimatedHeightForRowAt:)
- tableView(_:estimatedHeightForHeaderInSection:)
- tableView(_:estimatedHeightForFooterInSection:)

헤더, 푸터, 행의 높이를 예측할 때 중요한 것은 정확도보단 속도이다. 테이블 뷰는 모든 항목에 대해 예측치를 물어보며, 이러한 델리게이트 메소드에서 오래걸리는 작업을 수행하면 안된다. 대신에, 스크롤링에 유용하게 근사치를 생성해야한다. 테이블 뷰는 항목들이 화면에 보여질 때, 예측 값을 실제 값으로 대체한다.

테이블 뷰가 높이 예측치를 사용할 때, 스크롤 뷰로부터 상속한 contentOffset과 contentSize 프로퍼티를 활발하게 관리한다. 이러한 프로퍼티를 직접 읽거나 변경하지 말자. 그 값들은 UITableView에만 의미 있는 값이다.