
function submitSearch() {
  let composer = document.getElementById("composer-search").value;
  let title = document.getElementById("title-search").value;
  let query = "https://www.google.com/search?q=site:imslp.org " + composer + " " + title;
  console.log(composer);
  if (composer !== "" && title !== "") {
    window.open(query);
  }
}

function showDropdown(elementId) {
  dropdown = document.getElementById(elementId + "-dropdown");
  dropdown.style.display = "block";
  textBox = document.getElementById(elementId + "-search")
  if (textBox.value.length === 0) {
    dropdown.style.display = "none";
  }
}

// def match(keywords, album):
//     return (keywords in album) or all(keyword in album for keyword in keywords.split())

function match(search, tags) {
  in = tags.includes(search);
  matches = [];
  for (const word in search.split(" ")) {
    matches.push(tags.includes(word))
  }
  return tags.includes(search) || matches.every(true);
}

function test() {
  alert("test");
}
