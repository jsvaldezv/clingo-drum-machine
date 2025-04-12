## 🥁 Clingo Drum Machine

https://github.com/user-attachments/assets/2125b154-0439-4d83-9fea-bf9eb8464c61

This project is an interactive drum machine built with Python and Clingo. It allows you to choose which sounds will represent the kick, snare, and hi-hat. Using Answer Set Programming (ASP) via Clingo, the system then analyzes and selects the best combination of sound design and rhythm pattern.

The solver evaluates multiple beat configurations and selects the optimal loop based on centroid, spectral spread, and maximum peak, aiming to create a musically cohesive and dynamic groove. This fusion of audio analysis and logic programming results in a powerful tool for generative beat creation.

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
