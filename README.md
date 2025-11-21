```
VLN-Qwen/
├── assets/              # 运行过程中的视觉快照 (Step-by-step screenshots)
├── core/
│   ├── bot_eyes.py      # [Vision] VLM 交互接口，处理 Prompt 与图像推理
│   ├── bot_body.py      # [Control] AI2-THOR 环境封装，处理动作空间
│   └── bot_memory.py    # [record] 机器人记忆，记录探索节点以供llm回溯
├── main.py              
├── requirements.txt     
├── build_map.py         # [Step1] 初步探索整个地图
├── find_item.py         # [Step2] 根据指令寻找物品    
└── README.md            
```
