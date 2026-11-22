import os
import json
import base64
import uuid
import re
from PIL import Image, ImageOps

from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from google import genai
from google.genai import types

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

load_dotenv()

app = Flask(__name__)
from werkzeug.utils import secure_filename


APP_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = APP_DIR / "uploads"
OUTPUT_DIR = APP_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def save_optimized_image(file):
    """업로드된 이미지를 자동으로 축소하고 압축한다."""
    image = Image.open(file.stream)

    # 사진 방향 보정
    image = ImageOps.exif_transpose(image)

    # 최대 크기 1800 x 1800
    image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)

    # JPEG 저장을 위해 RGB로 변환
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 고유한 파일명으로 저장
    filename = uuid.uuid4().hex + ".jpg"
    path = UPLOAD_DIR / filename

    # 이미지 압축
    image.save(
        path,
        format="JPEG",
        quality=82,
        optimize=True,
        progressive=True
    )

    return path
    
ALLOWED = {"png", "jpg", "jpeg", "webp", "pdf"}
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

def client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다.")
    return genai.Client(api_key=key)

def file_to_data_url(path):
    ext = path.suffix.lower()
    mime = {".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".webp":"image/webp"}.get(ext)
    if not mime:
        raise ValueError("현재 이미지 파일만 AI 시각 분석에 직접 전달할 수 있습니다. PDF는 JPG/PNG로 변환해 업로드해 주세요.")
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"

def ask_ai(prompt, paths):
    content = [prompt]

    for p in paths:
        ext = p.suffix.lower()

        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp"
        }.get(ext)

        if not mime:
            raise ValueError("지원하지 않는 이미지 형식입니다.")

        content.append(
            types.Part.from_bytes(
                data=p.read_bytes(),
                mime_type=mime
            )
        )

    ai_client = client()

    try:
        response = ai_client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
            contents=content,
            config={
                "response_mime_type": "application/json"
            }
        )

        return response.text

    finally:
        ai_client.close()

def extract_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    for start, end in [("[", "]"), ("{", "}")]:
        first = text.find(start)
        last = text.rfind(end)

        if first != -1 and last > first:
            try:
                return json.loads(text[first:last + 1])
            except json.JSONDecodeError:
                pass

    return {"raw": text}
@app.errorhandler(413)
def too_large(e):
    return jsonify(
        error="업로드한 파일의 전체 용량이 너무 큽니다. 사진 용량을 줄이거나 파일 수를 줄여 주세요."
    ), 413
@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze-style")
def analyze_style():
    try:
    
            try:
                p = save_optimized_image(f)
                paths.append(p)
            except Exception:
                return jsonify(error="이미지를 읽을 수 없습니다. JPG, PNG, WEBP 사진을 확인해 주세요."), 400

            try:
    p = save_optimized_image(f)
    paths.append(p)
except Exception:
    return jsonify(error="이미지를 읽을 수 없습니다. JPG, PNG, WEBP 사진을 확인해 주세요."), 400
        if not paths: return jsonify(error="시험지 사진을 한 장 이상 업로드해 주세요."),400
        prompt="""너는 평가문항 분석 전문가다. 첨부된 기존 시험지 이미지를 읽고 출제자의 관찰 가능한 출제 스타일을 분석하라.
추측은 추측이라고 표시하고, 이미지에서 읽히지 않는 부분은 불명확하다고 밝혀라. 선생님의 성격이나 신원을 추정하지 말고 문항의 형식만 분석하라.
JSON 객체만 출력하라. 형식:
{"profile_name":"내 선생님","summary":"요약","question_types":[{"type":"객관식/서술형 등","estimated_share":"비율 또는 추정","features":"특징"}],"difficulty":"난이도 설명","distractor_style":"오답 선지 특징","wording":"질문 표현 특징","topic_selection":"세부 개념/자료 활용 특징","patterns":["관찰된 특징"],"uncertainties":["판독 한계"],"generation_rules":["새 시험지에 적용할 규칙"]}"""
        result=extract_json(ask_ai(prompt,paths))
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)),500

@app.post("/api/generate")
def generate():
    
            try:
                p = save_optimized_image(f)
                paths.append(p)
            except Exception:
                return jsonify(error="이미지를 읽을 수 없습니다. JPG, PNG, WEBP 사진을 확인해 주세요."), 400

        if not paths: return jsonify(error="새 시험범위 사진을 업로드해 주세요."),400
        style=request.form.get("style","")
        count=max(5,min(40,int(request.form.get("count", "15"))))
        types=request.form.get("types","객관식, 단답형, 서술형")
        prompt=f"""너는 교사가 사용하는 평가문항 개발 전문가다. 첨부한 이미지는 새 시험범위 자료다.
아래의 출제 스타일 분석을 참고하되 문항과 정답은 새 시험범위 내용에 근거해 독창적으로 작성하라.
스타일 분석(참고): {style}
문제 수: {count}. 선호 유형: {types}.
중요: 자료에 없는 사실을 정답 근거로 만들지 말고, 이미지 판독이 불확실하면 해당 내용을 출제하지 마라.
문항마다 정답과 간결하지만 충분한 해설을 포함하라. 난이도도 표시하라.
JSON 배열만 출력:
[{{"number":1,"type":"객관식","difficulty":"중","question":"질문","choices":["① ...","② ...","③ ...","④ ..."],"answer":"정답","explanation":"해설","source_topic":"시험범위의 관련 개념"}}]
객관식 외 유형은 choices를 빈 배열로 둔다. 객관식은 정답이 하나만 있도록 검토하고, 선택지는 서로 겹치지 않게 작성하라."""
        result=extract_json(ask_ai(prompt,paths))
        if isinstance(result,dict) and "raw" in result:
            return jsonify(error="AI 응답을 문제 데이터로 변환하지 못했습니다. 다시 시도해 주세요.", raw=result["raw"]),500
        if isinstance(result,dict) and "questions" in result: result=result["questions"]
        if not isinstance(result,list): return jsonify(error="문제 생성 결과 형식이 올바르지 않습니다.", raw=result),500
        return jsonify(questions=result)
    except Exception as e:
        return jsonify(error=str(e)),500

@app.post("/api/export")
def export_pdf():
    data=request.get_json(force=True)
    title=data.get("title","AI 맞춤형 모의고사")
    questions=data.get("questions",[])
    answers=data.get("include_answers",False)
    if not questions: return jsonify(error="PDF로 저장할 문제가 없습니다."),400
    out=OUTPUT_DIR/(uuid.uuid4().hex+".pdf")
    doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42)
    styles=getSampleStyleSheet()
    pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
    title_style=ParagraphStyle("TitleK",parent=styles["Title"],fontName="HYSMyeongJo-Medium",fontSize=18,leading=24,alignment=TA_CENTER,spaceAfter=18)
    body=ParagraphStyle("BodyK",parent=styles["BodyText"],fontName="HYSMyeongJo-Medium",fontSize=10.5,leading=16,spaceAfter=7)
    story=[Paragraph(title.replace("&","&amp;"),title_style),Paragraph("이 자료는 AI가 업로드한 학습 자료를 바탕으로 생성한 연습용 문항입니다.",body),Spacer(1,10)]
    for q in questions:
        story.append(Paragraph(f"<b>{q.get('number','')}번. [{q.get('type','')}] [{q.get('difficulty','')}]</b> {q.get('question','')}",body))
        for c in q.get("choices",[]) or []: story.append(Paragraph(c,body))
        story.append(Spacer(1,10))
        if answers:
            story.append(Paragraph(f"<b>정답:</b> {q.get('answer','')}",body))
            story.append(Paragraph(f"<b>해설:</b> {q.get('explanation','')}",body))
            story.append(Spacer(1,10))
    doc.build(story)
    return jsonify(url=f"/download/{out.name}")

@app.get("/download/<name>")
def download(name):
    path=OUTPUT_DIR/secure_filename(name)
    if not path.exists(): return "파일을 찾을 수 없습니다.",404
    return send_file(path,as_attachment=True,download_name="맞춤형_모의고사.pdf")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
