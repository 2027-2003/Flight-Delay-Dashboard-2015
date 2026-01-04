import pandas as pd
from pathlib import Path
import os

# تحديد مسار مجلد البيانات بشكل آمن
BASE_DIR = Path(os.path.dirname(__file__)).parent
DATA_DIR = BASE_DIR / 'data'


# دالة لتحميل البيانات الثلاثة
def load_flight_data():
    """
    تحميل بيانات airlines, airports, و flights من مجلد data
    """
    files = {
        'airlines': 'airlines.csv',
        'airports': 'airports.csv',
        'flights': 'flights.csv'
    }

    data = {}
    for key, filename in files.items():
        path = DATA_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"لم أجد الملف: {path}")
        df = pd.read_csv(path)
        data[key] = df

    return data


# اختبار عند تشغيل هذا الملف مباشرة
if __name__ == "_main_":
    data = load_flight_data()
    print("=== Airlines ===")
    print(data['airlines'].head(3))
    print("\n=== Airports ===")
    print(data['airports'].head(3))
    print("\n=== Flights ===")
    print(data['flights'].head(3))