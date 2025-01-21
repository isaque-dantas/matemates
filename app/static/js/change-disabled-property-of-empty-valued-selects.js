document.addEventListener("DOMContentLoaded", () => {
    const selects = document.querySelectorAll("select");

    console.log(selects)

    selects.forEach((select) => {
        const options = Array.from(select.options)

        for (let option of options) {
            if (option.value === "") {
                option.disabled = true;

                if (!options.some((option) => option.selected)) option.selected = true;
            }
        }
    });

})


