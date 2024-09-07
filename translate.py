import os
import time

from openai import OpenAI
import json

client = OpenAI(
    api_key = os.environ.get("ARK_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
)

def translate(pre_txt, txt):
    # Non-streaming:
    print("================================================")
    print(txt)
    # 重试
    for i in range(3):
        try:
            completion = client.chat.completions.create(
                model = "ep-20240901132849-dnk7p",  # your model endpoint ID
                messages = [
                    {"role": "system", "content": f"你需要把用户发送的内容重写小学生可以理解的文字，不需要复述原文，也不需要发表个人的评论， 也不需要提到作者, 尽量保留原文的意思。 请直接返回重写后的文字。可以参考前一个段落的内容如下：{pre_txt}"},
                    {"role": "user", "content": txt},
                ],
            )
            time.sleep(1)
            return completion.choices[0].message.content
        except Exception as e:
            print(e)
        #休眠1分钟
        print("sleep 1 min")
        time.sleep(60)

def save_to_json(paragraphs, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    name = "水滸傳.json"
    input_file = f"chunks/{name}"
    output_char_dir = f"小学生/水浒传/"

    # 读取output_file的内容
    with open(input_file, 'r', encoding='utf-8') as f:
        chapters = json.load(f)
        file_chunks = []
        # 使用豆包的API进行翻译
        last_txt = ""

        for chapter in chapters:
            chapter_chunks = []
            next_line = 1
            #如果文件存在
            if os.path.exists(output_char_dir + f"{chapter[0]}.json"):
                with open(output_char_dir + f"{chapter[0]}.json", 'r', encoding='utf-8') as f:
                    chapter_chunks = json.load(f)
                    next_line = chapter_chunks[-1][0] + 1

            line = 1
            for paragraph in chapter:
                if line < next_line:
                    print(f"{chapter[0]} skip {line}")
                    line += 1
                    continue
                if line == 1:
                    chapter_chunks.append([line, paragraph, paragraph])
                    is_first = False
                else:
                    # 翻译
                    translated_paragraph = translate(last_txt, paragraph)
                    print(translated_paragraph)
                    chapter_chunks.append([line, paragraph, translated_paragraph])
                    last_txt = translated_paragraph

                save_to_json(chapter_chunks, output_char_dir + f"{chapter[0]}.json")
                line += 1
            file_chunks.append(chapter_chunks)


