# load_logs.py — 접속 로그 1,000건 생성·적재 (몇 번 돌려도 결과가 같다)
import random
from datetime import datetime, timedelta
from pymongo import MongoClient

random.seed(42)

client = MongoClient('mongodb://localhost:27017')
col = client['logdb']['access_logs']

deleted = col.delete_many({'source': 'load_logs'}).deleted_count

levels = ['INFO', 'INFO', 'INFO', 'WARN', 'ERROR']
paths = ['/', '/login', '/search', '/api/pay', '/mypage']
base = datetime(2026, 8, 31, 9, 0, 0)

docs = []
for i in range(1000):
    level = random.choice(levels)
    doc = {
        'ts': base + timedelta(seconds=i * 3),
        'level': level,
        'path': random.choice(paths),
        'status': 500 if level == 'ERROR' else 200,
        'user': 'u' + str(random.randint(1, 50)).zfill(3),
        'source': 'load_logs',
    }
    if level == 'ERROR':
        doc['error'] = {
            'code': 'E' + str(random.randint(10, 99)),
            'message': 'auto-generated'
        }
    docs.append(doc)

result = col.insert_many(docs)
print('deleted:', deleted, '/ inserted:', len(result.inserted_ids))
