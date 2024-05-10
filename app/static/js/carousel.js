const carouselItems = document.querySelectorAll(".carousel-item");
carouselItems.forEach((item) => {
  const caption = item.querySelector(".caption");
  const image = item.querySelector('img')
  console.log(caption);
  if (caption) {
    image.style.right = '-15%'
  }
});
