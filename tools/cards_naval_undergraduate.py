# -*- coding: utf-8 -*-
"""Undergraduate requirement cards for the Department of Naval Architecture and Ocean Engineering (조선해양공학과),
students admitted in 2023, 2024, 2025 and 2026, written by hand from the department's own document
"교과목 이수규정" (course completion rules, 2026 academic year; 50 pages, dated 23 February 2026).
Download it from https://naoe.snu.ac.kr/department/rule (the post "교과목 이수 규정 (2013학번~ 현재)")
into sources/NAVAL/ first.

    cd tools && ../.venv/bin/python cards_naval_undergraduate.py     checks every card; writes nothing

The one document covers every year of admission from 2013. The parts used here (PDF page, printed page in brackets):
    page 3 (1)       table of graduation credits by year of admission (학번별 졸업이수학점 기준표)
    pages 4-5 (2-3)  2026 entrants: major rules, then liberal-education rules
    pages 6-7 (4-5)  2025 entrants: word for word the same as pages 4-5
    pages 8-9 (6-7)  2024 entrants
    pages 10-11 (8-9) 2023 entrants
Pages 12 to 50 are for entrants of 2022 and earlier and are not used.

Because all years are in one file, the code check can only confirm that a quote is somewhere in it. Each card
therefore also quotes the heading of the section of every year it applies to ("2024학번 이수 규정"), added by `ug`
below, and its first quote is chosen so that the page shown is a page of a section the card covers.

The document does not contain: a grade-average requirement, a limit on credits per semester, a graduation thesis
or project requirement (it only lists two thesis research courses), prerequisites, anything specific to
international students, or rules for students of other departments who take this major as a second one.
The standard form of major courses (전공이수 표준형태) is a table with a column per semester; the extracted text keeps
the year of each course but not its semester column, so the cards give the year only.
The checks are in tools/cards_pdf.py.
"""
from cards_pdf import card, pages, verify

NAME, PAGES = pages("NAVAL", "교과목 이수규정(2026학년도)")
TEXTS = {"ug": PAGES}
# A second, short document, "학부 졸업" (attached to the post "졸업관련 규정" on the same page): how to apply for the
# bachelor's thesis. The file itself was not downloaded; the developer pasted its text on 13 November 2026, and the paste
# breaks off partway through section 2 (prizes for graduates, which is not a requirement). The cards below use section 1
# only. If the PDF is later put in sources/NAVAL/, it is read instead of the pasted text.
import pathlib  # noqa: E402
_FOLDER = pathlib.Path(__file__).resolve().parent.parent / "sources" / "NAVAL"
_PDF = [f for f in _FOLDER.glob("*.pdf") if "학부 졸업" in f.name]
TEXTS["ug-graduation"] = pages("NAVAL", "학부 졸업")[1] if _PDF else [f.read_text(encoding="utf-8") for f in _FOLDER.glob("학부 졸업*.txt")]

ALL = [2023, 2024, 2025, 2026]
NEW, OLD = [2025, 2026], [2023, 2024]
FROM_2025 = "※ 상기 이수규정은 2025학년도 입학생부터 적용함."      # printed under the liberal-education table of 2025 and 2026
RECOMMENDED = "필수과목에 병기된 이수학기는 권장사항임"
TABLE_HEAD = "학번 졸업학점 교양학점 주전공학점 단일전공이수 타전공병행이수 (부전공, 복수전공, 연계전공)"
STAR = "*는 전공필수 교과목임"
ASK = "Ask the department office."


def ug(id, group, title, key, rule, quotes, years, why="", when="", trap=""):
    """One undergraduate card. The heading of each year's section is added to the quotes, so a reader can find the
    right section of the one document."""
    return card(id, ["undergraduate"], group, "ug", title, key, rule, quotes + [f"{year}학번 이수 규정" for year in sorted(years, reverse=True)],
                why, when=when, trap=trap, entry_years=years)


CARDS = [
    # ---- start early
    ug("na-ug-timing", "start_early", "Recommended semesters for first courses", "Labels such as [1-1] are recommendations",
       ["The liberal-education table labels required courses with a semester, read here as year and semester: [1-1] 대학 글쓰기 1 and 수학 1; [1-2] 대학 글쓰기 2: 과학기술글쓰기 and 수학 2; [2-1] 공학수학 1; [2-2] 공학수학 2.",
        "The document says the semester written beside a required course is a recommendation.",
        "In the major, the standard form (전공이수 표준형태) places the first required course, 414.110 조선해양공학의 이해, in year 1."],
       ["[1-1] 대학 글쓰기 1 [1-2] 대학 글쓰기 2: 과학기술글쓰기", "[1-1] 수학 1과 수학연습 1 또는 고급수학 1과 고급수학연습 1",
        "[1-2] 수학 2와 수학연습 2 또는 고급수학 2와 고급수학연습 2", "[2-1] 공학수학 1 [2-2] 공학수학 2", RECOMMENDED,
        "전공이수 표준형태", "비고 1 414.110* 조선해양공학의 이해"],
       ALL),
    ug("na-ug-physics-placement", "start_early", "Which physics courses to take", "Depends on high-school Physics 2",
       ["In principle, a student who completed high-school Physics 2 (or a physics course of the same or a higher level) takes 물리학 1 and 2; a student who did not takes 물리의 기본 1 and 2.",
        "A student who should take 물리의 기본 1 and 2 but wishes to take 물리학 1 and 2 must sit the physics achievement test (물리학성취도평가) and obtain a certain score.",
        "The document does not give that score."],
       ["고교과정 물리 2(고교과정 물리 2와 동급 또는 더 높은 수준의 물리과목)를 이수한 학생은 ‘물리학 1, 2’를, 이수하지 않은 학생은 ‘물리의 기본 1, 2’를 이수하는 것을 원칙으로 함.",
        "‘물리의 기본 1, 2’를 이수해야 하는 학생이 ‘물리학 1, 2’를 수강하고자 할 경우 물리학성취도평가에 응시하여 일정 점수를 취득해야 함."],
       ALL),

    # ---- liberal education
    ug("na-ug-ge", "general_education", "Liberal education credits by area", "At least 49 credits",
       ["Liberal education (교양): 49 credits or more.",
        "학문의 토대 (foundations of scholarship): writing and speaking (글쓰기와 말하기) 4 credits; foreign languages (외국어) 6; mathematics [수학] 12; science [과학] 12; computing [컴퓨팅] 3.",
        "지성의 열쇠 (keys of intellect): 9 credits or more.",
        "베리타스 (Veritas): 3 credits or more.",
        "Among all liberal education courses (전체 교양 교과목) the student chooses freely.",
        "The document says these rules apply from entrants of 2025."],
       ["교양 49학점 이상", "학문의 토대 글쓰기와 말하기 [1-1] 대학 글쓰기 1 [1-2] 대학 글쓰기 2: 과학기술글쓰기 4 외국어 [1-1, 1-2] 외국어 2개 교과목 6",
        "[수학] [1-1] 수학 1과 수학연습 1", "[2-1] 공학수학 1 [2-2] 공학수학 2 12", "[과학] [1-1, 1-2] 선택적 필수 과목", "해양학과 해양학실험 중에서 4학점 12",
        "[컴퓨팅] [1-1] 컴퓨터의 개념 및 실습 3 지성의 열쇠",
        "3개 영역(문화 해석과 상상, 역사적 탐구와 철학적 사유, 인간의 이해와 사회 분석)에서 9학점 이상 이수", "베리타스 영역에서 3학점 이상 이수",
        "전체 교양 교과목 중 학생이 자유롭게 선택", FROM_2025],
       NEW),
    ug("na-ug-ge-b", "general_education", "Liberal education credits by area", "At least 53 credits",
       ["Liberal education (교양): 53 credits or more.",
        "학문의 기초 (foundations of scholarship): thinking and expression (사고와 표현) 4 credits; foreign languages (외국어) 6; quantitative analysis and reasoning (수량적 분석과 추론) 12; scientific thinking and experiment (과학적 사고와 실험) 16; computer and information use (컴퓨터와 정보 활용) 3.",
        "학문의 세계 (worlds of scholarship): 12 credits.",
        "Among all liberal education courses (전체 교양 교과목) the student chooses freely."],
       ["교양 53학점 이상", "학문의 기초 사고와 표현 [1-1] 대학 글쓰기 1 [1-2] 대학 글쓰기 2: 과학기술글쓰기 4 외국어 [1-1,2] 외국어 2개 교과목 6",
        "수량적 분석과 추론 [1-1] 수학 1과 수학연습 1", "[2-1] 공학수학 1 [2-2] 공학수학 2 12", "과학적 사고와 실험 [1학년 1․2] 선택적 필수 과목",
        "해양학실험 중에서 학기별로 4학점, 총 8학점 16", "컴퓨터와 정보 활용", "컴퓨터의 개념 및 실습 3 학문의 세계 언어와 문학 12",
        "전체 교양 교과목 중 학생이 자유롭게 선택"],
       OLD),
    ug("na-ug-writing", "general_education", "Writing courses", "Two courses, 4 credits",
       ["Complete 대학 글쓰기 1 (College Writing 1) and 대학 글쓰기 2: 과학기술글쓰기 (College Writing 2: Science and Technology Writing).",
        "The table gives 4 credits for the two together."],
       ["[1-1] 대학 글쓰기 1 [1-2] 대학 글쓰기 2: 과학기술글쓰기 4"],
       ALL),
    ug("na-ug-foreign-language", "general_education", "Foreign-language courses and the English requirement", "2 courses, 6 credits; English if New TEPS 525 or below",
       ["Complete 2 foreign-language courses (외국어 2개 교과목): 6 credits.",
        "A student whose score at admission was TEPS 900 (New TEPS 525) or below must complete 1 English course.",
        "The document does not say which English course. " + ASK],
       ["외국어 2개 교과목 6", "입학 시 TEPS 900점(New TEPS 525점) 이하인 학생은 영어 1과목 필수 이수"],
       ALL),
    ug("na-ug-math", "general_education", "Mathematics courses", "12 credits: 수학 1 and 2, 공학수학 1 and 2",
       ["수학 1 (Mathematics 1) with 수학연습 1, or 고급수학 1 with 고급수학연습 1.",
        "수학 2 (Mathematics 2) with 수학연습 2, or 고급수학 2 with 고급수학연습 2.",
        "공학수학 1 and 공학수학 2 (Engineering Mathematics 1 and 2).",
        "The table gives 12 credits for these.",
        "In principle a course that has a practice course (연습) is taken together with that practice course in the same semester."],
       ["[1-1] 수학 1과 수학연습 1 또는 고급수학 1과 고급수학연습 1", "[1-2] 수학 2와 수학연습 2 또는 고급수학 2와 고급수학연습 2", "[2-1] 공학수학 1 [2-2] 공학수학 2 12",
        "연습이 있는 교과목을 수강하는 학생은 해당 학기에 연습교과목을 동시에 수강하는 것을 원칙으로 함"],
       ALL),
    ug("na-ug-science", "general_education", "Science courses with experiments", "12 credits: physics 8, one more science 4",
       ["Science [과학], courses required with a choice (선택적 필수): 12 credits.",
        "물리학 1 with 물리학실험 1, and 물리학 2 with 물리학실험 2: 4 credits each semester, 8 in total. 물리의 기본 1 or 고급물리학 1 may replace 물리학 1; 물리의 기본 2 or 고급물리학 2 may replace 물리학 2.",
        "4 more credits from: 화학 1 with 화학실험 1; 화학 2 with 화학실험 2; 화학 (or 고급화학) with 화학실험; 통계학 with 통계학실험; 지구과학 with 지구과학실험; 해양학 with 해양학실험.",
        "In principle a course in the science area (statistics included) is taken at the same time as its experiment course."],
       ["[과학] [1-1, 1-2] 선택적 필수 과목",
        "물리학 1*(물리의 기본 1 또는 고급물리학 1 대체 가능)과 물리학실험 1, 물리학 2*(물리의 기본 2 또는 고급물리학 2 대체 가능)와 물리학실험 2를 학기별로 4학점, 총 8학점",
        "화학 1과 화학실험 1, 화학 2와 화학실험 2, 화학(또는 고급화학)과 화학실험, 통계학과 통계학실험, 지구과학과 지구과학실험, 해양학과 해양학실험 중에서 4학점 12",
        "[과학] 영역(통계학 포함)은 이론교과목과 해당 교과의 실험 교과목을 동시에 수강하는 것을 원칙으로 함.", FROM_2025],
       NEW),
    ug("na-ug-science-b", "general_education", "Science courses with experiments", "16 credits: physics 8, other sciences 8",
       ["Scientific thinking and experiment (과학적 사고와 실험), courses required with a choice (선택적 필수), year 1: 16 credits.",
        "물리학 1 with 물리학실험 1, and 물리학 2 with 물리학실험 2: 4 credits each semester, 8 in total. 물리의 기본 1 or 고급물리학 1 may replace 물리학 1; 물리의 기본 2 or 고급물리학 2 may replace 물리학 2.",
        "8 more credits, 4 each semester, from: 화학 1 with 화학실험 1; 화학 2 with 화학실험 2; 생물학 1 with 생물학실험 1; 생물학 2 with 생물학실험 2; 화학 (or 고급화학) with 화학실험; 생물학 with 생물학실험; 통계학 with 통계학실험; 지구과학 with 지구과학실험; 해양학 with 해양학실험.",
        "In principle a course in this area (statistics included) is taken at the same time as its experiment course.",
        "통계학 and 통계학실험 belong to the area 수량적 분석과 추론 but are recognised as completing this area."],
       ["과학적 사고와 실험 [1학년 1․2] 선택적 필수 과목",
        "물리학1*(물리의 기본 1 또는 고급물리학 1 대체 가능)과 물리학실험 1, 물리학 2*(물리의 기본 2 또는 고급물리학 2 대체 가능)와 물리학실험 2를 학기별로 4학점, 총 8학점",
        "화학1과 화학실험1,화학2와 화학실험2, 생물학 1과 생물학실험1, 생물학2와 생물학실험2, 화학(또는 고급화학)과 화학실험, 생물학과 생물학실험, 통계학과 통계학실험, 지구과학과 지구과학실험, 해양학과 해양학실험 중에서 학기별로 4학점, 총 8학점 16",
        "과학적 사고와 실험 영역(통계학 포함)은 이론교과목과 해당 교과의 실험 교과목을 동시에 수강하는 것을 원칙으로 함.",
        "※ 통계학, 통계학실험은 수량적 분석과 추론 영역에 속하는 교과목이나 과학적 사고와 실험 영역 이수로 인정함"],
       OLD),
    ug("na-ug-computing", "general_education", "Computing course", "컴퓨터의 개념 및 실습; 3 credits",
       ["Complete 컴퓨터의 개념 및 실습 (Computer Concepts and Practice): 3 credits.",
        "It is labelled [1-1], read here as year 1, semester 1. The document says the labelled semester is a recommendation."],
       ["[1-1] 컴퓨터의 개념 및 실습 3", RECOMMENDED],
       [2024, 2025, 2026]),
    ug("na-ug-computing-b", "general_education", "Computing course", "컴퓨터의 개념 및 실습; 3 credits",
       ["Complete 컴퓨터의 개념 및 실습 (Computer Concepts and Practice): 3 credits.",
        "It is labelled [1-2], read here as year 1, semester 2. The document says the labelled semester is a recommendation."],
       ["[1-2] 컴퓨터의 개념 및 실습 3", RECOMMENDED],
       [2023]),
    ug("na-ug-keys", "general_education", "지성의 열쇠 (keys of intellect) courses", "At least 9 credits in 3 areas",
       ["Complete 9 credits or more in 3 areas: 문화 해석과 상상 (interpreting culture and imagination), 역사적 탐구와 철학적 사유 (historical inquiry and philosophical thought), 인간의 이해와 사회 분석 (understanding people and analysing society).",
        "The table shows 3 credits against each of the 3 areas.",
        "A further area, 과학적 사고와 응용, is listed with no credits against it."],
       ["3개 영역(문화 해석과 상상, 역사적 탐구와 철학적 사유, 인간의 이해와 사회 분석)에서 9학점 이상 이수", "지성의 열쇠 문화 해석과 상상 3",
        "역사적 탐구와 철학적 사유 3 인간의 이해와 사회 분석 3 과학적 사고와 응용", FROM_2025],
       NEW),
    ug("na-ug-veritas", "general_education", "베리타스 (Veritas) courses", "At least 3 credits",
       ["Complete 3 credits or more in the 베리타스 (Veritas) area.",
        "The table lists 베리타스 강좌 1, 베리타스 강좌 2 and 베리타스 실천 under this area."],
       ["베리타스 영역에서 3학점 이상 이수", "베리타스 강좌 1", "베리타스 강좌 2 베리타스 실천", FROM_2025],
       NEW),
    ug("na-ug-worlds", "general_education", "학문의 세계 (worlds of scholarship) courses", "12 credits from at least 4 of 5 areas",
       ["Complete 12 credits from at least 4 of these 5 areas: 언어와 문학 (language and literature), 문화와 예술 (culture and arts), 역사와 철학 (history and philosophy), 정치와 경제 (politics and economy), 인간과 사회 (people and society).",
        "The table also lists 자연과 기술 and 생명과 환경, which are not among the 5 areas named in the rule."],
       ["인간과 사회) 중 4개 영역 이상에서 12학점 이수", "5개 영역(언어와 문학, 문화와 예술, 역사와 철학, 정치와 경제, 인간과 사회) 중 4개 영역 이상에서 12학점 이수",
        "자연과 기술 생명과 환경 전체 교양 교과목"],
       [2024]),
    ug("na-ug-worlds-b", "general_education", "학문의 세계 (worlds of scholarship) courses", "12 credits from at least 3 of 5 areas",
       ["Complete 12 credits from at least 3 of these 5 areas: 언어와 문학 (language and literature), 문화와 예술 (culture and arts), 역사와 철학 (history and philosophy), 정치와 경제 (politics and economy), 인간과 사회 (people and society).",
        "The table also lists 자연과 기술 and 생명과 환경, which are not among the 5 areas named in the rule."],
       ["인간과 사회) 중 3개 영역 이상에서 12학점 이수", "5개 영역(언어와 문학, 문화와 예술, 역사와 철학, 정치와 경제, 인간과 사회) 중 3개 영역 이상에서 12학점 이수",
        "자연과 기술 생명과 환경 전체 교양 교과목"],
       [2023]),

    # ---- major courses
    ug("na-ug-major-credits", "major_courses", "Major credits with a single major", "63 credits: 30 required, at least 21 elective",
       ["A student whose single major is Naval Architecture and Ocean Engineering must complete 63 major credits in total.",
        "They must include the 30 credits of required major courses (전공필수) of the department's standard form (전공이수 표준형태) and at least 21 credits from elective major courses (전공선택)."],
       ["② 조선해양공학 단일전공 이수의 경우 본 전공과목 이수표준형태의 전공필수 교과목 30학점과 전공선택 교과목 중 21학점 이상을 포함하여 전공 교과목 총 63학점을 이수하여야 함."],
       NEW),
    ug("na-ug-major-credits-b", "major_courses", "Major credits", "66 credits or more: 30 required, at least 21 elective",
       ["Complete 66 or more major credits in total.",
        "They must include the 30 credits of required major courses (전공필수) of the department's standard form (전공이수 표준형태) and at least 21 credits from elective major courses (전공선택).",
        "The section for these years of admission states this one rule. A figure for students who also take another major appears only in the table of graduation credits (see the card on taking another major)."],
       ["③ 본 전공과목 이수표준형태의 전공필수 교과목 30학점과 전공 선택 교과목 중 21학점 이상을 포함하여 전공 교과목 총 66학점 이상 이수하여야 함"],
       OLD),
    ug("na-ug-other-major", "major_courses", "Major credits when another major is taken alongside", "48 credits: 30 required, at least 12 elective",
       ["A student who takes another major alongside (타전공병행이수: minor, double major, linked major and the like) must complete 48 major credits in total.",
        "They must include the 30 credits of required major courses (전공필수) of the department's standard form and at least 12 credits from elective major courses (전공선택).",
        "For such a student, courses from outside the department are recognised as major electives for up to 6 credits only (see the card on recognised courses)."],
       ["③ 타전공병행이수의 경우 본 전공과목 이수표준형태의 전공필수 교과목 30학점과 전공선택 교과목 중 12학점 이상을 포함하여 전공 교과목 총 48학점을 이수하여야 함.",
        "타전공병행이수(부/복수/연계전공 등)의 경우 최대 6학점까지 인정함."],
       NEW),
    ug("na-ug-other-major-b", "major_courses", "Major credits when another major is taken alongside", "45 major credits, stated only in the table",
       ["For a student who takes another major alongside (타전공병행이수: minor, double major, linked major), the table of graduation credits gives 45 major credits.",
        "The table prints this figure once, in a cell shared by the rows 2020 and 2021~2024.",
        "The sections for these years of admission do not mention it and give no split between required and elective courses. Confirm with the department office."],
       ["타전공병행이수 (부전공, 복수전공, 연계전공)", "2020 130 51 66 45 2021~2024 130 53", "학번별 졸업이수학점 기준표"],
       OLD),
    ug("na-ug-required", "major_courses", "Required major courses", "30 credits; the courses marked * in the standard form",
       ["Courses marked * in the standard form (전공이수 표준형태) are required major courses (전공필수): 30 credits.",
        "Year 1: 414.110 조선해양공학의 이해.",
        "Year 2: 414.251 구조정역학; 414.241 유체역학기초; 414.261 선박계산; 414.252 구조동역학; M1513.002400 선박 해양 탄소중립 에너지 개론; M1513.000700 해양열역학.",
        "Year 3: M1513.000800 컴퓨터이용선박설계; 414.341 선박해양유체역학.",
        "Year 4: M1513.001500 조선해양프로젝트."],
       ["비고 1 414.110* 조선해양공학의 이해",
        "2 414.251* 구조정역학 414.241* 유체역학기초 414.261* 선박계산 414.252* 구조동역학 M1513.002400* 선박 해양 탄소중립 에너지 개론 M1513.000700* 해양열역학 3 M1513.000800* 컴퓨터이용선박설계",
        "414.341* 선박해양유체역학", "4 M1513.002100 친환경선박추진시스템", "M1513.001500* 조선해양프로젝트", STAR, "전공필수 교과목 30학점", "전공이수 표준형태"],
       ALL),
    ug("na-ug-electives", "major_courses", "Other major courses in the standard form", "The courses without * in the standard form",
       ["The standard form marks required courses with *. It lists these other courses without that mark; the document does not say in so many words that they are elective major courses (전공선택).",
        "Year 3: 414.319 조선해양창의실험; 414.336 기초유한요소이론; 414.318 신호처리; 414.343 해양파역학; 414.361 선박해양설계이론; M1513.000900 선박해양구조진동학; M1513.001100 해양장비와 안전; M1513.002000 친환경선박해양공정시스템설계; M1513.001200 선박해양구조역학.",
        "Year 4: M1513.002100 친환경선박추진시스템; 414.419 조선해양경영론; M1513.001300 선박해양저항추진론; M1513.001400 선박해양운동조종론; 414.451 선박소음진동론; 414.461 선박해양생산공학; M1513.001600 조선해양기계학습; M1513.002200 조선해양 학사논문연구 1; M1513.002300 조선해양 학사논문연구 2."],
       ["3 M1513.000800* 컴퓨터이용선박설계 414.319 조선해양창의실험 (3-1-4) 414.336 기초유한요소이론 414.318 신호처리 414.343 해양파역학",
        "414.361 선박해양설계이론 M1513.000900 선박해양구조진동학 M1513.001100 해양장비와 안전 M1513.002000 친환경선박해양공정시스템설계 M1513.001200 선박해양구조역학 4 M1513.002100 친환경선박추진시스템 414.419 조선해양경영론 M1513.001300 선박해양저항추진론",
        "M1513.001400 선박해양운동조종론 414.451 선박소음진동론", "414.461 선박해양생산공학 M1513.001600 조선해양기계학습 M1513.002200 조선해양 학사논문연구 1 (1-1-0) M1513.002300 조선해양 학사논문연구 2",
        STAR, "전공이수 표준형태"],
       ALL),
    ug("na-ug-common-required", "major_courses", "College of Engineering common courses: required credits", "3 credits, outside the '공학기타' area",
       ["Complete 3 credits of College of Engineering common courses (공과대학 공통 교과목) from an area other than '공학기타' (engineering: other).",
        "The document does not list the areas or the courses in them.",
        "It does not say whether these 3 credits fall within the 6 credits of common courses recognised as major electives. " + ASK],
       ["①공과대학 공통 교과목 중 ‘공학기타’ 영역을 제외한 영역에서 3학점을 이수하여야 함",
        "①공과대학 공통교과목 전체(교과목 번호가 400으로 시작하거나, M2177로 시작하는 교과목, 최대6학점까지 인정)"],
       OLD),

    # ---- what counts
    ug("na-ug-recognised", "credit_rules", "Courses outside the department recognised as major electives", "Up to 12 credits; up to 6 with another major",
       ["Recognised as major electives: all undergraduate common courses of the College of Engineering (course number starting with 400 or M2177), and undergraduate major courses of other departments of the College of Engineering.",
        "Up to 12 credits are recognised; up to 6 for a student who takes another major alongside (minor, double major, linked major and the like).",
        "The Korean sentence can be read two ways: the 12-credit limit covers both kinds of course together, or only the other departments' courses. " + ASK],
       ["① 공과대학 공통 학사과정 교과목 전체(교과목 번호가 400으로 시작하거나 M2177로 시작하는 교과목) 및 공과대학 타학과(부) 전공 학사과정 교과목 최대 12학점까지 인정, 타전공병행이수(부/복수/연계전공 등)의 경우 최대 6학점까지 인정함.",
        "전공선택 인정과목"],
       NEW),
    ug("na-ug-recognised-b", "credit_rules", "Courses outside the department recognised as major electives", "College of Engineering common courses, up to 6 credits",
       ["Recognised as major electives: all common courses of the College of Engineering (course number starting with 400 or M2177), up to 6 credits.",
        "The sections for these years of admission say nothing about major courses of other departments."],
       ["①공과대학 공통교과목 전체(교과목 번호가 400으로 시작하거나, M2177로 시작하는 교과목, 최대6학점까지 인정)", "전공선택 인정과목"],
       OLD),
    ug("na-ug-leadership", "credit_rules", "Limit on 공학도의 도전과 리더십 credits", "At most 3 credits count as major credits",
       ["공학도의 도전과 리더십 1, 2 and 3 are courses offered by the College of Engineering.",
        "Even if all of them are taken, at most 3 credits are recognised as major credits.",
        "The limit is stated as applying from 2017."],
       ["교과목에 대하여 모두 수강하더라도 최대 3학점까지만 전공학점으로 인정됨", "공학도의 도전과 리더십 1,2,3", "공과대학 개설 교과목인",
        "공학도의 도전과 리더십 이수학점 제한 규정 (2017년부터)"],
       ALL),
    ug("na-ug-computing-exemption", "credit_rules", "Exemption from the computing course", "Area minimum counts as met; the total still applies",
       ["A student exempted, through a separate procedure, from the courses 컴퓨터의 기초, 컴퓨터의 개념 및 실습 is recognised as having completed the minimum credits of the area 학문의 기초 (컴퓨터와 정보 활용), even without earning those credits.",
        "The minimum total of liberal education credits must still be met.",
        "The document does not describe the procedure."],
       ["※ 별도의 절차를 통해 ‘컴퓨터의 기초, 컴퓨터의 개념 및 실습’ 교과목을 면제 받은 경우 학문의 기초(컴퓨터와 정보 활용)에서 이수학점을 충족하지 못하더라도 학문의 기초(컴퓨터와 정보 활용) 최저이수학점을 이수한 것으로 인정함. 단 전체 교양최저이수학점은 충족시켜야 함"],
       OLD),

    # ---- totals
    ug("na-ug-total", "finish_coursework", "Credits required to graduate", "130 credits; 63 in the major (48 with another major)",
       ["Graduation credits (졸업학점): 130.",
        "Liberal education credits (교양학점): 49.",
        "Major credits (주전공학점): 63 with a single major (단일전공이수); 48 when another major is taken alongside (타전공병행이수: minor, double major, linked major).",
        "The document states no grade-average requirement and does not say how the remaining credits are filled. See the university regulations or ask the department office."],
       [TABLE_HEAD, "2025~2026 130 49 63 48", "학번별 졸업이수학점 기준표"],
       NEW, why="These are the figures of the row 2025~2026 in the table of graduation credits by year of admission."),
    ug("na-ug-total-b", "finish_coursework", "Credits required to graduate", "130 credits; 66 in the major",
       ["In the table row 2021~2024: graduation credits (졸업학점) 130; liberal education credits (교양학점) 53.",
        "Major credits (주전공학점): the table prints one pair of figures, in cells shared by the rows 2020 and 2021~2024: 66 with a single major (단일전공이수), 45 when another major is taken alongside (타전공병행이수: minor, double major, linked major).",
        "The section for these years of admission also states 66 or more major credits.",
        "The document states no grade-average requirement and does not say how the remaining credits are filled.",
        "See the university regulations or ask the department office."],
       [TABLE_HEAD, "2020 130 51 66 45 2021~2024 130 53", "학번별 졸업이수학점 기준표", "전공 교과목 총 66학점 이상 이수하여야 함"],
       OLD),

    # ---- other conditions to graduate
    ug("na-ug-foreign-taught", "for_degree", "Courses taught in a foreign language", "At least 3 courses, including at least 1 major course",
       ["Take 3 or more courses taught in a foreign language (외국어진행강좌), including 1 or more major course.",
        "College English (대학영어) is excluded.",
        "The document states this as an obligation for students admitted from 2012."],
       ["2012학년도 신입생부터 1과목 이상의 전공교과목을 포함하여 3과목 이상의 외국어진행강좌를 수강하여야 함 (대학영어제외)", "외국어 진행 강좌 학생 수강 의무"],
       ALL),
    ug("na-ug-life-respect", "for_degree", "Life-respect (suicide prevention) education", "Certificate copy due when applying to graduate",
       ["The College of Engineering's life-respect (suicide prevention) education has been compulsory since 2016.",
        "When applying for graduation, submit a copy of the certificate of completion to the department.",
        "A student who has not completed it cannot graduate.",
        "To apply: College of Engineering website (http://eng.snu.ac.kr/) > 온라인 > 예약 및 신청 > 생명존중(자살예방) 교육 신청."],
       ["2016학년도부터 서울대학교 공과대학 생명존중(자살예방) 교육이 의무화 되어, 졸업 신청 시 생명존중(자살예방) 교육 이수 수료증 사본을 학과(부)에 제출하여야 함 (미이수 시 졸업 불가)",
        "신청방법: 공과대학 홈페이지(http://eng.snu.ac.kr/) >‘온라인’클릭 > 예약 및 신청 > ‘생명존중(자살예방) 교육 신청’ 클릭",
        "생명존중(자살예방) 교육 실시 안내 (2016년부터)"],
       ALL, when="The certificate copy is handed in with the graduation application."),
    ug("na-ug-thesis-courses", "for_degree", "Bachelor's thesis research courses", "Two year-4 courses, not marked as required",
       ["The standard form lists M1513.002200 조선해양 학사논문연구 1 and M1513.002300 조선해양 학사논문연구 2 (bachelor's thesis research) in year 4.",
        "Neither carries the * that marks a required major course.",
        "This document does not say whether a graduation thesis is required in order to graduate. " + ASK],
       ["M1513.002200 조선해양 학사논문연구 1 (1-1-0) M1513.002300 조선해양 학사논문연구 2 (2-2-0)", "4 M1513.002100 친환경선박추진시스템", STAR],
       ALL),
    card("na-ug-thesis-application", ["undergraduate"], "for_degree", "ug-graduation", "Applying for the bachelor's thesis", "At least 2 semesters before you graduate",
         ["Apply for the bachelor's thesis while at least 2 semesters remain before your graduation.",
          "The document's example: to graduate in February 2021, apply in the 1st semester of 2020 at the latest; applying in the 2nd semester of 2020 is not allowed.",
          "If this is not kept, your graduation may be delayed."],
         ["○ 학부 졸업 논문 신청은 본인의 졸업 잔여 학기가 최소 2개 학기 이전에 해야 합니다.",
          "(예, 2021년 2월 졸업 => 늦어도 2020년 1학기 신청해야 함. 2020년 2학기에 신청하는 것은 불허)", "* 이 사항이 지켜지지 않을 경우 졸업시기가 늦춰질 수 있음."],
         "", entry_years=ALL),
    card("na-ug-thesis-advisor", ["undergraduate"], "for_degree", "ug-graduation", "Advisor for the bachelor's thesis", "Your preference counts, but you may be assigned",
         ["When the thesis advisor is chosen, your preference is taken into account as far as possible.",
          "If students' applications are concentrated, you may be assigned an advisor other than the one you asked for."],
         ["○ 지도 교수 선정 시 학생의 희망을 최대한 고려하되, 학생들의 신청 결과가 편중될 경우 본인의 희망과 달리 강제 배정될 수 있습니다."],
         "", entry_years=ALL),
]

if __name__ == "__main__":
    verify(CARDS, TEXTS)
    print(len(CARDS), "undergraduate cards verified")
