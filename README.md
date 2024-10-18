# Installation Steps
Create a Virtual Environment and Install Dependencies
```
conda create -n AlignBot python=3.11
conda activate AlignBot
pip install -r requirements.txt
```

# AlignBot - LLaVA Training with LLaMA Factory
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

# Getting Started
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