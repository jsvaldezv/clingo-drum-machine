## Clingo Drum Machine

<img width="995" alt="builder" src="https://user-images.githubusercontent.com/47612276/143788853-f8e6d8c9-085d-445d-990b-ada0aa87f816.png">

Interactive drum machine using Python and Clingo where you can select which sound will be the kick, the snare, and the hihat. The solver will then create a sound design and a beat, providing you with the best loop based on centroid, spread, and maximum peak. The solver is based on Answer Set Programming using Clingo.

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
