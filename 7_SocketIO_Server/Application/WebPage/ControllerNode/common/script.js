const socket = io();
console.log("HELLO");

socket.on('connect', () => {
  console.log('Connected to server');
  var message = {"method":"problem.get","params":{"hostgroupName":hostgroupName,"topic":topic}};
  // socket.emit('SOCKET',{"topic":topic,"message": message}); // Request initial status from server on connect
});

socket.on(topic, (message) => {
  console.log("Received message from server");
  updateHostStatus(message);
  resetCounter(); // Gọi hàm để đặt lại biến đếm sau khi nhận được gói tin cập nhật từ server
  //Save message to local storage
  localStorage.setItem("LOCAL_STORE_HOST_PROBLEM", JSON.stringify(message));
});





