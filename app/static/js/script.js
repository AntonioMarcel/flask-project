function fetchOrdenadorDespesas() {
  let masp = document.querySelector("#masp").value;
  let nomeOrdenador = document.querySelector("#nome-ordenador");

  fetch(`/get_ordenador_name?masp=${masp}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.nome) {
        nomeOrdenador.value = data.nome;
      } else {
        nomeOrdenador.value = data.error;
      }
    })
    .catch((error) => console.log(error));
}

function fetchEmpData() {
  let ue = document.querySelector("#ue").value;
  let ano = document.querySelector("#ano").value;
  let empenho = document.querySelector("#empenho").value;

  let gmiFp = document.querySelector("#gmi-fp");
  let nomeCredor = document.querySelector("#nome-credor");
  let cnpjCpfCredor = document.querySelector("#cnpj-cpf-credor");

  fetch(`/get_emp_data?ue=${ue}&ano=${ano}&empenho=${empenho}`)
    .then((response) => response.json())
    .then((data) => {
      if (ue && ano && empenho) {
        gmiFp.value = data.gmi_fp;
        nomeCredor.value = data.nome_credor;
        cnpjCpfCredor.value = data.cpnj_cpf_credor;
      } else {
        gmiFp.value = data.error;
        nomeCredor.value = data.error;
        cnpjCpfCredor.value = data.error;
      }

      // console.log(data);
      // console.log(data.cpnj_cpf_credor);
      //        cnpjCpfCredor.value = data.cnpj_cpf_credor;
    })
    .catch((error) => console.log(error));
}

function formatProcessoSei() {
  let input = document.querySelector("#processo-sei").value;

  // Remove todos os caracteres não numéricos
  input = input.replace(/\D/g, "");

  // Adiciona pontos, barra e hífen conforme o padrão desejado
  if (input.length > 4) {
    input = input.slice(0, 4) + "." + input.slice(4); // Adiciona o primeiro ponto após os 4 primeiros dígitos
  }
  if (input.length > 7) {
    input = input.slice(0, 7) + "." + input.slice(7); // Adiciona o segundo ponto após os 7 primeiros dígitos
  }
  if (input.length > 15) {
    input = input.slice(0, 15) + "/" + input.slice(15); // Adiciona a barra após os 14 primeiros dígitos
  }
  if (input.length > 20) {
    input = input.slice(0, 20) + "-" + input.slice(20, 22); // Adiciona o hífen após os 19 primeiros dígitos e limita o campo a 21 caracteres
  }

  document.querySelector("#processo-sei").value = input;
}

function formatNumber(fieldId) {
  let input = document.querySelector(`#${fieldId}`).value;

  // Remove todos os caracteres não numéricos
  input = input.replace(/\D/g, "");

  document.querySelector(`#${fieldId}`).value = input;
}

function limitCharacters(fieldId, maxChars) {
  // Verifica se o valor inserido ultrapassa o limite
  let input = document.querySelector(`#${fieldId}`).value;

  if (input.length > maxChars) {
    input = input.slice(0, maxChars); // Trunca o valor para o limite permitido
  }

  document.querySelector(`#${fieldId}`).value = input;
}

// function formatReais(fieldId) {
//   let input = document.querySelector(`#${fieldId}`).value;

//   // Remove todos os caracteres que não sejam números
//   input = input.replace(/\D/g, "");
//   if (input != "") { //if input exists (is equal to type number)
//     // Converte o valor para um formato de centavos
//     input = (parseInt(input, 10) / 100).toFixed(2); // Garante duas casas decimais

//     let [whole, fraction] = input.split(".")
//     // console.log(input)
//     // console.log(whole)
//     // console.log(fraction)

//     remainder = whole.length % 3
//     if (whole.length > 3) {
//       if (whole.length % 3 == 1) {
//         console.log(whole[0]+"."+whole.slice(1)+","+fraction)

//       }

//       if (whole.length % 3 == 2) {
//         console.log(whole.slice(0,2)+"."+whole.slice(2)+","+fraction)


//       }

//       // console.log(whole)
//       // console.log(remainder)

      
// //      && whole.length % 3 != 0
//     }



//     // console.log(whole)

//     // console.log(remainder)

//   }
// }
  //   if (whole.length > 3) {


  //   }




// function formatReais(fieldId) {
//   let input = document.querySelector(`#${fieldId}`).value;

//   let formattedWholeNumber = "";

//   input = (parseInt(input, 10) / 100).toFixed(2); // Garante duas casas decimais
//   // console.log(input)

//   let [whole, fraction] = input.split(".")

//   if (whole.length > 3 && whole.length % 3 == 1) { //adds "." in number for every 3 characters, after number length higher or equal than 4
//     remainder = whole.length % 3;

//     for (let i = 0; i < whole.length; i++) {
//       if (i % 3 == 2) {
//         formattedWholeNumber = formattedWholeNumber + whole.slice(i - 2, i + 1) + ".";
//       }
//     }

//     if (remainder != 0) {//get last characters
//       formattedWholeNumber = formattedWholeNumber + whole.slice(remainder * -1);
//     }

//     console.log(formattedWholeNumber + "," + fraction);
//   }


// }

function formatReais(fieldId) {
  let input = document.querySelector(`#${fieldId}`).value;
  console.log(input)
  formatString = ""

  i = -1
  
  quocient = Math.floor(input.length/3)
  remainder = input.length%3
  firstDigits = input.slice(0, remainder) //get number first digits
  input = input.slice(remainder) //remove number first digits
  
  for (let q = 0; q < quocient-1; q++) {
    if (q == 0) { //começa a partir do 2º grupo de 3, então a iteração tem que ser reduzida em 1
      formatString = "." + input.slice((3*i)-3, 3*i) + "." + input.slice(-3) + formatString
      // formatString = "." + input.slice((3*i)-3, 3*i) + formatString
    } else if (q == quocient-2) { // na penúltima iteração, não adiciona ponto 
      formatString = input.slice((3*i)-3, 3*i) + formatString 
    } else {
      formatString = "." + input.slice((3*i)-3, 3*i) + formatString 
    }
    i--
  }
  console.log(formatString)

  if (quocient > 1 && remainder != 0) {
    formatString = firstDigits + "." + formatString 
  
  }
  
  // console.log(formatString)
  
}

function addSeparator(myString) {
  myString = "11111"
  i = -1
  formatString = ""
  quocient = Math.floor(myString.length/3)
  remainder = myString.length%3
  

  if (myString.length > 3) {
    if (quocient == 1) {
      formatString = myString.slice(0,remainder) + "." + myString.slice(-3)
      console.log(formatString)
      //formatString = "." + myString.slice(-3);
    }
    if (quocient == 2) {
      if (remainder != 0) {
      formatString = myString.slice(0,remainder) + "." + myString.slice(-6, -3)+ "." + myString.slice(-3)
      console.log(formatString)
    } else {
      formatString = myString.slice(-6, -3)+ "." + myString.slice(-3)
      console.log(formatString)

    }

    }
    if (quocient > 2) {
      firstDigits = myString.slice(0, remainder) //get number first digits
      myString = myString.slice(remainder) //remove number first digits
      
      for (let q = 0; q < quocient-1; q++) {
        if (q == 0) { //começa a partir do 2º grupo de 3, então a iteração tem que ser reduzida em 1
          formatString = "." + myString.slice((3*i)-3, 3*i) + "." + myString.slice(-3) + formatString
          // formatString = "." + myString.slice((3*i)-3, 3*i) + formatString
        } else if (q == quocient-2) { // na penúltima iteração, não adiciona ponto 
          formatString = myString.slice((3*i)-3, 3*i) + formatString 
        } else {
          formatString = "." + myString.slice((3*i)-3, 3*i) + formatString 
        }
        i--
      }
      
      if (quocient > 1 && remainder != 0) {
        formatString = firstDigits + "." + formatString 
      }
      console.log(formatString)
      
    }   

  }

}



console.log(myString.slice(-3, 0))


console.log(myString.slice(-6, -3))
console.log(myString.slice(-9, -6))
console.log(myString.slice(-12, -9))



"12231231123".slice(-3, -6)
console.log(formatString)


remainder = myString.length % 3
quocient = Math.floor(myString.length/3)

if (remainder != 0) {
  console.log(myString.slice(0, remainder))
}

i = 3 

for (let q = 0; q < quocient; q++) {
  console.log("." + myString.slice(-1*i*q))

}


formattedString = ""

for (let i = 0; i < myString.length; i++) {
  if (i%3 == 2) {
    formattedString = formattedString + myString.slice(i-2, i+1) + "."
  } 

}

if (remainder != 0) { //get last characters
  formattedString = formattedString + myString.slice(remainder*-1)
}

console.log(formattedString)


  //   // Formata o valor para o padrão brasileiro
  //   input = input.replace(".", ",");
  //   // Adiciona o símbolo de R$
  //   document.querySelector(`#${fieldId}`).value = "R$" + input;
  // } else {
  //   document.querySelector(`#${fieldId}`).value = input;
  // }
// }

// function formatReais(fieldId) {
//   let input = document.querySelector(`#${fieldId}`).value;

//   // Remove all non-numeric characters
//   input = input.replace(/\D/g, "");
//   if (input !== "") { // If input exists (is a valid number)
//     // Convert the value to a format with cents
//     input = (parseInt(input, 10) / 100).toFixed(2); // Ensures two decimal places

//     // Separate the whole number and fractional parts
//     let [whole, fraction] = input.split(".");

//     // Add a dot every three digits in the whole number part
//     whole = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

//     // Combine the formatted whole number and fraction with a comma
//     input = whole + "," + fraction;

//     // Add the "R$" symbol
//     document.querySelector(`#${fieldId}`).value = "R$" + input;
//   } else {
//     document.querySelector(`#${fieldId}`).value = input; // Keep the input empty if there's no valid number
//   }
// }


// implement "this" element logic
