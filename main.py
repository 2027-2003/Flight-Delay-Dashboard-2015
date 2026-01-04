
from src.load_data import load_flight_data

# استدعاء الدالة للحصول على البيانات
data = load_flight_data()  # <-- هذه الآن dict تحتوي على جميع البيانات

# الوصول لكل DataFrame
df_airlines = data['airlines']
df_airports = data['airports']
df_flights = data['flights']

# --- تنظيف بيانات الرحلات ---
# تعبئة القيم الفارغة في أعمدة التأخير بالصفر
delay_cols = [
    'DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'AIR_SYSTEM_DELAY',
    'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY'
]
df_flights[delay_cols] = df_flights[delay_cols].fillna(0)

# تحويل أعمدة المطار والشركة إلى نصوص
df_flights['ORIGIN_AIRPORT'] = df_flights['ORIGIN_AIRPORT'].astype(str)
df_flights['DESTINATION_AIRPORT'] = df_flights['DESTINATION_AIRPORT'].astype(str)
df_flights['AIRLINE'] = df_flights['AIRLINE'].astype(str)

# اختيار الأعمدة المهمة فقط
important_cols = [
    'YEAR', 'MONTH', 'DAY', 'DAY_OF_WEEK', 'AIRLINE',
    'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
    'DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'CANCELLED', 'DIVERTED'
]
df_flights = df_flights[important_cols]

print("تنظيف البيانات تم ✅")
print("شكل جدول الرحلات بعد التنظيف:", df_flights.shape)


# عرض أول 5 صفوف
print(df_flights.head())

# إحصاءات وصفية لأعمدة التأخير
print(df_flights[['DEPARTURE_DELAY', 'ARRIVAL_DELAY']].describe())

# عدد الرحلات الملغاة والمحوّلة
print("عدد الرحلات الملغاة:", df_flights['CANCELLED'].sum())
print("عدد الرحلات المحوّلة:", df_flights['DIVERTED'].sum())

airline_delay = df_flights.groupby('AIRLINE')['ARRIVAL_DELAY'].mean().sort_values(ascending=False)
print("متوسط تأخير الوصول حسب شركة الطيران:")
print(airline_delay.head(10))


origin_delay = df_flights.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].mean().sort_values(ascending=False)
print("أكثر مطارات الانطلاق تأخيرًا:")
print(origin_delay.head(10))

monthly_delay = df_flights.groupby('MONTH')['ARRIVAL_DELAY'].mean()
print("متوسط التأخير حسب الشهر:")
print(monthly_delay)