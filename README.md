# AI_tools_Network_Engineering
A collection of tools created using Codes AI.

## Local Web App
This repo now includes a lightweight Flask app that provides:
- IPv4 decimal ↔ binary conversion with per-octet detail.
- Usable host calculations from IPv4 CIDR blocks.

### Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in your browser. If port 5000 is busy, run
`PORT=5001 python app.py` and use `http://127.0.0.1:5001`.
