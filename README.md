# AlignBot Code Repository

[![Releases](https://img.shields.io/github/release/Zhefan-Xu/CERLAB-UAV-Autonomy.svg)](https://github.com/Zhefan-Xu/CERLAB-UAV-Autonomy/releases)
![Noetic Ubuntu 20.04](https://github.com/Zhefan-Xu/CERLAB-UAV-Autonomy/actions/workflows/Ubuntu20.04-build.yaml/badge.svg) 
[![license](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) 
[![Linux platform](https://img.shields.io/badge/platform-linux--64-orange.svg)](https://releases.ubuntu.com/20.04/)

[[Project page]](https://yding25.com/AlignBot/)
[[Paper]](https://arxiv.org/pdf/2409.11905)
[[Code]](https://github.com/zxzm-zak/AlignBot)
[[Video]](https://yding25.com/AlignBot/assets/images/0922video.mp4)

**AlignBot: Aligning VLM-powered Customized Task Planning with User Reminders Through Fine-Tuning for Household Robots**

[Zhaxizhuoma]()<sup>1,†</sup>,
[Pengan Chen]()<sup>1,2,†</sup>,
[Ziniu Wu]()<sup>1,3,†</sup>,
[Jiawei Sun]()<sup>1</sup>,
[Dong Wang]()<sup>1</sup>,
[Peng Zhou]()<sup>2</sup>,
[Nieqing Cao]()<sup>4</sup>,
[Yan Ding]()<sup>1,*</sup>
[Bin Zhao]()<sup>1,5</sup>,
[Xuelong Li]()<sup>1,6</sup>

<sup>1</sup>Shanghai Artificial Intelligence Laboratory,
<sup>2</sup>The University of Hong Kong,
<sup>3</sup>University of Bristol, 
<sup>4</sup>Xi’an Jiaotong-Liverpool University,
<sup>5</sup>Northwestern Polytechnical University, 
<sup>6</sup>Institute of Artificial Intelligence, China Telecom Corp Ltd

†Equal contribution, *Corresponding author: Yan Ding [yding25 (at) binghamton.edu]

## Abstract

This paper presents AlignBot, a novel framework designed to optimize VLM-powered customized task planning for household robots by effectively aligning with user reminders. In domestic settings, aligning task planning with user reminders poses significant challenges due to the limited quantity, diversity, and multimodal nature of the reminder itself. To address these challenges, AlignBot employs a fine-tuned LLaVA-7B model, functioning as an adapter for GPT-4o. This adapter model internalizes diverse forms of user reminders—such as personalized preferences, corrective guidance, and contextual assistance—into structured that prompt GPT-4o in generating customized task plans. Additionally, AlignBot integrates a dynamic retrieval mechanism that selects relevant historical interactions as prompts for GPT-4o, further enhancing task planning accuracy. To validate the effectiveness of AlignBot, experiments are conducted in a real-world household environment. A multimodal dataset with 1,500 entries derived from volunteer reminder was used for training and evaluation. The results demonstrate that AlignBot significantly improves customized task planning, outperforming existing LLM- and VLM-powered planners by interpreting and aligning with user reminders, achieving 86.8% success rate compared to the vanilla GPT-4o baseline at 21.6%, reflecting 65% improvement and over four times greater effectiveness.


## 🛠️ Installation Steps

Create a Virtual Environment and Install Dependencies
```
conda create -n AlignBot python=3.11
conda activate AlignBot
pip install -r requirements.txt
```

## ⚙️ AlignBot - LLaVA Training with LLaMA Factory
If you'd like to train LLaVA, this guide will help you get started using the LLaMA Factory framework. 
1. Install LLaMA Factory:
```
conda activate AlignBot
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```
Use pip install --no-deps -e . to resolve package conflicts.

2. Fine-Tuning with LLaMA Board GUI
```
llamafactory-cli webui
```
or also you can use the following 3 commands to run LoRA fine-tuning, inference and merging of the model:
```
llamafactory-cli train examples/train_lora/llama3_lora_sft.yaml
llamafactory-cli chat examples/inference/llama3_lora_sft.yaml
llamafactory-cli export examples/merge_lora/llama3_lora_sft.yaml
```
Models can be fine-tuned via gui and commands. There are detailed parameter adjustments in the gui, and the fine-tuned model will be saved in LLaMA-Factory/saves. Before training, need to store the entire content of the training dataset in LLaMA-Factory/data and add dataset description in dataset_info.json. How to fill in the dataset description can refer to config/dataset_info.json

3. Deploy with OpenAI-style API and vLLM by LLaMA Factory
```
API_PORT=8000 llamafactory-cli api /AlignBot/config/llavaapi_config.yaml
```
The original model path and the fine-tuned model path need to be filled in llavaapi_config.yaml.

4. For more details on training LLaVA using LLaMA Factory, please visit the official https://github.com/hiyouga/LLaMA-Factory/

## 🦾 Getting Started
Use the following commands to run model
```
main.py --mode llava --img use_url
```
- **`--mode`**: Selects the execution mode.
    - `llava`: Runs the model with reminder form LLaVA api.
    - `with_memory`: Runs the model with memory.
    - `no_memory`: Runs the model without memory.
- **`--img`**: Specifies how to handle images.
    - `use_url`: Upload or reference images via URL.
    - `use_base64`: Base64-encoded images.


## 🏷️ License
This repository is released under the MIT license. See [LICENSE](LICENSE) for additional details.
