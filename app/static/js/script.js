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

function formatReais(fieldId) {
  let input = document.querySelector(`#${fieldId}`).value;

  // Remove todos os caracteres que não sejam números
  input = input.replace(/\D/g, "");
  if (input != "") { //if input exists (is equal to type number)
    // Converte o valor para um formato de centavos
    input = (parseInt(input, 10) / 100).toFixed(2); // Garante duas casas decimais
    // Formata o valor para o padrão brasileiro
    input = input.replace(".", ",");
    // Adiciona o símbolo de R$
    document.querySelector(`#${fieldId}`).value = "R$" + input;
  } else {
    document.querySelector(`#${fieldId}`).value = input;
  }
}

// implement "this" element logic
