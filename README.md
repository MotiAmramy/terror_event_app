# analyze terror events

analyze terror events is a Python project for dealing with terror analyze and show them on mpas.

## Installation

```bash
pip install kafka-python-ng pandas pymongo elasticsearch Flask folium
```



## Usage

```
הפרויקט נועד לתכנן וליישם פלטפורמה אנליטית לניתוח 
והצגת נתונים על טרור עולמי בעבר ממספר מקורות,
 בין השנים 1970 ל-2022, וגם להזין נתונים 
 בזמן אמת שמגיעים ממקור של API של אתר חדשות.
הפלטפורמה תשלב ארכיטקטורת מיקרו-שירותים, 
ועליכם לבחור את מסדי הנתונים המתאימים למשימות המתאימות,
 מערכות מסרים (messaging) מתאימות במידת הצורך 
ורכיבי עיבוד מידע מתאימים (Pandas, Numpy, Spark וכו').
```


## Architecture
This project is based on a modular architecture that separates concerns into well-defined components:
- **Frontend**: Built with folium maps using html/css/js for user interactions.
- **Backend**: flask app for API handling and api request.
- **Database**: MongoDB for data storage and elastic search for data storage.
- **Deployment**: Hosted on github.


## GitHub repository

```python
https://github.com/MotiAmramy/terror_event_app.git
```

