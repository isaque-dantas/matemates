const selects = document.querySelectorAll("select");
selects.forEach((select) => {
  const options = select.options;
  for (let i = 0; i < options.length; i++) {
    const option = options.item(i);
    if (option.value === "") {
      option.disabled = true;
      option.selected = true;
    }
  }
});
