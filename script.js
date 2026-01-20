const products = [
  {
    name: "Beetroot Microgreens",
    img: "images/beetrootmicrogreen.png",
    desc: "Vibrant red stems with a sweet, earthy flavor."
  },
  {
    name: "Broccoli Microgreens",
    img: "images/brocallymicrogreen.png",
    desc: "Mild, crunchy, and packed with sulforaphane."
  },
  {
    name: "Pea Shoot Microgreens",
    img: "images/peasoot microgreen.png",
    desc: "Sweet, crunchy shoots, perfect for salads."
  },
  {
    name: "Radish Microgreens",
    img: "images/radish microgreen.png",
    desc: "Spicy and peppery, adds a kick to any dish."
  },
  {
    name: "Sunflower Microgreens",
    img: "images/sunflowermicrogreen.png",
    desc: "Nutty, crunchy, and rich in protein."
  }
];

// Marquee Logic
const marqueeTrack = document.getElementById('marqueeTrack');
if (marqueeTrack) {
  const marqueeContent = products.map(p => `
    <div class="marquee-item w-64 h-64 flex-shrink-0 mx-4 rounded-xl overflow-hidden shadow-lg border-2 border-green-100 bg-white">
      <img src="${p.img}" alt="${p.name}" class="w-full h-full object-cover">
    </div>
  `).join('');

  // Duplicate content 3 times for seamless scrolling
  marqueeTrack.innerHTML = marqueeContent + marqueeContent + marqueeContent;
}

const grid = document.getElementById("productGrid");

products.forEach(p => {
  grid.innerHTML += `
    <div class="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 border border-gray-100">
      <div class="aspect-square bg-gray-100 overflow-hidden">
        <img src="${p.img}" alt="${p.name}" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300">
      </div>
      <div class="p-4">
        <h3 class="text-lg font-semibold mb-2 text-gray-900">${p.name}</h3>
        <p class="text-sm text-gray-600">${p.desc}</p>
      </div>
    </div>
  `;
});
