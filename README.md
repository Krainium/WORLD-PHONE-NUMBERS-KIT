# PhoneKit — Phone Number Generator & Validator

A Python CLI tool that generates random phone numbers for any country, validates them using Google's `phonenumbers` library, and saves only the valid (live) numbers. Features a progress bar, multi-threaded validation, and styled terminal output.

Created by **Krainium**.

---

## Features

- **190+ countries supported** — generate numbers for any country by dialing code
- **Validation** — checks every generated number against Google's `phonenumbers` library (the same engine behind Android's phone number handling)
- **Multi-threaded** — validates numbers in parallel using 50 worker threads for maximum speed
- **Progress bar** — live tqdm progress bar shows checking speed, ETA, and completion
- **Validate existing files** — import and validate phone number lists you already have
- **Styled output** — pyfiglet ASCII banner, color-coded results, and clean formatting
- **Hit rate stats** — shows percentage of valid numbers found per run
- **Works on Windows, macOS, and Linux**

---

## Preview

```
    ____  __                    __ __ _ __
   / __ \/ /_  ____  ____  ___/ //_/(_) /_
  / /_/ / __ \/ __ \/ __ \/ _ / ,<  / / __/
 / ____/ / / / /_/ / / / /  __/ /| |/ / /_
/_/   /_/ /_/\____/_/ /_/\___/_/ |_/_/\__/

  Phone Number Generator & Validator
  Generate random phone numbers, validate them,
  and save only the live ones.

  ─────────────────────────────────────────────

  ---- Menu ----
    1) Generate & Validate phone numbers
    2) Validate existing file
    3) List country codes
    4) Quit

  Choose an option [1-4]: 1

  [Generate & Validate]

  Enter country code (e.g. +1, +44, +91): +44
  [*] Country: United Kingdom (+44)
  How many numbers to generate: 10000

  [*] Generating 10,000 random phone numbers for United Kingdom...
  [+] Generated 10,000 numbers.

  [*] Validating numbers...
  Checking ████████████████████████████████████████| 10000/10000 [00:03<00:00, 3215.42num/s]

  [Results]
  [+] Valid (live):   1,247
  [-] Invalid (dead): 8,753
  [*] Hit rate:       12.5%

  [+] Saved 1,247 valid numbers to Phone-numbers/44_valid.txt
  [*] All generated numbers saved to Phone-numbers/44_all.txt
```

---

## Requirements

- **Python 3.7+** — [Download here](https://www.python.org/downloads/)
- Three pip packages:

```bash
pip install phonenumbers tqdm pyfiglet
```

---

## Quick Start

```bash
# Install dependencies
pip install phonenumbers tqdm pyfiglet

# Download and run
python phone-kit.py
```

That's it. The interactive menu walks you through everything.

---

## Usage

### Menu Options

#### 1) Generate & Validate

Generate random phone numbers for a specific country and validate them.

1. Enter a country code (e.g. `+1` for USA, `+44` for UK, `+91` for India)
2. Enter how many numbers to generate (e.g. `10000`)
3. Watch the progress bar as numbers are validated
4. Valid numbers are saved to `Phone-numbers/{code}_valid.txt`
5. All generated numbers are saved to `Phone-numbers/{code}_all.txt`

```
  Enter country code (e.g. +1, +44, +91): +234
  [*] Country: Nigeria (+234)
  How many numbers to generate: 50000

  [*] Generating 50,000 random phone numbers for Nigeria...
  [+] Generated 50,000 numbers.

  [*] Validating numbers...
  Checking ████████████████████████████████████████| 50000/50000 [00:14<00:00, 3412.87num/s]

  [Results]
  [+] Valid (live):   5,832
  [-] Invalid (dead): 44,168
  [*] Hit rate:       11.7%

  [+] Saved 5,832 valid numbers to Phone-numbers/234_valid.txt
  [*] All generated numbers saved to Phone-numbers/234_all.txt
```

#### 2) Validate Existing File

Validate phone numbers from a text file you already have (one number per line, must include the `+` country code prefix).

```
  Enter path to phone numbers file: my-numbers.txt
  [*] Loaded 25,000 numbers from my-numbers.txt

  [*] Validating numbers...
  Checking ████████████████████████████████████████| 25000/25000 [00:07<00:00, 3298.11num/s]

  [Results]
  [+] Valid (live):   18,420
  [-] Invalid (dead): 6,580
  [*] Hit rate:       73.7%

  [+] Saved 18,420 valid numbers to Phone-numbers/my-numbers_valid.txt
```

**Input file format** — one phone number per line with country code:
```
+14155552671
+447911123456
+919876543210
+2348012345678
```

#### 3) List Country Codes

Shows all 190+ supported country codes in a two-column table:

```
  [Available Country Codes]

    +93  Afghanistan                           +355  Albania
    +213  Algeria                              +376  Andorra
    +244  Angola                               +54  Argentina
    +374  Armenia                              +297  Aruba
    +61  Australia                             +43  Austria
    ...
```

#### 4) Quit

Exit the program. All files are already saved.

---

## Output

### File Structure

```
Phone-numbers/
  1_valid.txt          # Valid US/Canada numbers
  1_all.txt            # All generated US/Canada numbers
  44_valid.txt         # Valid UK numbers
  44_all.txt           # All generated UK numbers
  234_valid.txt        # Valid Nigeria numbers
  my-numbers_valid.txt # Valid numbers from imported file
```

### Output Format

Each output file contains one phone number per line with the full international format:

```
+447911234567
+447722345678
+447533456789
+447844567890
```

---

## Supported Countries

190+ countries are supported. Here are some common ones:

| Code | Country | Digits After Code |
|------|---------|-------------------|
| `+1` | USA / Canada / Caribbean | 10 |
| `+44` | United Kingdom | 10 |
| `+91` | India | 10 |
| `+86` | China | 11 |
| `+81` | Japan | 10 |
| `+49` | Germany | 11 |
| `+33` | France | 9 |
| `+55` | Brazil | 11 |
| `+234` | Nigeria | 10 |
| `+61` | Australia | 9 |
| `+82` | South Korea | 10 |
| `+7` | Russia / Kazakhstan | 10 |
| `+971` | United Arab Emirates | 9 |
| `+966` | Saudi Arabia | 9 |
| `+27` | South Africa | 9 |
| `+52` | Mexico | 10 |
| `+62` | Indonesia | 10 |
| `+63` | Philippines | 10 |
| `+90` | Turkey | 10 |
| `+20` | Egypt | 10 |

Use option **3** in the menu to see the full list.

---

## How It Works

1. **Generation** — creates random digit sequences of the correct length for the chosen country code (e.g. 10 digits for `+1`, 9 digits for `+44`)

2. **Validation** — each number is parsed and checked by Google's `phonenumbers` library, which verifies:
   - Correct number length for the country
   - Valid area/mobile prefix
   - Proper number formatting rules

3. **Multi-threading** — uses a pool of 50 threads to validate numbers in parallel, typically achieving 3,000+ validations per second

4. **Output** — valid numbers are written to the output file, invalid ones are discarded. Stats are shown with the hit rate percentage

### Why Random Generation?

Random generation produces numbers across the entire number space for a country. The hit rate depends on the country — some countries have a small valid number space (lower hit rate), while others have a larger one (higher hit rate). Typical hit rates range from 5% to 30%.

To get more valid numbers, simply generate more. For example, to get ~5,000 valid US numbers, generate around 50,000.

---

## Tips

- **Generate in bulk** — the validator is fast (3,000+ numbers/second), so don't be afraid to generate 100,000+ at once
- **Run multiple times** — each run appends to a different file, so you can run for the same country multiple times to build a larger list
- **Validate your own lists** — option 2 lets you clean up any phone number list you already have
- **Numbers must include `+`** — when importing files, every number must start with `+` followed by the country code

---

## Troubleshooting

### "Missing required package"

Install all three dependencies:
```bash
pip install phonenumbers tqdm pyfiglet
```

If you're on a system with both Python 2 and 3:
```bash
pip3 install phonenumbers tqdm pyfiglet
```

### "Unknown country code"

Make sure you include the `+` prefix. Use option 3 to see all available codes.

### Low hit rate

This is normal for random generation. Different countries have different valid number ranges. Generate more numbers to get more valid results.

### Permission errors on Windows

If you get permission errors creating the `Phone-numbers` folder, run the command prompt as Administrator or use a directory you have write access to.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| [phonenumbers](https://pypi.org/project/phonenumbers/) | Phone number parsing and validation (Google's libphonenumber port) |
| [tqdm](https://pypi.org/project/tqdm/) | Progress bar for validation tracking |
| [pyfiglet](https://pypi.org/project/pyfiglet/) | ASCII art banner |

---

## License

MIT
