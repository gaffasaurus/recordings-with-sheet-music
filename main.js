//
// function loadJSON(callback) {
//   url = "https://raw.githubusercontent.com/gaffasaurus/recordings-with-sheet-music/master/scores.json";
//   const xhr = new XMLHttpRequest();
//   xhr.open('GET', url, true);
//   xhr.responseType = 'json';
//   xhr.onload = () => {
//   var status = xhr.status;
//   if (status === 200) {
//     callback(null, xhr.response);
//   } else {
//     callback(status, xhr.response);
//   }
// };
// xhr.send();
// }


fetch('https://raw.githubusercontent.com/gaffasaurus/recordings-with-sheet-music/master/scores.json')
  .then(response => response.json())
  .then(json => {
    readJSON(json)
  })

const selected = []

function readJSON(scores) {
  //add items to dropdown menus
  //composers
  const composerKeys = Object.keys(scores).sort();
  const composerInput = document.getElementById("composer-search");
  const composerDiv = document.getElementById("composer-dropdown");
  for (let i = 0; i < composerKeys.length; i++) {
    let composer = document.createElement('p');
    composer.onclick = () => {
      selected.splice(0, 1, composerKeys[i]);
      composerInput.value = composerKeys[i];
      clearChildren(document.getElementById('title-dropdown'));
      loadTitles(scores, composerKeys[i]);
    }
    composer.innerHTML = composerKeys[i];
    composerDiv.appendChild(composer);
  }
}

function firstUpper(str) {
  split = str.split(" ");
  for (let i = 0; i < split.length; i++) {
    split[i] = split[i].substr(0, 1).toUpperCase() + split[i].substr(1);
  }
  return split.join(" ");
}

function loadTitles(scores, name) {
  const composer = scores[name]
  const titleInput = document.getElementById('title-search');
  const titleDiv = document.getElementById('title-dropdown');
  titleInput.disabled = false;
  titleInput.placeholder = "Title...";

  for (let i = 0; i < composer.length; i++) {
    if (composer[i]['score'] === "none") {
      continue
    }
    let title = document.createElement('p');
    let pieceName = firstUpper(composer[i]['title']);
    title.onclick = () => {
      selected.splice(1, 1, composer[i]['score']);
      titleInput.value = pieceName
    }
    composer[i]['search_tags'].push(cleanUp(composer[i]['catalogue']));
    title.dataset.tags = composer[i]['search_tags'].join(" ");
    title.innerHTML = pieceName;
    titleDiv.appendChild(title);
  }
}

function submitSearch() {
  let composer = selected[0];
  let title = document.getElementById('title-search').value;
  let score = selected[1];
  if (score !== null && score !== "") {
    const imslp = document.createElement('object');
    imslp.height = 600;
    imslp.width = 500;
    // imslp.src = "https://www.youtube.com/results?search_query=" + title.split(" ").join("+");
    imslp.data = "http://conquest.imslp.info/files/imglnks/usimg/b/bc/IMSLP86431-PMLP02259-Chopin_Fantaisie_Impromptu_Op_66_Schlesinger_4392_First_Edition_1855.pdf";
    const embed = document.createElement('embed');
    embed.height = 600;
    embed.width = 500;
    embed.src = "http://conquest.imslp.info/files/imglnks/usimg/b/bc/IMSLP86431-PMLP02259-Chopin_Fantaisie_Impromptu_Op_66_Schlesinger_4392_First_Edition_1855.pdf";
    document.body.appendChild(imslp);
    imslp.appendChild(embed);

    window.open(score);
  }
}

document.addEventListener("click", () => {
  const dropdowns = document.getElementsByClassName("dropdown");
  for (let i = 0; i < dropdowns.length; i++) {
    dropdowns[i].style.display = "none";
  }
});

function clearChildren(parent) {
  while (parent.firstElementChild) {
    parent.removeChild(parent.firstElementChild);
  }
}

function showDropdown(elementId) {
  dropdown = document.getElementById(elementId + "-dropdown");
  dropdown.style.display = "block";
  textBox = document.getElementById(elementId + "-search")
  if (textBox.value.length === 0 && elementId === "composer") {
    dropdown.style.display = "none";
    titleInput = document.getElementById('title-search');
    titleInput.disabled = true;
    titleInput.value = "";
    titleInput.placeholder = "Title (composer required)";
    clearChildren(document.getElementById('title-dropdown'));
    selected[0] = "";
    selected[1] = "";
  }
  //Filter by searching
  const children = dropdown.childNodes;
  for (let i = 0; i < children.length; i++) {
    if (children[i].innerHTML != null) {
      if (elementId === "composer") {
        filterComposers(children[i]);
      } else if (elementId === "title") {
        filterTitles(children[i]);
      }
    }
  }
}

function filterComposers(child) {
  if (!match(cleanUp(textBox.value), cleanUp(child.innerHTML))) {
    child.style.display = "none";
  } else {
    child.style.display = "block";
  }
}

function filterTitles(child) {
  if (!match(cleanUp(textBox.value), cleanUp(child.dataset.tags))) {
    child.style.display = "none";
  } else {
    child.style.display = "block";
  }
}

function match(search, tags) {
  matches = [];
  for (i = 0; i < search.split(" ").length; i++) {
    word = search.split(" ")[i];
    matches.push(tags.includes(word))
  }
  return tags.includes(search) || matches.every(b => {return b});
}

function cleanUp(str) {
  return removePeriods(str.toLowerCase());
}

function removePeriods(str) {
  return str.replace(".", "");
}
