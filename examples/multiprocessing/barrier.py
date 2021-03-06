import time

from lithops.multiprocessing import Pool, Barrier, SimpleQueue, getpid


def f(barrier, q):
    barrier.wait()
    pid = getpid()
    ts = time.time()
    msg = 'process: {} - timestamp: {}'.format(pid, ts)
    q.put(msg)


if __name__ == "__main__":
    q = SimpleQueue()
    n = 4
    barrier = Barrier(n)

    with Pool() as p:
        p.map_async(f, [[barrier, q]] * (n - 1))  # all - 1

        print('Result queue empty:', q.empty())

        time.sleep(3)
        p.apply_async(f, [barrier, q])
        for _ in range(n):
            print(q.get())
