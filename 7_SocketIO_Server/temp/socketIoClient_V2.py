import socketio

# Tạo một client socketio
sio = socketio.Client()

# Khi kết nối thành công
@sio.event
def connect():
    print('Kết nối thành công')

# Khi nhận được sự kiện 'my_event' từ server
@sio.event
def my_event(data):
    print('Nhận được sự kiện:', data)

# Kết nối tới server socketio
sio.connect('http://100.100.100.4:5000')

# Kích hoạt sự kiện 'my_event' và truyền dữ liệu
sio.emit('SKRX', '{"topic":"WSN_GW_01C823","message":"Hello World!"}')

# Ngắt kết nối
sio.disconnect()