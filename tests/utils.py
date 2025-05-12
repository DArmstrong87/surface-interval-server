DELIMITER = "==========="


def print_test_info(msg):
    statement = f"{DELIMITER} {msg} {DELIMITER}"
    print(statement)


def print_assert_that(msg):
    statement = f"🧪 Asserting that {msg}."
    print(statement)


def print_test_action(msg):
    statement = f"\n🔱 {msg}"
    print(statement)


def print_test_setup(test_case):
    statement = f"\n\n\n🛠️  Setting up {test_case.__class__.__name__} \n"
    print(statement)
