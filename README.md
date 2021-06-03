# Find Covid-19 Vaccine Availibility

> It is difficult to scan the avaiibilty of covid-19 vaccine at one go in cowin portal
> and it's even more difficult to do it all day. Thanks to this code, it allows you to run it
> and let it scane the cowin portal for you. When it finds vaccine slot between 5 to 200
> it gives you a small notification sound and if it's more than 200 a big notification sound.
> (* these settings are configurable and one can chnage them as required)

### Requirements

```python
import requests
import pandas as pd
import beepy
```

### Run command

```bash
python3 fetch_vaccine_info.py --date "31-05-2021" --city "bangalore" --token "" --save_csv "y" --dose 2 --age_limit 45

```

### Sample display output

```bash
110092 | Free | 03-06-2021 | DGD I.P. Extn. | COVISHIELD
110092 | Free | 05-06-2021 | DGD I.P. Extn. | COVISHIELD
110092 | Free | 07-06-2021 | DGD I.P. Extn. | COVISHIELD
110092 | Free | 03-06-2021 | GGSSS Kiran Vihar Site -3 | COVISHIELD
110092 | Free | 04-06-2021 | GGSSS Kiran Vihar Site -3 | COVISHIELD
110092 | Free | 05-06-2021 | GGSSS Kiran Vihar Site -3 | COVISHIELD
```

### For complete output have a look at

> 03-05-2021_bangalore_45_plus_dose-2.csv

### Thanks to the data and services being used in the project

[Co-WIN Public APIs](https://apisetu.gov.in/public/marketplace/api/cowin)

### For support

Please star the Repo and share it. Thanks !!
