import asyncio
import json
import threading
from typing import Dict, List

from kafka import KafkaConsumer, KafkaProducer
import aiohttp

KAFKA_BROKER = 'localhost:9092'

_topic_threads: Dict[str, threading.Thread] = {}
_subscribers: Dict[str, List[str]] = {}
_producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def subscribe(topic: str, endpoint: str):
    _subscribers.setdefault(topic, []).append(endpoint)

    if topic not in _topic_threads:
        t = threading.Thread(target=_run_topic_consumer, args=(topic,), daemon=True)
        _topic_threads[topic] = t
        t.start()


def _run_topic_consumer(topic: str):
    asyncio.run(_consume_topic(topic))


def publish(topic: str, payload: dict):
    _producer.send(topic, payload)
    _producer.flush()


def close():
    _producer.close()


async def _consume_topic(topic: str):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id=f"group_{topic}",
        auto_offset_reset="latest"
    )

    async with aiohttp.ClientSession() as session:
        for msg in consumer:
            for endpoint in _subscribers.get(topic, []):
                await _post(session, endpoint, msg.value)


async def _post(session: aiohttp.ClientSession, endpoint: str, data: dict):
    try:
        async with session.post(endpoint, json=data, timeout=30) as resp:
            print(f"Posted to {endpoint}: {resp.status}")
    except Exception as e:
        print(f"Failed posting to {endpoint}: {e}")
