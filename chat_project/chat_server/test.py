import socket
import select
import queue
import threading
import json
import errno
import sys

from absl import app, flags

HOST = "127.0.0.1"
FLAGS = flags.FLAGS

flags.DEFINE_integer(name='port', default=None, required=True, help='사용할 서버 port 번호')
flags.DEFINE_integer(name='worker', default=2, help='필요한 worker thread의 개수')
flags.DEFINE_enum(name='format', default='json', enum_values=['json', 'protobuf'], help='메시지 포맷')

RID = 0  # room 식별 번호

clients = {}  # 연결된 client 목록
rooms = {}  # 채팅방 목록

clients_socket_list = []
clients_q = []  # client Queue
message_q = []  # message Queue

m = threading.Lock()  # mutex
cv = threading.Condition(m)  # Condition Variable

class SocketClosed(RuntimeError):
  pass


def make_json_serialized(msg, msg_type, data_type, isChat=False, chatMember=None):
    '''
    client에게 전달할 메세지를 json화 해주고\n
    serialized 해준다.\n
    (isChat, chatMember 인자는 채팅 데이터일 경우에만 사용)
    '''
    # json 데이터 생성
    message = {}
    message['type'] = msg_type
    message[data_type] = msg
    if isChat:
        message['member'] = chatMember
    message_json = json.dumps(message)

    # 2byte를 앞에 붙여줌
    serialized = bytes(message_json, 'utf-8')
    to_send = len(serialized)
    to_send_big_endian = int.to_bytes(to_send, byteorder='big', length=2)
    serialized = to_send_big_endian + serialized

    return serialized


def client_data_handler(client):
    '''
    client가 보낸 데이터를 상황에 따라서 나눠주는 함수
    '''
    # 1. 보낸 데이터 타입이 protobuf일 경우 (미 구현)
    if FLAGS.format != 'json':
        pass

    # 2. 보낸 데이터 타입이 json일 경우
    try:
        data = client.recv(1024)[2:].decode('utf-8')  # 앞의 2byte의 데이터 뺴고 json만 받음
        parsed_data = json.loads(data)
        message_type = parsed_data['type']
    except json.decoder.JSONDecodeError:
        raise (f"[sys] {clients[client]['name']}로부터 중지 명령 들어옴")

    # type_handler에 받은 메세지 타입이 있는지 확인 후 전달
    if message_type not in type_handlers:
        raise Exception('Invalid type: ' + message_type)
    else:
        type_handlers[message_type](client, parsed_data)


def message_handler(client, data):
    '''
    client들이 보내는 채팅 메시지를 관리해주는 함수
    '''
    text = data['text']
    msg_type = "SCChat"

    # producer-consumer모델로 queue 사용해 메시지 다루기 (미 구현)

    if not clients[client]['room']:
        # 1. 해당 client가 채팅방에 참가해 있지 않을 경우 -> 시스템 메세지 전송
        text = "현재 대화방에 들어가 있지 않습니다."
        msg_type = "SCSystemMessage"
        send_message_to_client(client, text, msg_type)
        return

    # 2. 해당 client가 채팅방에 참가해 있을 경우
    # 같은 채팅방에 있는 모든 참가자들에게 메세지를 전달.(자신 제외)
    send_chat_to_client(client, text, msg_type)


def onChangeName(client, data):
    '''
    /name 명령어에 대한 처리 함수\n
    client의 이름을 받아온 데이터값으로 바꿔줌 (default: (ip, port))\n
    채팅방 내에서 변경시 채팅방내 모든 사용자에게 시스템 메세지 전달
    '''
    newName = data['name']
    oldName = clients[client]['name']
    clients[client]['name'] = newName
    msg = f"이름이 {newName} 으로 변경되었습니다."
    msg_type = "SCSystemMessage"

    if not clients[client]['room']:
        # 1. 채팅방 밖에서 변경시 -> 나한테만 메세지 출력
        send_message_to_client(client, msg, msg_type)
    else:
        # 2. 채팅방 안에서 변경시 -> 방 내 모든 client에게 메세지 전달
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

    # rooms의 members를 client의 name 리스트로 변경
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
       

 # 1. 현재 참여중인 채팅방이 있는 경우
        pass
    else:
        # 2. 현재 참여중인 채팅방이 없는 경우
        title = data['title']
        roomId = str(RID + 1)
        members = [client]
        rooms[roomId] = {
            "roomId": roomId,
            "title": title,
            "members": members
        }
        RID += 1
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
        # 1. 현재 참여중인 채팅방이 있는 경우
        msg = "대화 방에 있을 때는 다른 방에 들어갈 수 없습니다."
    else:
        # 2. 현재 참여중인 채팅방이 없는 경우
        if roomId not in list(rooms.keys()):
            # 2-1. 채팅방이 존재하지 않는 경우
            pass
        else:
            # 2-2. 채팅방이 존재하는 경우
            title = rooms[roomId]['title']
            name = clients[client]['name']
            msg = f"방제 [{title}] 방에 입장했습니다."
            broad_msg = f"[{name}] 님이 입장했습니다."

            rooms[roomId]['members'].append(client)
            clients[client]['room'] = roomId

            send_message_to_room_client(client, broad_msg, msg_type)

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
        # 1. 현재 참여중인 채팅방이 없는 경우
        pass
    else:
        # 2. 현재 참여중인 채팅방이 있는 경우
        roomId = clients[client]['room']
        title = rooms[roomId]['title']
        name = clients[client]['name']
        msg = f"방제 [{title}] 대화 방에서 퇴장했습니다."
        broad_msg = f"[{name}] 님이 퇴장했습니다."

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

        send_message_to_room_client(client, broad_msg, msg_type)

    send_message_to_client(client, msg, msg_type)


def onShutdownServer(client, data):
    '''
    /shutdown 명령어에 대한 처리 함수\n
    모든 쓰레드 정리 후 시스템 종료
    '''

def send_message_to_client(client, msg, msg_type):
    '''
    client 개인에게 시스템 메세지(json)값을 전달해주는 함수
    '''
    data_type = 'text'

    # /rooms 결과 처리시
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


def send_message_to_room_client(client, msg, msg_type):
    '''
    채팅방 내에있는 모든 client(자신 미포함)에게 시스템 메세지를 보내는 함수
    '''
    serialized = make_json_serialized(msg, msg_type, 'text')
    roomId = clients[client]['room']

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

# def client_handler(server_socket, threads):
#         while True:
#             try:
#                 readables, writeables, exceptions = select.select(clients_socket_list, [], [])
#                 for sock in readables:
#                     #새로운 client 연결
#                     if sock == server_socket:
#                         #Active 소켓 생성
#                         client_socket, addr = server_socket.accept()
#                         clients[client_socket] = {
#                             "addr": addr,
#                             "name": addr, #default
#                             "room": None
#                         }
#                         with m:
#                             #clinet 대기열에 추가
#                             clients_socket_list.append(client_socket)
#                     #기존 client 통신
#                     else:
#                         #여기가 쓰레드 처리 과정이 있어야할듯한데
#                         #사용자 입력을 받는 부분임    
#                         with m:
#                             clients_q.append(sock)

#                         for t in threads:
#                             t.start()

#             except:
#                 print(f"[sys] {clients[sock]['name']}의 연결을 중단.")
#                 del clients[sock]
      

def producer(server_socket):
    while True:
        try:
            print("========================================")
            print(f"Producer[{threading.get_native_id()}]가 사용자 입력을 대기중...")
            readables, writeables, exceptions = select.select(clients_socket_list, [], [])
            for sock in readables:
                print(f"Producer[{threading.get_native_id()}]가 사용자 입력 받음")
                #새로운 client 연결
                if sock == server_socket:
                    print(f"Producer[{threading.get_native_id()}]가 새로운 사용자를 받음")
                    #Active 소켓 생성
                    client_socket, addr = server_socket.accept()
                    clients[client_socket] = {
                        "addr": addr,
                        "name": addr, #default
                        "room": None
                    }
                    with m:
                        #clinet 대기열에 추가
                        clients_socket_list.append(client_socket)
                #기존 client 통신
                else:   
                    with m:
                        print(f"Producer[{threading.get_native_id()}]가 기존 사용자로부터 데이터 받음")
                        message_q.append(sock)
                        cv.notify()
        except:
            print(f"[sys] {clients[sock]['name']} 로부터 연결 중단 요청 들어옴.")
            with m:
                print(f"[sys] {clients[sock]['name']}의 연결을 중지.")
                del clients[sock]


def consumer():
    while True:
        try:
            with m:
                print("========================================")
                print(f"Consumer[{threading.get_native_id()}]가 대기 상태로 돌입...")
                cv.wait()
                print(f"Consumer[{threading.get_native_id()}]가 작업 시작")
                if len(message_q) == 0:
                    print("message queue가 비어서 작업 못하겠음")
                else:
                    client = message_q.pop(0)
                    client_data_handler(client)
                    print(f"Consumer[{threading.get_native_id()}]가 작업을 완료함")
        except:
            print(f"Consumer[{threading.get_native_id()}]가 작업 중 뭔가 오류 발생함")
            

def process_client(client):
    '''
    연결되어있는 클라이언트로부터 온\n
    데이터를 처리해주는 함수.
    '''


def client_socket_close(client):
    '''
    강제 중지 혹은 연결이 끊킨\n
    클라이언트를 서버 소켓으로부터 연결 해제 시켜주는 함수
    ''' 
    

def server(argv):
    '''
    메인 서버 함수

    argv: 사용되지 않음
    '''
    if not FLAGS.port:
        print('서버의 Port 번호를 지정해주세요.')
        sys.exit(1)

    #TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # worker 스레드를 생성
    p_worker = []
    c_worker = []
    threads = []


    with server_socket:
        #ip주소와 port번호를 함께 socket에 바인드 한다.
        server_socket.bind((HOST, FLAGS.port))
        #Passive 소켓 생성
        server_socket.listen(10)

        #통신 대기중인 client 리스트
        clients_socket_list.append(server_socket)
        csl = [server_socket]

        for i in range(FLAGS.worker):
            if (i + 1) % 2 == 1: #홀수번 worker -> consumer thread
                t = threading.Thread(target=consumer, name=f"consumer[{i + 1}]")
                # p_worker.append(t)
                t.start()
                print(f"[sys] Consumer 작업 쓰레드 {t.name} 생성")
                threads.append(t)
            else: #짝수번 worker -> producer thread
                t = threading.Thread(target=producer, args=(server_socket,), name=f"producer[{i + 1}]")
                # c_worker.append(t)
                t.start()
                print(f"[sys] Producer 작업 쓰레드 {t.name} 생성")
                threads.append(t)

        # client_handler(server_socket, threads)

        # while True:
        #     try:
        #         readables, writeables, exceptions = select.select(clients_socket_list, [], [])
        #         for sock in readables:
        #             #새로운 client 연결
        #             if sock == server_socket:
        #                 #Active 소켓 생성
        #                 client_socket, addr = server_socket.accept()
        #                 clients[client_socket] = {
        #                     "addr": addr,
        #                     "name": addr, #default
        #                     "room": None
        #                 }
        #                 with m:
        #                     #clinet 대기열에 추가
        #                     csl.append(client_socket)
        #                     clients_socket_list.append(client_socket)
        #             #기존 client 통신
        #             else:
        #                 #올바른 입력 여부 or 중지 요청 여부 확인 
        #                 if not process_client(sock):
        #                     print(f"[sys] ({clients[sock]['addr']})클라이언트 {clients[sock]['name']} 접속 종료")
        #                     with m:
        #                         client_socket_close(sock)

        #     except SocketClosed:
        #         print(f"[sys] 서버를 중지합니다.")
        #         break

        for t in threads:
            t.join()
            print(f"[sys] 작업 쓰레드[{t.name}] 을 종료함.")
            

if __name__ == "__main__":
    app.run(server)