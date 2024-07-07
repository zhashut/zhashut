import requests
import os
import re
from pathlib import Path

# 你的语雀文档ID和cookie
YUQUE_DOC_ID = '24381935'

def get_word_count(doc_id, cookie):
    url = f'https://www.yuque.com/api/books/{doc_id}/overview'
    headers = {
        'cookie': f'cookie={cookie}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['data']['wordCount']
    else:
        raise Exception(f"Failed to fetch data, status code: {response.status_code}")


def update_readme(word_count):
    # 确保README.md存在
    readme_path = Path('README.md')
    if not readme_path.is_file():
        raise Exception("README.md not found in the current directory.")

    # 读取README.md内容
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配 <strong> 标签内的内容
    # 假设标签格式为 <strong>数字</strong>
    pattern = re.compile(r'<strong>(\d+)</strong>')

    # 使用正则表达式替换标签内的内容
    # 将匹配到的数字替换为新的字数
    updated_content = pattern.sub(r'<strong>' + str(word_count) + '</strong>', content)

    # 写回更新后的内容到README.md
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)


def main():
    COOKIE = os.environ.get('YUQUE_COOKIE')
    # 确保cookie不为空
    if not COOKIE:
        raise ValueError("The cookie value cannot be empty.")
    try:
        word_count = get_word_count(YUQUE_DOC_ID, COOKIE)
        update_readme(word_count)
        print(f"Updated README.md with word count: {word_count}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
