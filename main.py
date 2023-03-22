import socket
import cv2
import pickle
import struct

# create socket
weights = "yunet.onnx"
face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.68.106'  # paste your server ip address here
port = 9999
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4096)  # 4K
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = cv2.resize(pickle.loads(frame_data), (1280, 960), cv2.INTER_AREA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    # detect faces
    face_detector.setInputSize((1280, 960))

    _, faces = face_detector.detect(frame)
    faces = faces if faces is not None else []
    for face in faces:
        box = list(map(int, face[:4]))
        color = (0, 0, 255)
        thickness = 2
        cv2.rectangle(frame, box, color, thickness, cv2.LINE_AA)
    cv2.imshow("Sharo's eyes", frame)
    if cv2.waitKey(1) == 27:
        break
client_socket.close()
