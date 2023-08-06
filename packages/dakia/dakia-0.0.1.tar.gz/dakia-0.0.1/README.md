Drop dead simple alerts and updates for every project on any platfrom!
This package lets your code send messages to you about its status.
As of now, the best option is using Telegram (other platforms will be added in the future).

Drop this into your code:


## Installation
```python
pip install dakia
```

## Usage
```python
from dakia import Dakia

cryptoBearDakia = Dakia(token='secret1', chatId='something2')
cryptoBullDakia = Dakia(token='secret1', chatId='something2')

genDakia = Dakia(token='secret3', chatId='something3')

# Multiple messengers for seprate tasks / projects
if win:
    cryptoBullDakia('brrr')
    else:
    cryptoBearDakia('oof')


genDakia.dak(f"🔥 #new-user-signup {username}")
genDakia.dak(f"💵 #sale {amount}")
genDakia.dak(f"🌟 #project-{projectName} deployed successfully")


genDakia.dak('warning', '#project-quotes-crawler : Memory usage > 80%')

```





d = dakia.dak('hi') # Keep it short
d('hi')