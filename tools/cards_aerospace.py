# -*- coding: utf-8 -*-
"""Requirement cards for Aerospace Engineering's graduate programs, entrants from 2021, written by hand from the
department's own web pages (read by tools/pages_aerospace.py).

    .venv/bin/python tools/pages_aerospace.py     first: read the pages
    .venv/bin/python tools/cards_aerospace.py     then: check every card and write data/AEROSPACE/cards.json

No second reader has re-read these cards (the developer's decision, to keep the ChatGPT Edu quota for the demo), and
the site says so. In its place, code refuses to write the file unless, for every card:
  1. each Korean quote is found, word for word, in the tab for entrants from 2021 of the page the card cites
     (the same pages carry the rules for entrants up to 2020, with different numbers);
  2. every number in the card's English title, key fact and rule lines appears in its Korean quotes.
That catches a wrong number and a quote from the wrong rule set. It does not catch a wrong reading of the Korean.
Course names are left in Korean with their course numbers: the department's pages give no English names.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages_aerospace import PAGES, SITE, pane  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALL, DOCTORAL = ["masters", "phd", "integrated"], ["phd", "integrated"]
FORM = "Submit the course approval form (이수승인신청서) to the department office when you register for the course."
OUTSIDE = "Inside this limit, undergraduate-level courses (학사과정 이수학점) count for up to 6 credits, and that 6 is one total across your graduate programs (대학원 과정 통산)."
SUBSTITUTE = "International students may take graduate major courses of the department instead."
RESEARCH = "Register for the thesis research course opened by your own advisor. These credits are not counted as major credits."
OTHER_RULES = "Other rules of the university and the department also apply."
OTHER_KO = "* 기타 서울대 및 학과에서 정한 규정을 만족해야 함."
ONLY_3 = "「발사체 시스템 개론 및 현장실무응용」과 「위성 시스템 개론 및 현장실무응용」은 두 과목 모두 수강하여도 수료사정 시 3학점만 인정됨."


def card(id, programs, group, page, title, key, rule, quotes, why, when="", trap=""):
    return {"id": id, "programs": programs, "group": group, "title": title, "key": key, "rule": rule, "why": why, "when": when,
            "trap": trap, "applies_from": "Entrants from 2021", "events": [], "source_file": page, "source_page": 0,
            "source_page_also": 0, "source_quote_ko": quotes[0], "quotes_ko": quotes, "check": "unchecked", "entry_years": [], "updates": []}


CARDS = [
    # ---- completing coursework: master's
    card("ae-ms-completion", ["masters"], "finish_coursework", "completion", "Completion: registrations, credits and grade average",
         "4 to 8 registrations; 24 credits; 3.0 average",
         ["Registered semesters: at least 4, at most 8.", "Credits: at least 24.", "Grade point average: at least 3.0."],
         [": 등록횟수 4회 이상 8회까지, 24학점 이상, 평점평균 3.0이상"], "These are the main thresholds for completing coursework; the required-course rules also apply."),
    card("ae-ms-thesis-research", ["masters"], "credit_rules", "completion", "Thesis research credits", "At most 6 of the 24 credits",
         ["At most 6 thesis research credits count toward the 24.", RESEARCH],
         ["24학점 이상 취득, 논문연구학점(지도교수가 개설한 과목 신청) 6학점 이내 (논문연구학점은 전공학점으로 미인정)"],
         "Thesis research credits beyond the limit do not help you complete."),
    card("ae-ms-other-department", ["masters"], "credit_rules", "completion", "Courses from other departments", "At most 9 credits, with approval",
         ["Graduate courses of other departments count up to 9 credits, on your advisor's recommendation and with the department head's approval.", OUTSIDE, FORM],
         ["전공지도교수의 추천에 의하여 학과장이 인정하는 타학과(부) 대학원과정 교과목: 9학점 까지(대학원 과정 통산하여 학사과정 이수학점 6학점 포함) 인정. 이 경우 수강 신청 시 “이수승인신청서” 를 학과사무실로 제출."],
         "Credits taken outside the department without approval may not count.", trap="The form is due when you register for the course."),
    card("ae-ms-bachelor-credits", ["masters"], "credit_rules", "completion", "Graduate credits earned as an undergraduate", "Up to 6 credits can be carried over",
         ["Graduate credits earned during a bachelor's program count toward the master's, up to 6 credits.", "Only credits that were not counted toward the bachelor's degree.",
          "Apply when the carry-over notice is posted at the start of a semester: submit the form (학/석사간 교과학점 통산인정신청서) with a transcript to the department office."],
         ["학사 과정에서 취득한 대학원 학점은 학사과정 졸업학점에 포함하지 않은 학점으로 6학점까지 석사과정 수료학점에 포함할 수 있음. 이 경우 학기 초 통산인정 신청 공지 시 \"학/석사간 교과학점 통산인정신청서\"를 작성하여 성적표와 함께 학과사무실로 제출."],
         "It can shorten the coursework, but only if you apply.", when="Start of a semester, when the notice is posted"),
    card("ae-ms-required-courses", ["masters"], "start_early", "completion", "Required courses", "Two required courses; international students may substitute",
         ["Required: 공학연구윤리 및 논문작성법 (M1570.000300, research ethics and thesis writing) and 항공우주 연구방법론 (M3229.000500, aerospace research methodology).", SUBSTITUTE],
         ["「공학연구윤리 및 논문작성법」, 「항공우주 연구방법론」 필수. (단, 외국인학생은 항공우주공학과 대학원 전공과목으로 대체할 수 있다.)",
          "공학연구윤리 및 논문작성법 (M1570.000300)", "항공우주 연구방법론 (M3229.000500)"],
         "Coursework cannot be completed without them, or without the substitute courses."),
    card("ae-ms-seminar", ["masters"], "credit_rules", "completion", "Department graduate seminar", "Recommended; not counted toward completion",
         ["The department's graduate seminar (항공우주산업 최신기술동향, M3229.000400) does not count toward completion credits.", "Taking it is recommended."],
         ["항공우주공학과 대학원 세미나 과목(항공우주산업 최신기술동향 M3229.000400)은 수료학점에 포함되지 아니하나 수강을 권장함."],
         "Do not rely on it to reach 24 credits."),
    card("ae-common-competency", ["masters", "phd"], "credit_rules", "completion", "Graduate common competency courses", "Up to 3 credits, counted as other-department courses",
         ["Graduate common competency courses (대학원 공통역량교과목) count as other-department courses, up to 3 credits."],
         ["대학원 공통역량교과목은 최대 3학점까지 타학과 교과목으로 인정한다.[신설 2021.12.16.]"], "They are recognised as other-department courses, and only up to this many credits."),
    # ---- completing coursework: PhD
    card("ae-phd-completion", ["phd"], "finish_coursework", "completion", "Completion: registrations, credits and grade average",
         "4 to 12 registrations; 36 credits; 3.0 average",
         ["Registered semesters: at least 4, at most 12.", "Credits: at least 36.", "Grade point average: at least 3.0."],
         [": 등록횟수 4회이상 12회까지, 36학점 이상, 평점평균 3.0이상"], "These are the main thresholds for completing coursework; the required-course rules also apply."),
    card("ae-phd-thesis-research", ["phd"], "credit_rules", "completion", "Thesis research credits", "At most 12 of the 36 credits, seminar included",
         ["At most 12 thesis research credits count toward the 36.", "Thesis research and the department's graduate seminar (M3229.000400) together count as thesis research credits, up to 12.", RESEARCH],
         ["36학점 이상 취득, 논문연구학점(지도교수가 개설한 과목 신청) 12학점 이내(논문연구학점은 전공학점으로 미인정)",
          "논문연구, 항공우주공학과 대학원 세미나 과목(항공우주산업 최신기술동향 M3229.000400)은 12학점까지 논문연구학점으로 인정."],
         "Thesis research credits beyond the limit do not help you complete."),
    card("ae-phd-other-department", ["phd"], "credit_rules", "completion", "Courses from other departments", "At most 12 credits, with approval",
         ["Graduate courses of other departments count up to 12 credits, on your advisor's recommendation and with the department head's approval.", OUTSIDE, FORM],
         ["전공지도교수의 추천에 의하여 학과장이 인정하는 타학과(부) 대학원과정 교과목: 12학점 까지(대학원 과정 통산하여 학사과정 이수학점 6학점 포함) 인정. 이 경우 수강 신청 시 “이수승인신청서” 를 학과사무실로 제출."],
         "Credits taken outside the department without approval may not count.", trap="The form is due when you register for the course."),
    card("ae-phd-masters-credits", ["phd"], "credit_rules", "completion", "Credits carried over from a master's program", "Up to 12 credits, grade B0 or higher",
         ["Courses taken in a master's program beyond its 24 credits count toward the PhD, up to 12 credits.", "Only courses with a grade of B0 or higher, from the same or a similar department or major.",
          "Apply when the carry-over notice is posted at the start of a semester: submit the form (석·박사간 교과학점 통산인정신청서) with a transcript to the department office."],
         ["석사 과정에서 24학점을 초과하여 수강한 과목은 학점이 B0 이상인 교과목에 한하여 12학점 까지 박사과정 수료학점으로 인정.(동일 및 유사 학과(부)·전공) 이 경우 학기 초 통산인정 신청 공지 시 \"석·박사간 교과학점 통산인정신청서\"를 작성하여 성적표와 함께 학과사무실로 제출."],
         "It can shorten the coursework, but only if you apply.", when="Start of a semester, when the notice is posted"),
    card("ae-phd-required-courses", ["phd"], "start_early", "completion", "Required courses", "Two required courses; credit for those taken in the master's",
         ["Required: 공학연구윤리 및 논문작성법 (M1570.000300) and 항공우주 연구방법론 (M3229.000500). Each is accepted if already completed in a master's program.",
          SUBSTITUTE + " A substitution accepted in the master's program is accepted again."],
         ["「공학연구윤리 및 논문작성법」(석사과정에서 기 이수한 경우 인정) 및 「항공우주 연구방법론」(석사과정에서 기 이수한 경우 인정) 필수. (단, 외국인학생은 항공우주공학과 대학원 전공과목으로 대체(석사과정에서 항공우주공학과 대학원 전공과목으로 대체 인정받은 경우도 인정)할 수 있다.)",
          "공학연구윤리 및 논문작성법 (M1570.000300)", "항공우주 연구방법론 (M3229.000500)"],
         "Coursework cannot be completed without them, or without the substitute courses."),
    card("ae-phd-repeated-course", ["phd"], "credit_rules", "completion", "A course already taken in the master's program", "Not counted again in the PhD",
         ["A course completed in the master's program and taken again in the PhD program is a duplicate: it does not count toward PhD completion.",
          "It is not treated as a retake either: its grade still enters your credits and your average."],
         ["대학원 석사과정과 박사과정의 교과목은 통합 운영하는 것을 원칙으로 하고 있으며, 석사과정에서 이수한 교과목을 박사과정에서 다시 이수하였을 경우에는 중복이수가 되어 박사과정 수료학점에 포함되지 않으나 재수강 처리는 되지 않고 학점이나 평균에 모두 반영됨."],
         "Master's and PhD courses are run as one list, so a PhD student can register again for a course already taken. It will not count toward completion."),
    # ---- completing coursework: integrated
    card("ae-int-completion", ["integrated"], "finish_coursework", "completion", "Completion: registrations, credits and grade average",
         "6 to 16 registrations; 60 credits; 3.0 average",
         ["Registered semesters: at least 6, at most 16.", "Credits: at least 60.", "Grade point average: at least 3.0."],
         [": 등록횟수 6회이상 16회까지, 60학점 이상, 평점평균 3.0이상"], "These are the main thresholds for completing coursework; the required-course rules also apply."),
    card("ae-int-thesis-research", ["integrated"], "credit_rules", "completion", "Thesis research credits", "At most 18 of the 60 credits, seminar included",
         ["At most 18 thesis research credits count toward the 60.", "Thesis research and the department's graduate seminar (M3229.000400) together count as thesis research credits, up to 18.", RESEARCH],
         ["60학점 이상 취득, 논문연구학점(지도교수가 개설한 과목 신청) 18학점 이내 (논문연구학점은 전공학점으로 미인정)",
          "논문연구, 항공우주공학과 대학원 세미나 과목(항공우주산업 최신기술동향 M3229.000400)은 18학점까지 논문연구학점으로 인정."],
         "Thesis research credits beyond the limit do not help you complete."),
    card("ae-int-other-department", ["integrated"], "credit_rules", "completion", "Courses from other departments", "At most 21 credits, with approval",
         ["Graduate courses of other departments count up to 21 credits, on your advisor's recommendation and with the department head's approval.", OUTSIDE, FORM],
         ["전공지도교수의 추천에 의하여 학과장이 인정하는 타학과(부) 대학원과정 교과목: 21학점 까지(대학원 과정 통산하여 학사과정 이수학점 6학점 포함) 인정. 이 경우 수강 신청 시 “이수승인신청서” 를 학과사무실로 제출."],
         "Credits taken outside the department without approval may not count.", trap="The form is due when you register for the course."),
    card("ae-int-common-competency", ["integrated"], "credit_rules", "completion", "Graduate common competency courses", "Up to 6 credits, counted as other-department courses",
         ["Graduate common competency courses (대학원 공통역량교과목) count as other-department courses, up to 6 credits."],
         ["대학원 공통역량교과목은 최대 6학점까지 타학과 교과목으로 인정한다.[신설 2021.12.16.]"], "They are recognised as other-department courses, and only up to this many credits."),
    card("ae-int-required-courses", ["integrated"], "start_early", "completion", "Required courses", "Two required courses; international students may substitute",
         ["Required: 공학연구윤리 및 논문작성법 (M1570.000300, research ethics and thesis writing) and 항공우주 연구방법론 (M3229.000500, aerospace research methodology).", SUBSTITUTE],
         ["「공학연구윤리 및 논문작성법」 및 「항공우주 연구방법론」 필수. (단, 외국인학생은 항공우주공학과 대학원 전공과목으로 대체할 수 있다.)",
          "공학연구윤리 및 논문작성법 (M1570.000300)", "항공우주 연구방법론 (M3229.000500)"],
         "Coursework cannot be completed without them, or without the substitute courses."),
    # ---- every program
    card("ae-two-system-courses", ALL, "credit_rules", "completion", "Launch vehicle and satellite system courses", "Both taken: only 3 credits count",
         ["If you take both 발사체 시스템 개론 및 현장실무응용 and 위성 시스템 개론 및 현장실무응용, only 3 credits count toward completion."],
         [ONLY_3], "If you take both, only 3 credits in total are recognised toward completion."),
    card("ae-no-duplicate-course", ALL, "credit_rules", "completion", "Taking a course of the same name twice", "Not allowed, with named exceptions",
         ["In each of the bachelor's, master's and PhD programs, a course of the same name must not be taken twice.", "Exceptions are the courses designated separately, such as thesis research (논문연구)."],
         ["교과목을 이수할 때 학·석·박사 각 과정에서는 별도로 지정되어 있는 교과목 (군사학, 논문연구 등) 이외에는 동일 명칭의 과목 (학기 완성 과목과 통년 완성 과목 모두)을 중복 이수하여서는 안 됨."],
         "The document states this as a prohibition."),
    card("ae-subtitled-courses", ALL, "credit_rules", "completion", "Courses with a subtitle (course group Ⅱ)", "A different subtitle counts as a different course, with exceptions",
         ["A graduate course designated as course group Ⅱ counts as a separate course when its subtitle is different, so it is not treated as a duplicate.",
          "First exception: if you take both 발사체 시스템 개론 및 현장실무응용 and 위성 시스템 개론 및 현장실무응용, only 3 credits in total are recognised.",
          "Second exception: among the group-2 courses of the interdisciplinary Space Systems program (협동과정 우주시스템전공, also named 협동과정 지능형우주항공시스템전공), only one course is recognised at completion even when the subtitles differ."],
         ["대학원 과정에서 교과목군 Ⅱ로 지정된 교과목으로서, 부제목이 다를 경우에는 별개의 교과목으로 인정되어 중복 처리되지 아니함. (단, 「발사체 시스템 개론 및 현장실무응용」과 「위성 시스템 개론 및 현장실무응용」은 두 과목 모두 수강하여도 3학점만 인정되며, 협동과정 우주시스템전공(협동과정 지능형우주항공시스템전공) 교과목(2군교과목)은 중복처리됨)",
          "협동과정 우주시스템전공(협동과정 지능형우주항공시스템전공) 교과목 중 2군교과목은 부제 달리하여 수강하여도 수료사정 시 한과목만 인정됨."],
         "A different subtitle normally keeps a group Ⅱ course from being treated as a duplicate."),
    card("ae-semester-limit", ALL, "every_semester", "completion", "Credits per semester", "At most 12 credits a semester",
         ["You cannot register for more than 12 credits in one semester."], ["매학기 수강신청 학점은 12학점을 초과할 수 없음."],
         "It limits how quickly coursework can be finished.", when="Every semester, at course registration"),
    card("ae-english-courses", ALL, "credit_rules", "completion", "English courses for graduate students", "Not counted toward completion",
         ["The English courses for graduate students, 990.664 고급영어학술작문 and 990.666 고급영어학술발표, are not included in completion credits."],
         ["대학원생을 위한 영어교과목 990.664 고급영어학술작문 / 990.666 고급영어학술발표 는 수료학점에 불포함."],
         "They do not move you toward completion."),
    card("ae-average-below", ALL, "finish_coursework", "completion", "Completing with an average below 3.0", "Possible on request, but then no degree",
         ["The average required for completion is 3.0 or higher.", "A student who wishes may still complete without it.",
          "After that, research-student registration is not possible, so a thesis cannot be submitted and graduation is not possible."],
         ["수료 기준 평점 평균은 3.0 이상이나, 학생이 원할 경우 3.0을 만족하지 않아도 수료 가능하며, 이후에는 연구생등록이 불가하여 학위논문을 제출할 수 없으므로 졸업은 가능하지 않음."],
         "Completion and graduation are different things here.", trap="Completing below 3.0 closes the way to the degree."),
    # ---- the thesis qualifying examination
    card("ae-qe-english", ALL, "before_exam", "qualifying", "Qualifying examination: English", "New TEPS 327 or TOEFL iBT 86",
         ["English is met by a score: New TEPS 327 or higher, or TOEFL iBT 86 or higher.", "A score accepted at admission stays valid until graduation.",
          "Without one, submit a score obtained within the last 2 years to the department office before the thesis examination documents are due: end of March in the first semester, end of September in the second.",
          "TOEFL iBT Special Home Edition and MyBest Scores are accepted. For MyBest Scores, on the day you submit, the earliest test date among the 4 sections must still be within the 2-year validity.",
          "You must be registered in a regular semester."],
         ["- 2005학번이후: 327점 이상(개정TEPS), 86점 이상(TOEFL(iBT))", "MyBest Scores는 제출일 기준 4개 평가 영역 중 가장 이른 영역의 시행일자가 유효기간(2년 이내)을 경과하지 않아야 함.",
          "정규학기 등록이 되어 있는 자", "* 기합격여부 확인: 마이스누 → 졸업정보",
          "* 본교 대학원 입학 시 인정받은 영어점수는 졸업 시까지 유효하며, 영어성적이 없는 경우 2년 이내 받은 성적(TEPS 나 TOEFL(iBT))표를 반드시 학위논문심사서류 제출 전(1학기는 3월말, 2학기는 9월말)까지 기준 점수이상을 취득한 성적을 학과사무실에 제출.",
          "* TOEFL iBT Special Home Edition 및 MyBest Scores 성적 인정."],
         "The thesis cannot be examined until both parts of the qualifying examination are passed.", when="Score due by the end of March or the end of September",
         trap="Check whether you are already recorded as passed: mySNU, graduation information (마이스누 → 졸업정보)."),
    card("ae-qe-korean", ALL, "before_exam", "qualifying", "Qualifying examination: Korean, for some international students", "Only if English is your native or official language",
         ["The Korean examination applies only to international students whose native or official language is English.", "Pass mark: 60 for the master's program, 70 for the PhD.",
          "Exempt if you take the Korean course opened as its substitute (한국어와 한국문화 1 or 2) and earn C- or higher, or S. That course does not count toward completion.",
          "Held once at the start of each semester, in March and September.",
          "The page does not say whether Korean replaces the English requirement for these students, and gives no pass mark for the integrated program. Ask the department office."],
         ["영어, 한국어(영어가 모국어 또는 공용어인 외국인만 해당)", "한국어: 석사 60점 이상, 박사 70점 이상 합격",
          "논문제출자격시험의 대체과목으로 개설된 한국어 과목(한국어와 한국문화 1 또는 2)을 수강하고, 그 성적이 “C－이상\" 또는 ”S\"의 성적을 취득한 경우에는 한국어시험을 면제하되, 수료학점에는 포함하지 않음.",
          "시험실시 횟수: 매 학기 초(3월, 9월) 1회 실시 (교무처 주관)"],
         "It applies only to international students whose native or official language is English.", when="Start of each semester (March, September)"),
    card("ae-qe-basic", ["masters"], "before_exam", "qualifying", "Basic examination (master's)", "Before the major examination; late February or late August",
         ["Separate from the major examination, and required before it.", "Held at the end of February and at the end of August.", "Open after at least 1 completed semester.",
          "Written questions on undergraduate and graduate coursework related to your own research."],
         ["* 시행 시기:2월말, 8월말 실시", "* 응시 자격:최소 1개 학기 이수 후", "* 시험 방법:본인 연구내용과 연관된 학부 및 대학원 교과과정에 대한 서술형 문제", "2. 기초시험*(전공시험과 상이)"],
         "The major examination is closed to you until this is passed.", when="End of February, end of August"),
    card("ae-qe-major-ms", ["masters"], "before_exam", "qualifying", "Qualifying examination: major (master's)", "Three courses; 60 points to pass",
         ["Eligible if you have registered for at least 2 semesters, passed the basic examination, and completed the two trainings: laboratory safety (환경안전교육) and life respect (생명존중교육).",
          "Choose 3 graded courses offered by the department, with your advisor's approval.", "The score is calculated from your grades in those courses; 60 or higher passes.",
          "Points by grade: A+ 100, A0 90, A- 80, B+ 70, B0 60, B- 50, C+ 40, C0 30, C- or lower 0.",
          "After failing, 2 more attempts. After 3 failures, only with the approval of your advisor and the department head."],
         ["2개 학기 이상 등록, 기초시험* 통과한 자. 환경안전원의 환경안전교육과 공과대학에서 제공하는 생명존중(자살예방)교육을 이수한 자",
          "항공우주공학과 개설 교과목 중 총 3과목 선택하며, 과목은 성적이 부여되는 과목으로 지도교수의 승인을 받아야 함.", "시험 성적은 선택한 과목에 대한 이수성적으로 산정함.",
          "이수성적별 점수 산정방법: A+(100점),A0(90점),A-(80점),B+(70점),B0(60점),B-(50점),C+(40점),C0(30점),C-이하(0점)", "60점 이상 합격",
          "불합격 시 2회에 한하여 재응시 가능하며, 총 3회 이상 불합격 시 지도교수와 학과장의 승인을 득한 경우에 한해 재응시 가능", "매 학기 초(3월,9월) 1회 실시"],
         "The score comes from your grades in the courses you choose.", when="Start of each semester (March, September)"),
    card("ae-qe-major-phd", DOCTORAL, "before_exam", "qualifying", "Qualifying examination: major (PhD and integrated)", "PhD: 3rd registered semester; integrated: within 4 semesters; 70 to pass",
         ["Eligible if you have registered for at least 2 semesters in the PhD or integrated program and completed the two trainings: laboratory safety (환경안전교육) and life respect (생명존중교육).",
          "PhD students must sit it in their 3rd registered semester. Integrated-program students must sit it at least once within 4 semesters.",
          "Questions test overall understanding of the PhD major courses; 70 or higher passes.", "After failing, 2 more attempts, each in the semester right after the failure.",
          "A 3rd retake is an oral examination, with a presentation of the thesis topic, before a committee of 3 professors that includes the department head and your advisor. Failing it ends the PhD program.",
          "An integrated-program student who meets the master's requirements can then still receive a master's degree."],
         ["박사과정 및 석박사통합과정에서 2개 학기 이상 등록하고 환경안전원의 환경안전교육과 공과대학에서 제공하는 생명존중(자살예방)교육을 이수한 자",
          "박사과정은 등록 3개 학기째에 응시해야하며, 석박사통합과정은 4개학기 이내 최소 한 번은 응시하여야 함.[개정2023.5.1]", "70점 이상 합격", "박사과정 전공과목에 대한 전반적인 이해수준을 평가하는 문제",
          "불합격 시 2회에 한하여 재응시 할 수 있으며, 불합격 다음 학기에 재응시 하여야 함. 3회 재응시 하는 경우는 학과장과 지도교수를 포함한 3인의 교수로 구성된 위원회에서 논문 주제 발표를 포함한 구술고사를 실시하며, 불합격 시 박사학위 과정을 지속할 수 없음. 단, 석박사통합과정 학생은 항공우주공학과 석·박사 학위 취득 규정 제8조에 의거하여 석사학위 수여 요건을 갖추면 석사학위를 취득할 수 있음."],
         "The timing is fixed by rule, and repeated failure ends the program.", trap="PhD students have no choice of semester: it is the 3rd registered semester. Integrated students must have sat it at least once within 4 semesters."),
    # ---- toward the degree
    card("ae-committee", DOCTORAL, "for_degree", "committee", "Doctoral thesis advisory committee", "Within 6 semesters of entry (integrated: 8)",
         ["3 members including your advisor as chair: professors, or experts from academia or research institutes.",
          "Form it within 6 semesters of entering the PhD program (8 for the integrated program), and hold its meeting in that same semester.",
          "It reviews the research plan and sets the schedule of the preliminary and final examinations. If a member is replaced, the same formation procedure applies.", "It is dissolved when the advising result report (논문지도결과보고서) is received. Its members are appointed as members of the thesis examination committee."],
         ["위원회는 위원장인 지도교수를 포함한 3인의 교수 또는 학계, 연구계의 전문가로 구성. 지도위원을 교체하는 경우에도 구성절차에 준함.",
          "논문지도 위원회는 박사과정 입학 후 6학기(석박사통합과정은 입학 후 8학기)이내에 구성하여, 해당 학기 중에 논문지도 위원회 회의를 개최 하여야 함.",
          "학위논문 연구계획의 심사, 학위논문 연구에 관련된 지도, 학위논문 계획변경에 관한 지도와 승인, 향후 초심, 종심 일정 결정 등 기타 필요하다고 인정되는 사항을 심의함.",
          "“논문지도결과보고서”의 접수와 동시에 해산하며, 논문지도위원회 위원은 학위논문 심사위원회 위원으로 위촉됨."],
         "It has its own deadline, counted from the semester you entered."),
    card("ae-thesis-ms", ["masters"], "for_degree", "thesis", "Master's thesis examination", "Documents in April or October; thesis within 4 years",
         ["Eligible with 24 credits earned or to be earned by the end of that semester, both parts of the qualifying examination passed, and registration (research-student registration if coursework is completed).",
          "Documents: April in the first semester, October in the second, on the announced dates.", "Examination: late May to early June, or late November to early December.",
          "The thesis and its presentation are in English, in principle.", "Submit the thesis within 4 years of completing coursework. Military service is not counted. After review by the graduate academic committee, the head of the college or graduate school can extend this by up to 2 years.", OTHER_RULES],
         ["24학점 이상 당해 학기말까지 취득하였거나 취득할 수 있어야 하고, 논자시(외국어+전공) 합격한자, 등록생(수료자인 경우 연구생 등록생)", "1학기는 4월, 2학기는 10월 공고 기간",
          "1학기는 5월말~6월초, 2학기는 11월말~12월초 공고 기간", "영어로 하는 것을 원칙으로 함.",
          "과정수료 후 4년 이내 (단, 군복무 기간은 이에 산입하지 않으며, 소속 대학(원)장이 대학원 학사위원회 심의를 거쳐 2년까지 연장이 가능하다.)", OTHER_KO],
         "The last step before the degree, with its own time limit.", when="Documents in April or October"),
    card("ae-thesis-phd", DOCTORAL, "for_degree", "thesis", "Doctoral thesis examination", "Two journal papers first; thesis within 6 years",
         ["Eligible with at least 36 credits (통산 60학점: 60 in combined total), earned or to be earned by the end of that semester; both parts of the qualifying examination passed; and registration (research-student registration if coursework is completed).",
          "Documents: April in the first semester, October in the second, on the announced dates.",
          "At least 2 papers in internationally recognised journals, 1 as lead author and 1 as co-author, published or with proof of acceptance, and the department head's permission.",
          "Preliminary examination at the start of the semester (April or October); final examination, with a public presentation, at the end (June or December).",
          "The thesis and its presentation are in English, in principle.", "Submit the thesis within 6 years of completing coursework. Military service is not counted. After review by the graduate academic committee, the head of the college or graduate school can extend this by up to 2 years.",
          "Make the thesis public (공표) within 1 year of receiving the degree: as a book, in a journal or periodical, by presenting it at an academic seminar, or in another way. This can be deferred after review, for a patent or a similar reason.", OTHER_RULES],
         ["36학점(통산 60학점) 이상 당해 학기말까지 취득하였거나 취득할 수 있어야 하고, 논자시(외국어+전공) 합격한자, 등록생(수료자인 경우 연구생 등록생), 학과 내규 만족하는 자*",
          "국제적으로 인정되는 학술지에 논문 2편 (주저자 1편, 공동저자 1편) 이상 게재하거나 게재예정증명서를 제출하여 학과장의 허가를 받아야 함.",
          "초심은 학기초(1학기 4월, 2학기 10월), 종심은 공개발표를 포함하여 학기말(1학기 6월, 2학기 12월) 시행", "영어로 하는 것을 원칙으로 함.", "1학기는 4월, 2학기는 10월 공고 기간", OTHER_KO,
          "과정수료 후 6년 이내 (단, 군복무 기간은 이에 산입하지 않으며, 소속 대학(원)장이 대학원 학사위원회 심의를 거쳐 2년까지 연장이 가능하다.)",
          "박사학위를 받은 자는 학위수여일로부터 1년 이내에 단행본 발간, 학회지 게재, 정기간행물 게재, 국제학술지 게재, 학술세미나에서 발표, 기타의 방법으로 박사학위논문을 공표하여야 함. 특허 및 업무보완 등의 이유로 부득이하게 학위논문 공표를 유보하고자 할 경우 심의를 거쳐 공표를 유보할 수 있음."],
         "The papers must be published or accepted before the examination can be requested.", when="Documents in April or October", trap="The examination cannot be requested until both papers are published or accepted."),
]


def numbers(text):
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def check():
    tabs = {page: "\n".join(pane(page, "tab-2021")) for page in PAGES}
    older = {page: "\n".join(pane(page, "tab-2020")) for page in PAGES}
    plain = lambda text: re.sub(r"\s+", "", text)
    problems, only_new = [], 0
    for c in CARDS:
        text = plain(tabs[c["source_file"]])
        for quote in c["quotes_ko"]:
            if plain(quote) not in text:
                problems.append(f"{c['id']}: a quote is not in the 2021 tab of '{c['source_file']}': {quote[:50]}")
        only_new += any(plain(q) not in plain(older[c["source_file"]]) for q in c["quotes_ko"])
        said = numbers(" ".join([c["title"], c["key"]] + c["rule"]))
        missing = said - numbers(" ".join(c["quotes_ko"]))
        if missing:
            problems.append(f"{c['id']}: numbers in the English that are in no quote: {sorted(missing)}")
    if len({c["id"] for c in CARDS}) != len(CARDS):
        problems.append("two cards share an id")
    return problems, only_new


if __name__ == "__main__":
    problems, only_new = check()
    if problems:
        sys.exit("Nothing was written.\n" + "\n".join(problems))
    target = ROOT / "data" / "AEROSPACE" / "cards.json"
    target.write_text(json.dumps(CARDS, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    by = {p: sum(p in c["programs"] for c in CARDS) for p in ALL}
    print(f"{len(CARDS)} cards written to {target.relative_to(ROOT)}: {by}")
    print(f"Every quote is in the tab for entrants from 2021, and every number in the English is in a quote.")
    print(f"{only_new} cards rest on a line that the rules for entrants up to 2020 do not contain.")
    print("Sources:", ", ".join(SITE + path for path in PAGES.values()))
