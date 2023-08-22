# A. Hàm build & update image:
# 1. docker build -f Dockerfile -t meomay22/eclipse-mosquitto-pwfile:1.0 .
# 2. docker push meomay22/eclipse-mosquitto-pwfile:1.0
# B. Update:
# 1. Change mode cho toàn bộ thư mục và các thư mục con của /mosquitto thành 666
# 2. Cài đặt tài khoản đăng nhập: mqtt_broker/!Da#ImU%VuF3V
FROM eclipse-mosquitto

USER root
ADD ./pwfile /mosquitto/config/pwfile
ADD ./mosquitto.conf /mosquitto/config/mosquitto.conf
WORKDIR /mosquitto
