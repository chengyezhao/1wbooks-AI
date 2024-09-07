import os
import json
from bs4 import BeautifulSoup
from opencc import OpenCC
from pathlib import Path


def extract_paragraphs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    #查找所有p或者h2开头的段落
    paragraphs = soup.find_all(['p', 'h2'])
    return [p.get_text() for p in paragraphs]

def convert_to_simplified(text):
    cc = OpenCC('t2s')
    return cc.convert(text)

def process_html_files(directory):
    all_paragraphs = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = Path(root) / file
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                paragraphs = extract_paragraphs(html_content)
                simplified_paragraphs = [convert_to_simplified(p) for p in paragraphs]
                all_paragraphs.append(simplified_paragraphs)
    
    return all_paragraphs

def save_to_json(paragraphs, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_directory = "D:\\source\\hanchuancaolu-master\\莊子"
    output_file = "raw/莊子.json"

    paragraphs = process_html_files(input_directory)
    save_to_json(paragraphs, output_file)
    print(f"处理完成的段落已保存到 {output_file}")
