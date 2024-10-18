# AlignBot

```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```

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
