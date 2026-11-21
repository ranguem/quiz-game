from default_quizzes import get_default_quizzes


def show_menu():
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def read_number(prompt, min_value, max_value):
    """범위 안의 숫자를 입력받는다. 잘못되면 다시 입력받는다.
    Ctrl+C / EOF 가 발생하면 None 을 반환한다."""
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


def play_quiz(quizzes):
    """퀴즈를 순서대로 출제하고 맞힌 개수를 반환한다."""
    if not quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.\n")
        return None

    total = len(quizzes)
    correct = 0
    print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

    for number, quiz in enumerate(quizzes, start=1):
        print("\n" + "-" * 40)
        print(f"[문제 {number}]")
        quiz.display()
        print()

        answer = read_number("정답 입력: ", 1, 4)
        if answer is None:
            print("퀴즈를 중단합니다.")
            return None

        if quiz.is_correct(answer):
            print("✅ 정답입니다!")
            correct += 1
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

    score = int(correct / total * 100)
    print("\n" + "=" * 40)
    print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
    print("=" * 40 + "\n")
    return correct


def main():
    quizzes = get_default_quizzes()

    while True:
        show_menu()
        choice = read_number("선택: ", 1, 5)

        if choice is None or choice == 5:
            print("\n👋 게임을 종료합니다.")
            break
        elif choice == 1:
            play_quiz(quizzes)
        elif choice == 2:
            print("\n[퀴즈 추가] 준비 중입니다.\n")
        elif choice == 3:
            print("\n[퀴즈 목록] 준비 중입니다.\n")
        elif choice == 4:
            print("\n[점수 확인] 준비 중입니다.\n")


if __name__ == "__main__":
    main()