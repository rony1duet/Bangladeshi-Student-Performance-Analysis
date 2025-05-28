def get_user_choice(prompt, choices):
    print(f"\n{prompt}")
    for idx, choice in enumerate(choices, 1):
        print(f"{idx}. {choice}")
    try:
        choice = int(input("Enter your choice: "))
        if 1 <= choice <= len(choices):
            return choices[choice - 1]
        else:
            print("Invalid choice. Try again.")
            return get_user_choice(prompt, choices)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_user_choice(prompt, choices)
