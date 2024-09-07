import json
import os
from pathlib import Path

import re

# 中文数字到阿拉伯数字的映射表
cn2num = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '十': 10, '百': 100, '千': 1000, '万': 10000
}


def chinese_to_number(chinese):
    total = 0
    unit = 1
    prev_unit = 1

    if chinese.startswith('十'):
        # 处理"十"开头的情况，比如"十五"应为15，而"十"应为10
        total += 10
        chinese = chinese[1:]

    for i in range(len(chinese) - 1, -1, -1):
        curr_char = chinese[i]
        if curr_char in cn2num:
            num = cn2num[curr_char]
            if num >= 10:
                unit = num
                prev_unit = unit
            else:
                total += num * prev_unit
                prev_unit = 1
        else:
            prev_unit = 1

    return total


def extract_number_from_filename(filename):
    match = re.search(r'第(.+?)回', filename)
    if match:
        chinese_number = match.group(1)
        return chinese_to_number(chinese_number)
    return 0



if __name__ == "__main__":
    directory = "小学生/水浒传"
    # 生成一个html，分成两列，左边列是原文，右边列是译文

    output_file = f"成品/小学生版水浒传.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("<html><body><h1>水浒传</h1>")

        for root, dirs, files in os.walk(directory):
            # files里面的文件名是中文的数字，例如第一回，第一百回这种，需要按照数字的来排序
            sorted_files = sorted(files, key=extract_number_from_filename)
            for ff in sorted_files:
                print(ff)
            for input_file in sorted_files:
                file_path = Path(root) / input_file
                with open(file_path, 'r', encoding='utf-8') as f2:
                    # f.write("<tr><td><h3>原文<h3></td><td><h3>译文</h3></td>")

                    paragraphs = json.load(f2)

                    is_first = True
                    for paragraph in paragraphs:
                        if is_first:
                            f.write("<h2>" + paragraph[2] + "</h2><table>")
                            is_first = False
                        else:
                            f.write("<tr><td>")
                            f.write("<p>"+ paragraph[1] + "<br><br></p></td>")
                            f.write("<td>")
                            f.write("<p>"+ paragraph[2] + "<br><br></p>")
                            f.write("</tr>")
                f.write("</table>")
        f.write("</body></html>")

    #markdown

    output_file = f"小学生版水浒传.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 水浒传"+ "\n\n")

        for root, dirs, files in os.walk(directory):
            # files里面的文件名是中文的数字，例如第一回，第一百回这种，需要按照数字的来排序
            sorted_files = sorted(files, key=extract_number_from_filename)
            for ff in sorted_files:
                print(ff)
            for input_file in sorted_files:
                file_path = Path(root) / input_file
                with open(file_path, 'r', encoding='utf-8') as f2:
                    paragraphs = json.load(f2)

                    is_first = True
                    # f.write("<tr><td><h3>原文<h3></td><td><h3>译文</h3></td>")
                    for paragraph in paragraphs:
                        # f.write("<tr>")
                        if is_first:
                            f.write("## " + paragraph[2]+ "\n\n")
                            is_first = False
                        else:
                            # f.write("<td>")
                            # f.write("<p>"+ paragraph[1] + "<br><br></p></td>")
                            # f.write("<td>")
                            f.write(paragraph[2] + "\n\n")
