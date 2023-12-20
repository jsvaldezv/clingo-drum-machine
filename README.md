## Smart Builder

<img width="995" alt="builder" src="https://user-images.githubusercontent.com/47612276/143788853-f8e6d8c9-085d-445d-990b-ada0aa87f816.png">

Smart drum machine with Python and Clingo where you can choose which sound will be the kick, which the snare and which the hihat. Then, the A.I. will make a sound
design, a beat and will give you the best loop based on the centroid, spread and maximun peak. The intelligence is based on Answer Set Programming using Clingo.

## Local running

### 1. Create venv
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
(venv) pip install -r requirements.txt
```

### 3. Run main file
```bash
(venv) python Python/main.py
```

## Recommendations

### 1. Run black to format your files with Python coding standards
```bash
(venv) black .
```
