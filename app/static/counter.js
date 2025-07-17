function updateButtonText(id) {
    const button = document.getElementById(`button-${id}`);
    const priceElement = document.getElementById(`product-price-${id}`);
    const price = parseFloat(priceElement.textContent);
    const quantity = parseInt(document.getElementById(`counter-value-${id}`).value);
  
    if (quantity > 0) {
      button.textContent = (price * quantity).toFixed(2);
      button.disabled = false;
    } else {
      button.textContent = 'BUY';
      button.disabled = true;
    }
  }
  
  function increase(counterId, id) {
    const counter = document.getElementById(counterId);
    counter.value = parseInt(counter.value) + 1;
    updateButtonText(id);
  }
  
  function decrease(counterId, id) {
    const counter = document.getElementById(counterId);
    counter.value = Math.max(0, parseInt(counter.value) - 1);
    updateButtonText(id);
  }
  
  function validateInput(input, id) {
    input.value = Math.max(0, parseInt(input.value) || 0);
    updateButtonText(id);
  }
  