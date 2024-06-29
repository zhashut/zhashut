import requests
import os
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

    # 读取并更新README.md内容
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 假设wordCount是直接文本，替换它
    updated_content = content.replace('wordCount', str(word_count))

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
