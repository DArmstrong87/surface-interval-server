DELIMITER = "==========="


def print_test_info(msg):
    statement = f"{DELIMITER} {msg} {DELIMITER}"
    print(statement)


def print_assert_info(msg):
    statement = f"🧪 Asserting that {msg}."
    print(statement)


def print_test_action(msg):
    statement = f"\n🔱 {msg}"
    print(statement)
