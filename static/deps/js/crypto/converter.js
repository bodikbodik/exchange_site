document.getElementById("convertForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const fromCurrency = document.getElementById("from_currency").value.toUpperCase() + "USDT";
    const toCurrency = document.getElementById("to_currency").value.toUpperCase() + "USDT";
    const amount = document.getElementById("amount").value;

    fetch(`/convert_crypto/?from_currency=${fromCurrency}&to_currency=${toCurrency}&amount=${amount}`)
        .then(response => response.json())
        .then(data => {
            const resultElement = document.getElementById("result");
            if (data.error) {
                resultElement.innerHTML = `${data.error}`;
            } else {
                resultElement.innerHTML = `
                    ${data.amount} ${data.from_currency} = ${data.converted_amount} ${data.to_currency}
                    <br>
                    Ціна ${data.from_currency}: ${data.from_price} 
                    <br>
                    Ціна ${data.to_currency}: ${data.to_price}
                `;
            }
        })
        .catch(error => {
            document.getElementById("result").innerHTML = `${error.message}`;
        });
});
