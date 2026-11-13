# -*- coding: utf-8 -*-
"""Requirement cards for Naval Architecture and Ocean Engineering's graduate programs, written by hand from the
department's own rule document, "조선해양공학과 대학원 졸업 규정" (18 pages). Download both versions from
https://naoe.snu.ac.kr/graduate/rule into sources/NAVAL/ first: the current one ("2026.09.01", comprehensive
examination subjects revised) and the one before it ("2025.09.01").

    .venv/bin/python tools/cards_naval.py     checks every card and writes data/NAVAL/cards.json

The document has one section for each program (master's on PDF pages 3 to 6, PhD on 7 to 10, integrated MS-PhD on
11 to 14) and never says that the PhD rules cover integrated students. So a card is shown for more than one program
only where the Korean text is the same in each of those sections; it then cites the first section that has it. Where
the numbers differ (credits, registrations, examination attempts, time limits) there is one card for each program.

The two versions differ only in the subjects of the comprehensive examination (종합시험(전공) 과목), and they differ
for all three programs. The current lines say "(2026년 9월 입학생부터 적용)"; the older lines are kept as separate
cards for entrants up to March 2026 and cite "rules-before". Every other card cites "rules".

Left out: the section for Navy (조함병과) commissioned master's students, the blank forms, the table of contents.
The document says nothing on seminars or on how an advisor is chosen. The checks are in tools/cards_pdf.py.
"""
from cards_pdf import ALL, DOCTORAL, card, pages, write

NAME, TEXT = pages("NAVAL", "2026.09.01")
NAME_BEFORE, TEXT_BEFORE = pages("NAVAL", "2025.09.01")

MS, PHD, INT = ["masters"], ["phd"], ["integrated"]
NOW, BEFORE = "Entrants from September 2026", "Entrants before September 2026 (the newer rule applies from September 2026 entrants)"
FROM_2021 = "Entrants from the 1st semester of 2021"
FROM_2022 = "New students from 2022"
FROM_2022_2 = "Entrants from the 2nd semester of 2022"
FROM_2023_2 = "New students from the 2nd semester of 2023"

THESIS_RESEARCH = "- 취득한도 내에서 반복 수강할 수 있으나 한 학기에 2개강좌 이상 수강할 수 없음"
CARRIED_NOT_IN_GPA = "- 통산 인정 학점은 이수 학점에는 포함되나 평점 평균에는 포함되지 않음"
HALF_BASIS = "- 1/2범위 산정시, 과정별 수료학점에서 논문연구학점을 제외한 잔여 학점을 기준으로 하는 것을 원칙으로 함."
HALF_RULE = ("- 지도교수의 추천에 의하여 학과장이 인정하는‘공과대학 및 자연과학대학’타 개설학과(부)의 대학원과정 교과목을 이수할 경우 "
             "과정별 수료학점의 1/2범위 내에서 전공과목으로 인정할 수 있고, 수료학점으로 인정(‘타학과과목 이수 승인신청서’ 제출)")
HALF_RULE_INT = ("- 지도교수의 추천에 의하여 학과(부)장이 인정하는‘공과대학 및 자연과학대학’타 개설학과(부)의 대학원과정 교과목을 이수할 경우 "
                 "과정별 수료학점의 1/2범위 내에서 전공과목으로 인정할 수 있고, 수료학점으로 인정(‘타학과과목 이수 승인신청서’ 제출)")
HALF_LINES = ["Graduate courses of other departments of the College of Engineering and the College of Natural Sciences, recommended by your advisor and "
              "recognised by the department head, can count as major courses and as completion credits, within 1/2 of the completion credits of your program.",
              "In principle the 1/2 is taken after thesis research credits are removed: (completion credits − thesis research credits actually taken) × 1/2.",
              "Submit the form 타학과과목 이수 승인신청서."]
ETHICS_LINES = ["Complete 1 of these courses: 연구윤리의 이해 (M2480.000100, 1 credit), 공학연구윤리 및 논문작성법 (M1570.000300, 2 credits) or 연구윤리 (990.501A, 3 credits).",
                "It is recognised as an other-major course (타전공 인정); submit the form 타학과과목 이수 승인신청서.",
                "A course whose classification is 공통 also counts as a common competency course (공통역량과목)."]
ETHICS_QUOTES = ["○ 대학원 과정 연구윤리 교과목 필수 이수",
                 "- 2023학년도 2학기 신입생부터 적용, 타전공 인정(‘타학과과목 이수 승인신청서’ 제출)",
                 "- M2480.000100 연구윤리의 이해 (1학점) 또는 M1570.000300 공학연구윤리 및 논문작성법 (2학점) 또는 990.501A 연구윤리(3학점) 중 1과목 필수 이수",
                 "- 교과 구분이‘공통’인 과목은 아래의 ‘공통역량과목’에도 해당됨"]
COMPETENCY_QUOTES = ["○ 공과대학 ‘공통역량과목’ 이수학점 수료학점에 포함", "2022학년도 신입생부터 적용, 타전공 인정(‘타학과과목 이수 승인신청서’ 제출)"]
TRAINED = "- ‘환경안전신규교육’,‘생명존중 (자살예방) 교육’ 이수자"
FIVE_NUMBERED = "- 5개 교과목: 1) 414.556 선박설계자동화특강 2) 414.561 선체구조설계특강 3) 414.552 선박생산공학특강 4) 414.562 해양공학설계특강 5) 414.557 선박유체역학특강"
FIVE_PLAIN = "- 5개 교과목: 1) 선박설계자동화특강 2) 선체구조설계특강 3) 선박생산공학특강 4) 해양공학설계특강 5) 선박유체역학특강"
FIVE_LINE = "The 5 subjects: 선박설계자동화특강 (414.556), 선체구조설계특강 (414.561), 선박생산공학특강 (414.552), 해양공학설계특강 (414.562), 선박유체역학특강 (414.557)."
OWN_MASTERS = "2) 본학과 석사과정을 졸업하고 본학과 박사과정에 입학한 자는‘선박유체역학특강’과목을 기합격한 것으로 간주하며, 이를 제외한 1개 과목의 시험 합격시 논문제출자격시험에 합격한 것으로 함"
NOT_COUNTED = "- 병역의무이행 기간 및 임신/출산/육아 기간은 이에 산입하지 않음."
EXTENSION = "- 단, 논문 제출 기한의 연장을 신청하는 경우는 소속 대학(원)장이 대학원 학사 위원회의 심의를 거쳐 2년의 범위내에서 승인할 수 있음"
DEADLINE_LINES = ["Periods of military service and of pregnancy, childbirth or childcare are not counted.",
                  "If you apply for an extension, the dean of your college or graduate school (대학(원)장) can approve up to 2 more years after review by the graduate academic affairs committee (대학원 학사 위원회)."]

CARDS = [
    # ---- credits, registrations, grades
    card("na-registration-ms", MS, "finish_coursework", "rules", "Registered semesters (master's)", "At least 4 registrations, at most 8",
         ["Register at least 4 times and at most 8 times (등록 횟수)."],
         ["□ 등록 횟수 : 최소 4회 이상 최대 8회 까지"], ""),
    card("na-registration-phd", PHD, "finish_coursework", "rules", "Registered semesters (PhD)", "At least 4 registrations, at most 12",
         ["Register at least 4 times and at most 12 times (등록 횟수)."],
         ["□ 등록 횟수 : 최소 4회 이상 최대 12회 까지"], ""),
    card("na-registration-integrated", INT, "finish_coursework", "rules", "Registered semesters (integrated)", "At least 6 registrations, at most 16",
         ["Register at least 6 times and at most 16 times (등록 횟수).", "The document adds that the regular semesters are 8 (정규학기는 8학기임)."],
         ["□ 등록 횟수 : 최소 6회 이상 최대 16회 까지(단, 정규학기는 8학기임)"], ""),
    card("na-credits-ms", MS, "finish_coursework", "rules", "Coursework credits (master's)", "At least 24 credits; thesis research counts up to 6",
         ["Earn at least 24 credits.", "Thesis research (대학원 논문연구) is recognised up to 6 credits.",
          "It can be taken again within that limit, but you cannot take 2 or more thesis research courses in one semester.",
          "Navy-commissioned master's students of the shipbuilding branch (해군 조함병과 위탁생) follow a separate section of the rules."],
         ["□ 이수학점: 24학점 이상", "○ 대학원 논문연구: 최대 6학점까지 인정", THESIS_RESEARCH, "□ 해당 규정은 해군‘조함병과’석사과정 위탁생의 규정이며"], ""),
    card("na-credits-phd", PHD, "finish_coursework", "rules", "Coursework credits (PhD)", "At least 36 credits; thesis research counts up to 12",
         ["Earn at least 36 credits.", "Thesis research (대학원 논문연구) is recognised up to 12 credits.",
          "It can be taken again within that limit, but you cannot take 2 or more thesis research courses in one semester."],
         ["□ 취득학점: 36학점 이상", "○ 대학원 논문연구: 최대 12학점까지 인정", THESIS_RESEARCH], ""),
    card("na-credits-integrated", INT, "finish_coursework", "rules", "Coursework credits (integrated)", "At least 60 credits; thesis research counts up to 18",
         ["Earn at least 60 credits.", "Thesis research (대학원 논문연구) is recognised up to 18 credits.",
          "It can be taken again within that limit, but you cannot take 2 or more thesis research courses in one semester.",
          "Exception for integrated-program students: up to 2 courses, if your advisor approves."],
         ["□ 취득학점: 60학점 이상", "○ 대학원 논문연구: 최대 18학점까지 인정", THESIS_RESEARCH, "(단, 석박통합과정생은 지도교수의 인정에 따라 2개 강좌까지 이수할 수 있음)"], ""),
    card("na-grades", ALL, "finish_coursework", "rules", "Grade point average", "3.0 or higher, over all courses and over major courses",
         ["The grade point average of all your courses and the grade point average of your major courses (전공 평점) must be 3.0 or higher."],
         ["□ 성적: 전 교과목 성적의 평점 평균 및 전공 평점 3.0 이상"], ""),
    card("na-status-integrated", INT, "finish_coursework", "rules", "Recognition as a PhD student (integrated)", "From the 4th semester, after 3 semesters and 24 credits",
         ["A student who has completed 3 or more semesters and earned 24 or more credits is recognised as a PhD student from the 4th semester.",
          "Certificates about your student record are then issued as 'enrolled in the PhD program'."],
         ["○ 3개 학기 이상을 이수하고, 24학점 이상을 취득한 학생은 4학기 때부터 박사과정으로 인정하며, 학적 관련 제 증명 등을 발급할 때는 박사과정 재학 중으로 발급됨"], ""),

    # ---- what counts
    card("na-carried-bachelor", ["masters", "integrated"], "credit_rules", "rules", "Graduate courses taken during an SNU bachelor's degree", "Up to 6 credits can be carried over, on application",
         ["On application, up to 6 credits are recognised (학-석사간 교과 학점 통산 인정).",
          "Only graduate courses of the same or a similar major, taken in an SNU bachelor's program beyond the credits needed to graduate, with a grade of B0 or higher.",
          "The recognised credits count as earned credits but are not included in the grade point average."],
         ["○ 학-석사간 교과 학점 통산 인정 신청: 최대 6학점까지 인정",
          "- 본교 학사과정에서 졸업학점을 초과하여 이수한 동일·유사전공 대학원 과목 중 성적이 B0 이상인 과목에 한하여 신청 가능", CARRIED_NOT_IN_GPA], ""),
    card("na-carried-masters", PHD, "credit_rules", "rules", "Graduate courses taken during an SNU master's degree", "Up to 12 credits can be carried over, on application",
         ["On application, up to 12 credits are recognised (석-박사과정 간 교과 학점 통산 인정).",
          "Only graduate courses of the same or a similar major, taken in an SNU master's program beyond the credits required for completion, with a grade of B0 or higher.",
          "The recognised credits count as earned credits but are not included in the grade point average."],
         ["○ 석-박사과정 간 교과 학점 통산 인정 신청: 최대 12학점까지 인정",
          "- 본교 석사과정에서 수료기준학점을 초과하여 이수한 동일·유사전공 대학원 과목 중 성적이 B0이상인 과목에 한하여 신청 가능", CARRIED_NOT_IN_GPA], ""),
    card("na-undergraduate-courses", ALL, "credit_rules", "rules", "Undergraduate courses", "Up to 6 credits in total, with approval",
         ["Undergraduate courses approved by your advisor count as completion credits up to 6 credits, counted over the master's and PhD programs together.",
          "They are recognised as other-major credits (타전공 인정); submit the form 학부과목 이수 승인신청서.",
          "Only courses of the same or a similar major count. General and liberal-education courses (일반·교양과목) are excluded.",
          "The university rule printed on the form asks for the approval of your advisor and of the department head or the major's chair."],
         ["○ 대학원 과정의 학생이 학사과정 교과목을 이수하고자 할 경우, 지도교수의 승인을 받은 학부 교과목은 석사, 박사 통산 6학점까지 수료학점으로 인정",
          "- 타전공 인정(‘학부과목 이수 승인신청서’ 제출)", "- 동일·유사 전공과목에 한하며, 일반·교양과목은 제외",
          "전공주임 교수의 승인을 받아 학점을 취득할 수 있으며, 대학원과정 통산하여 6학점 이내에서 과정수료"], ""),
    card("na-other-department-ms", MS, "credit_rules", "rules", "Courses of other departments (master's)", "At most half of the credits left after thesis research",
         HALF_LINES + ["The document's examples for 24 completion credits: with 6 thesis research credits, up to 9 other-major credits and at least 9 own-major credits; "
                       "with 3 thesis research credits, 10.5 and at least 10.5."],
         [HALF_RULE, HALF_BASIS, "* 타전공 수업 인정 범위: (과정별 수료학점 – 실제 이수한 논문연구학점) × 1/2", "석사 수료 24학점",
          "원전공 9학점 이상", "타전공 9학점", "논문연구 6학점 이수할 경우", "원전공 10.5학점 이상", "타전공 10.5학점", "논문연구 3학점 이수할 경우", "○ 타전공교과목 이수범위"],
         "", applies_from=FROM_2021),
    card("na-other-department-phd", PHD, "credit_rules", "rules", "Courses of other departments (PhD)", "At most half of the credits left after thesis research",
         HALF_LINES + ["The document's examples for 36 completion credits: with 12 thesis research credits, up to 12 other-major credits and at least 12 own-major credits; "
                       "with 6 thesis research credits, 15 and at least 15."],
         ["- 타전공 수업 인정 범위: (과정별 수료학점 – 실제 이수한 논문연구학점) × 1/2", HALF_RULE, HALF_BASIS, "박사 수료 36학점",
          "원전공 12학점 이상", "타전공 12학점", "논문연구 12학점 이수할 경우", "원전공 15학점 이상", "타전공 15학점", "논문연구 6학점 이수할 경우", "○ 타전공교과목 이수범위"],
         "", applies_from=FROM_2021),
    card("na-other-department-integrated", INT, "credit_rules", "rules", "Courses of other departments (integrated)", "At most half of the credits left after thesis research",
         HALF_LINES + ["The document's examples for 60 completion credits: with 18 thesis research credits, up to 21 other-major credits and at least 21 own-major credits; "
                       "with 12 thesis research credits, 24 and at least 24."],
         [HALF_RULE_INT, HALF_BASIS, "- 타전공 수업 인정 범위: (과정별 수료학점 – 실제 이수한 논문연구학점) × 1/2", "석박통합 수료 60학점",
          "원전공 21학점 이상", "타전공 21학점", "논문연구 18학점 이수할 경우", "원전공 24학점 이상", "타전공 24학점", "논문연구 12학점 이수할 경우", "○ 타전공교과목 이수범위"],
         "", applies_from=FROM_2021),
    card("na-interdisciplinary-courses", ALL, "credit_rules", "rules", "Smart Ocean Mobility interdisciplinary major courses (융합전공)",
         "S/U-graded M3507. courses may not count toward completion",
         ["Courses opened for this interdisciplinary major with the code 414. or M1513. count as credits of your own major (원전공), whether or not you have entered the interdisciplinary major.",
          "Courses with the code M3507. that are graded A/F also count as own-major credits.",
          "For a student who has entered the interdisciplinary major, M3507. courses graded S/U count as completion credits of the interdisciplinary major.",
          "For a student of this department who has not entered it, or who entered and gave it up, M3507. courses graded S/U are not own-major credits and are not included in completion credits.",
          "That exclusion applies from those entering in the 2nd semester of 2023 (2023년 2학기 진입생). A student who took such a course in the 1st semester of 2023 or earlier "
          "gets other-major credit for it, included in completion credits."],
         ["○ 스마트오션모빌리티 융합전공 교과목 관련 수료학점 인정여부",
          "과목코드: 414. 또는 M1513. - 일반과정 기준 원전공 학점으로 인정",
          "과목코드: M3507. - A/F 학점으로 분류되는 과목: 일반과정기준 원전공 학점으로 인정 - S/U 학점으로 분류되는 과목: 융합전공 수료 학점으로 인정",
          "- S/U 학점으로 분류되는 과목: (조선해양공학과) 일반과정 기준 원전공 학점으로 인정하지 않으며, 수료학점 미포함***",
          "*** 융합전공에 진입하지 않거나 진입 후 중도 포기한 조선해양공학과 학생의 경우 M3507. 교과목 중 S/U학점 분류 과목에 대한 원전공 학점 미인정은 2023년 2학기 진입생부터 적용하며, "
          "2023년 1학기 혹은 그 이전에 M3507. 교과목 중 S/U학점 분류 교과목을 수강한 학생은 융합전공 진입하지 않았거나 중도 포기한 경우에도 타전공 학점으로 인정(수료학점 포함).",
          "* 일반과정: 석사, 박사, 석박통합과정"], ""),
    card("na-common-competency", ["masters", "phd"], "credit_rules", "rules", "College of Engineering common competency courses (공통역량과목)",
         "Count toward completion up to 3 credits; not in the major average",
         ["Credits from the College of Engineering's common competency courses (공통역량과목) are included in completion credits, up to 3 credits.",
          "They are not reflected in the major grade point average.",
          "They are recognised as other-major courses (타전공 인정); submit the form 타학과과목 이수 승인신청서."],
         COMPETENCY_QUOTES + ["최대 3학점까지 인정(수료학점으로는 인정되나 전공평점에 반영되지 않음)"], "", applies_from=FROM_2022),
    card("na-common-competency-integrated", INT, "credit_rules", "rules", "College of Engineering common competency courses (공통역량과목)",
         "Count toward completion up to 6 credits; not in the major average",
         ["Credits from the College of Engineering's common competency courses (공통역량과목) are included in completion credits, up to 6 credits.",
          "They are not reflected in the major grade point average.",
          "They are recognised as other-major courses (타전공 인정); submit the form 타학과과목 이수 승인신청서."],
         ["○ 최대 6학점까지 인정(수료학점으로는 인정되나 전공평점에 반영되지 않음)"] + COMPETENCY_QUOTES, "", applies_from=FROM_2022),

    # ---- to begin early
    card("na-research-ethics", ["masters", "integrated"], "start_early", "rules", "Research ethics course", "1 of 3 named courses is required",
         ETHICS_LINES, ETHICS_QUOTES, "", applies_from=FROM_2023_2),
    card("na-research-ethics-phd", PHD, "start_early", "rules", "Research ethics course (PhD)", "1 of 3 named courses, unless taken in an SNU master's program",
         ETHICS_LINES + ["If you completed a research ethics course in an SNU master's program, you do not have to take one again in the PhD program."],
         ["- 본교 대학원 석사과정에서 “연구윤리 교과목”을 이수한 경우, 박사과정에서 중복 이수하지 않아도 됨"] + ETHICS_QUOTES, "", applies_from=FROM_2023_2),
    card("na-mandatory-trainings", ALL, "start_early", "rules", "Two mandatory trainings", "In principle both in your first semester; without them, no qualifying examination",
         ["Completing the environmental safety training for newcomers (환경안전신규교육) and the respect-for-life (suicide prevention) training (생명존중 (자살예방) 교육) "
          "is a condition for sitting the comprehensive examination.",
          "In principle, complete both in your first semester.",
          "If they are not completed, you cannot sit the thesis qualifying examination (the integrated-program section says you cannot apply for it)."],
         [TRAINED, "- 두 개의 필수 교육 모두 첫 번째 학기에 이수하는 것을 원칙으로 함", "- 두 개의 필수교육 미이수의 경우 논문제출자격시험 응시 불가",
          "- 두 개의 필수교육 미이수의 경우 논문제출자격시험 신청 불가", "○ 종합시험(전공) 응시 자격:"], "", when="In your first semester, in principle."),
    card("na-publication-ms", MS, "start_early", "rules", "Journal paper or conference presentation (master's)", "A thesis-related paper or an international oral presentation",
         ["By the day the result of your master's thesis examination is reported, meet at least one of the two conditions below.",
          "Condition 1: a paper related to your thesis, as first author or corresponding author, published in a KCI-listed Korean journal or an SCIE/SCOPUS-listed international journal; "
          "or documents proving that it will be published, submitted to the department office.",
          "Condition 2: an oral presentation, as first author or corresponding author, of a paper related to your thesis at an international conference.",
          "For condition 2 the conference must have presenters from 4 or more countries and 20 or more oral presentations in total, and the 3 examiners must recognise it as an international conference.",
          "For military-commissioned students (군 위탁 교육생), a presentation at a military-related conference is not recognised."],
         ["- 학위 예정자는 석사학위 논문심사 결과보고일까지 다음의 조건 중 하나 이상을 만족",
          "1) 졸업논문과 연관성이 있는 논문을 KCI 등재된 국내 학술 논문지 또는 SCIE/SCOPUS 등재된 국제 학술 논문지에 제1저자 또는 교신저자로 게재하거나, 게재 예정임을 증명할 수 있는 관련 문서를 학과 행정실에 제출한 경우",
          "2) 4개국 이상의 발표자가 참여하고 총 구두 발표 논문이 20건 이상이며, 심사위원 3인이 국제적인 학술대회임을 인정하는 국제 학술대회에서 졸업논문과 연관성이 있는 논문을 제1저자 또는 교신저자로 구두 발표한 경우",
          "○ 2022년도 2학기 입학자부터 적용 (학과 내규)", "※ 군 위탁 교육생의 경우 군 관련 학술대회 발표 실적을 인정하지 않음."], "", applies_from=FROM_2022_2),
    card("na-publication-phd", DOCTORAL, "start_early", "rules", "Journal papers for the doctoral thesis examination", "2 SCIE papers, or 1 paper in a top 25% (Q1) journal",
         ["To have your doctoral thesis examined, meet at least one of the two conditions below while enrolled in the SNU graduate school.",
          "Condition 1: 2 or more papers, as first author or corresponding author, in internationally recognised journals that belong to SCIE.",
          "Condition 2: 1 or more papers, as first author or corresponding author, in an international journal in the top 25% (Q1) of the SJR or JCR classification you choose.",
          "Under either condition the paper is published, or documents proving that it will be published are submitted to the department office by the day of the final examination (종심일).",
          "For Q1 you may choose whether the ranking is judged at the time the paper was submitted or at the time it was accepted."],
         ["- 학과에서 박사학위를 수여받을 예정자(이하 ‘학위예정자’)가 학위논문심사를 받기 위해서는 본교 대학원 재학 중 다음의 조건 중 하나 이상을 만족하여야 한다.",
          "1) SCIE에 속하는 국제적으로 인정되는 학술논문지(이하‘국제논문지’)에 2편 이상의 논문을 제1저자 또는 교신저자로 게재하거나, 게재 예정임을 증명할 수 있는 관련 문서를 종심일까지 학과 행정실에 제출한 경우",
          "2) 학위예정자가 선택한 SJR 혹은 JCR 기준 분류에서 상위 25%(Q1)에 해당하는 국제 논문지에 1편 이상의 논문을 제1저자 또는 교신저자로 게재하거나, 게재 예정임을 증명할 수 있는 관련 문서를 종심일까지 학과 행정실에 제출한 경우.",
          "이때 상위 25%(Q1)를 판정하는 시기는 논문의 투고 시점 혹은 게재 승인 시점 중 학위예정자가 선택할 수 있다.",
          "○ 2022년도 2학기 입학자부터 추가반영 사항 (학과 내규)"], "", applies_from=FROM_2022_2),

    # ---- thesis qualifying examination
    card("na-qualifying-examination", ALL, "before_exam", "rules", "Thesis qualifying examination (논문제출자격시험)", "Two parts: comprehensive (major) and foreign language",
         ["Pass both the comprehensive examination in the major (종합시험(전공)) and the foreign language examination (English or Korean).",
          "The document gives March or September for the thesis qualifying examination."],
         ["□ 논문 제출 자격 시험(3월 또는 9월)", "○ 종합시험(전공) 및 외국어시험(영어 또는 한국어)에 합격"], "", when="March or September."),
    card("na-comprehensive-attempts-ms", MS, "before_exam", "rules", "Comprehensive examination: eligibility and attempts (master's)", "Registered for 2 or more semesters; repeat sittings limited to 2",
         ["Eligible: students registered for 2 or more semesters who have completed the two mandatory trainings.",
          "Repeated sitting of the comprehensive examination (major) is allowed only up to 2 times after entry (반복 응시는 입학 후 2회까지만 허용).",
          "The document does not say whether the first sitting is counted in the 2; its next line is about failing 2 times."],
         ["- 2개 학기 이상 등록자", "1) 종합시험(전공)의 반복 응시는 입학 후 2회까지만 허용함.", TRAINED, "○ 종합시험(전공) 응시 자격:",
          "2) 종합시험(전공)에서 2회 불합격하는 경우"], ""),
    card("na-engineering-mathematics-ms", MS, "before_exam", "rules", "Engineering mathematics examination as a substitute (master's)",
         "After 2 failures: 60 of 100, or 50 for international students",
         ["If you fail the comprehensive examination (major) 2 times, it can be replaced by the engineering mathematics (공학수학) examination, at your advisor's request and by a decision of the department.",
          "That examination is held 2 times a year.",
          "Score needed: 60 or higher out of 100. For international students (외국인) and students commissioned by the military: 50 or higher.",
          "You can apply for the engineering mathematics examination at most 2 times."],
         ["2) 종합시험(전공)에서 2회 불합격하는 경우 지도교수의 요청과 학과 의결을 통해 1년 2회 실시하는 공학수학 시험에 응시하여 100점 만점 중 60점 (군교육 위탁생 및 외국인의 경우 50점) 이상 "
          "취득하는 것으로 대체할 수 있으며, 공학수학 시험은 최대 2회까지 지원할 수 있음"], ""),
    card("na-qualifying-attempts-phd", PHD, "before_exam", "rules", "Thesis qualifying examination: eligibility and attempts (PhD)", "Registered for 4 or more semesters; repeat sittings limited to 3",
         ["Eligible for the comprehensive examination: students registered for 4 or more semesters who have completed the two mandatory trainings.",
          "You can apply for the thesis qualifying examination after registering for 4 or more semesters since entry and completing the required courses of the field you will sit (응시 분야의 필수 교과목).",
          "Repeated sitting of the thesis qualifying examination is allowed only up to 3 times (반복 응시는 3회까지만 허용).",
          "The document does not say whether the first sitting is counted in the 3, and it does not list required courses by field."],
         ["- 4개 학기 이상 등록자", "1) 논문제출자격시험의 반복 응시는 3회까지만 허용함",
          "3) 논문제출자격시험은 입학 후 4개 학기 이상을 등록하고 응시 분야의 필수 교과목을 이수한 후 신청할 수 있음", TRAINED, "○ 종합시험(전공) 응시 자격:"], ""),
    card("na-qualifying-attempts-integrated", INT, "before_exam", "rules", "Thesis qualifying examination: eligibility and attempts (integrated)", "Registered for 4 or more semesters; repeat sittings limited to 3",
         ["Eligible for the comprehensive examination: students registered for 4 or more semesters who have completed the two mandatory trainings.",
          "You can apply for the thesis qualifying examination after registering for 4 or more semesters since entry and completing the required courses of the field you will sit (응시 분야의 필수 교과목).",
          "Repeated sitting of the thesis qualifying examination (논자시) is allowed only up to 3 times (반복 응시는 3회까지만 허용).",
          "The document does not say whether the first sitting is counted in the 3, and it does not list required courses by field."],
         ["1) 논자시의 반복 응시는 3회까지만 허용함", "- 4개 학기 이상 등록자",
          "2) 논문제출자격시험은 입학 후 4개 학기 이상을 등록하고 응시 분야의 필수 교과목을 이수한 후 신청할 수 있음", TRAINED, "○ 종합시험(전공) 응시 자격:"], ""),

    # ---- comprehensive examination subjects: the current rule and the one before it, for each program
    card("na-comprehensive-subjects-ms", MS, "before_exam", "rules", "Comprehensive examination subjects (master's)", "1 of 5 subjects; 70 of 100 to pass",
         ["Sit 1 of the 5 subjects and score 70 or higher out of 100 in it to pass.", FIVE_LINE,
          "In addition, 선박유체역학특강 is a required course (필수 이수 과목).",
          "The document does not say whether that only means taking the course, or also sitting it in the examination."],
         ["○ 종합시험(전공) 과목:‘5개 교과목 중 1개 과목을 응시하여 각 과목별 100점 만점 중 70점 이상의 성적을 받아야 합격으로 인정함. 단, 선박유체역학특강은 필수 이수 과목으로 함. (2026년 9월 입학생부터 적용)",
          "- 5개 교과목: 1) 선박설계자동화특강(414.556) 2) 선체구조설계특강(414.561) 3) 선박생산공학특강(414.552) 4) 해양공학설계특강(414.562) 5) 선박유체역학특강(414.557)"],
         "", applies_from=NOW),
    card("na-comprehensive-subjects-ms-before", MS, "before_exam", "rules-before", "Comprehensive examination subject (master's)", "One examination on 선박유체역학특강 (414.557); 70 of 100 to pass",
         ["The examination is set from what is taught in the course 선박유체역학특강 (414.557).", "Score 70 or higher out of 100 to pass."],
         ["○ 종합시험(전공) 과목:‘414.557 선박유체역학특강’교과목 강의 범위에서 출제되는 시험에서 100점 만점 중 70점 이상의 성적을 받아야 합격으로 인정함."],
         "", applies_from=BEFORE),
    card("na-comprehensive-subjects-phd", PHD, "before_exam", "rules", "Comprehensive examination subjects (PhD)", "2 of 5 subjects; 70 of 100 in each",
         ["Sit 2 of the 5 subjects and score 70 or higher out of 100 in each to pass.", FIVE_LINE,
          "If you passed the written test in 선박유체역학특강 in this department's master's thesis qualifying examination and then entered this department's PhD program, "
          "that subject counts as already passed, and passing 1 other subject passes the thesis qualifying examination.",
          "If you did not complete this department's 선박유체역학특강 during your master's program, you must complete it (필수 이수과목).",
          "A separate line of the same section says that anyone who graduated from this department's master's program and entered its PhD program is treated as having passed "
          "선박유체역학특강. The document does not say how the two lines fit together."],
         ["○ 종합시험(전공) 과목: 5개 교과목 중 2개 과목을 응시하여 각 과목별 100점 만점 중 70점 이상의 성적을 받아야 합격으로 인정함. 단, 본 학과 석사 논문제출자격시험의‘선박유체역학특강’지필 시험을 합격하고 "
          "본 학과 박사과정에 입학한 자는‘선박유체역학특강’과목을 기합격한 것으로 간주하며, 이를 제외한 1개 과목의 시험 합격 시 논문제출자격시험에 합격한 것으로 함. "
          "석사과정 때 본 학과의 선박유체역학특강을 이수하지 않은 학생은 필수 이수과목으로 함 (2026년 9월 입학생부터 적용)",
          FIVE_NUMBERED, OWN_MASTERS], "", applies_from=NOW),
    card("na-comprehensive-subjects-phd-before", PHD, "before_exam", "rules-before", "Comprehensive examination subjects (PhD)", "2 of 5 subjects; 70 of 100 in each",
         ["Sit 2 of the 5 subjects of the thesis qualifying examination and score 70 or higher out of 100 in each to pass.", FIVE_LINE,
          "If you graduated from this department's master's program and entered its PhD program, 선박유체역학특강 counts as already passed, "
          "and passing 1 other subject passes the thesis qualifying examination."],
         ["○ 종합시험(전공) 과목: 논문제출자격시험 5개 교과목 중 2개 과목을 응시하여 각 과목별 100점 만점 중 70점 이상의 성적을 받아야 합격으로 인정함.", FIVE_NUMBERED, OWN_MASTERS],
         "", applies_from=BEFORE),
    card("na-comprehensive-subjects-integrated", INT, "before_exam", "rules", "Comprehensive examination subjects (integrated)", "2 of 5 subjects; 70 of 100 in each",
         ["Sit 2 of the 5 subjects and score 70 or higher out of 100 in each to pass.", FIVE_LINE,
          "In addition, 선박유체역학특강 is a required course (필수 이수 과목).",
          "The document does not say whether that only means taking the course, or also sitting it in the examination.",
          "The integrated-program section lists the subjects without course numbers; the numbers are from the list in the PhD section."],
         ["○ 종합시험(전공) 과목: 석박통합과정: 5개 교과목 중 2개 과목을 응시하여 각 과목별 100점 만점 중 70점 이상의 성적을 받아야 합격으로 인정함. 단, 선박유체역학특강은 필수 이수 과목으로 함(2026년 9월 입학생부터 적용)",
          FIVE_PLAIN, FIVE_NUMBERED], "", applies_from=NOW),
    card("na-comprehensive-subjects-integrated-before", INT, "before_exam", "rules-before", "Comprehensive examination subjects (integrated)", "2 of 5 subjects, 선박유체역학특강 among them; 70 of 100 in each",
         ["Sit 2 of the 5 subjects of the thesis qualifying examination and score 70 or higher out of 100 in each to pass.",
          "For the integrated program, the 2 subjects must include 선박유체역학특강.", FIVE_LINE,
          "The integrated-program section lists the subjects without course numbers; the numbers are from the list in the PhD section."],
         ["- 석박통합과정의 경우, 2개 응시 분야 중 “선박유체역학특강”을 반드시 포함해야 함",
          "○ 종합시험(전공) 과목: 논문제출자격시험 5개 교과목 중 2개 과목을 응시하여 각 과목별 100점 만점 중 70점 이상의 성적을 받아야 합격으로 인정함.", FIVE_PLAIN, FIVE_NUMBERED],
         "", applies_from=BEFORE),

    # ---- foreign language examination
    card("na-language-international", ALL, "before_exam", "rules", "Foreign language examination for international students", "English or Korean; Korean if English is native or official",
         ["Pass an examination in English or in Korean.", "International graduate students (외국인 대학원생) choose one of the two.",
          "A student whose native language or official language is English chooses Korean."],
         ["2) 외국인 대학원생: 영어/한국어 중 택1(단, 영어가 모국어, 공용어인 학생은 한국어 선택)", "○ 외국어시험: 영어 또는 한국어 시험에 합격하여야 함"], ""),
    card("na-korean-course-exemption", ALL, "before_exam", "rules", "Korean course in place of the Korean examination", "Grade S in 한국어와 한국문화 1 or 2 can exempt you",
         ["If you take 한국어와 한국문화 1 (990.804) or 한국어와 한국문화 2 (990.805) and earn the grade S, you can be exempted from the Korean subject of the thesis qualifying examination.",
          "The course is not included in completion credits.",
          "Taking it in the same semester in which you submit the thesis is not accepted (논문제출학기 동시 수강 인정 안됨).",
          "The line ends with 석사/박사 각각 이수: completed separately for the master's and for the PhD."],
         ["3)“한국어와 한국문화 1(990.804)” 또는 “한국어와 한국문화 2(990.805)” 교과목을 수강하여 ‘S’를 취득하였을 경우, 석박사학위 논문제출자격시험의 한국어과목을 면제받을 수 있음"
          "(수료학점 미포함, 논문제출학기 동시 수강 인정 안됨) 석사/박사 각각 이수)"],
         "", trap="A course taken in the semester in which you submit the thesis is not accepted."),
    card("na-english-score", ALL, "before_exam", "rules", "English score for the thesis qualifying examination", "NEW TEPS 327 (student numbers from 2005); TOEFL iBT 86 or 96 by year of entry",
         ["The document describes the English route under 'Korean graduate students' (한국인 대학원생): since the 1st semester of 2006 the score recognised at admission through the general admission track (대학원 일반전형) stands in place of the examination.",
          "Those not already treated as passed must take NEW TEPS or TOEFL and reach the standard score set by the College of Engineering before submitting the thesis examination documents, "
          "and submit the score to the department.",
          "On the day of submission the test date must be within the validity period of 2 years.",
          "Standard for student numbers from 2005 (2005학번 이후), master's and PhD alike: 327 on the revised TEPS (total 600), which is 601 on the former TEPS (total 990).",
          "The TOEFL iBT score for that standard: 86 for entrants up to 2022, 96 for entrants from 2023.",
          "The document does not say whether an international student who chooses English follows this same route."],
         ["1) 한국인 대학원생: 외국어 시험(영어)은 2006학년도 1학기부터 자격인정제도로 대체(대학원 일반전형 입학시 인정받은 성적으로 대체)하여 시행하고 있는 바 대상자(기 합격처리 인정을 받지 못한 자)는 "
          "반드시 학위논문심사서류 제출 전까지 NEW TEPS 또는 TOEFL에 응시하여 공과대학에서 정한 기준점수 이상을 취득하고, 그 성적을 소속 학과(부)에 제출하여야 함"
          "(제출일자 기준 응시일자가 유효기간 2년을 경과하지 않아야 함)",
          "논문제출자격 영어과목 (TEPS) 기준 점수", "2005학번 이후", "기존 TEPS (총점990점) 501점 550점 601점", "개정 TEPS (총점600점) 268점 296점 327점",
          "TOEFL(iBT) 2022년 입학생 까지 2023년 입학생 이후 601 327 86 96"], ""),
    card("na-english-score-notes", ALL, "before_exam", "rules", "English scores: accepted TOEFL forms and special cases", "Home Edition and MyBest Scores are accepted",
         ["TOEFL iBT Special Home Edition and MyBest Scores are accepted.",
          "For MyBest Scores, the earliest test date among the 4 sections must still be within the validity period (2 years) on the day of submission.",
          "PhD entrants from 2023: an English score that SNU officially recognised for you earlier (at graduate admission or in a thesis qualifying examination, as a master's graduate) is not enough by itself. "
          "A score from a test other than TEPS (TOEFL and others) must meet the new conversion standard for entrants from 2023.",
          "Students with a hearing impairment: 196 on the revised TEPS or 371 on the former TEPS, as the sum of the sections other than listening."],
         ["※ TOEFL iBT Special Home Edition 및 MyBest Scores 성적을 인정하며, MyBest Scores는 제출일 기준 4개 평가 영역 중 가장 이른 영역의 시행일자가 유효기간(2년 이내)을 경과하지 않아야 함.",
          "※ 본교에서 공식적으로 인정받은 성적(“본교 대학원 입학 시 또는 논문제출자격시험에서 인정받은” 석사 학위자의 영어성적)의 경우에도 2023년도 이후 박사 입학생은 타 영어시험(TOEFL 등)의 기준점수가 신규 환산기준을 충족해야 함.",
          "※ 청각장애학생 기준 점수", "기존 TEPS 371점 371점 청해영역을 제외한 나머지 영역의 합 개정 TEPS 196점 196점"], ""),

    # ---- thesis examination and submission
    card("na-thesis-application", ALL, "for_degree", "rules", "Application for the thesis examination", "April or October, after passing the qualifying examination",
         ["Students who have passed the thesis qualifying examination apply for the thesis examination. The document gives April or October for the application."],
         ["□ 학위논문 심사: 논문제출자격시험 합격자 중 학위논문심사 신청(4월 또는 10월)"], "", when="April or October."),
    card("na-preliminary-review-ms", MS, "for_degree", "rules", "Preliminary review of the master's thesis (학위논문 사전심사)", "Thesis plan and review form to 3 examiners before you apply",
         ["Before applying for the thesis examination in March or early September (3월 또는 9월 초), give 1 copy each of the master's thesis plan (석사학위 논문계획서) "
          "and the preliminary review form (석사 학위 논문 사전심사서) to the 3 examiners.",
          "Submit the approved preliminary review form when you register as a prospective thesis submitter in the semester in which you plan to graduate (April or October).",
          "At the public presentation the form is passed to the examiners and taken into account in the examination."],
         ["- 학위논문 심사 신청 전(3월 또는 9월 초)에 “석사학위 논문계획서” 및 “석사 학위 논문 사전심사서”를 각 1부씩 심사위원 3인에게 제출하고, 승인받은 “석사 학위논문 사전심사서”를 "
          "졸업 예정 학기 논문 제출 예정자 등록 시 제출 (4월 또는 10월)",
          "- 논문 공개발표 시 사전심사서를 심사위원에게 같이 전달하여 심사에 반영", "○ 학위논문 사전심사"], ""),
    card("na-thesis-examination-ms", MS, "for_degree", "rules", "Public presentation and thesis grade (master's)", "Presentation 2.5 of 5; thesis grade B; oral examination 60",
         ["The public presentation of the thesis is held in June or December.",
          "Before the day of the presentation submit 3 copies of the preliminary review form (석사학위 논문 사전 심사서), 1 research activity sheet (연구활동표) and 1 copy of the presentation material.",
          "The public presentation is passed with an examiners' score of 2.5 or higher out of 5.",
          "The thesis grade must be B or higher and the oral examination 60 or higher to pass.",
          "You must also pass every other step set by the examination committee appointed by the dean of the college or graduate school (대학(원)장)."],
         ["- 6월 또는 12월 논문 공개발표를 실시하며, 다음의 자료를 논문 공개발표일 전에 제출하여야 함.(석사학위 논문 사전 심사서 3부, 연구활동표 1부, 발표자료 1부)",
          "- 공개발표는 심사위원 심사점수 5점 만점에 2.5점 이상을 합격으로 함", "○ 논문성적 및 구술고사 성적: 논문성적 B 이상에 구술고사 60점 이상을 합격으로 함",
          "○ 이 밖의 대학(원)장이 위촉한 심사위원회에서 정한 모든 심사 과정에 통과하여야 함", "○ 논문 공개발표"], "", when="June or December."),
    card("na-thesis-examination-phd", DOCTORAL, "for_degree", "rules", "Doctoral thesis presentation and examination", "1 presentation, 2 preliminary examinations, final average of 70",
         ["Hold a thesis presentation at least 1 time, and have the preliminary thesis examination at least 2 times.",
          "Final thesis examination (종심) and oral examination: an average of 70 or higher.",
          "As a department rule, the public presentation is in principle held at the 1st or the 2nd session of the doctoral thesis examination (1심과 2심 중에); "
          "the document does not say which of the two.",
          "You must also pass every other step set by the examination committee appointed by the dean of the college or graduate school (대학(원)장)."],
         ["- 논문 발표회 1회 이상 개최, 논문 예비 심사 2회 이상 실시", "- 논문 종심 및 구술고사: 평균 70점 이상",
          "- 공개발표는 박사논문 심사 중 1심과 2심 중에 실시함을 원칙으로 함 (학과 내규)", "- 이 밖의 대학(원)장이 위촉한 심사위원회에서 정한 모든 심사 과정에 통과하여야 함",
          "○ 박사학위 논문발표 및 논문 (예비) 심사"], ""),
    card("na-thesis-deadline-ms", MS, "for_degree", "rules", "Time limit for submitting the thesis (master's)", "Within 4 years of completing coursework",
         ["Submit the thesis within 4 years after completing the coursework of the program (과정 수료)."] + DEADLINE_LINES,
         ["□ 학위논문 제출 허용기한: 과정 수료 후 4년 이내", NOT_COUNTED, EXTENSION], ""),
    card("na-thesis-deadline-phd", DOCTORAL, "for_degree", "rules", "Time limit for submitting the thesis (PhD and integrated)", "Within 6 years of completing coursework",
         ["Submit the thesis within 6 years after completing the coursework of the program (과정 수료)."] + DEADLINE_LINES,
         ["□ 학위논문 제출 허용기한: 과정 수료 후 6년 이내", NOT_COUNTED, EXTENSION], ""),
    card("na-withdrawal-integrated", INT, "for_degree", "rules", "Giving up the integrated program", "Withdrawal form by the halfway point (2/4선) of the 3rd semester",
         ["If you submit the form for giving up the integrated program (석박사통합과정 포기원) by the halfway point of the 3rd semester (3학기 수업연한 2/4선 내; the document gives no date), you can graduate from the master's program.",
          "The document does not explain this term or give a date."],
         ["○ 석박사통합과정 포기: 3학기 수업연한 2/4선 내에 석박사통합과정 포기원을 제출하면 석사과정으로 졸업 가능"], ""),
]

if __name__ == "__main__":
    write("NAVAL", CARDS, {"rules": TEXT, "rules-before": TEXT_BEFORE})
