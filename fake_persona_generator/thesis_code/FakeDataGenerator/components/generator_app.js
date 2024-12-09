async function fetchSamples(count) {
    const samples = [];
    for (let i = 1; i <= count; i++) {
        samples.push({
            firstName: `Imię ${i}`,
            lastName: `Nazwisko ${i}`,
            email: `imie${i}.nazwisko@gmail.com`,
            age: Math.floor(Math.random() * 50) + 20,
            gender: Math.random() > 0.5 ? 'K' : 'M',
            position: `Stanowisko ${i}`
        });
    }
    return samples;
}

var chosenPositionText = "";
var chosenPosition = false;
var chosenDomain = "";
var domainShouldBeChosen = true;
var chosenGender = "";
var chosenFileFormat = ""



document.querySelectorAll('.dropdown-button').forEach(button => {
    button.addEventListener('click', function () {
      document.querySelectorAll('.dropdown').forEach(dropdown => {
        if (dropdown !== this.parentElement) {
          dropdown.classList.remove('active');
        }
      });
      this.parentElement.classList.toggle('active');
    });
  });
  

  window.addEventListener('click', function(event) {
    if (!event.target.matches('.dropdown-button')) {
      document.querySelectorAll('.dropdown').forEach(dropdown => {
        dropdown.classList.remove('active');
      });
    }
  });

function toggleDropdown(id) {
    const dropdownContent = document.getElementById(id);
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
}

function selectFormat(format) {
    const button = document.getElementById('formatPlikuTextHolder');
    button.textContent = `Format pliku: ${format}`;
    chosenFileFormat = format;
}

function selectGender(plec) {
  const button = document.getElementById('plecHolder');
  button.textContent = `Plec: ${plec}`;
  chosenGender = plec;
}

function selectAge(wiek) {
  const button = document.getElementById('wiekHolder');
  button.textContent = `Wiek: ${wiek}`;
}

function selectPosition(position) {
  const button = document.getElementById('positionHolder');
  button.textContent = `Stanowisko: ${position}`;
  if(position == "Tak"){
    chosenPosition = true;
  }
  else{
    chosenPosition = false;
  }
  chosenPositionText = position;

}

function selectMail(mail) {
  const button = document.getElementById('mailHolder');
  button.textContent = `E-mail: ${mail}`;
  domainFieldHolder = document.getElementById("domainInputHolder");
  domainField = document.getElementById("emailInput");
  if (mail == "Firmowy"){
    domainFieldHolder.style.display = 'block';
    domainShouldBeChosen = true;
  }
  else{
    domainFieldHolder.style.display = 'none';
    domainField.value = '';
    domainShouldBeChosen = false;
  }
}

function saveInput() {
  const inputValue = document.getElementById('emailInput').value;

  const domainPattern = /^@[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}$/;

  if (inputValue && domainPattern.test(inputValue)) {
      localStorage.setItem('savedEmail', inputValue);
      alert(`Saved: ${inputValue}`);
      chosenDomain = inputValue;
  } else {
      alert('Proszę wpisać poprawną domenę (np.: @gmail.com).');
  }
}

function getSavedInput() {
  const savedValue = localStorage.getItem('savedEmail');
  return savedValue;
}

async function generateRandomData() {
  var sampleCount = document.getElementById("sampleCountInput").value;

  var gender = document.getElementById('plecHolder').textContent;
  var position = document.getElementById("positionHolder").textContent;
  var emailDomain = document.getElementById("emailInput").value;

  var response = await ExecuteDataGenerationRequest(gender, emailDomain, sampleCount)
  console.log(response)
  const firstNames = response.Imie;
  const lastNames = response.Nazwisko;
  const emails = response.Email;
  const jobs = response.Stanowisko;
  const genders = response.Plec;
  const ageRanges = response.Wiek;

  const data = [];

  const length = firstNames.length;

  for (let i = 0; i < length; i++) {
    const row = {
      firstName: firstNames[i],
      lastName: lastNames[i],
      email: emails[i],
      age: ageRanges[i],
      gender: genders[i],
      job: jobs[i]
    };
    data.push(row);
  };

  return data;
}

async function displayTable() {
  if ((chosenDomain == "" && domainShouldBeChosen) || chosenFileFormat == "" || chosenGender == "" || (!chosenPosition && chosenPositionText == "")){
    alert("Proszę uzupełnić i ewentualnie zatwierdzić wszystkie pola przed wyświetleniem tabeli.");
    return;
  }
  var sampleCount = document.getElementById("sampleCountInput").value;
  if(!Number.isInteger(Number(sampleCount)) || sampleCount == ""){
    alert("Proszę wprowadzić właściwą liczbę próbek");
    return;
  }
  if(sampleCount)
  var data = await generateRandomData()
  const tableBody = document.querySelector("#data-table tbody");
  const tableHeader = document.querySelector("#data-table thead");

  tableBody.innerHTML = "";
  tableHeader.innerHTML = "";

  let headerHTML = `
    <th>Imię</th>
    <th>Nazwisko</th>
    <th>Email</th>
    <th>Wiek</th>
    <th>Płeć</th>
  `;
  
  if (chosenPosition) {
    headerHTML += `<th>Stanowisko</th>`;
  }
  

  tableHeader.innerHTML = `<tr>${headerHTML}</tr>`;

  // Tworzymy dane tabeli
  data.forEach((row) => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${row.firstName}</td>
      <td>${row.lastName}</td>
      <td>${row.email}</td>
      <td>${row.age}</td>
      <td>${row.gender}</td>
      ${chosenPosition ? `<td>${row.job}</td>` : ""}  <!-- Dodanie kolumny 'job' jeśli includePosition jest true -->
    `;
    
    tableBody.appendChild(tr);
  });

  document.querySelector("#table-container").style.display = "block";
  document.getElementById("download-button").style.display = "block";
}

dataGenerationUrl = "http://127.0.0.1:5000/generate";
async function ExecuteDataGenerationRequest(gender, emailDomain, sampleCount){

  var generationData = {
      "gender" : gender,
      "emailDomain": emailDomain,
      "sampleCount": sampleCount
  };

  return await fetch( dataGenerationUrl,{
      method: 'POST',
      headers:{'Content-Type': 'application/json'},
      body: JSON.stringify(generationData)
  })
  .then(Response => Response.json())
  .then(responseData => {return responseData})
  .catch(error => {
    console.log(error)
  });
  }

function downloadTable() {
  var format = chosenFileFormat;

  const table = document.querySelector("#data-table");
  const rows = Array.from(table.querySelectorAll("tbody tr"));

  let data = [];
  rows.forEach(row => {
    const rowData = Array.from(row.querySelectorAll("td")).map(td => td.textContent);
    data.push(rowData);
  });

  if (format === '.csv') {
    downloadCSV(data);
  } else if (format === '.txt') {
    downloadTXT(data);
  } else if (format === '.xlsx') {
    downloadXLSX(data);
  } else if (format === '.zip') {
    downloadZIP(data);
  }
}

function downloadCSV(data) {
  const csv = data.map(row => row.join(",")).join("\n");
  const blob = new Blob([csv], { type: 'text/csv' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'data.csv';
  link.click();
}

function downloadTXT(data) {
  const txt = data.map(row => row.join("\t")).join("\n");
  const blob = new Blob([txt], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'data.txt';
  link.click();
}

function downloadTable() {
  var format = chosenFileFormat;

  const table = document.querySelector("#data-table");
  const rows = Array.from(table.querySelectorAll("tbody tr"));

  const headers = Array.from(table.querySelectorAll("thead th")).map(th => th.textContent.trim());

  let data = [headers];

  rows.forEach(row => {
    const rowData = Array.from(row.querySelectorAll("td")).map(td => td.textContent);
    data.push(rowData);
  });

  if (format === '.csv') {
    downloadCSV(data);
  } else if (format === '.txt') {
    downloadTXT(data);
  } else if (format === '.xlsx') {
    downloadXLSX(data);
  } else if (format === '.zip') {
    downloadZIP(data);
  }
}

function downloadCSV(data) {
  const csv = data.map(row => row.join(",")).join("\n");
  const blob = new Blob([csv], { type: 'text/csv' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'data.csv';
  link.click();
}

function downloadTXT(data) {
  const txt = data.map(row => row.join("\t")).join("\n");
  const blob = new Blob([txt], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'data.txt';
  link.click();
}

function downloadXLSX(data) {
  const XLSX = window.XLSX;
  const ws = XLSX.utils.aoa_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
  const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'binary' });

  const blob = new Blob([s2ab(wbout)], { type: 'application/octet-stream' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'data.xlsx';
  link.click();
}

function s2ab(s) {
  const buf = new ArrayBuffer(s.length);
  const view = new Uint8Array(buf);
  for (let i = 0; i < s.length; i++) {
    view[i] = s.charCodeAt(i) & 0xFF;
  }
  return buf;
}

function downloadZIP(data) {
  const JSZip = window.JSZip;
  const zip = new JSZip();

  const csv = data.map(row => row.join(",")).join("\n");
  zip.file("data.csv", csv);

  zip.generateAsync({ type: "blob" }).then(function(content) {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(content);
    link.download = "data.zip";
    link.click();
  });
}