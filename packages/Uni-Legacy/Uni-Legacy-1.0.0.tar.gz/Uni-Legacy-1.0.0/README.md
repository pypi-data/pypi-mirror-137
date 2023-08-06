# Uni-Legacy
--- ---
###### Uni-Legacy is a Python library used to Sinhala unicode font Converte to legacy font offline.
 - ###### FM legacy Font
 - ###### Isi legacy Font

## Installation
###### To install, run the following command:
```bash
python3 pip install Uni-Legacy
```

## for FM fonts
###### Sinhala Unicode convert to FM font type
```python
from uni_legacy import uni2fm
Unicode_font = "සිංහල යුනිකේත"
FM_font = uni2fm(Unicode_font)
print(FM_font)
```

## for Isi fonts
###### Sinhala Unicode convert to Isi font type

```python
from uni_legacy import uni2isi
Unicode_font = "සිංහල යුනිකේත"
Isi_font = uni2isi(Unicode_font)
print(Isi_font)
```