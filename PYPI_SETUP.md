# PyPI 배포 가이드 — Trusted Publishers

이 가이드는 `korean-data-mcp`를 PyPI에 배포하는 방법을 설명합니다.  
GitHub Actions + OIDC Trusted Publishers 방식 (API 토큰 불필요).

---

## 1단계: PyPI 계정 생성

1. https://pypi.org/account/register/ 방문
2. 계정 정보 입력:
   - **이름**: Session Zero
   - **이메일**: sessionzero42@gmail.com
   - **사용자명**: sessionzero42
   - **패스워드**: (강력한 비밀번호 사용)
3. hCaptcha 체크박스 클릭 (사람입니다)
4. "계정 생성" 클릭
5. 이메일에서 인증 링크 클릭

> ⚠️ 2FA (이중 인증) 설정을 권장합니다.

---

## 2단계: PyPI Trusted Publisher 설정

1. PyPI 로그인 후 https://pypi.org/manage/account/publishing/ 방문
2. **"Add a new pending publisher"** 클릭
3. 다음 정보 입력:
   - **Project name**: `korean-data-mcp`
   - **Owner**: `leadbrain`
   - **Repository name**: `korean-data-mcp`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `pypi`
4. "Add" 클릭

---

## 3단계: GitHub Repository Environments 설정

1. GitHub 레포 → Settings → Environments
2. `pypi` environment 생성 (이름 정확히 입력)
3. (선택) Deployment protection rules 설정

---

## 4단계: 첫 배포

### 방법 A: GitHub Release 생성 (자동)
```bash
# 로컬에서 태그 생성
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```
GitHub에서 Release 생성 → Actions 자동 실행 → PyPI 배포

### 방법 B: 수동 실행
GitHub Actions → Publish to PyPI → Run workflow → `pypi` 선택

---

## 5단계: 설치 확인

```bash
pip install korean-data-mcp
```

---

## TestPyPI 테스트 (선택)

위와 동일하게 https://test.pypi.org 에서 계정 생성 후:
- Environment name: `testpypi`
- Workflow 수동 실행 시 `testpypi` 선택

```bash
pip install --index-url https://test.pypi.org/simple/ korean-data-mcp
```
