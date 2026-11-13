# -*- coding: utf-8 -*-
"""Requirement cards for Nuclear Engineering's graduate programs, entrants from 2021, written by hand from the
department's own rule document, "원자핵공학과 대학원과정 졸업요건 규정(2021학번~)" (three pages; applied from the second
semester of 2026). Download it from https://nucleng.snu.ac.kr/graduate/rule into sources/NUCLEAR/ first.

    .venv/bin/python tools/cards_nuclear.py     checks every card and writes data/NUCLEAR/cards.json

The document says that "PhD students" in it include integrated MS-PhD students (Article 1, paragraph 2), so the PhD
cards are shown for both. It leaves the credits themselves to the university's degree regulations and gives no numbers.
Its supplementary provisions say from which semester some paragraphs apply; the cards carry those dates. They also say
that for the integrated program the semester of selection counts as entry (석·박통합과정은 선발 진입학기를 입학으로 한다).
The checks are in tools/cards_pdf.py.
"""
from cards_pdf import DOCTORAL, card, pages, verify, write

NAME, TEXT = pages("NUCLEAR", "2021학년도 입학생 이후")
A = "Entrants from 2021"

CARDS = [
    card("ne-credits", ["masters", "phd", "integrated"], "finish_coursework", "rules", "Coursework credits", "Set by the university's degree regulations",
         ["Complete the credits your program requires for completion, as set in the university's degree-conferral regulations (학위수여규정).",
          "This department's document gives no number of its own."],
         ["제 3 조 (학점요건) ① 학생은 학위수여규정에 정해진 대로 각 과정의 수료에 필요한 소정의 학점을 이수하여야 한다."],
         "The number of credits is not in this department's document; look it up in the university regulations.", applies_from=A),
    card("ne-qualifying", ["masters", "phd", "integrated"], "before_exam", "rules", "Qualification to submit a thesis", "Comprehensive examination and foreign language examination",
         ["To qualify to submit a thesis, pass both the comprehensive examination (종합시험) and the foreign language examination (외국어시험).",
          "This document does not say which foreign language test or score is required. See the university regulations or ask the department office."],
         ["제 4 조 (논문제출자격요건) ① 학생은 논문제출자격을 취득하기 위하여 종합시험 및 외국어시험에 합격하여야 한다.", "제 5 조 (논문심사합격요건) ① 학생은 논문제출자격을 획득한 후 학위논문을 작성하여 학위수여규정과 다음에 정해진 절차와 기준에 따라 논문심사에 합격해야 한다."],
         "A thesis cannot be examined before this qualification is obtained.", applies_from=A),
    card("ne-comprehensive-ms", ["masters"], "before_exam", "rules", "Comprehensive examination (master's)", "60 points on average to pass; two written questions",
         ["A written examination of 1 question on a topic related to your courses and 1 question on a topic related to your thesis.",
          "Each question is marked out of 100. The average must be 60 or higher to pass."],
         ["② 석사과정 학생은 수강교과목에 관련된 주제 1문제, 학위 논문과 관련된 주제 1문제로 구성된 필기시험에서 문제당 100점 만점으로 채점한 결과의 평균이 60점 이상이 되어야 합격한 것으로 한다.", "3조 2항, 3항 및 4조 2항, 3항의 사항은 2023학년도 1학기부터 적용한다."],
         "One of the two questions is on your own thesis topic.", applies_from=A + ". This examination format applies from the first semester of 2023."),
    card("ne-comprehensive-phd", DOCTORAL, "before_exam", "rules", "Comprehensive examination (PhD and integrated)", "70 points on each of three questions; 290 in total over five",
         ["Choose and answer 5 questions of the comprehensive written examination. Each is marked out of 100.",
          "To pass: 70 or higher on each of 3 questions, and 290 or higher in total over the 5.",
          "The examination score, converted to 100, is the average of the 3 questions with 70 or higher."],
         ["③ 박사과정 학생은 출제된 종합필기시험에서 5문제를 선택하여 답하여야 하며, 문제당 100점 만점으로 채점한 결과가 3문제에 대해서는 각각 70점 이상을 획득하여 5문제 총점은 290점 이상이 되어야 합격한 것으로 한다. 단, 100점으로 환산된 종합시험 점수의 산출은 70점 이상 획득한 3문제 점수의 평균으로 한다.", "3조 2항, 3항 및 4조 2항, 3항의 사항은 2023학년도 1학기부터 적용한다."],
         "Both conditions must hold at once: three strong answers and the total.", applies_from=A + ". This examination format applies from the first semester of 2023."),
    card("ne-comprehensive-limit", DOCTORAL, "before_exam", "rules", "Time limit for the doctoral thesis-submission qualifying examination (박사논문제출자격시험)", "PhD: within 6 semesters; integrated: within 8; at most 3 attempts",
         ["PhD students may sit the thesis-submission qualifying examination (박사논문제출자격시험) within 6 registered semesters of entry; integrated-program students within 8.", "At most 3 attempts.",
          "An integrated-program student who has not passed by the 8th registered semester, or who gives up partway (중도에 포기), can receive a master's degree on meeting the master's requirements.",
          "If the examination is not passed within the limit, the department's faculty meeting makes the final decision."],
         ["④ 박사과정 학생은 입학 후 등록 학기 기준으로 6학기 이내에, 석박사통합과정 학생은 8학기 이내에 최대 3회에 한하여 박사논문제출자격 시험에 응시할 수 있다. 만약 석박사통합과정 학생이 등록 8학기까지 논문제출자격시험에 합격하지 못하거나 중도에 포기할 경우, 석사졸업 요건을 충족하면 석사학위를 취득할 수 있다.",
          "⑤ 논문제출자격시험을 기한 내 통과하지 못한 경우 학과 교수회의에서 최종 심의하여 결정한다.", "4조 4항, 5항은 2024학년도 2학기부터 적용한다."],
         "The semesters are counted from entry, by registered semesters.", trap="Both the number of semesters and the number of attempts are limited.",
         applies_from=A + ". These limits apply from the second semester of 2024."),
    card("ne-thesis-ms", ["masters"], "for_degree", "rules", "Master's thesis examination", "Presentation before a committee of 3",
         ["After obtaining the qualification to submit a thesis, write the thesis and, under the university's degree-conferral regulations (학위수여규정), present it to a master's thesis examination committee of 3 members and pass the examination."],
         ["② 석사과정 학생은 3인으로 구성된 석사 논문심사위원회에서 발표 후 심사에 합격해야 한다.",
          "제 5 조 (논문심사합격요건) ① 학생은 논문제출자격을 획득한 후 학위논문을 작성하여 학위수여규정과 다음에 정해진 절차와 기준에 따라 논문심사에 합격해야 한다."],
         "You must hold the qualification to submit a thesis before this examination.", applies_from=A),
    card("ne-preliminary-phd", DOCTORAL, "for_degree", "rules", "Preliminary thesis examination (PhD and integrated)", "Before the regular semester preceding your graduation semester begins",
         ["Pass the preliminary examination before the start of the regular semester that comes right before the semester in which you plan to graduate. The summer session is not counted.",
          "3 thesis advisory committee members examine your thesis proposal and presentation: whether the topic is suitable, some results, and whether the plan for the final thesis is sound."],
         ["③ 박사과정 학생은 졸업예정 학기의 직전 정규학기(여름학기 제외) 개시 이전에 논문예비심사에 합격하여야 한다. 논문예비심사에서는 3인의 논문지도위원이 학생의 논문제안서와 발표를 바탕으로 논문주제의 적정성과 일부 결과, 최종논문 연구계획의 타당성에 대해 심사하도록 한다."],
         "It has to be passed well ahead of the graduation semester.", trap="The deadline is the start of the semester before your graduation semester, not the graduation semester itself.", applies_from=A),
    card("ne-thesis-phd", DOCTORAL, "for_degree", "rules", "Doctoral thesis examination", "Draft to a committee of 5, two weeks before the presentation",
         ["After obtaining the qualification to submit a thesis, and under the university's degree-conferral regulations (학위수여규정): submit a draft of the thesis to a thesis examination committee of 5 members no later than 2 weeks before the scheduled presentation.", "Present it and pass the examination."],
         ["④ 박사과정 학생은 5인으로 구성된 논문심사위원회에 예정된 발표심사일 2주전까지 논문초안을 제출하고, 발표 후 심사에 합격해야 한다.",
          "제 5 조 (논문심사합격요건) ① 학생은 논문제출자격을 획득한 후 학위논문을 작성하여 학위수여규정과 다음에 정해진 절차와 기준에 따라 논문심사에 합격해야 한다."],
         "The draft is due before the presentation, not on the day.", applies_from=A),
    card("ne-publication-ms", ["masters"], "start_early", "rules", "Presentation or publication (master's)", "At least 1, as lead author, by the thesis examination",
         ["By the day of your thesis examination, have at least 1 paper or conference presentation as lead author (주저자), on research done during the degree.",
          "An exception can be approved by the department's faculty meeting if your thesis advisor submits a statement of reasons."],
         ["② 석사과정 학생은 논문심사일까지 주저자로서 최소한 1회의 논문 또는 학술대회 발표실적이 있어야 한다.",
          "④ 학위논문 지도교수가 예외 인정 사유서를 제출한 경우, 학과교수회의 심의를 통해 승인할 수 있다.",
          "제 6 조 (대외논문발표요건) ① 학생은 학위과정 중 연구성과에 대한 학술대회 혹은 학술지 논문 발표실적에 관해 아래에 정해진 요건을 충족하여야 한다.", "6조 2항, 3항의 규정은 2026학년도 2학기부터 학위논문 심사대상자의 대외논문발표요건에 적용한다."],
         "It must exist by the day of the thesis examination.", applies_from=A + ". Applies to students whose thesis is examined from the second semester of 2026."),
    card("ne-publication-phd", DOCTORAL, "start_early", "rules", "Journal paper (PhD and integrated)", "At least 1 SCI(E) paper accepted, as lead author, by the day of the 초심",
         ["By the day of your 초심 (the first examination of the doctoral thesis; this document does not define the term), have at least 1 paper on research done during the degree accepted for publication in an SCI(E)-level journal, as lead author (주저자).", "Online publication counts.",
          "An exception can be approved by the department's faculty meeting if your thesis advisor submits a statement of reasons."],
         ["③ 박사과정 학생은 초심일까지 주저자로서 최소한 1편의 SCI(E)급 논문 게재 승인실적이 있어야 한다. 논문게재의 경우 온라인 출간도 인정한다.",
          "④ 학위논문 지도교수가 예외 인정 사유서를 제출한 경우, 학과교수회의 심의를 통해 승인할 수 있다.", "6조 2항, 3항의 규정은 2026학년도 2학기부터 학위논문 심사대상자의 대외논문발표요건에 적용한다."],
         "The paper must be accepted by the day of the 초심.", trap="초심 is a different word from the preliminary examination (논문예비심사) on the neighbouring card. Confirm with the department office which date counts.",
         applies_from=A + ". Applies to students whose thesis is examined from the second semester of 2026."),
]

if __name__ == "__main__":
    # the undergraduate cards live in their own file and are checked against their own documents
    from cards_nuclear_undergraduate import CARDS as UNDERGRADUATE, TEXTS as UNDERGRADUATE_TEXTS
    write("NUCLEAR", verify(UNDERGRADUATE, UNDERGRADUATE_TEXTS) + verify(CARDS, {"rules": TEXT}))
