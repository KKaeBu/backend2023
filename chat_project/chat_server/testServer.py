import socket
import select
import queue
import threading
import json

# 서버 설정
HOST = '127.0.0.1'
PORT = 9140

# 클라이언트 소켓과 큐를 저장할 딕셔너리
clients = {}
message_queues = {}

# Lock 객체 생성 (클라이언트와 메시지 큐에 대한 안전한 동시 액세스 보장)
lock = threading.Lock()

# 함수: 메시지 핸들러
def process_command(client_socket, command):
    # 이전에 정의한 클라이언트 메시지 핸들러와 동일한 로직을 사용
    pass

# 함수: 클라이언트 메시지 핸들러
def process_client_message(client_socket, messages):
    for msg in messages:
        msg_type = msg.get('type')

        if msg_type == 'COMMAND':
            process_command(client_socket, msg)
        else:
            print(f'Unknown message type: {msg_type}')

# 함수: 소켓으로부터 메시지를 읽고 처리
def process_socket(client_socket):
    received_buffer = client_socket.recv(1024)
    if not received_buffer:
        return False

    with lock:
        if not message_queues.get(client_socket):
            message_queues[client_socket] = queue.Queue()

    try:
        message = json.loads(received_buffer.decode('utf-8'))
        with lock:
            message_queues[client_socket].put(message)
    except json.JSONDecodeError:
        print('Error decoding JSON')

    return True

# 함수: 클라이언트에게 메시지를 전송
def send_message(client_socket, message):
    try:
        serialized = json.dumps(message).encode('utf-8')
        client_socket.send(serialized)
        return True
    except Exception as e:
        print(f'Error sending message: {e}')
        return False

# 함수: 새로운 클라이언트 연결 처리
def handle_new_connection(server_socket):
    client_socket, addr = server_socket.accept()
    with lock:
        clients[client_socket] = addr
        message_queues[client_socket] = queue.Queue()

    print(f'Accepted connection from {addr}')

# 함수: 클라이언트에게 메시지 전송을 처리하는 쓰레드
def message_sender_thread(client_socket):
    while True:
        try:
            message = message_queues[client_socket].get_nowait()
            if not send_message(client_socket, message):
                break
        except queue.Empty:
            # 메시지 큐가 비어있으면 넘어감
            pass
        except Exception as e:
            print(f'Error in message_sender_thread: {e}')
            break

# 함수: 메인 서버 루프
def server_loop():
    # 서버 소켓 생성 및 설정
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    # non-blocking으로 설정
    server_socket.setblocking(0)

    # 입력으로 받을 것들을 read set 에 추가
    inputs = [server_socket]

    while True:
        readable, _, _ = select.select(inputs, [], [])

        for s in readable:
            if s is server_socket:
                # 새로운 연결이 들어오면 핸들링
                handle_new_connection(server_socket)
            else:
                # 기존 클라이언트에서 데이터를 읽고 처리
                if not process_socket(s):
                    # 소켓이 닫혔으면 연결 제거
                    with lock:
                        print(f'Connection closed from {clients[s]}')
                        del clients[s]
                        del message_queues[s]
                        inputs.remove(s)
                        s.close()

        # 모든 클라이언트에게 메시지 전송 처리
        with lock:
            for client_socket in clients.keys():
                threading.Thread(target=message_sender_thread, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    server_loop()
