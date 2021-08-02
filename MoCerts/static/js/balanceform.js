window.addEventListener('DOMContentLoaded', function()  {
  
  // Поле имени можно вводить только цифры
  document.getElementById('id_withdrawal_amount').addEventListener('keyup', function () {
    this.value = this.value.replace(/[^0-9+]/g, '');
  });
  document.getElementById('id_amount').addEventListener('keyup', function () {
    this.value = this.value.replace(/[^0-9+]/g, '');
  });

})