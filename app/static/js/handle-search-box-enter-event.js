const searchInputs = document.querySelectorAll(
  ".search-box > input.search-txt"
);

// document.addEventListener(
//     'keypress',
//     (event) => {
//         console.log(event.key)
//     }
// )

searchInputs.forEach((searchInput) => {
  searchInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      location.href = `/search/${searchInput.value}`;
    }
  });
});
