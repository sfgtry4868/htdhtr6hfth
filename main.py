import base64
import requests
import urllib.parse

# دیکشنری نگاشت کلمات کلیدی کشورها (فارسی و انگلیسی) به ایموجی پرچم
COUNTRY_FLAGS = {
    'germany': '🇩🇪', 'آلمان': '🇩🇪', 'de': '🇩🇪',
    'united states': '🇺🇸', 'usa': '🇺🇸', 'america': '🇺🇸', 'آمریکا': '🇺🇸', 'us': '🇺🇸',
    'netherlands': '🇳🇱', 'holland': '🇳🇱', 'هلند': '🇳🇱', 'nl': '🇳🇱',
    'france': '🇫🇷', 'فرانسه': '🇫🇷', 'fr': '🇫🇷',
    'turkey': '🇹🇷', 'ترکیه': '🇹🇷', 'tr': '🇹🇷',
    'united kingdom': '🇬🇧', 'uk': '🇬🇧', 'england': '🇬🇧', 'انگلیس': '🇬🇧', 'بریتانیا': '🇬🇧', 'gb': '🇬🇧',
    'canada': '🇨🇦', 'کانادا': '🇨🇦', 'ca': '🇨🇦',
    'uae': '🇦🇪', 'dubai': '🇦🇪', 'امارات': '🇦🇪', 'دبی': '🇦🇪',
    'iran': '🇮🇷', 'ایران': '🇮🇷', 'ir': '🇮🇷',
    'finland': '🇫🇮', 'فنلاند': '🇫🇮',
    'sweden': '🇸🇪', 'سوئد': '🇸🇪',
    'switzerland': '🇨🇭', 'سوئیس': '🇨🇭',
    'russia': '🇷🇺', 'روسیه': '🇷🇺',
    'japan': '🇯🇵', 'ژاپن': '🇯🇵',
    'korea': '🇰🇷', 'کره': '🇰🇷',
    'singapore': '🇸🇬', 'سنگاپور': '🇸🇬',
    'italy': '🇮🇹', 'ایتالیا': '🇮🇹',
    'spain': '🇪🇸', 'اسپانیا': '🇪🇸',
}

def get_flag(config_line):
    original_name = ""
    if '#' in config_line:
        original_name = urllib.parse.unquote(config_line.split('#')[-1]).lower()
    
    full_text = original_name + " " + config_line.lower()
    
    for keyword, flag in COUNTRY_FLAGS.items():
        if keyword in full_text:
            return flag
    return '🌐' # پرچم پیش‌فرض اگر کشور مشخص نبود

def update_subscription():
    target_url = "https://erabinhood.ir/iran/config.php?sub"
    
    try:
        response = requests.get(target_url, timeout=15)
        raw_content = response.text.strip()
    except Exception as e:
        print(f"Error fetching source: {e}")
        return

    is_base64 = False
    try:
        decoded_bytes = base64.b64decode(raw_content)
        decoded_text = decoded_bytes.decode('utf-8')
        is_base64 = True
    except Exception:
        decoded_text = raw_content

    lines = decoded_text.splitlines()
    modified_lines = []
    index = 1

    for line in lines:
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('#'):
            continue

        flag = get_flag(line)
        new_name = f"{flag} t.me/VeEpN_vpnBot {index}"
        index += 1

        if '#' in line:
            base_config = line.split('#')[0]
            modified_line = f"{base_config}#{new_name}"
        else:
            modified_line = f"{line}#{new_name}"

        modified_lines.append(modified_line)

    final_text = "\n".join(modified_lines)

    if is_base64:
        final_output = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    else:
        final_output = final_text

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(final_output)

if __name__ == "__main__":
    update_subscription()
