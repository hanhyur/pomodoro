# 실행방법

## cmd 사용

`.py`파일이 위치한 폴더에서

```
python [파일이름].py
```

## .exe 생성

### 1. 클론
```
git clone [repo]
```

### 2. pyinstaller 설치
```
pip install pinstaller
```

### 3. .exe 파일 생성
```
pyinstaller --onefile --windowed --icon=[아이콘파일이름].ico --name=[exe파일 이름] --clean [파일이름].py
```
