import threading
import time

class WatcherThread(threading.Thread):
    def __init__(self, threads_to_watch):
        super(WatcherThread, self).__init__()
        self.threads_to_watch = threads_to_watch
        self.daemon = True  # 데몬 스레드로 설정하여 메인 스레드 종료 시 함께 종료되도록 함
        self._exit_event = threading.Event()

    def stop(self):
        self._exit_event.set()

    def run(self):
        while not self._exit_event.is_set():
            for thread in self.threads_to_watch:
                if not thread.is_alive():
                    print(f"감시 대상 스레드 {thread.name}에서 문제가 발생했습니다.")
                    # 여기에서 추가적인 작업 수행 가능
            time.sleep(1)  # 1초 주기로 감시

def target_function(thread_name):
    try:
        # 의도적으로 예외 발생
        raise Exception("감시 대상 스레드에서 의도적으로 예외 발생")
    except Exception as e:
        print(f"{thread_name} 스레드에서 예외 발생: {e}")

# 감시될 스레드들을 생성
thread1 = threading.Thread(target=target_function, args=("Thread-1",), name="Thread-1")
thread2 = threading.Thread(target=target_function, args=("Thread-2",), name="Thread-2")

# 감시자 스레드 생성
watcher_threads = [thread1, thread2]
watcher = WatcherThread(watcher_threads)

# 스레드 시작
for thread in watcher_threads:
    thread.start()

watcher.start()

# 모든 스레드의 종료를 대기
for thread in watcher_threads:
    thread.join()

# 감시자 스레드 종료
watcher.stop()
watcher.join()

print("메인 스레드 종료")
