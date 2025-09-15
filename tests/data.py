user_data = [
    {
        "id": index,
        "first_name": f"test first_name {index}",
        "last_name": f"test last_name {index}",
        "email": f"test{index}@email.com",
        "password": f"test password {index}",
    }
    for index in range(1, 4)
]

board_data = [
    {
        "id": index,
        "name": f"test name {index}"
    }
    for index in range(1, 4)
]

task_data = [
    {
        "id": index,
        "title": f"test title {index}",
        "body": f"test body {index}",
        "status_id": index,
        "priority_id": index,
    }
    for index in range(1, 4)
]
