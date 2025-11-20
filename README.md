```
VLN-Qwen/
├── assets/              # 运行过程中的视觉快照 (Step-by-step screenshots)
├── core/
│   ├── bot_eyes.py      # [Vision] VLM 交互接口，处理 Prompt 与图像推理
│   └── bot_body.py      # [Control] AI2-THOR 环境封装，处理动作空间
├── main.py              # [Planner] 主程序，包含 CoT 思维链与决策循环
├── requirements.txt     # 项目依赖
└── README.md            # 项目文档
```
