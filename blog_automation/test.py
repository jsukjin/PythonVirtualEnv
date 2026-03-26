def test_post_handler(item) -> dict:
    return {
        "received_name": item.name,
        "processed_message": f"Hello! Your message '{item.message}' was received successfully."
    }

def calculate_handler(item) -> dict:
    """덧셈, 뺄셈 등 계산을 수행하는 함수"""
    num1 = item.num1
    num2 = item.num2
    operation = item.operation

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        result = num1 / num2 if num2 != 0 else "Error: Division by zero"
    else:
        result = "Error: Unknown operation"

    return {
        "num1": num1,
        "num2": num2,
        "operation": operation,
        "result": result
    }

def user_info_handler(item) -> dict:
    """사용자 정보를 처리하는 함수"""
    return {
        "status": "success",
        "user_name": item.name,
        "user_email": item.email,
        "user_age": item.age,
        "message": f"User {item.name} registered successfully!"
    }
