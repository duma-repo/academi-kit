import gradio as gr
import config
import gr_funcs

css = """
    #box_shad { box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.6); /* 设置阴影 */ }
"""

with gr.Blocks(title="论文助手", theme=gr.themes.Soft(), analytics_enabled=False, css=css) as demo:
    gr.Markdown('## 一、确定选题')
    with gr.Row():
        paper_title_exp = '例如：我是一名本科生，专业是人工智能专业，现在要写学士毕业论文'
        paper_title = gr.Text(value='我是一名本科生，专业是人工智能专业，现在要写学士毕业论文', label='确定选题', placeholder=paper_title_exp, container=False, elem_id='box_shad', scale=5)
        paper_title_btn = gr.Button('生成选题', variant='primary', scale=1)

    paper_title_list = gr.Dataframe(label='选择选题', visible=False, interactive=False)

    with gr.Row():
        paper_title_radio = gr.Radio(visible=True, container=False, interactive=True)

    paper_outline_md = gr.Markdown('## 二、论文大纲', visible=False)
    with gr.Row():
        paper_outline_prompt = gr.Text(container=False, interactive=True, visible=False, elem_id='box_shad', scale=5)
        paper_outline_btn = gr.Button('生成论文大纲', variant='primary', visible=False, scale=1)

    paper_outline = gr.Markdown()

    paper_text_md = gr.Markdown('## 三、论文正文', visible=False)
    with gr.Row():
        paper_text_prompt = gr.Text(elem_id='box_shad', container=False, visible=False, scale=5)
        paper_text_btn = gr.Button('生成正文', visible=False, variant='primary', scale=1)
    paper_text = gr.Markdown()

    # 选题
    paper_title_btn.click(lambda: gr.update(visible=True), outputs=[paper_title_list])
    paper_title_btn.click(gr_funcs.gen_paper_title, inputs=[paper_title], outputs=[paper_title_list, paper_title_radio])

    paper_title_radio.change(gr_funcs.visible_paper_outline,
                             inputs=[paper_title_list, paper_title_radio],
                             outputs=[paper_outline_btn, paper_outline_md, paper_outline_prompt])

    # 大纲
    paper_outline_btn.click(gr_funcs.gen_paper_outline,
                            inputs=[paper_title, paper_outline_prompt],
                            outputs=[paper_outline, paper_text_md, paper_text_prompt, paper_text_btn])

    # 正文
    paper_text_btn.click(gr_funcs.gen_paper_text, inputs=[paper_title, paper_outline, paper_text_prompt], outputs=[paper_text])

demo.launch()

