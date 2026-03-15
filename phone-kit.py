#!/usr/bin/env python3

import random
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import phonenumbers
except ImportError:
    print("Missing required package: phonenumbers")
    print("Install it with: pip install phonenumbers")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    print("Missing required package: tqdm")
    print("Install it with: pip install tqdm")
    sys.exit(1)

try:
    import pyfiglet
except ImportError:
    print("Missing required package: pyfiglet")
    print("Install it with: pip install pyfiglet")
    sys.exit(1)


country_codes = {
    "+93": {"len": 9, "name": "Afghanistan"},
    "+355": {"len": 9, "name": "Albania"},
    "+213": {"len": 9, "name": "Algeria"},
    "+376": {"len": 6, "name": "Andorra"},
    "+244": {"len": 9, "name": "Angola"},
    "+54": {"len": 10, "name": "Argentina"},
    "+374": {"len": 8, "name": "Armenia"},
    "+297": {"len": 7, "name": "Aruba"},
    "+61": {"len": 9, "name": "Australia"},
    "+43": {"len": 10, "name": "Austria"},
    "+994": {"len": 9, "name": "Azerbaijan"},
    "+973": {"len": 8, "name": "Bahrain"},
    "+880": {"len": 10, "name": "Bangladesh"},
    "+375": {"len": 9, "name": "Belarus"},
    "+32": {"len": 9, "name": "Belgium"},
    "+501": {"len": 7, "name": "Belize"},
    "+229": {"len": 8, "name": "Benin"},
    "+975": {"len": 8, "name": "Bhutan"},
    "+591": {"len": 8, "name": "Bolivia"},
    "+387": {"len": 8, "name": "Bosnia and Herzegovina"},
    "+267": {"len": 8, "name": "Botswana"},
    "+55": {"len": 11, "name": "Brazil"},
    "+673": {"len": 7, "name": "Brunei"},
    "+359": {"len": 9, "name": "Bulgaria"},
    "+226": {"len": 8, "name": "Burkina Faso"},
    "+257": {"len": 8, "name": "Burundi"},
    "+238": {"len": 7, "name": "Cabo Verde"},
    "+855": {"len": 9, "name": "Cambodia"},
    "+237": {"len": 8, "name": "Cameroon"},
    "+1": {"len": 10, "name": "USA / Canada / Caribbean"},
    "+236": {"len": 8, "name": "Central African Republic"},
    "+235": {"len": 8, "name": "Chad"},
    "+56": {"len": 9, "name": "Chile"},
    "+86": {"len": 11, "name": "China"},
    "+57": {"len": 10, "name": "Colombia"},
    "+269": {"len": 7, "name": "Comoros"},
    "+242": {"len": 7, "name": "Congo"},
    "+243": {"len": 9, "name": "DR Congo"},
    "+682": {"len": 5, "name": "Cook Islands"},
    "+506": {"len": 8, "name": "Costa Rica"},
    "+385": {"len": 9, "name": "Croatia"},
    "+53": {"len": 8, "name": "Cuba"},
    "+599": {"len": 7, "name": "Curacao"},
    "+357": {"len": 8, "name": "Cyprus"},
    "+420": {"len": 9, "name": "Czech Republic"},
    "+225": {"len": 8, "name": "Cote d'Ivoire"},
    "+45": {"len": 8, "name": "Denmark"},
    "+253": {"len": 8, "name": "Djibouti"},
    "+593": {"len": 9, "name": "Ecuador"},
    "+20": {"len": 10, "name": "Egypt"},
    "+503": {"len": 8, "name": "El Salvador"},
    "+240": {"len": 9, "name": "Equatorial Guinea"},
    "+291": {"len": 7, "name": "Eritrea"},
    "+372": {"len": 8, "name": "Estonia"},
    "+251": {"len": 9, "name": "Ethiopia"},
    "+500": {"len": 5, "name": "Falkland Islands"},
    "+298": {"len": 6, "name": "Faroe Islands"},
    "+679": {"len": 8, "name": "Fiji"},
    "+358": {"len": 10, "name": "Finland"},
    "+33": {"len": 9, "name": "France"},
    "+594": {"len": 9, "name": "French Guiana"},
    "+689": {"len": 6, "name": "French Polynesia"},
    "+241": {"len": 7, "name": "Gabon"},
    "+220": {"len": 7, "name": "Gambia"},
    "+995": {"len": 9, "name": "Georgia"},
    "+49": {"len": 11, "name": "Germany"},
    "+233": {"len": 9, "name": "Ghana"},
    "+350": {"len": 8, "name": "Gibraltar"},
    "+30": {"len": 10, "name": "Greece"},
    "+299": {"len": 6, "name": "Greenland"},
    "+590": {"len": 9, "name": "Guadeloupe"},
    "+502": {"len": 8, "name": "Guatemala"},
    "+224": {"len": 8, "name": "Guinea"},
    "+245": {"len": 7, "name": "Guinea-Bissau"},
    "+592": {"len": 7, "name": "Guyana"},
    "+509": {"len": 8, "name": "Haiti"},
    "+504": {"len": 8, "name": "Honduras"},
    "+852": {"len": 8, "name": "Hong Kong"},
    "+36": {"len": 9, "name": "Hungary"},
    "+354": {"len": 7, "name": "Iceland"},
    "+91": {"len": 10, "name": "India"},
    "+62": {"len": 10, "name": "Indonesia"},
    "+98": {"len": 10, "name": "Iran"},
    "+964": {"len": 10, "name": "Iraq"},
    "+353": {"len": 9, "name": "Ireland"},
    "+972": {"len": 9, "name": "Israel"},
    "+39": {"len": 10, "name": "Italy"},
    "+81": {"len": 10, "name": "Japan"},
    "+962": {"len": 9, "name": "Jordan"},
    "+7": {"len": 10, "name": "Kazakhstan / Russia"},
    "+254": {"len": 9, "name": "Kenya"},
    "+686": {"len": 5, "name": "Kiribati"},
    "+965": {"len": 8, "name": "Kuwait"},
    "+996": {"len": 9, "name": "Kyrgyzstan"},
    "+856": {"len": 8, "name": "Laos"},
    "+371": {"len": 8, "name": "Latvia"},
    "+961": {"len": 8, "name": "Lebanon"},
    "+266": {"len": 8, "name": "Lesotho"},
    "+231": {"len": 8, "name": "Liberia"},
    "+218": {"len": 9, "name": "Libya"},
    "+423": {"len": 7, "name": "Liechtenstein"},
    "+370": {"len": 8, "name": "Lithuania"},
    "+352": {"len": 8, "name": "Luxembourg"},
    "+853": {"len": 8, "name": "Macao"},
    "+389": {"len": 8, "name": "North Macedonia"},
    "+261": {"len": 9, "name": "Madagascar"},
    "+265": {"len": 8, "name": "Malawi"},
    "+60": {"len": 9, "name": "Malaysia"},
    "+960": {"len": 7, "name": "Maldives"},
    "+223": {"len": 8, "name": "Mali"},
    "+356": {"len": 8, "name": "Malta"},
    "+692": {"len": 7, "name": "Marshall Islands"},
    "+596": {"len": 9, "name": "Martinique"},
    "+222": {"len": 8, "name": "Mauritania"},
    "+230": {"len": 8, "name": "Mauritius"},
    "+52": {"len": 10, "name": "Mexico"},
    "+691": {"len": 7, "name": "Micronesia"},
    "+373": {"len": 8, "name": "Moldova"},
    "+377": {"len": 8, "name": "Monaco"},
    "+976": {"len": 8, "name": "Mongolia"},
    "+382": {"len": 8, "name": "Montenegro"},
    "+212": {"len": 9, "name": "Morocco"},
    "+258": {"len": 9, "name": "Mozambique"},
    "+95": {"len": 8, "name": "Myanmar"},
    "+264": {"len": 9, "name": "Namibia"},
    "+674": {"len": 6, "name": "Nauru"},
    "+977": {"len": 10, "name": "Nepal"},
    "+31": {"len": 9, "name": "Netherlands"},
    "+687": {"len": 6, "name": "New Caledonia"},
    "+64": {"len": 10, "name": "New Zealand"},
    "+505": {"len": 8, "name": "Nicaragua"},
    "+227": {"len": 8, "name": "Niger"},
    "+234": {"len": 10, "name": "Nigeria"},
    "+683": {"len": 4, "name": "Niue"},
    "+672": {"len": 4, "name": "Norfolk Island"},
    "+850": {"len": 9, "name": "North Korea"},
    "+47": {"len": 8, "name": "Norway"},
    "+968": {"len": 8, "name": "Oman"},
    "+92": {"len": 10, "name": "Pakistan"},
    "+680": {"len": 7, "name": "Palau"},
    "+970": {"len": 9, "name": "Palestine"},
    "+507": {"len": 8, "name": "Panama"},
    "+675": {"len": 8, "name": "Papua New Guinea"},
    "+595": {"len": 9, "name": "Paraguay"},
    "+51": {"len": 9, "name": "Peru"},
    "+63": {"len": 10, "name": "Philippines"},
    "+48": {"len": 9, "name": "Poland"},
    "+351": {"len": 9, "name": "Portugal"},
    "+974": {"len": 8, "name": "Qatar"},
    "+82": {"len": 10, "name": "South Korea"},
    "+40": {"len": 10, "name": "Romania"},
    "+250": {"len": 8, "name": "Rwanda"},
    "+966": {"len": 9, "name": "Saudi Arabia"},
    "+221": {"len": 9, "name": "Senegal"},
    "+381": {"len": 8, "name": "Serbia"},
    "+248": {"len": 7, "name": "Seychelles"},
    "+232": {"len": 8, "name": "Sierra Leone"},
    "+65": {"len": 8, "name": "Singapore"},
    "+421": {"len": 9, "name": "Slovakia"},
    "+386": {"len": 8, "name": "Slovenia"},
    "+677": {"len": 7, "name": "Solomon Islands"},
    "+252": {"len": 8, "name": "Somalia"},
    "+27": {"len": 9, "name": "South Africa"},
    "+211": {"len": 9, "name": "South Sudan"},
    "+34": {"len": 9, "name": "Spain"},
    "+94": {"len": 10, "name": "Sri Lanka"},
    "+249": {"len": 9, "name": "Sudan"},
    "+597": {"len": 7, "name": "Suriname"},
    "+268": {"len": 8, "name": "Eswatini"},
    "+46": {"len": 10, "name": "Sweden"},
    "+41": {"len": 9, "name": "Switzerland"},
    "+963": {"len": 9, "name": "Syria"},
    "+886": {"len": 9, "name": "Taiwan"},
    "+992": {"len": 9, "name": "Tajikistan"},
    "+255": {"len": 9, "name": "Tanzania"},
    "+66": {"len": 9, "name": "Thailand"},
    "+670": {"len": 7, "name": "Timor-Leste"},
    "+228": {"len": 8, "name": "Togo"},
    "+690": {"len": 4, "name": "Tokelau"},
    "+676": {"len": 7, "name": "Tonga"},
    "+216": {"len": 8, "name": "Tunisia"},
    "+90": {"len": 10, "name": "Turkey"},
    "+993": {"len": 8, "name": "Turkmenistan"},
    "+688": {"len": 5, "name": "Tuvalu"},
    "+256": {"len": 9, "name": "Uganda"},
    "+380": {"len": 9, "name": "Ukraine"},
    "+971": {"len": 9, "name": "United Arab Emirates"},
    "+44": {"len": 10, "name": "United Kingdom"},
    "+598": {"len": 8, "name": "Uruguay"},
    "+998": {"len": 9, "name": "Uzbekistan"},
    "+678": {"len": 7, "name": "Vanuatu"},
    "+58": {"len": 10, "name": "Venezuela"},
    "+84": {"len": 10, "name": "Vietnam"},
    "+681": {"len": 6, "name": "Wallis and Futuna"},
    "+967": {"len": 9, "name": "Yemen"},
    "+260": {"len": 9, "name": "Zambia"},
    "+263": {"len": 9, "name": "Zimbabwe"},
}


def print_banner():
    banner = pyfiglet.figlet_format("PhoneKit", font="slant")
    print("\033[96m" + banner + "\033[0m")
    print("\033[93m  Phone Number Generator & Validator\033[0m")
    print("\033[90m  Generate random phone numbers, validate them,\033[0m")
    print("\033[90m  and save only the live ones.\033[0m")
    print()
    print("\033[90m  ─────────────────────────────────────────────\033[0m")
    print()


def print_section(title):
    print(f"\n\033[96m  [{title}]\033[0m")


def print_success(msg):
    print(f"\033[92m  [+] {msg}\033[0m")


def print_info(msg):
    print(f"\033[94m  [*] {msg}\033[0m")


def print_warn(msg):
    print(f"\033[93m  [!] {msg}\033[0m")


def print_error(msg):
    print(f"\033[91m  [-] {msg}\033[0m")


def is_valid(number):
    try:
        parsed = phonenumbers.parse(number)
        return phonenumbers.is_valid_number(parsed)
    except Exception:
        return False


def validate_number(number):
    number = number.strip()
    if number.startswith("+") and is_valid(number):
        return number
    return None


def list_countries():
    print_section("Available Country Codes")
    print()
    sorted_codes = sorted(country_codes.items(), key=lambda x: x[1]["name"])
    col_width = 45
    items = [f"  {code:>6}  {info['name']}" for code, info in sorted_codes]
    mid = (len(items) + 1) // 2
    left = items[:mid]
    right = items[mid:]
    for i in range(max(len(left), len(right))):
        l = left[i] if i < len(left) else ""
        r = right[i] if i < len(right) else ""
        print(f"\033[37m{l:<{col_width}}{r}\033[0m")
    print()


def generate_numbers(country_code, count):
    info = country_codes[country_code]
    num_len = info["len"]
    numbers = []
    for _ in range(count):
        digits = "".join([str(random.randint(0, 9)) for _ in range(num_len)])
        numbers.append(country_code + digits)
    return numbers


def main():
    print_banner()

    while True:
        print("\033[97m  ---- Menu ----\033[0m")
        print("    1) Generate & Validate phone numbers")
        print("    2) Validate existing file")
        print("    3) List country codes")
        print("    4) Quit")
        print()

        choice = input("\033[97m  Choose an option [1-4]: \033[0m").strip()

        if choice == "1":
            print_section("Generate & Validate")

            country_code = input("\n\033[97m  Enter country code (e.g. +1, +44, +91): \033[0m").strip()

            if country_code not in country_codes:
                print_error(f"Unknown country code: {country_code}")
                print_info("Use option 3 to see all available country codes.")
                print()
                continue

            country_name = country_codes[country_code]["name"]
            print_info(f"Country: {country_name} ({country_code})")

            try:
                num_count = int(input("\033[97m  How many numbers to generate: \033[0m").strip())
            except ValueError:
                print_error("Invalid number. Please enter a whole number.")
                print()
                continue

            if num_count <= 0:
                print_error("Number must be greater than 0.")
                print()
                continue

            print()
            print_info(f"Generating {num_count:,} random phone numbers for {country_name}...")
            numbers = generate_numbers(country_code, num_count)
            print_success(f"Generated {len(numbers):,} numbers.")

            print()
            print_info("Validating numbers...")
            valid_numbers = []
            invalid_count = 0

            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {executor.submit(validate_number, num): num for num in numbers}
                with tqdm(
                    total=len(numbers),
                    desc="  Checking",
                    unit="num",
                    bar_format="\033[94m  {l_bar}{bar:40}\033[0m| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
                    ncols=100,
                ) as pbar:
                    for future in as_completed(futures):
                        result = future.result()
                        if result is not None:
                            valid_numbers.append(result)
                        else:
                            invalid_count += 1
                        pbar.update(1)

            print()
            print_section("Results")
            print_success(f"Valid (live):   {len(valid_numbers):,}")
            print_error(f"Invalid (dead): {invalid_count:,}")
            print_info(f"Hit rate:       {len(valid_numbers) / len(numbers) * 100:.1f}%")

            if len(valid_numbers) > 0:
                output_dir = "Phone-numbers"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                filename = os.path.join(output_dir, f"{country_code.replace('+', '')}_valid.txt")
                with open(filename, "w") as f:
                    f.write("\n".join(valid_numbers) + "\n")
                print()
                print_success(f"Saved {len(valid_numbers):,} valid numbers to {filename}")
            else:
                print()
                print_warn("No valid numbers found. Try generating more numbers.")

            all_file = os.path.join("Phone-numbers", f"{country_code.replace('+', '')}_all.txt")
            with open(all_file, "w") as f:
                f.write("\n".join(numbers) + "\n")
            print_info(f"All generated numbers saved to {all_file}")
            print()

        elif choice == "2":
            print_section("Validate Existing File")

            filepath = input("\n\033[97m  Enter path to phone numbers file: \033[0m").strip()
            if not os.path.isfile(filepath):
                print_error(f"File not found: {filepath}")
                print()
                continue

            with open(filepath, "r") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if len(lines) == 0:
                print_error("File is empty.")
                print()
                continue

            print_info(f"Loaded {len(lines):,} numbers from {filepath}")
            print()
            print_info("Validating numbers...")

            valid_numbers = []
            invalid_count = 0

            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {executor.submit(validate_number, num): num for num in lines}
                with tqdm(
                    total=len(lines),
                    desc="  Checking",
                    unit="num",
                    bar_format="\033[94m  {l_bar}{bar:40}\033[0m| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
                    ncols=100,
                ) as pbar:
                    for future in as_completed(futures):
                        result = future.result()
                        if result is not None:
                            valid_numbers.append(result)
                        else:
                            invalid_count += 1
                        pbar.update(1)

            print()
            print_section("Results")
            print_success(f"Valid (live):   {len(valid_numbers):,}")
            print_error(f"Invalid (dead): {invalid_count:,}")
            if len(lines) > 0:
                print_info(f"Hit rate:       {len(valid_numbers) / len(lines) * 100:.1f}%")

            if len(valid_numbers) > 0:
                output_dir = "Phone-numbers"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                base = os.path.splitext(os.path.basename(filepath))[0]
                filename = os.path.join(output_dir, f"{base}_valid.txt")
                with open(filename, "w") as f:
                    f.write("\n".join(valid_numbers) + "\n")
                print()
                print_success(f"Saved {len(valid_numbers):,} valid numbers to {filename}")
            else:
                print()
                print_warn("No valid numbers found in the file.")
            print()

        elif choice == "3":
            list_countries()

        elif choice in ("4", "q", "quit", "exit"):
            print()
            print_info("Goodbye!")
            print()
            break

        else:
            print_error("Invalid choice. Please enter 1, 2, 3, or 4.")
            print()


if __name__ == "__main__":
    main()
