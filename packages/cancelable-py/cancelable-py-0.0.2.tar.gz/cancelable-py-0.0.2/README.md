# Installation
```
pip install cancelable-py
```

# Usage
Without the normal time package:

```python
from cancelable import time
import threading

def count():
  i = 1
  while True:
    time.sleep(1)
    print(i)
    i += 1

threading._start_new_thread(count, ())

input("Click enter to cancel counting\n")

time.cancel()
```
With the normal time package:
```python
from cancelable import time as cancelableTime
import threading

def count():
  i = 1
  while True:
    cancelableTime.sleep(1)
    print(i)
    i += 1

threading._start_new_thread(count, ())

input("Click enter to cancel counting\n")

cancelableTime.cancel()
```

# To do
Add more functions such as input()