import base64
import os
import shutil
import urllib.parse
import requests

# دیکشنری نگاشت کلمات کلیدی کشورها به (کد فایل, ایموجی پرچم)
COUNTRY_MAP = {
    'germany': ('DE', '🇩🇪'), 'آلمان': ('DE', '🇩🇪'), 'de': ('DE', '🇩🇪'),
    'united states': ('US', '🇺🇸'), 'usa': ('US', '🇺🇸'), 'america': ('US', '🇺🇸'), 'آمریکا': ('US', '🇺🇸'), 'us': ('US', '🇺🇸'),
    'netherlands': ('NL', '🇳🇱'), 'holland': ('NL', '🇳🇱'), 'هلند': ('NL', '🇳🇱'), 'nl': ('NL', '🇳🇱'),
    'france': ('FR', '🇫🇷'), 'فرانسه': ('FR', '🇫🇷'), 'fr': ('FR', '🇫🇷'),
    'turkey': ('TR', '🇹🇷'), 'ترکیه': ('TR', '🇹🇷'), 'tr': ('TR', '🇹🇷'),
    'united kingdom': ('GB', '🇬🇧'), 'uk': ('GB', '🇬🇧'), 'england': ('GB', '🇬🇧'), 'انگلیس': ('GB', '🇬🇧'), 'بریتانیا': ('GB', '🇬🇧'), 'gb': ('GB', '🇬🇧'),
    'canada': ('CA', '🇨🇦'), 'کانادا': ('CA', '🇨🇦'), 'ca': ('CA', '🇨🇦'),
    'uae': ('AE', '🇦🇪'), 'dubai': ('AE', '🇦🇪'), 'امارات': ('AE', '🇦🇪'), 'دبی': ('AE', '🇦🇪'),
    'iran': ('IR', '🇮🇷'), 'ایران': ('IR', '🇮🇷'), 'ir': ('IR', '🇮🇷'),
    'finland': ('FI', '🇫🇮'), 'فنلاند': ('FI', '🇫🇮'),
    'sweden': ('SE', '🇸🇪'), 'سوئد': ('SE', '🇸🇪'),
    'switzerland': ('CH', '🇨🇭'), 'سوئیس': ('CH', '🇨🇭'),
    'russia': ('RU', '🇷🇺'), 'روسیه': ('RU', '🇷🇺'),
    'japan': ('JP', '🇯🇵'), 'ژاپن': ('JP', '🇯🇵'),
    'korea': ('KR', '🇰🇷'), 'کره': ('KR', '🇰🇷'),
    'singapore': ('SG', '🇸🇬'), 'سنگاپور': ('SG', '🇸🇬'),
    'italy': ('IT', '🇮🇹'), 'ایتالیا': ('IT', '🇮🇹'),
    'spain': ('ES', '🇪🇸'), 'اسپانیا': ('ES', '🇪🇸'),
}

OUTPUT_DIR = "countries"


def detect_country(config_line):
    original_name = ""
    if '#' in config_line:
        original_name = urllib.parse.unquote(config_line.split('#')[-1]).lower()

    full_text = original_name + " " + config_line.lower()

    for keyword, (code, flag) in COUNTRY_MAP.items():
        if keyword in full_text:
            return code, flag

    return "OTHER", "🌐"


def format_output(lines_list, is_base64):
    final_text = "\n".join(lines_list)
    if is_base64:
        return base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    return final_text


def update_subscription():
    target_url = "https://erabinhood.ir/iran/config.php?sub"

    try:
        response = requests.get(target_url, timeout=15)
        response.raise_for_status()
        raw_content = response.text.strip()
    except Exception as e:
        print(f"Error fetching source: {e}")
        return

    is_base64 = False
    try:
        decoded_bytes = base64.b64decode(raw_content, validate=True)
        decoded_text = decoded_bytes.decode('utf-8')
        is_base64 = True
    except Exception:
        decoded_text = raw_content

    lines = decoded_text.splitlines()
    modified_lines = []
    country_buckets = {}
    index = 1

    for line in lines:
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('#'):
            continue

        code, flag = detect_country(line)
        new_name = f"{flag} t.me/VeEpN_vpnBot {index}"
        index += 1

        if '#' in line:
            base_config = line.split('#')[0]
            modified_line = f"{base_config}#{new_name}"
        else:
            modified_line = f"{line}#{new_name}"

        modified_lines.append(modified_line)
        country_buckets.setdefault(code, []).append(modified_line)

    # ذخیره ساب اصلی
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(format_output(modified_lines, is_base64))

    # پاکسازی پوشه قبلی و ساخت فایل مجزا برای هر کشور
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for code, c_lines in country_buckets.items():
        file_path = os.path.join(OUTPUT_DIR, f"{code}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(format_output(c_lines, is_base64))


if __name__ == "__main__":
    update_subscription()
