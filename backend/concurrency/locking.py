
import threading

# Store locks for individual bank accounts
_account_locks = {}
_registry_lock = threading.Lock()


def get_account_lock(bank_name, account_id):
    """Return a unique lock for each bank account."""
    key = f"{bank_name}:{account_id}"

    with _registry_lock:
        if key not in _account_locks:
            _account_locks[key] = threading.RLock()

        return _account_locks[key]


def acquire_account_lock(bank_name, account_id):
    """Acquire the lock for an account."""
    lock = get_account_lock(bank_name, account_id)
    lock.acquire()
    print(f"{bank_name}:{account_id} - LOCK ACQUIRED")
    return lock


def release_account_lock(bank_name, account_id, lock):
    """Release the lock for an account."""
    lock.release()
    print(f"{bank_name}:{account_id} - LOCK RELEASED")
