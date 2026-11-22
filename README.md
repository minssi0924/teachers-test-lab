# TEACHER'S TEST LAB

기존 시험지 이미지에서 관찰 가능한 출제 스타일을 분석하고, 새 시험범위 이미지로 연습문제를 생성하는 Flask 웹앱입니다.

## 실행 방법 (Windows / macOS / Linux)

1. Python 3.10 이상을 설치합니다.
2. 압축을 푼 폴더에서 터미널을 열고 실행합니다.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

3. `.env.example`을 복사해 `.env` 파일을 만들고 OpenAI API 키를 입력합니다.
4. 환경변수를 불러오도록 아래처럼 실행합니다.

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="발급받은_API_키"
python app.py

# macOS/Linux
export OPENAI_API_KEY="발급받은_API_키"
python app.py
```

5. 브라우저에서 `http://127.0.0.1:5000`을 엽니다.

## 사용 순서

- 출제 스타일 분석: 기존 시험지 사진(JPG/PNG/WEBP)을 여러 장 업로드
- 문제 생성: 새 시험범위 사진 업로드, 문제 수와 유형 선택
- 문제 보관함: 문제 확인, 인쇄 또는 정답·해설 포함 PDF 생성

## 중요 안내

- 이 버전은 실제 AI API를 호출하는 실행형 MVP입니다. API 키와 API 사용 요금이 필요합니다.
- 업로드는 현재 이미지 형식(JPG/PNG/WEBP)을 지원합니다. PDF 시험지는 페이지를 이미지로 변환한 뒤 올려주세요.
- 파일은 서버의 `uploads/`, 생성 PDF는 `outputs/`에 저장됩니다. 운영 배포 전 인증, 개인정보 보호, 업로드 파일 자동 삭제, 저장소(DB), 악성 파일 검사, 요청 제한, HTTPS 등을 추가해야 합니다.
- AI가 읽지 못한 글자나 도표가 있을 수 있고 생성 문항에 오류가 생길 수 있으므로 실제 시험 대비 전 원본 자료와 대조하세요.
- 특정 교사의 문체를 완벽히 복제하거나 실제 출제를 보장하는 기능은 아닙니다. 공개된 문항에서 관찰된 형식적 경향을 참고해 연습문제를 만드는 학습 보조 도구입니다.

## 인터넷에 배포하기 (Render)

1. GitHub에 로그인하고 새 저장소를 만듭니다.
2. 압축을 푼 프로젝트 파일을 GitHub 저장소에 업로드합니다.
3. Render에 로그인한 뒤 **New → Blueprint**를 선택하고 해당 GitHub 저장소를 연결합니다.
4. `render.yaml` 설정을 확인하고 배포합니다.
5. Render 서비스의 **Environment**에서 `OPENAI_API_KEY` 값을 입력합니다.
6. 배포가 끝나면 Render가 발급한 `https://...onrender.com` 주소로 접속합니다.

주의:
- GitHub/Render 계정 연결, 배포 승인, API 키 입력은 소유자가 직접 해야 합니다. 이 대화에서 계정에 로그인하거나 비밀 키를 대신 입력할 수는 없습니다.
- 무료 인스턴스는 유휴 시 잠들 수 있으며 서버 로컬 파일은 재배포/재시작 시 보존되지 않을 수 있습니다. 장기 운영 전에는 영구 저장소와 데이터베이스 연결이 필요합니다.
- API 키를 GitHub 코드에 올리지 말고 Render의 Environment에만 입력하세요.
