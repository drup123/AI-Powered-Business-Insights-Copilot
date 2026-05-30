import os

def extract_lines(lines, start_str, end_str):
    out = []
    capture = False
    for line in lines:
        if start_str in line and not capture:
            capture = True
        if capture:
            out.append(line)
        if end_str in line and capture:
            break
    return out

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. config.py
with open('config.py', 'w', encoding='utf-8') as f:
    f.write('GROQ_API_KEY = "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"\n')
    f.write('GROQ_MODEL   = "llama-3.1-8b-instant"\n')
    f.write('DATASET_PATH = "improved_business_dataset.csv"\n\n')
    f.write('CORR_STRONG   = 0.6\n')
    f.write('CORR_MODERATE = 0.3\n')
    f.write('CORR_WEAK     = 0.2\n')
    f.write('DIFF_THRESHOLD = 0.05\n')
    f.write('PALETTE = ["#6366f1", "#38bdf8", "#34d399", "#fb923c", "#f472b6", "#a78bfa", "#facc15"]\n')

# 2. data_layer.py
with open('data_layer.py', 'w', encoding='utf-8') as f:
    f.write('import os\nimport pandas as pd\nimport streamlit as st\nfrom config import DATASET_PATH\n\n')
    f.writelines(lines[164:181])

# 3. intent_engine.py
with open('intent_engine.py', 'w', encoding='utf-8') as f:
    f.writelines(lines[186:234])

# 4. analysis_engine.py
with open('analysis_engine.py', 'w', encoding='utf-8') as f:
    f.write('import pandas as pd\nfrom config import CORR_STRONG, CORR_MODERATE, CORR_WEAK, DIFF_THRESHOLD\n\n')
    f.writelines(lines[239:426])
    f.write('\n')
    f.writelines(lines[431:484])
    f.write('\n')
    f.writelines(lines[489:532])
    f.write('\n')
    f.writelines(lines[537:606])

# 5. llm_layer.py
with open('llm_layer.py', 'w', encoding='utf-8') as f:
    f.write('import json\nimport hashlib\nfrom groq import Groq\nfrom config import GROQ_MODEL\n\n')
    f.writelines(lines[610:637])
    f.write('\n')
    f.writelines(lines[642:703])

# 6. visualizations.py
with open('visualizations.py', 'w', encoding='utf-8') as f:
    f.write('import plotly.express as px\nimport plotly.graph_objects as go\nimport pandas as pd\nfrom config import PALETTE\n\n')
    f.writelines(lines[708:716])
    f.write('\n')
    vis_lines = lines[719:778]
    # Insert the plotly figure code
    # def plot_visuals(df: pd.DataFrame, result: dict) -> tuple:
    #     intent = result["intent"]
    #     tbl    = result["table"]
    new_vis_lines = []
    for line in vis_lines:
        new_vis_lines.append(line)
        if line.strip() == 'tbl    = result["table"]':
            new_vis_lines.append('\n    if tbl is None or tbl.empty:\n        return go.Figure(), go.Figure()\n')
    f.writelines(new_vis_lines)

print("Split logic created.")
