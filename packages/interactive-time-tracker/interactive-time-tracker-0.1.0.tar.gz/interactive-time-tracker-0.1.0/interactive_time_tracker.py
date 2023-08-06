import threading
import time


class TimeIt:
    def __init__(self, func):
        self.func = func
        self._stop = False
        self._t0: float = 0.0

    def __counter(self):
        while not self._stop:
            delta = time.time() - self._t0
            print(f"{delta:.2f}s elapsed", end="\r")
            time.sleep(0.1)

        print(f'Total time elapsed: {time.time() - self._t0:.2f}s')

    def __call__(self, *args, **kwargs):
        t = threading.Thread(target=self.__counter)
        self._t0 = time.time()
        t.start()

        result = self.func(*args, **kwargs)

        self._stop = True
        return result


@TimeIt
def expensive_func():
    import time
    time.sleep(5)
    return "expensive_func"


if __name__ == "__main__":
    print(expensive_func())
