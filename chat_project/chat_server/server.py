import socket
import select
import queue
import threading
import json
import errno
import time
import sys

from absl import app, flags

import message_pb2 as pb

HOST = "127.0.0.1"
FLAGS = flags.FLAGS

flags.DEFINE_integer(name='port', default=9140, help='사용할 서버 port 번호 (default: 9140)')
flags.DEFINE_integer(name='worker', default=2, help='필요한 worker thread의 개수 (default: 2)')
flags.DEFINE_enum(name='format', default='json', enum_values=['json', 'protobuf'], help='메시지 포맷')

RID = 0 #room 식별 번호

clients = {} #연결된 client 목록
rooms = {} #채팅방 목록
message_queue = queue.Queue() #쓰레드간 통신을 위한 큐

#공유 자원을 위한 뮤텍스 설정
clients_lock = threading.Lock()
rooms_lock = threading.Lock()
message_lock = threading.Lock()

#쓰레드간 통신을 위한 Condition Variable
message_cv = threading.Condition(message_lock)

exit_flag = False #쓰레드를 종료시키기 위한 플래그

def worker_thread_handler():
    '''
    작업 쓰레드들을 Message Queue의\n
    데이터 여부에 따라서 작업을 처리해주는 쓰레드 함수\n
    (consumer 역할)
    '''
    global exit_flag
    while not exit_flag:
        try:
            #큐에 메세지가 들어오기를 기다림
            with message_lock:
                message_cv.wait()
                message_data = message_queue.get(block=True, timeout=1)
                if message_data is not None:
                    client, parsed_data = message_data
                    message_type = parsed_data['type']
                    type_handlers[message_type](client, parsed_data)
        except queue.Empty:
            pass


def make_json_serialized(msg, msg_type, data_type, isChat=False, chatMember=None):
    '''
    client에게 전달할 메세지를 json화 해주고\n
    serialized 해준다.\n
    (isChat, chatMember 인자는 채팅 데이터일 경우에만 사용)
    '''
    #json 데이터 생성
    message = {}
    message['type'] = msg_type
    message[data_type] = msg
    if isChat:
        message['member'] = chatMember
    message_json = json.dumps(message)

    #2byte를 앞에 붙여줌
    serialized = bytes(message_json, 'utf-8')
    to_send = len(serialized)
    to_send_big_endian = int.to_bytes(to_send, byteorder='big', length=2)
    serialized = to_send_big_endian + serialized

    return serialized

def client_data_handler(client):
    '''
    client가 보낸 데이터를 지정한 타입으로 파싱\n
    파싱된 데이터를 Message Queue에 넣어줌\n
    (producer 역할)
    '''
    #1. 보낸 데이터 타입이 protobuf일 경우 (구현 중)
    if FLAGS.format != 'json':
        pass
    else:
        #2. 보낸 데이터 타입이 json일 경우
        data = client.recv(1024)[2:].decode('utf-8') #앞의 2byte의 데이터 뺴고 json만 받음
        parsed_data = json.loads(data)
        message_type = parsed_data['type']

    #type_handler에 받은 메세지 타입이 있는지 확인 후 전달
    if message_type not in type_handlers:
        raise Exception('Invalid type: ' + message_type)
    else:
        #메세지 큐(작업 큐)에 데이터를 넣음
        with message_lock:
            message_queue.put((client, parsed_data))
            message_cv.notify()


def message_handler(client, data):
    '''
    client들이 보내는 채팅 메시지를 관리해주는 함수
    '''
    text = data['text']
    msg_type = "SCChat"

    if not clients[client]['room']:
        #1. 해당 client가 채팅방에 참가해 있지 않을 경우 -> 시스템 메세지 전송
        text = "현재 대화방에 들어가 있지 않습니다."
        msg_type = "SCSystemMessage"
        send_message_to_client(client, text, msg_type)
        return

    #2. 해당 client가 채팅방에 참가해 있을 경우
    #같은 채팅방에 있는 모든 참가자들에게 메세지를 전달.(자신 제외)
    send_chat_to_client(client, text, msg_type)



def onChangeName(client, data):
    '''
    /name 명령어에 대한 처리 함수\n
    client의 이름을 받아온 데이터값으로 바꿔줌 (default: (ip, port))\n
    채팅방 내에서 변경시 채팅방내 모든 사용자에게 시스템 메세지 전달
    '''
    with clients_lock:
        newName = data['name']
        oldName = clients[client]['name']
        clients[client]['name'] = newName
    msg = f"이름이 {newName} 으로 변경되었습니다."
    msg_type = "SCSystemMessage"

    if not clients[client]['room']:
        #1. 채팅방 밖에서 변경시 -> 나한테만 메세지 출력
        send_message_to_client(client, msg, msg_type)
    else:
        #2. 채팅방 안에서 변경시 -> 방 내 모든 client에게 메세지 전달
        msg = f"{oldName} 의 이름이 {newName} 으로 변경되었습니다."
        send_message_to_all_client(msg, msg_type)
    
    
    print(f"[sys] {clients[client]['addr']}의 이름이 {newName}으로 변경되었습니다.")


def onShowRoomList(client, data):
    '''
    /rooms 명령어에 대한 처리 함수.\n
    생성되어있는 채팅방 목록을 client에게 전달해줌\n
    (방ID, 방 이름, 방 Members)

    data: 사용되지 않음
    '''
    msg_type = "SCRoomsResult"
    room_arr = []

    #rooms의 members를 client의 name 리스트로 변경
    with rooms_lock:
        for room in rooms:
            room_data = {}
            room_data['roomId'] = rooms[room]['roomId']
            room_data['title'] = rooms[room]['title']
            members = rooms[room]['members']
            members_name = []
            for m in members:
                members_name.append(clients[m]['name'])
            room_data['members'] = members_name

            room_arr.append(room_data)


    send_message_to_client(client, room_arr, msg_type)
    

def onCreateRoom(client, data):
    '''
    /create 명령어에 대한 처리 함수\n
    새로운 채팅방을 받아온 데이터값을 이름으로 생성해줌\n
    생성과 동시에 해당 사용자는 만들어진 채팅방에 입장하게됨
    '''
    global RID

    msg = "대화 방에 있을 때는 방을 개설 할 수 없습니다."
    msg_type = "SCSystemMessage"

    if clients[client]['room']:
        #1. 현재 참여중인 채팅방이 있는 경우
        pass
    else:
        #2. 현재 참여중인 채팅방이 없는 경우
        with rooms_lock:
            title = data['title']
            roomId = str(RID + 1)
            members = [client]
            rooms[roomId] = {
                "roomId": roomId,
                "title": title,
                "members": members
            }
            RID += 1

        with clients_lock:
            clients[client]['room'] = roomId

        msg = f"방제 [{title}] 방에 입장했습니다."
        print(f"[sys] 새로운 채팅방 {title} 을 개설했습니다.")

    send_message_to_client(client, msg, msg_type)


def onJoinRoom(client, data):
    '''
    /join 명령어에 대한 처리 함수\n
    client를 받아온 데이터에 있는 채팅방으로 입장시켜줌\n
    기존 채팅방 입장시 모든 사용자에게 입장 메세지 전달\n
    없는 방 입장 시도시 시스템 메세지 전달
    '''
    roomId = str(data['roomId'])
    msg = "대화방이 존재하지 않습니다."
    msg_type = "SCSystemMessage"

    if clients[client]['room']:
        #1. 현재 참여중인 채팅방이 있는 경우
        msg = "대화 방에 있을 때는 다른 방에 들어갈 수 없습니다."
    else:
        #2. 현재 참여중인 채팅방이 없는 경우
        if roomId not in list(rooms.keys()):
            #2-1. 채팅방이 존재하지 않는 경우
            pass
        else:
            #2-2. 채팅방이 존재하는 경우
            with rooms_lock:
                title = rooms[roomId]['title']
                name = clients[client]['name']
                msg = f"방제 [{title}] 방에 입장했습니다."
                broad_msg = f"[{name}] 님이 입장했습니다."

                rooms[roomId]['members'].append(client)
            
            with clients_lock:
                clients[client]['room'] = roomId

        send_message_to_room_client(client, roomId, broad_msg, msg_type)

    send_message_to_client(client, msg, msg_type)


def onLeaveRoom(client, data):
    '''
    /leave 명령어에 대한 처리 함수\n
    client가 현재 들어가 있는 채팅방을 떠나게 해줌\n
    채팅방 떠날시 채팅방에 남아있는 모든 client들에게 시스템 메세지 전달\n
    채팅방에 속해있지 않을 경우 시스템 메세지 전달

    :data 사용되지 않음
    '''
    msg = "현재 대화방에 들어가 있지 않습니다."
    msg_type = "SCSystemMessage"

    if not clients[client]['room']:
        #1. 현재 참여중인 채팅방이 없는 경우
        pass
    else:
        #2. 현재 참여중인 채팅방이 있는 경우
        with rooms_lock:
            roomId = clients[client]['room']
            title = rooms[roomId]['title']
            name = clients[client]['name']
            msg = f"방제 [{title}] 대화 방에서 퇴장했습니다."
            broad_msg = f"[{name}] 님이 퇴장했습니다."

            #rooms에서 해당 client 제거
            members = rooms[roomId]['members']
            index = members.index(client)
            members.pop(index)

        with clients_lock:
            #client의 room값 업데이트 -> None
            clients[client]['room'] = None

        with rooms_lock:
            #본인이 나갈시 방에 남은 인원이 없는 경우 -> 방폭
            if len(members) == 0:
                print(f"[sys] roomId: {roomId}방을 인원 부족으로 방폭")
                del rooms[roomId]
            else:
                send_message_to_room_client(client, roomId, broad_msg, msg_type)

    send_message_to_client(client, msg, msg_type)


def onShutdownServer(client, data):
    '''
    /shutdown 명령어에 대한 처리 함수\n
    모든 쓰레드 정리 후 시스템 종료
    '''
    #메인 쓰레드와 작업 쓰레드 모두 종료 시킨다.
    global exit_flag
    exit_flag = True

    #서버 종료를 client에게 알림
    msg = "서버가 종료됩니다."
    msg_type = "SCSystemMessage"
    send_message_to_all_client(msg, msg_type)
    
    #작업 스레드가 shutdowon 명령 처리시 메인 스레드는
    #select()문에서 blocking되있음 하지만 그전까지 exit_flag의 값이 false라
    #해당 스레드에서 값을 바꿔도 다음 사용자 입력 혹은 연결이 올때까지 인지할 수 없었음
    #그래서 일부로 사용자 입력을 집어넣어 메인 스레드에서
    #exit_flag의 값이 바뀐것을 알려줌
    #shut_socket은 단순히 분기문을 실행시키기 위한 수단임
    shut_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    shut_socket.connect((HOST, FLAGS.port))



def send_message_to_client(client, msg, msg_type):
    '''
    client 개인에게 시스템 메세지(json)값을 전달해주는 함수
    '''
    data_type = 'text'

    #/rooms 결과 처리시
    if isinstance(msg, list):
        data_type = 'rooms'

    serialized = make_json_serialized(msg, msg_type, data_type)

    client.send(serialized)


def send_message_to_all_client(msg, msg_type):
    '''
    전체 client(자신 포함)에게 시스템 메세지를 보내는 함수
    '''
    serialized = make_json_serialized(msg, msg_type, 'text')

    for client in clients:
        client.send(serialized)

def send_message_to_room_client(client, roomId, msg, msg_type):
    '''
    채팅방 내에있는 모든 client(자신 미포함)에게 시스템 메세지를 보내는 함수
    '''
    serialized = make_json_serialized(msg, msg_type, 'text')

    for c in clients:
        if c != client and clients[c]['room'] == roomId:
            c.send(serialized)

def send_chat_to_client(client, msg, msg_type):
    '''
    채팅 메세지를 채팅방 내에있는 모든 client(자신 미포함)전달하는 함수
    '''
    member = clients[client]['name']
    serialized = make_json_serialized(msg, msg_type, 'text', True, member)
    roomId = clients[client]['room']

    for c in clients:
        if c != client and clients[c]['room'] == roomId:
            c.send(serialized)



type_handlers = {
    'CSChat': message_handler,
    'CSName': onChangeName,
    'CSRooms': onShowRoomList,
    'CSCreateRoom': onCreateRoom,
    'CSJoinRoom': onJoinRoom,
    'CSLeaveRoom': onLeaveRoom,
    'CSShutdown': onShutdownServer,
}

def handle_client_disconnect(client):
    # 해당 클라이언트가 채팅방에 속해있다면
    if clients[client]['room']:
        roomId = clients[client]['room']
        name = clients[client]['name']
        broad_msg = f"[{name}] 님이 퇴장했습니다."
        msg_type = "SCSystemMessage"

        with rooms_lock:
            # rooms에서 해당 client 제거
            members = rooms[roomId]['members']
            index = members.index(client)
            members.pop(index)

            # client의 room값 업데이트 -> None
            clients[client]['room'] = None

            # 본인이 나갈시 방에 남은 인원이 없는 경우 -> 방폭
            if len(members) == 0:
                print(f"[sys] roomId: {roomId}방을 인원 부족으로 방폭")
                del rooms[roomId]
            else:
                send_message_to_room_client(client, roomId, broad_msg, msg_type)


def server(argv):
    '''
    메인 서버 함수

    argv: 사용되지 않음
    '''
    global exit_flag

    #TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    with server_socket:
        #ip주소와 port번호를 함께 socket에 바인드 한다.
        server_socket.bind((HOST, FLAGS.port))
        #Passive 소켓 생성
        server_socket.listen(10)
        #대기중인 client socket
        clients_socket_list = [server_socket]

        #worker 쓰레드 생성
        worker_threads = []
        for i in range(FLAGS.worker):
            thread = threading.Thread(target=worker_thread_handler, name=f"작업 쓰레드[{i}]")
            thread.start()
            print(f"{thread.name} 을 생성 및 실행")
            worker_threads.append(thread)
        
        try:
            while not exit_flag:
                readables, writeables, exceptions = select.select(clients_socket_list, [], [])
                for sock in readables:
                    try:    
                        #서버 종료를 위한 분기문
                        if exit_flag:
                            raise Exception
                                            
                        #새로운 client 연결
                        if sock == server_socket:
                            #Active 소켓 생성
                            client_socket, addr = server_socket.accept()
                            clients[client_socket] = {
                                "addr": addr,
                                "name": addr, #default
                                "room": None
                            }
                            #client 대기열에 추가
                            with clients_lock:
                                clients_socket_list.append(client_socket)
                            print(f"[sys] new client {addr} 가 연결됨.")
                        #기존 client 통신
                        else:
                            #client가 보낸 데이터 처리
                            client_data_handler(sock)
                    except socket.error as err:
                        if err.errno == errno.ECONNRESET:
                            print("[sys] 소켓 error로 인한 client 소켓 연결 해제")
                            #client 연결 중지 처리
                            with clients_lock:
                                # 클라이언트 연결 해제 처리
                                print(f"[sys] {clients[sock]['addr']}와의 연결이 끊어졌습니다.")
                                handle_client_disconnect(sock)
                                clients_socket_list.remove(sock)
                                del clients[sock]
                                print("[sys] 연결 해제됨.")
                    except json.decoder.JSONDecodeError:
                        print("[sys] 키보드 중지 입력으로인한 client 소켓 연결 해제")
                        #client 연결 중지 처리
                        with clients_lock:
                            # 클라이언트 연결 해제 처리
                            print(f"[sys] {clients[sock]['addr']}와의 연결을 해제중...")
                            handle_client_disconnect(sock)
                            clients_socket_list.remove(sock)
                            del clients[sock]
                            print("[sys] 연결 해제됨.")               
        except KeyboardInterrupt:
            print("[sys] 키보드 중지 요청으로 인한 서버 종료.")
        except:
            pass
        finally:
            exit_flag = True
            with message_lock:
                message_queue.put(None)  # 워커 스레드에 종료 신호를 보냅니다
                message_cv.notify_all()

            print("[sys] 메인 쓰레드 종료중")
            for thread in worker_threads:
                print(f"[sys] {thread.name}의 join() 실행")
                thread.join()
                print(f"[sys] {thread.name}의 join() 종료")

        print("[sys] 메인 쓰레드 종료.")

if __name__ == "__main__":
    app.run(server)