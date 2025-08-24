from rq import Connection, Worker

from app.tasks.queue import get_queue, get_redis_connection


def run() -> None:
    connection = get_redis_connection()
    queue = get_queue()
    with Connection(
        connection=connection,
    ):
        worker = Worker(
            queues=[queue],
        )
        worker.work(
            with_scheduler=True,
        )


if __name__ == "__main__":
    run()


