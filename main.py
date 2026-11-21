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


def get_menu_choice():
    while True:
        try:
            choice = input("선택: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n프로그램을 안전하게 종료합니다.")
            return 5

        if choice == "":
            print("⚠️ 입력이 비어 있습니다. 1-5 사이의 숫자를 입력하세요.")
            continue
        if not choice.isdigit():
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        number = int(choice)
        if number < 1 or number > 5:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue
        return number


def main():
    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == 1:
            print("\n[퀴즈 풀기] 준비 중입니다.\n")
        elif choice == 2:
            print("\n[퀴즈 추가] 준비 중입니다.\n")
        elif choice == 3:
            print("\n[퀴즈 목록] 준비 중입니다.\n")
        elif choice == 4:
            print("\n[점수 확인] 준비 중입니다.\n")
        elif choice == 5:
            print("\n👋 게임을 종료합니다.")
            break


if __name__ == "__main__":
    main()