import argparse
import random
import string

def generate_password(length, include_special_chars, include_capital_letters, include_numbers):
    chars = string.ascii_lowercase
    if include_capital_letters:
        chars += string.ascii_uppercase
    if include_numbers:
        chars += string.digits
    if include_special_chars:
        chars += string.punctuation

    # Ensure the presence of at least one required character
    password = []
    if include_capital_letters:
        password.append(random.choice(string.ascii_uppercase))
    if include_numbers:
        password.append(random.choice(string.digits))
    if include_special_chars:
        password.append(random.choice(string.punctuation))

    # Fill the rest of the password
    password += [random.choice(chars) for _ in range(length - len(password))]
    
    # Shuffle the password to randomize positions
    random.shuffle(password)
    
    return ''.join(password)

def main():
    parser = argparse.ArgumentParser(description="Generate a random password.")
    parser.add_argument('-l', '--length', type=int, default=12, help='Length of the password')
    parser.add_argument('--no-special', action='store_true', help='Disable special characters in the password')
    parser.add_argument('--no-capital', action='store_true', help='Disable capital letters in the password')
    parser.add_argument('--no-numbers', action='store_true', help='Disable numbers in the password')
    
    args = parser.parse_args()
    password = generate_password(
        args.length, 
        not args.no_special, 
        not args.no_capital, 
        not args.no_numbers
    )
    
    print(f"Generated Password: {password}")

if __name__ == "__main__":
    main()
