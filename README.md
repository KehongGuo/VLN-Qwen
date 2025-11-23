# VLN-qwen

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

## Future Work (Related Papers)

| Title | Key Method / Concept | Links |
| :--- | :--- | :--- |
| **SLAM-Former: Putting SLAM into One Transformer** | **[SLAM-Former]** 将传统的 SLAM 前端（跟踪）和后端（建图）整合进一个单一的 Transformer 网络中。虽然它是几何 SLAM，但其端到端的设计思路可以为您未来升级“视觉特征提取”模块提供灵感。 | [arXiv:2509.16909](https://arxiv.org/abs/2509.16909) |
| **ReMEmbR: Building and Reasoning Over Long-Horizon Spatio-Temporal Memory for Robot Navigation** | **[ReMEmbR]** 使用 VLM 构建时空语义记忆库，支持长程推理和模糊查询。**您的项目 `build_map.py` 的核心理念与之高度对齐**，即“先建图，后问询”的范式。 | [arXiv:2409.13682](https://arxiv.org/abs/2409.13682) |
| **JanusVLN: Decoupling Semantics and Spatiality with Dual Implicit Memory for Vision-Language Navigation** | **[JanusVLN]** 模仿人脑左右半球，将“语义理解”和“空间感知”解耦为两套隐式记忆。解决了 VLM 在处理纯空间几何关系时“晕头转向”的问题，是解决您遇到的“路径回溯”精度问题的高级方案。 | [arXiv:2509.22548](https://arxiv.org/abs/2509.22548) |
| **MapNav: A Novel Memory Representation via Annotated Semantic Maps for Vision-and-Language Navigation** | **[MapNav]** 提出用“注记语义地图 (Annotated Semantic Map)”来替代笨重的历史视频帧。这本质上就是您 `memory.json` 的**工业级完全体**，它证明了基于文本/语义标签的稀疏地图在端侧部署上的巨大优势。 | [arXiv:2502.13451](https://arxiv.org/abs/2502.13451) |
| **WMNav: Integrating Vision-Language Models into World Models for Object Goal Navigation** | **[WMNav]** 结合世界模型（World Model）与 VLM。机器人可以在脑海中“想象”动作的后果（例如：走这条走廊可能会看到厨房），从而在不动身的情况下优化路径规划。这是“智能巡逻”策略的终极形态。 | [arXiv:2503.02247](https://arxiv.org/abs/2503.02247) |
| **Rethinking the Embodied Gap in Vision-and-Language Navigation: A Holistic Study of Physical and Visual Disparities** | **[VLN-PE]** 提出了 VLN-PE 基准，专门研究仿真算法部署到真机（如机器狗）时遇到的光照、碰撞和物理限制问题。面试时提到它，能证明您对 **Sim-to-Real** 落地难点有深刻认知。 | [arXiv:2507.13019](https://arxiv.org/abs/2507.13019) |