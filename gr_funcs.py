import json
import re

import gradio as gr
import pandas as pd
from pandas import DataFrame

import llm_server

sys_prompt = '你是一名经验丰富的导师，正在知道学生写毕业论文。'


def gen_paper_title(prompt):
    user_prompt = f'{prompt}。\n请为我提供5个该方向的论文选题，要求体现学术创新性。\n' \
                  f'返回结果需要json格式。\n' \
                  f'示例：{{"选题列表": [{{"序号": 1, "选题": "论文选题", "描述": "选题描述"}}, ...]}}'

    response = llm_server.request_llm(sys_prompt, [(user_prompt, None)])
    llm_response = next(response)

    paper_title_list = json.loads(llm_response)['选题列表']

    title_no_list = [f'选题{i + 1}' for i in range(len(paper_title_list))]
    return pd.DataFrame(paper_title_list), gr.update(choices=title_no_list, visible=True)


def get_paper_title(title_list: DataFrame, selected_title: str):
    title_no = int(selected_title.replace('选题', ''))
    title_info = title_list.iloc[title_no - 1]

    title_name = title_info['选题']
    title_desc = title_info['描述']

    return title_name, title_desc


def visible_paper_outline(title_list: DataFrame, selected_title: str):
    title_name, title_desc = get_paper_title(title_list, selected_title)
    prompt = f'请根据以下内容，生成 5-6 个章节的论文大纲，要求符合毕业论文格式。\n论文题目：{title_name}, 题目描述：{title_desc}'

    return gr.update(visible=True), \
           gr.update(visible=True), \
           gr.update(value=prompt, visible=True)


def gen_paper_outline(paper_bg, prompt):
    user_prompt = f'{prompt}\n学生背景：{paper_bg}\n请用 MarkDown 格式返回，并以"### `论文题目`大纲"为开头。'
    response = llm_server.request_llm(sys_prompt, [(user_prompt, None)], stream=True)

    final_content = ''
    for chunk_content in response:
        final_content = chunk_content
        yield chunk_content, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    paper_text_prompt = '请你根据我提供的论文大纲写一篇完成论文，完成每一章节详细内容，总字数6000-7000字左右。\n' \
                        '涉及到你无法生成的内容，如：图表，你需要标注出来。' \
                        '同样，对于需要阅读参考文献的地方，你也需要标注出来。' \
                        '标注的内容单独占一行，黑体显示，以"注意你需要做的："开头。示例：**注意你需要做的：阅读xxx文献了解xxx相关的内容，补充在xxx地方**'
    yield final_content, gr.update(visible=True), gr.update(value=paper_text_prompt, visible=True), gr.update(visible=True)


def gen_paper_text(paper_bg, paper_outline, prompt):
    user_prompt = f'{prompt}\n' \
                  f'## 学生背景：{paper_bg}\n' \
                  f'## 论文大纲\n{paper_outline}\n' \
                  f'**论文大纲**的第一行格式是"`论文题目` 大纲"\n' \
                  f'请你用 MarkDown 格式返回，并以"### `论文题目` 正文" 开始。完成每一章节详细内容，总字数6000-7000字左右'

    response = llm_server.request_llm(sys_prompt, [(user_prompt, None)], stream=True)

    for chunk_content in response:
        yield chunk_content
