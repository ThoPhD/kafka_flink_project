import argparse
import json
import random
from datetime import datetime
from uuid import uuid4

import clickhouse_connect
from confluent_kafka import Producer
from faker import Faker

fake = Faker()


# Generate user data
def gen_user_data(num_user_records: int) -> None:
    for id in range(num_user_records):
        client = clickhouse_connect.get_client(host='localhost', username='flinkuser', password='flinkpass')
        client.command(
            """CREATE DATABASE IF NOT EXISTS commerce"""
        )

        client.command(
            """CREATE TABLE IF NOT EXISTS commerce.users(
                id UInt32,
                email String,
                username String,
                password String
            )
            ENGINE = MergeTree()
            PRIMARY KEY (id)
             """
        )
        # client.command(
        #     """CREATE TABLE IF NOT EXISTS commerce.products (
        #          id UUID,
        #          name String,
        #          description String,
        #          price Float64
        #      ) ENGINE = MergeTree() 
        #      PRIMARY KEY (id)"""
        # )

        client.command(
            """INSERT INTO commerce.users
             (id, username, password) VALUES (%s, %s, %s)""",
            (id, fake.user_name(), fake.password()),
        )

        # client.command(
        #     """INSERT INTO commerce.products
        #      (id, name, description, price) VALUES (%s, %s, %s, %s)""",
        #     (fake.uuid4(), fake.name(), fake.text(), fake.random_int(min=1, max=100)),
        # )

        # update 10 % of the time
        # if random.randint(1, 1000) >= 900:
        #     client.command(
        #         "UPDATE commerce.users SET username = %s WHERE id = %s",
        #         (fake.user_name(), id),
        #     )
        #     client.command(
        #         "UPDATE commerce.products SET name = %s WHERE id = %s",
        #         (fake.name(), fake.uuid4()),
        #     )
    return


# Stream clicks and checkouts data


# Generate a random user agent string
def random_user_agent():
    return fake.user_agent()


# Generate a random IP address
def random_ip():
    return fake.ipv4()


# Generate a click event with the current click_time
def generate_click_event(user_id, product_id=None):
    click_id = str(uuid4())
    product_id = product_id or str(uuid4())
    product = fake.word()
    price = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    url = fake.uri()
    user_agent = random_user_agent()
    ip_address = random_ip()
    click_time = datetime.now()

    click_event = {
        "click_id": click_id,
        "user_id": user_id,
        "product_id": product_id,
        "product": product,
        "price": price,
        "url": url,
        "user_agent": user_agent,
        "ip_address": ip_address,
        "click_time": click_time.strftime("%Y-%m-%d %H:%M:%S.%f")[
            :-3
        ],
    }

    return click_event


# Generate a checkout event with the current checkout_time
def generate_checkout_event(user_id, product_id):
    payment_method = fake.credit_card_provider()
    total_amount = fake.pyfloat(left_digits=3, right_digits=2, positive=True)
    shipping_address = fake.address()
    billing_address = fake.address()
    user_agent = random_user_agent()
    ip_address = random_ip()
    checkout_time = datetime.now()

    checkout_event = {
        "checkout_id": str(uuid4()),
        "user_id": user_id,
        "product_id": product_id,
        "payment_method": payment_method,
        "total_amount": total_amount,
        "shipping_address": shipping_address,
        "billing_address": billing_address,
        "user_agent": user_agent,
        "ip_address": ip_address,
        "checkout_time": checkout_time.strftime("%Y-%m-%d %H:%M:%S.%f")[
            :-3
        ],
    }

    return checkout_event


# Function to push the events to a Kafka topic
def push_to_kafka(event, topic):
    producer = Producer({'bootstrap.servers': 'localhost:9093'})
    producer.produce(topic, json.dumps(event).encode('utf-8'))
    producer.flush()


def gen_clickstream_data(num_click_records: int) -> None:
    for _ in range(num_click_records):
        user_id = random.randint(1, 100)
        click_event = generate_click_event(user_id)
        push_to_kafka(click_event, 'clicks')

        # simulate multiple clicks & checkouts 50% of the time
        while random.randint(1, 100) >= 50:
            click_event = generate_click_event(
                user_id, click_event['product_id']
            )
            push_to_kafka(click_event, 'clicks')

            push_to_kafka(
                generate_checkout_event(
                    click_event["user_id"], click_event["product_id"]
                ),
                'checkouts',
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-nu",
        "--num_user_records",
        type=int,
        help="Number of user records to generate",
        default=1000,
    )
    parser.add_argument(
        "-nc",
        "--num_click_records",
        type=int,
        help="Number of click records to generate",
        default=1000,
    )
    args = parser.parse_args()
    gen_user_data(args.num_user_records)
    gen_clickstream_data(args.num_click_records)
    print(
        f"Generated {args.num_user_records} user records and {args.num_click_records} click records."
    )
    print("Data generation completed successfully.")
    print("You can now run the Kafka consumer to process the data.")
