# 타이타닉 데이터셋 - 피처 엔지니어링 레퍼런스

## 데이터 구성

| 파일명 | 설명 |
|--------|------|
| `train.csv` | 학습용 데이터 (정답 레이블 포함) |
| `test.csv` | 예측용 데이터 (정답 레이블 없음) |
| `gender_submission.csv` | 제출 파일 예시 (여성 전원 생존 가정) |

---

## 변수 설명 (Data Dictionary)

| 변수명 | 설명 | 값 / 비고 |
|--------|------|-----------|
| `Survived` | 생존 여부 **(타깃 변수)** | `0` = 사망, `1` = 생존 |
| `Pclass` | 티켓 등급 (사회경제적 지위 proxy) | `1` = 1등석(상류층), `2` = 2등석(중산층), `3` = 3등석(하류층) |
| `Sex` | 성별 | `male`, `female` |
| `Age` | 나이 (세) | 1세 미만은 소수점 표기. 추정 나이는 `xx.5` 형식 |
| `SibSp` | 함께 탑승한 형제/자매 또는 배우자 수 | 형제·자매·이복형제 포함 / 배우자(남편·아내) 포함. 내연·약혼자 제외 |
| `Parch` | 함께 탑승한 부모 또는 자녀 수 | 부모(母·父), 자녀(딸·아들·의붓자녀) 포함. 유모와 함께 탑승한 아이는 `Parch=0` |
| `Ticket` | 티켓 번호 | 문자열 혼합, 그룹 탑승 시 번호 공유 가능 |
| `Fare` | 지불 운임 | 연속형, 그룹 탑승 시 총액 공유 가능성 있음 |
| `Cabin` | 객실 번호 | 결측 다수. 알파벳 접두사 = 갑판 위치 |
| `Embarked` | 승선 항구 | `C` = Cherbourg(프랑스), `Q` = Queenstown(아일랜드), `S` = Southampton(영국) |

---

## 피처 엔지니어링 아이디어

### 1. 가족 관련
```python
# 전체 가족 수
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

# 혼자 탑승 여부
df['IsAlone'] = (df['FamilySize'] == 1).astype(int)

# 가족 규모 카테고리 (소가족이 생존에 유리한 경향)
df['FamilyGroup'] = pd.cut(df['FamilySize'], bins=[0,1,4,20], labels=['alone','small','large'])
```

### 2. 나이(Age) 관련
```python
# 결측값 처리: Pclass + Sex 그룹별 중앙값으로 대체
df['Age'] = df.groupby(['Pclass','Sex'])['Age'].transform(lambda x: x.fillna(x.median()))

# 나이 구간화
df['AgeBin'] = pd.cut(df['Age'], bins=[0,12,18,35,60,100], labels=['child','teen','young','middle','senior'])

# 어린이 여부 (생존율 높음)
df['IsChild'] = (df['Age'] < 12).astype(int)
```

### 3. 호칭(Title) 추출
```python
# Name 컬럼에서 호칭 추출 → 사회적 지위·성별·나이 간접 반영
df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)

# 희귀 호칭 통합
rare = ['Lady','Countess','Capt','Col','Don','Dr','Major','Rev','Sir','Jonkheer','Dona']
df['Title'] = df['Title'].replace(rare, 'Rare')
df['Title'] = df['Title'].replace({'Mlle':'Miss', 'Ms':'Miss', 'Mme':'Mrs'})
```

### 4. 운임(Fare) 관련
```python
# 결측값: 중앙값 대체
df['Fare'] = df['Fare'].fillna(df['Fare'].median())

# 로그 변환 (우편향 분포 완화)
df['FareLog'] = np.log1p(df['Fare'])

# 구간화
df['FareBin'] = pd.qcut(df['Fare'], q=4, labels=['low','mid','high','very_high'])

# 1인당 운임 (그룹 공유 운임 보정)
df['FarePerPerson'] = df['Fare'] / df['FamilySize']
```

### 5. 객실(Cabin) 관련
```python
# 객실 보유 여부 (결측 = 없음으로 해석)
df['HasCabin'] = df['Cabin'].notna().astype(int)

# 갑판(Deck) 추출: 알파벳 첫 글자
df['Deck'] = df['Cabin'].str[0].fillna('Unknown')
```

### 6. 티켓(Ticket) 관련
```python
# 동일 티켓 번호 공유 인원 수 (그룹 탑승 여부)
df['TicketFreq'] = df.groupby('Ticket')['Ticket'].transform('count')
```

### 7. 승선 항구(Embarked) 관련
```python
# 결측값: 최빈값(S)으로 대체
df['Embarked'] = df['Embarked'].fillna('S')

# 인코딩
df = pd.get_dummies(df, columns=['Embarked'], prefix='Emb')
```

### 8. 성별 × 등급 교호작용
```python
# 성별과 Pclass 결합 피처
df['SexPclass'] = df['Sex'].astype(str) + '_' + df['Pclass'].astype(str)
```

---

## 주요 도메인 인사이트 (모델링 시 참고)

- **여성·어린이 우선 원칙** → `Sex`, `Age`, `IsChild` 피처 중요도 높음
- **1등석 승객** 생존율이 월등히 높음 → `Pclass` 핵심 피처
- **혼자 탑승(IsAlone=1)**보다 소가족(2~4명)이 생존율 높음; 대가족은 오히려 낮음
- **Cabin 결측** 자체가 하위 등급 proxy로 작용 가능
- **운임**은 Pclass와 상관관계 높음 → 다중공선성 주의

---

## 제거 권장 컬럼

| 컬럼 | 이유 |
|------|------|
| `PassengerId` | 단순 ID, 예측 무관 |
| `Name` | Title 추출 후 불필요 |
| `Ticket` | TicketFreq 파생 후 원본 제거 가능 |
| `Cabin` | Deck·HasCabin 파생 후 원본 제거 가능 |
