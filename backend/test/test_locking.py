
from threading import Thread
from time import sleep
from backend.concurrency.locking import (
    acquire_account_lock,
    release_account_lock
)



def test_account_lock(bank, account, thread_name):
    lock = acquire_account_lock(bank, account)

    try:
        print(f"{thread_name}: Entered critical section")
        sleep(2)
        print(f"{thread_name}: Leaving critical section")
    finally:
        release_account_lock(bank, account, lock)


thread1 = Thread(
    target=test_account_lock,
    args=("Bank_A", "A1001", "Thread 1")
)

thread2 = Thread(
    target=test_account_lock,
    args=("Bank_B", "B1001", "Thread 2")
)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("\nDifferent account concurrency test completed.")

print("\n--- SAME ACCOUNT CONCURRENCY TEST ---")

thread1 = Thread(
    target=test_account_lock,
    args=("Bank_A", "A1001", "Thread 1")
)

thread2 = Thread(
    target=test_account_lock,
    args=("Bank_A", "A1001", "Thread 2")
)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("\nSame account concurrency test completed.")
