# timems

Use this package to easily convert various time formats to seconds.


## What is it?

```py
from timems import ms

ms('2w') # 1209600
ms('1m') # 60
```

## How to use?

```py
from timems import ms
import asyncio

asyncio.sleep(ms('1h')) # sleeping 3600 sec. / 1h
```

## Formats

```
m, min, minute, h, ho, hour, d, day, w, week, y, year, mon, month, y, year
```

## Find a Bug?

Report it [here](https://github.com/AlmondPark/timems.py/issues)