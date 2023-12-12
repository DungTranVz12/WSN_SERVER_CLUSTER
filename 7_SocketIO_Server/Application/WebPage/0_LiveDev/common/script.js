// const socket = io();
// console.log("Console hello");

// document.addEventListener('DOMContentLoaded', () => {
//   const sliders = document.querySelectorAll('.toggle-switch input[type="checkbox"]');
//   sliders.forEach(slider => {
//     slider.addEventListener('change', () => {
//       const sliderId = slider.id; // Lấy ID của slider
//       const sliderStatus = slider.checked; // Lấy trạng thái của slider (true/false)
//       // Gửi ID và trạng thái đến server
//       socket.emit('toggleSlider', { id: sliderId, status: sliderStatus }); 
//       console.log('Slider toggled:', sliderId, 'Status:', sliderStatus);
//     });
//   });
// });


// socket.on('WSN_GW_01C823.WEB.TEST', (msg) => {
//   if (msg === 'LOCK') {
//     const sliders = document.querySelectorAll('.toggle-switch input[type="checkbox"]');
//     sliders.forEach(slider => {
//       slider.disabled = true; // Khóa slider
//       slider.parentNode.classList.add('locked'); // Thêm class để hiển thị viền đỏ
//     });
//     const lockIcons = document.querySelectorAll('.lock-icon');
//     lockIcons.forEach(icon => icon.style.display = 'inline'); // Hiển thị icon ổ khóa
//   }
// });

