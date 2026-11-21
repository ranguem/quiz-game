import json
import os

from default_quizzes import get_default_quizzes
from quiz import Quiz

# 프로젝트 루트(이 파일이 있는 폴더)의 state.json
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []
        self.best_score = None   # {"score": 점수, "correct": 정답수, "total": 문제수} 또는 None
        self.load_state()

    # ---------- 파일 저장/불러오기 ----------
    def load_state(self):
        """state.json에서 데이터를 불러온다. 없거나 손상되면 기본 데이터를 사용한다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data.get("best_score")
            if best_score is not None and not isinstance(best_score, dict):
                raise ValueError("best_score 형식이 올바르지 않습니다.")

            self.quizzes = quizzes
            self.best_score = best_score
            score_text = f"{best_score['score']}점" if best_score else "없음"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")

        except FileNotFoundError:
            print("📂 저장 파일이 없어 기본 퀴즈 데이터로 시작합니다.")
            self.use_default_data()

        except (json.JSONDecodeError, KeyError, TypeError, ValueError, UnicodeDecodeError):
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
            self.use_default_data()
            self.save_state()

        except OSError as e:
            print(f"⚠️ 파일을 읽을 수 없어 기본 데이터로 시작합니다. ({e})")
            self.use_default_data()

    def use_default_data(self):
        """기본 퀴즈 데이터로 초기화한다."""
        self.quizzes = get_default_quizzes()
        self.best_score = None

    def save_state(self):
        """퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"⚠️ 파일을 저장하지 못했습니다. ({e})")

    # ---------- 입력 처리 ----------
    def read_number(self, prompt, min_value, max_value):
        """범위 안의 숫자를 입력받는다. Ctrl+C / EOF 시 None 반환."""
        while True:
            try:
                text = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되었습니다.")
                return None

            if text == "":
                print(f"⚠️ 입력이 비어 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue
            if not text.isdigit():
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            number = int(text)
            if number < min_value or number > max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue
            return number

    def read_text(self, prompt):
        """비어 있지 않은 문자열을 입력받는다. Ctrl+C / EOF 시 None 반환."""
        while True:
            try:
                text = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되었습니다.")
                return None

            if text == "":
                print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
                continue
            return text

    # ---------- 화면 출력 ----------
    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    # ---------- 기능 ----------
    def play_quiz(self):
        """퀴즈를 출제하고 최고 점수를 갱신한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.\n")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print("\n" + "-" * 40)
            print(f"[문제 {number}]")
            quiz.display()
            print()

            answer = self.read_number("정답 입력: ", 1, 4)
            if answer is None:
                print("퀴즈를 중단합니다.")
                return

            if quiz.is_correct(answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = int(correct / total * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score["score"]:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = {"score": score, "correct": correct, "total": total}
            self.save_state()
        print("=" * 40 + "\n")

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가하고 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = self.read_text("문제를 입력하세요: ")
        if question is None:
            return

        choices = []
        for i in range(1, 5):
            choice = self.read_text(f"선택지 {i}: ")
            if choice is None:
                return
            choices.append(choice)

        answer = self.read_number("정답 번호 (1-4): ", 1, 4)
        if answer is None:
            return

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def list_quizzes(self):
        """등록된 퀴즈 목록을 출력한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.\n")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40 + "\n")

    def show_best_score(self):
        """최고 점수를 출력한다."""
        if self.best_score is None:
            print("\n⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요.\n")
            return

        print(
            f"\n🏆 최고 점수: {self.best_score['score']}점 "
            f"({self.best_score['total']}문제 중 {self.best_score['correct']}문제 정답)\n"
        )

    # ---------- 실행 ----------
    def run(self):
        """메뉴 루프를 실행한다. 종료 시 항상 저장한다."""
        try:
            while True:
                self.show_menu()
                choice = self.read_number("선택: ", 1, 5)

                if choice is None or choice == 5:
                    print("\n👋 게임을 종료합니다.")
                    break
                elif choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_best_score()
        finally:
            self.save_state()