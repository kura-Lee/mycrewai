import os
from crewai import Crew, Agent, Task, LLM, Process
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

LLM_CONFIG = {
    "model": "glm-4.5-air",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "base_url": os.getenv("OPENAI_BASE_URL"),
    "temperature": 0.2
}

model = LLM(**LLM_CONFIG)

# 1. 定义三个 Agent
researcher = Agent(
    role="AI趋势分析师",
    goal="分析2025年最重要的3个AI发展趋势",
    backstory="你是资深AI行业分析师，擅长精准预判技术趋势。",
    llm=model,
    verbose=True
)

writer = Agent(
    role="科技内容创作者",
    goal="将AI趋势分析写成通俗易懂的公众号文章",
    backstory="你擅长用生动比喻解释复杂技术，让普通读者也能理解。",
    llm=model,
    verbose=True
)

editor = Agent(
    role="内容编辑",
    goal="优化文章质量并生成规范的Markdown文件",
    backstory="你是专业的内容编辑，擅长修正语法错误、优化逻辑结构、确保格式规范。",
    llm=model,
    verbose=True
)

# 2. 定义任务依赖链
t1 = Task(
    description="分析2025年最值得关注的3个AI趋势，每个趋势包含技术特点和应用前景",
    expected_output="结构化的趋势报告：\n\n## 2025年AI趋势分析\n\n### 趋势一：[名称]\n**核心概述**（50字）\n**技术要点**（100字）\n**应用前景**（50字）\n\n### 趋势二：[名称]\n**核心概述**（50字）\n**技术要点**（100字）\n**应用前景**（50字）\n\n### 趋势三：[名称]\n**核心概述**（50字）\n**技术要点**（100字）\n**应用前景**（50字）",
    agent=researcher
)

t2 = Task(
    description="基于趋势分析报告，写一篇800字的文章，要求生动有趣、通俗易懂",
    expected_output="文章格式：\n\n**吸引人的标题**（15-25字）\n\n**引人入胜的开头**（100字）\n\n**正文**（600字）：用生动比喻解释3个AI趋势，强调对普通人的影响\n\n**总结思考**（100字）：给出有价值的建议\n\n总字数：800字左右",
    agent=writer,
    context=[t1]
)

# 生成动态文件名
current_time = os.popen('date +"%Y%m%d-%H%M"').read().strip()
output_filename = f"AI趋势分析-{current_time}.md"

t3 = Task(
    description="审核文章：1.修正语法/拼写错误 2.优化段落逻辑 3.确保关键词自然融入 4.调整标题吸引力",
    expected_output="最终的完整Markdown格式文章，包含标题、正文、结尾等完整结构",
    agent=editor,
    context=[t2],
    output_file=output_filename
)

# 3. 组 Crew 并开跑
content_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[t1, t2, t3],
    process=Process.sequential,
    verbose=True
)
result = content_crew.kickoff()
print(result)
