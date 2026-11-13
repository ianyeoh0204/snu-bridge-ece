# -*- coding: utf-8 -*-
"""Undergraduate requirement cards for the Department of Nuclear Engineering (원자핵공학과), written by hand from the
department's own one-page guide, "<원자핵공학과 전공 및 교양 교과과정 이수 안내>", one PDF per year of admission:
"2023학번 적용", "2024학번 적용" and "2025학번 적용". Download the three files from
https://nucleng.snu.ac.kr/undergraduate/rule into sources/NUCLEAR/ first.

    cd tools && ../.venv/bin/python cards_nuclear_undergraduate.py     checks every card; writes nothing

Years covered: entrants of 2023, 2024 and 2025. The department has not published a guide for 2026 entrants, so 2026 is
NOT covered and no card lists it.

Each guide is a course table (year 1 to 4, two semesters) with a notes column, and a summary box of credits beneath it.
What the guides do not contain: any grade-average requirement, any limit on credits per semester, rules for double
majors or minors, prerequisites, anything specific to international students, and any rule on submitting a graduation
thesis (only the two thesis-research courses are listed). They also do not print the 2025 split of the 62 major
credits into required and elective. The table's year and semester of each course is layout only (loose digits in the
extracted text), so no card says in which semester a course falls, except the writing courses, which a note places
in words ("[1-1]", "[1-2]").

Because each year has its own document, `verify` looks for every quote of a card in the document of EVERY year in
that card's `entry_years`. A rule that reads the same in all three guides is one card; where a line differs, there is
one card per variant (ids ending -b, -c). Course names stay in Korean with their course numbers: the guides give no
English names. The checks are in tools/cards_pdf.py.
"""
from cards_pdf import card, pages, verify

NAME_2023, TEXT_2023 = pages("NUCLEAR", "(2023학번)")
NAME_2024, TEXT_2024 = pages("NUCLEAR", "(2024학번)")
NAME_2025, TEXT_2025 = pages("NUCLEAR", "(2025학번)")
TEXTS = {"ug-2023": TEXT_2023, "ug-2024": TEXT_2024, "ug-2025": TEXT_2025}

U = ["undergraduate"]
ALL_YEARS = [2023, 2024, 2025]

# The science rows of the course table read the same in all three guides (spaces aside).
SCIENCE_ROWS = ["물리학1(또는 고급물리학1) (3)", "물리학 실험1 (1)", "물리학2(또는 고급물리학2) (3)", "물리학 실험2 (1)",
                "화학1 (3)/생물학1 (3)", "화학 실험1 (1)/생물학실험1 (1)", "화학2 / 생물학2 / 통계학 (3)", "화학실험2 / 생물학실험2 / 통계학실험 (1)"]
SCIENCE_LINES = ["Physics: 물리학 1 or 고급물리학 1 (3 credits) with 물리학실험 1 (1 credit), and 물리학 2 or 고급물리학 2 (3) with 물리학실험 2 (1).",
                 "Chemistry or biology: 화학 1 or 생물학 1 (3) with 화학실험 1 or 생물학실험 1 (1).",
                 "Then 화학 2, 생물학 2 or 통계학 (statistics) (3) with 화학실험 2, 생물학실험 2 or 통계학실험 (1)."]

CARDS = [
    # ---- first year
    card("ne-ug-writing", U, "start_early", "ug", "College writing courses", "대학 글쓰기 1 at [1-1], 대학 글쓰기 2 at [1-2]; 4 credits in total",
         ["The guide's note reads: [1-1] 대학 글쓰기 1 (College Writing 1), [1-2] 대학 글쓰기 2: 과학기술 글쓰기 (College Writing 2: Science and Technology Writing), 4 credits in total.",
          "Each of the two courses is 2 credits in the course table.",
          "The guide does not explain [1-1] and [1-2]. They are read here as year 1, semester 1 and year 1, semester 2."],
         ["[1-1] 대학 글쓰기 1, [1-2] 대학 글쓰기 2: 과학기술 글쓰기 총 4학점", "대학 글쓰기 1 (2)²", "대학 글쓰기 2: 과학기술 글쓰기 (2)²"],
         "", entry_years=ALL_YEARS),

    # ---- liberal education (교양)
    card("ne-ug-ge-total", U, "general_education", "ug", "Liberal-education credits", "53 credits: 학문의 기초 41 and 학문의 세계 12",
         ["Required liberal-education (교양필수) courses: 53 credits.",
          "학문의 기초 (foundations of scholarship): 41 credits.",
          "학문의 세계 (worlds of knowledge): 12 credits, from at least 3 of these 5 areas: 언어와 문학 (language and literature), 문화와 예술 (culture and arts), 역사와 철학 (history and philosophy), 정치와 경제 (politics and economy), 인간과 사회 (humans and society).",
          "The guide says the area rule applies from 2020 entrants."],
         ["교양필수 교과목 [53학점", "1. 학문의기초 …………  41", "2. 학문의 세계 ……..  12",
          "5개영역 (언어와 문학, 문화와 예술, 역사와 철학, 정치와 경제, 인간과 사회)중 3개 영역 이상에서 12학점 이수 - 2020학번부터"],
         "", entry_years=[2023]),
    card("ne-ug-ge-total-b", U, "general_education", "ug", "Liberal-education credits", "53 credits: 학문의 기초 41 and 학문의 세계 12",
         ["Required liberal-education (교양필수) courses: 53 credits.",
          "학문의 기초 (foundations of scholarship): 41 credits.",
          "학문의 세계 (worlds of knowledge): 12 credits, from at least 4 of these 5 areas: 언어와 문학 (language and literature), 문화와 예술 (culture and arts), 역사와 철학 (history and philosophy), 정치와 경제 (politics and economy), 인간과 사회 (humans and society).",
          "The guide says the area rule applies from 2024 entrants."],
         ["교양필수 교과목 [53학점]", "1. 학문의 기초 ………… 41", "2. 학문의 세계 ………… 12",
          "5개 영역(언어와 문학, 문화와 예술, 역사와 철학, 정치와 경제, 인간과 사회) 중 4개 영역 이상에서 12학점 이수 - 2024학번부터"],
         "", entry_years=[2024]),
    card("ne-ug-ge-total-c", U, "general_education", "ug", "Liberal-education credits", "53 credits: 학문의 토대 41, 지성의 열쇠 9, 베리타스 3",
         ["Required liberal-education (교양필수) courses: 53 credits.",
          "학문의 토대 (foundations of scholarship): 41 credits.",
          "지성의 열쇠 (keys of intellect): 9 credits in total, 3 credits from each of 3 areas: 문화 해석과 상상 (interpreting culture and imagination), 역사적 탐구와 철학적 사유 (historical inquiry and philosophical thought), 인간의 이해와 사회 분석 (understanding humans and analysing society).",
          "베리타스 (Veritas): 3 credits from its 3 areas, 베리타스 강좌 1, 베리타스 강좌 2 and 베리타스 실천. The course table words this slot as 베리타스 강좌 1 or 2 or 실천.",
          "The guide says both area rules apply from 2025 entrants."],
         ["교양필수 교과목 [53학점]", "1. 학문의 토대 ………… 41", "2. 지성의 열쇠 ………… 9",
          "- 3개 영역(문화 해석과 상상, 역사적 탐구와 철학적 사유, 인간의 이해와 사회 분석) 에서 각 3학점씩 총 9학점 이수 - 2025학번부터",
          "3. 베리타스 ………..…… 3", "- 3개 영역(베리타스 강좌 1, 2, 베리타스 실천) 에서 3학점 이수 - 2025학번부터", "베리타스 강좌1 또는 2 또는 실천"],
         "", entry_years=[2025]),
    card("ne-ug-ge-foundation", U, "general_education", "ug", "학문의 기초 (foundations of scholarship) courses", "41 credits: languages, mathematics, science, computing, writing",
         ["학문의 기초: 41 credits.",
          "Foreign language: 2 courses, or 고급영어 (Advanced English); the guide does not explain this 'or'.",
          "수학 및 연습 1 and 2 (Mathematics and Practice 1, 2), or 고급수학 및 연습 1 and 2 (Advanced Mathematics and Practice 1, 2).",
          "010.140 공학수학 1 and 010.141 공학수학 2 (Engineering Mathematics 1, 2), and 010.133 컴퓨터의 개념 및 실습; 3 credits each.",
          "과학적 사고와 실험 (scientific thinking and experiments) courses: 16 credits, with the lab taken in the same semester.",
          "대학 글쓰기 1 and 대학 글쓰기 2: 과학기술 글쓰기 (College Writing 1 and 2)."],
         ["1. 학문의 기초 ………… 41", "- 외국어 2개 교과목 or 고급영어, 수학및연습 1ㆍ2 or 고급수학및연습1ㆍ2,", "공학수학 1ㆍ2, 컴퓨터의개념 및 실습(3),",
          "과학적사고와실험과목(16)/해당학기에 실험 동시수강", "- 대학 글쓰기 1, 대학 글쓰기 2: 과학기술 글쓰기",
          "010.140 공학수학1 (3)²", "010.141 공학수학2 (3)²", "010.133 컴퓨터의 개념 및 실습 (3)²"],
         "", entry_years=[2023, 2024]),
    card("ne-ug-ge-foundation-b", U, "general_education", "ug", "학문의 토대 (foundations of scholarship) courses", "41 credits: writing 4, languages 6, maths 12, science 16, computing 3",
         ["학문의 토대: 41 credits.",
          "Writing and speaking area (글쓰기와 말하기): 대학 글쓰기 1 and 대학 글쓰기 2: 과학기술글쓰기 (College Writing 1 and 2), 4 credits.",
          "Foreign-language area: 2 foreign-language courses, 6 credits.",
          "Mathematics, 12 credits: 수학 및 연습 1 and 2 or 고급수학 및 연습 1 and 2, with the practice class (연습교과목) taken in the same semester, and 010.140 공학수학 1 and 010.141 공학수학 2.",
          "Science: 16 credits.",
          "Computing: 010.133 컴퓨터의 개념 및 실습, 3 credits."],
         ["1. 학문의 토대 ………… 41", "- 글쓰기와 말하기 영역: 대학 글쓰기 1, 대학 글쓰기 2: 과학기술글쓰기 (4학점)", "- 외국어 영역: 외국어 2개 교과목 (6학점)",
          "수학 및 연습 1ㆍ2 or 고급수학 및 연습 1ㆍ2 (동일학기에 연습교과목과 동시수강) / 공학수학 1ㆍ2 (수학 12학점)", "(과학 16학점)",
          "컴퓨터의 개념 및 실습 (컴퓨팅 3학점)", "010.140 공학수학 1 (3)²", "010.141 공학수학 2 (3)²", "010.133 컴퓨터의 개념 및 실습 (3)²"],
         "", entry_years=[2025]),
    card("ne-ug-science", U, "general_education", "ug", "Science courses and their labs", "16 credits, labs included; lab in the same semester as its course",
         ["과학적 사고와 실험 (scientific thinking and experiments) courses: 16 credits, labs included.",
          "Take the lab at the same time, in the same semester."] + SCIENCE_LINES,
         ["과학적사고와실험 16학점", "이수(실험포함)", "과학적사고와실험과목(16)/해당학기에 실험 동시수강"] + SCIENCE_ROWS,
         "", entry_years=[2023, 2024]),
    card("ne-ug-science-b", U, "general_education", "ug", "Science courses and their labs", "16 credits, labs included; lab in the same semester as its course",
         ["Science area: 16 credits, labs included.",
          "Take the lab course (실험교과목) at the same time, in the same semester.",
          "The summary names 물리학 및 실험 1 and 2, 화학 및 실험 1 and 2, 생물학 및 실험 1 and 2, and 통계학 및 실험, without saying which combination makes up the 16 credits; the course table lays it out as follows."]
         + SCIENCE_LINES,
         ["과학영역 16학점(실험 포함)", "(과학 16학점)", "물리학 및 실험 1ㆍ2 / 화학 및 실험 1ㆍ2  (동일학기에 실험교과목과 동시수강)",
          "생물학 및 실험 1ㆍ2 / 통계학 및 실험 (동일학기에 실험교과목과 동시수강)"] + SCIENCE_ROWS,
         "", entry_years=[2025]),
    card("ne-ug-foreign-language", U, "general_education", "ug", "Foreign-language courses", "2 courses; 1 English course if TEPS at admission was 900 or below",
         ["Complete 2 foreign-language courses.",
          "A student whose TEPS score at admission was 900 or below must complete 1 English course."],
         ["¹ 외국어 2개 교과목 이수 (입학 시 TEPS 900점 이하인 학생은 영어 1과목 필수 이수)"],
         "", trap="The guide writes only 'TEPS 900' and does not say which TEPS scale it means.", entry_years=ALL_YEARS),
    card("ne-ug-engineering-ge", U, "general_education", "ug", "College of Engineering required liberal-education courses (공대필수교양)", "Rows marked ² in the course table",
         ["The mark ² in the course table means a College of Engineering required liberal-education course (공대필수교양).",
          "Named courses that carry it: 010.133 컴퓨터의 개념 및 실습 (3 credits), 010.140 공학수학 1 (3), 010.141 공학수학 2 (3), 대학 글쓰기 1 (2) and 대학 글쓰기 2: 과학기술 글쓰기 (2)."],
         ["²  공대필수교양", "010.133 컴퓨터의 개념 및 실습 (3)²", "010.140 공학수학1 (3)²", "010.141 공학수학2 (3)²", "대학 글쓰기 1 (2)²", "대학 글쓰기 2: 과학기술 글쓰기 (2)²"],
         "", entry_years=ALL_YEARS),

    # ---- major (전공)
    card("ne-ug-major-total", U, "major_courses", "ug", "Major credits", "62 credits: 34 required and 28 elective",
         ["Major courses: 62 credits.",
          "Required major courses (전필): 34 credits.",
          "Elective major courses (전선): 28 credits."],
         ["전필34 + 전선28 = 전공62"],
         "", entry_years=[2023, 2024]),
    card("ne-ug-major-total-b", U, "major_courses", "ug", "Major credits", "62 credits; every required major course must be taken",
         ["Major courses: 62 credits, required (전필) plus elective (전선).",
          "All required major courses must be taken.",
          "This year's guide does not print how the 62 credits divide between required and elective."],
         ["전공 [62학점] (전필 + 전선)", "- 전필은 모두 수강해야함"],
         "", entry_years=[2025]),
    card("ne-ug-major-required", U, "major_courses", "ug", "Required major courses", "Courses marked * in the course table; 34 credits stated",
         ["Courses marked * in the course table are required major courses (전공필수교과목).",
          "409.201 핵공학개론 1, 409.202 핵공학개론 2, 409.214 공학물리기초, 409.209A 플라즈마전자역학 1 (3 credits each).",
          "409.223 핵공학기초실험, M1509.000900A 원자력열유체공학, M1509.000200 핵공학현대물리 (3 credits each).",
          "409.301A 원자로이론, 409.307A 플라즈마기초, M1509.001000 방사선 물리와 방호 (3 credits each).",
          "409.328 원자핵공학세미나 1 (1 credit).",
          "The guide states 34 required credits, but the courses it marks with * carry fewer; the two thesis-research courses are listed without the mark (see the card on them)."],
         ["*  전공필수교과목", "409.201* 핵공학개론1 (3)", "409.202* 핵공학개론2 (3)", "409.214* 공학물리기초 (3)", "409.209A* 플라즈마전자역학1 (3)",
          "409.223* 핵공학기초실험 (3)", "M1509.000900A* 원자력열유체공학 (3)", "M1509.000200* 핵공학현대물리 (3)",
          "409.301A* 원자로이론 (3)", "409.307A* 플라즈마기초 (3)", "M1509.001000* 방사선 물리와 방호 (3)", "409.328* 원자핵공학세미나1 (1)",
          "전필34 + 전선28 = 전공62"],
         "", entry_years=[2023]),
    card("ne-ug-major-required-b", U, "major_courses", "ug", "Required major courses", "Courses marked * in the course table; 34 credits",
         ["Courses marked * in the course table are required major courses (전공필수교과목); the guide states 34 required credits.",
          "409.201 핵공학개론 1, 409.202 핵공학개론 2, 409.214 공학물리 기초, 409.209A 플라즈마전자역학 1 (3 credits each).",
          "409.223 핵공학기초실험, M1509.000200 핵공학 현대물리, M1509.000900A 원자력열유체공학 (3 credits each).",
          "409.301A 원자로이론, 409.307A 플라즈마기초, M1509.001000 방사선 물리와 방호 (3 credits each).",
          "409.328 원자핵공학세미나 1 (1 credit).",
          "M1509.000500 원자핵공학 학사논문연구 1 (2 credits) and M1509.000600 원자핵공학 학사논문연구 2 (1 credit)."],
         ["* 전공필수교과목", "409.201* 핵공학개론 1 (3)", "409.202* 핵공학개론 2 (3)", "409.214* 공학물리 기초 (3)", "409.209A* 플라즈마전자역학 1 (3)",
          "409.223* 핵공학기초실험 (3)", "M1509.000200* 핵공학 현대물리 (3)", "M1509.000900A* 원자력열유체공학 (3)",
          "409.301A* 원자로이론 (3)", "409.307A* 플라즈마기초 (3)", "M1509.001000* 방사선 물리와 방호 (3)", "409.328* 원자핵공학세미나1 (1)",
          "M1509.000500* 원자핵공학 학사논문연구 1 (2)", "M1509.000600* 원자핵공학 학사논문연구 2 (1)", "전필34 + 전선28 = 전공62"],
         "", entry_years=[2024]),
    card("ne-ug-major-required-c", U, "major_courses", "ug", "Required major courses", "Courses marked * in the course table; all must be taken",
         ["Courses marked * in the course table are required major courses (전공필수교과목), and all of them must be taken.",
          "409.201 핵공학개론 1, 409.202 핵공학개론 2, M1509.001800 핵공학 물리 기초, 409.209A 플라즈마전자역학 1 (3 credits each).",
          "409.223 핵공학기초실험, M1509.000900 원자력열유체공학 (3 credits each).",
          "409.301A 원자로이론, 409.307A 플라즈마기초, M1509.001000 방사선 물리와 방호 (3 credits each).",
          "409.328 원자핵공학세미나 1 (1 credit).",
          "M1509.000500 원자핵공학 학사논문연구 1 (2 credits) and M1509.000600 원자핵공학 학사논문연구 2 (1 credit)."],
         ["* 전공필수교과목", "- 전필은 모두 수강해야함", "409.201* 핵공학개론 1 (3)", "409.202* 핵공학개론 2 (3)", "M1509.001800* 핵공학 물리 기초 (3)",
          "409.209A* 플라즈마전자역학 1 (3)", "409.223* 핵공학기초실험 (3)", "M1509.000900* 원자력열유체공학 (3)",
          "409.301A* 원자로이론 (3)", "409.307A* 플라즈마기초 (3)", "M1509.001000* 방사선 물리와 방호 (3)", "409.328* 원자핵공학세미나1 (1)",
          "M1509.000500* 원자핵공학 학사논문연구 1 (2)", "M1509.000600* 원자핵공학 학사논문연구 2 (1)"],
         "", entry_years=[2025]),
    card("ne-ug-lab", U, "major_courses", "ug", "Lab courses (실험교과목)", "9 credits from the guide's list of lab courses",
         ["Lab courses (실험교과목): 9 credits.",
          "The guide's list: 핵공학기초실험, 시스템에너지전달공학, 핵융합플라즈마실험, 원자로열유체실험, 원자력시스템실습, 원자로물리실험, 핵공학시뮬레이션실습.",
          "Their numbers in the course table: 409.223 핵공학기초실험, 409.313A 핵융합플라즈마 실험, M1509.000100 원자로열유체실험, 409.402F 원자력시스템실습, M1509.000400 원자로물리 실험, M1509.001100 핵공학 시뮬레이션 실습 (3 credits each).",
          "시스템에너지전달공학 is on the list but is not in this year's course table, so the guide gives no number for it."],
         ["1. 실험교과목 …….. 9학점", "- 핵공학기초실험,시스템에너지전달공학,핵융합플라즈마실험, 원자로열유체실험, 원자력시스템실습, 원자로물리실험, 핵공학시뮬레이션실습",
          "409.223* 핵공학기초실험 (3)", "409.313A 핵융합플라즈마 실험 (3)", "M1509.000100 원자로열유체실험 (3)", "409.402F 원자력시스템실습 (3)",
          "M1509.000400 원자로물리 실험 (3)", "M1509.001100 핵공학 시뮬레이션 실습 (3)"],
         "", entry_years=[2023]),
    card("ne-ug-lab-b", U, "major_courses", "ug", "Lab courses (실험교과목)", "9 credits: 3 courses required from the guide's list",
         ["Lab courses (실험교과목): 9 credits. 3 courses from the guide's list are required.",
          "The list: 409.223 핵공학기초실험, 409.313A 핵융합 플라즈마 실험, 409.402F 원자력시스템실습, M1509.000100 원자로 열유체 실험, M1509.000400 원자로물리 실험, M1509.001100 핵공학 시뮬레이션 실습, M1509.001700 원자력 재료 실험, 400.018 창의공학설계.",
          "원자력 재료 실험 is a new course; the guide says it applies from the second semester of 2024.",
          "400.018 창의공학설계 is recognised as a lab course only for students who took it from the second semester of 2024 onward."],
         ["1. 실험교과목 ………… 9학점",
          "- 핵공학기초실험, 핵융합 플라즈마 실험, 원자력시스템실습, 원자로 열유체 실험, 원자로물리 실험, 핵공학 시뮬레이션 실습, 원자력 재료 실험, 창의공학설계 ----- 3과목 필수",
          "원자력 재료 실험(신설)은 2024학년도 2학기부터 적용함.", "400.018 창의공학설계는 2024학년도 2학기부터 수강한 학생의 경우만 해당 교과목을 <실험교과목>으로 인정함.",
          "409.223* 핵공학기초실험 (3)", "409.313A 핵융합 플라즈마 실험 (3)", "409.402F 원자력시스템실습 (3)", "M1509.000100 원자로 열유체 실험 (3)",
          "M1509.000400 원자로물리 실험 (3)", "M1509.001100 핵공학 시뮬레이션 실습 (3)", "M1509.001700 원자력 재료 실험 (3)"],
         "", trap="창의공학설계 taken before the second semester of 2024 is not recognised as a lab course.", entry_years=[2024, 2025]),

    # ---- what counts
    card("ne-ug-department-credits", U, "credit_rules", "ug", "Credits from the department's own courses", "At least 48 credits in department-offered courses",
         ["Complete at least 48 credits in courses offered by the department (학과개설교과목).",
          "Courses can also be completed elsewhere in the College of Engineering and in the College of Natural Sciences.",
          "The guide does not list which courses outside the department are accepted."],
         ["학과개설교과목 48학점이상 이수, 기타 공과대학 및 자연과학대학에서도 이수가능"],
         "", entry_years=ALL_YEARS),

    # ---- total
    card("ne-ug-total", U, "finish_coursework", "ug", "Total credits to graduate", "130 credits; 53 of them required liberal education",
         ["130 credits in total.",
          "Required liberal-education (교양필수) courses: 53 credits.",
          "Major credits are on the card 'Major credits'.",
          "This guide states no grade-average requirement and no limit on credits per semester."],
         ["○  총 130학점", "교양필수 교과목 [53학점"],
         "", entry_years=ALL_YEARS),

    # ---- to graduate
    card("ne-ug-thesis", U, "for_degree", "ug", "Bachelor's thesis research courses", "학사논문연구 1 (2 credits) and 2 (1 credit) are required major courses",
         ["M1509.000500 원자핵공학 학사논문연구 1 (2 credits) and M1509.000600 원자핵공학 학사논문연구 2 (1 credit) carry the * that marks required major courses.",
          "The guide says nothing else about a graduation thesis: no rule on submitting it, its form or a deadline."],
         ["M1509.000500* 원자핵공학 학사논문연구 1 (2)", "M1509.000600* 원자핵공학 학사논문연구 2 (1)", "* 전공필수교과목"],
         "", entry_years=[2024, 2025]),
    card("ne-ug-thesis-b", U, "for_degree", "ug", "Bachelor's thesis research courses", "Listed without the * that marks required major courses",
         ["M1509.000500 원자핵공학 학사논문연구 1 (2 credits) and M1509.000600 원자핵공학 학사논문연구 2 (1 credit) are in the course table without the * that marks required major courses.",
          "The guide's text does not say whether these two courses are required; compare the 34 required major credits it states with the marked courses on the card 'Required major courses'.",
          "The guide says nothing else about a graduation thesis: no rule on submitting it, its form or a deadline."],
         ["M1509.000500 원자핵공학 학사논문연구1 (2)", "M1509.000600 원자핵공학 학사논문연구2 (1)", "*  전공필수교과목", "전필34 + 전선28 = 전공62"],
         "", entry_years=[2023]),
    card("ne-ug-foreign-lectures", U, "for_degree", "ug", "Courses taught in a foreign language", "Obligation: 3 courses, including 1 major course",
         ["Stated as an obligation (수강의무): take at least 3 courses taught in a foreign language, including 1 major course.",
          "The guide says this applies from 2008 entrants.",
          "From 2012 entrants, '대학영어' is excluded from the English-taught courses that count."],
         ["※ 외국어진행강좌 수강의무 : 2008학번부터 전공 1과목 포함하여 3과목이상의 외국어 진행강좌 수강", "(2012학번부터 영어강좌에서‘대학영어’제외)"],
         "", entry_years=[2023]),
    card("ne-ug-foreign-lectures-b", U, "for_degree", "ug", "Courses taught in a foreign language", "Recommended: 3 courses, including 1 major course",
         ["Stated as a recommendation (권장), not an obligation: take at least 3 courses taught in a foreign language, including 1 major course.",
          "The guide says the recommendation applies from 2024 entrants.",
          "From 2012 entrants, '대학영어' is excluded from the English-taught courses that count."],
         ["※ 외국어 진행강좌 수강 권장: 2024학번부터 전공 1과목 포함하여 3과목 이상의 외국어 진행강좌 수강 권장", "(2012학번부터 영어강좌에서 ‘대학영어’ 제외)"],
         "", entry_years=[2024, 2025]),
    card("ne-ug-life-respect", U, "for_degree", "ug", "Life-respect (suicide prevention) education", "Compulsory; certificate copy due when applying to graduate",
         ["Life-respect (suicide prevention) education (생명존중(자살예방) 교육) is compulsory for new students of the College of Engineering, undergraduate and graduate, from the 2016 academic year.",
          "When applying for graduation, submit a copy of the certificate of completion (이수증) to the department."],
         ["※ 생명존중(자살예방) 교육: 2016학년도 공과대학 학사과정 및 대학원과정 신입생부터 생명존중(자살예방) 교육 이수가 의무이며, 졸업 신청 시 생명존중(자살예방)교육 이수증 사본을 학과(부)에 제출하여야 함"],
         "", when="The certificate copy is handed in when applying for graduation.", entry_years=ALL_YEARS),
]

if __name__ == "__main__":
    verify(CARDS, TEXTS)
    print(len(CARDS), "undergraduate cards verified")
