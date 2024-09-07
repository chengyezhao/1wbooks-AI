import os
import json
from bs4 import BeautifulSoup
from opencc import OpenCC
from pathlib import Path

# 每次最多翻译1000字
MAX_TRANSLATE_LENGTH = 2000
# 短的段落可以合并
MIN_TRANSLATE_LENGTH = 50


def save_to_json(paragraphs, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    name = "西游记.json"
    input_file = f"D:\\source\\1wbooks\\raw\\{name}"
    output_file = f"chunks/{name}"

    #读取output_file的内容
    with open(input_file, 'r', encoding='utf-8') as f:
        chapters = json.load(f)
        # 使用豆包的API进行翻译
        file_chunks = []
        for chapter in chapters:
            last_paragraph = ""
            chapter_chunks = []
            is_first= True
            for paragraph in chapter:
                if len(paragraph) == 0:
                    continue
                if is_first:
                    #标题
                    chapter_chunks.append(paragraph)
                    is_first = False
                    continue
                #如果段落过长
                if len(paragraph) > MAX_TRANSLATE_LENGTH:
                    print(len(paragraph))
                    print(paragraph)
                    # 如果之前已经有current_paragraph，则翻译之前的current_paragraph
                    if len(last_paragraph) > 0:
                        chapter_chunks.append(last_paragraph)

                    last_paragraph = ""
                    current_len = 0
                    #对文字按照分隔符。进行拆分成小于MAX_TRANSLATE_LENGTH的块，然后翻译
                    split_arr = paragraph.split('。')
                    #过滤掉空的段落
                    split_arr = [p for p in split_arr if len(p) > 0]
                    i = 0
                    if len(split_arr) > 1:
                        for p in split_arr:
                            if current_len + len(p) < MAX_TRANSLATE_LENGTH:
                                last_paragraph += p + '。'
                                current_len += len(p)
                            else:
                                #如果后续剩下的文字很短
                                if len(paragraph) - len(last_paragraph) <= 2 * MIN_TRANSLATE_LENGTH:
                                    last_paragraph += p + '。'
                                    current_len += len(p)
                                else:
                                    # 加入翻译间隔
                                    last_paragraph += "####" + p + '。'
                                    # print(len(last_paragraph))
                                    current_len = len(p)
                            i += 1
                    else:
                        last_paragraph += paragraph

                    if len(last_paragraph) > 0 :
                        print(last_paragraph)
                        chapter_chunks.append(last_paragraph)
                        # print(len(last_paragraph))
                        last_paragraph = ""


                elif len(paragraph) <= MIN_TRANSLATE_LENGTH:
                    if len(paragraph) + len(last_paragraph) < MAX_TRANSLATE_LENGTH:
                        last_paragraph += paragraph
                        continue
                    else:
                        chapter_chunks.append(last_paragraph)
                        last_paragraph = paragraph
                else:
                    # 如果之前已经有current_paragraph，则翻译之前的current_paragraph
                    if len(last_paragraph) > 0:
                        chapter_chunks.append(last_paragraph)
                        last_paragraph = ""

                    # 翻译current_paragraph
                    chapter_chunks.append(paragraph)

            if len(last_paragraph) > 0:
                chapter_chunks.append(last_paragraph)
                last_paragraph = ""

            file_chunks.append(chapter_chunks)

        save_to_json(file_chunks, output_file)
