# log_analysis.py - максимально простой вариант
import pandas as pd
import matplotlib.pyplot as plt
import json

print("="*60)
print("ПРОСТОЙ АНАЛИЗ ЛОГОВ")
print("="*60)

# 1. Загрузка данных
print("\n1. Загружаю файл botsv1.json...")

try:
    with open('botsv1.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Превращаем JSON в таблицу
    events = []
    for item in data:
        events.append(item['result'])
    
    df = pd.DataFrame(events)
    print(f"✓ Загружено {len(df)} событий")
    
except FileNotFoundError:
    print("✗ Ошибка: Файл botsv1.json не найден!")
    print("  Положи файл в папку:", os.getcwd())
    exit()

# 2. Ищем подозрительные события
print("\n2. Ищу подозрительные события...")

# Список подозрительных EventID
suspicious_ids = ['4703', '4688', '4689', '4624']

# Описания событий
event_names = {
    '4703': 'Изменение прав',
    '4688': 'Создание процесса',
    '4689': 'Завершение процесса', 
    '4624': 'Успешный вход'
}

# Отбираем подозрительные события
suspicious = []
for idx, row in df.iterrows():
    event_id = str(row.get('EventCode', ''))
    if event_id in suspicious_ids:
        event_info = {
            'время': row.get('_time', 'неизвестно'),
            'компьютер': row.get('ComputerName', 'неизвестно'),
            'event_id': event_id,
            'событие': event_names.get(event_id, 'неизвестно'),
            'подробно': row.get('Message', '')[:100] + '...' if len(str(row.get('Message', ''))) > 100 else row.get('Message', '')
        }
        suspicious.append(event_info)

# Создаем DataFrame с подозрительными событиями
suspicious_df = pd.DataFrame(suspicious)

print(f"✓ Найдено {len(suspicious_df)} подозрительных событий")

# 3. Статистика
print("\n3. Статистика подозрительных событий:")
stats = suspicious_df['событие'].value_counts()
for event, count in stats.items():
    print(f"   - {event}: {count} раз")

# 4. Рисуем график
print("\n4. Рисую график...")

plt.figure(figsize=(10, 6))

# Топ-10 событий (если их меньше, покажем все)
top_events = suspicious_df['событие'].value_counts().head(10)

# Рисуем столбики
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
plt.bar(range(len(top_events)), top_events.values, color=colors[:len(top_events)])

# Настройки графика
plt.title('Топ-10 подозрительных событий', fontsize=16)
plt.xlabel('Тип события', fontsize=12)
plt.ylabel('Количество', fontsize=12)
plt.xticks(range(len(top_events)), top_events.index, rotation=45)

# Добавляем цифры на столбики
for i, v in enumerate(top_events.values):
    plt.text(i, v + 0.5, str(v), ha='center', fontsize=11)

plt.tight_layout()

# Сохраняем график
plt.savefig('my_suspicious_events.png')
print("✓ График сохранен как 'my_suspicious_events.png'")

# Показываем график
plt.show()

# 5. Сохраняем результаты
print("\n5. Сохраняю результаты...")
suspicious_df.to_csv('suspicious_events.csv', index=False)
print("✓ Результаты сохранены в 'suspicious_events.csv'")

print("\n" + "="*60)
print("ГОТОВО! Проверь файлы:")
print("   - my_suspicious_events.png (график)")
print("   - suspicious_events.csv (таблица с событиями)")
print("="*60)
