from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


password = "TestPassword123"

hashed = hash_password(password)

print("Original password:")
print(password)

print("\nHashed password:")
print(hashed)

print("\nCorrect password:")
print(verify_password(password, hashed))

print("\nWrong password:")
print(verify_password("WrongPassword", hashed))


token = create_access_token({
    "user_id": 1,
    "email": "test@example.com"
})

print("\nJWT token:")
print(token)

decoded = decode_access_token(token)

print("\nDecoded token:")
print(decoded)