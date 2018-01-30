# Whatsapp message sending script
### Dependency
Please use that fork https://github.com/AragurDEV/yowsup
```git submodule update --init --recursive
cd yowsup
python setup.py install
```

### Registration
```
yowsup-cli registration --requestcode sms --phone 7XXXXXXXXXX --cc 7 --mcc 250 --mnc 20 --env android
yowsup-cli registration --register 294701 --phone 7XXXXXXXXXX --cc 7
```

### Usage
Create a file named `run.py` in directory above with next content
```python
from whatsapp_dispatch import YowsupEchoStack

credentials = ("7XXXXXXXXXX", "J3ZbSap/PS0E4aSHmyF1+FFlLLI=")
stack = YowsupEchoStack(credentials)
stack.start()
```

Execute script like that `python run.py`
