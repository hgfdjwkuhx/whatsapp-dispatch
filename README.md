# Whatsapp message sending script
### Dependency
Please use that fork https://github.com/AragurDEV/yowsup

### Usage
Create a file named `run.py` in directory above with next content
```python
from whatsapp_dispatch import YowsupEchoStack

credentials = ("79600722162", "J3ZbSap/PS0E4aSHmyF1+FFlLLI=")
stack = YowsupEchoStack(credentials)
stack.start()
```

Execute script like that `python run.py`
