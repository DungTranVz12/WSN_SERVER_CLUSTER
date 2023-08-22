const socket = io(); // Replace with your actual Socket.io server URL
socket.on('connect', () => {
  console.log('Connected to server');
  var message = {"method":"problem.get","params":{"hostgroupName":hostgroupName,"topic":topic}};
  socket.emit('SOCKET',{"topic":topic,"message": message}); // Request initial status from server on connect
});

function updateHostStatus (message){
  message = JSON.parse(message.replace(/'/g, '"'));
  // Check if message["method"] = "problem.update". If yes, then update node name and status to the web page if node is found. If not found, then add new node to the web page.
  if (message["method"] == "problem.update") {
    for (var i = 0; i < message["params"].length; i++) {
      var node_name = message["params"][i]["name"];
      var node_status = message["params"][i]["status"];
      var node_problemLink = message["params"][i]["problemLink"];
      if (document.getElementById(node_name) != null) {
        console.log("Node " + node_name + " found. Updating status to " + node_status);
        updateNodeStatus(node_name, node_status == "OK",node_problemLink);
      } else {
        console.log("Node " + node_name + " not found. Adding node to web page with status " + node_status);
        addNode(node_name, node_status == "OK",node_problemLink);
      }
    }
  }
}
socket.on(topic, (message) => {
  console.log("Received message from server");
  updateHostStatus(message);
  //Save message to local storage
  localStorage.setItem("LOCAL_STORE_HOST_PROBLEM", JSON.stringify(message));
});

function addNode(nodeName, isActive,node_problemLink) {
  var nodeElement = document.createElement("div");
  nodeElement.id = nodeName;
  nodeElement.classList.add("status-dot");
  if (isActive) {
    nodeElement.classList.add("active");
  } else {
    nodeElement.classList.add("inactive");
  }
  document.getElementById("node-container").appendChild(nodeElement);

  var nodeText = document.createElement("b");
  //Chỉ lấy nodeName là Chuỗi ký tự sau dấu "_" đầu tiên tìm thấy
  nodeNameDisp = nodeName.substring(nodeName.indexOf("_") + 1);
  //Đổi tên của node có dạng GATEWAY_NODE_2 thành Gateway_Node_2
  nodeNameDisp = nodeNameDisp.replace(/_/g, " ");
  nodeNameDisp = nodeNameDisp.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
  var nodeTextContent = document.createTextNode(nodeNameDisp);
  nodeText.appendChild(nodeTextContent);
  document.getElementById("node-container").appendChild(nodeText);

  //Add button
  var nodeButton = document.createElement("button");
  // set class cho button
  nodeButton.classList.add("btn");
  nodeButton.classList.add("btn-danger");
  nodeButton.classList.add("problemBtn");
  nodeButton.id = nodeName + "_btn";
  var nodeButtonText = document.createTextNode("Show Problem");
  nodeButton.appendChild(nodeButtonText);
  document.getElementById("node-container").appendChild(nodeButton);
  document.getElementById(nodeName+"_btn").onclick = () => {
    window.open(node_problemLink, '_blank');
  }
  var newline = document.createElement("br");
  document.getElementById("node-container").appendChild(newline);
  if (isActive) {
    document.getElementById(nodeName+"_btn").style.display = 'none';
  } else {
    document.getElementById(nodeName+"_btn").style.display = 'inline-block';
  }
  
}

function updateNodeStatus(nodeName, isActive,node_problemLink) {
  const nodeElement = document.getElementById(nodeName);
  if (isActive) {
    nodeElement.classList.add('active');
    nodeElement.classList.remove('inactive');
    document.getElementById(nodeName+"_btn").style.display = 'none';
  } else {
    nodeElement.classList.add('inactive');
    nodeElement.classList.remove('active');
    document.getElementById(nodeName+"_btn").style.display = 'inline-block';
    document.getElementById(nodeName+"_btn").onclick = () => {
      window.open(node_problemLink, '_blank');
    };
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Load initial status from local storage
  var message = JSON.parse(localStorage.getItem("LOCAL_STORE_HOST_PROBLEM"));
  if (message != null) {
    updateHostStatus(message);
  }

  // Periodically send update status request
  setInterval(() => {
    var message = {"method":"problem.get","params":{"hostgroupName":hostgroupName,"topic":topic}};
    socket.emit('SOCKET',{"topic":topic,"message": message}); // Request initial status from server on connect
  }, 60000);
});

