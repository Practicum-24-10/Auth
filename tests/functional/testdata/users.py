from faker import Faker

fake = Faker()
user = [{
    "username": "usertest",
    "password": "2wewew34",
    "id": "ac657d07-ee24-47ec-b862-f5f1f17fcece",
}
]

persons_data = user + [{
    "username": str(fake.profile()['username']),
    "password": str(fake.password())
} for _ in range(10)]
