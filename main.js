const iconMarkup = `
<svg viewBox="0 0 48 48" role="presentation" aria-hidden="true">
  <circle cx="24" cy="24" r="14"></circle>
  <path d="M24 10v28M10 24h28"></path>
</svg>`;

fetch('siteData.json')
  .then((response) => response.json())
  .then((data) => {
    const achievementList = document.querySelector('#achievement-list');
    const businessGrid = document.querySelector('#business-grid');
    const historyList = document.querySelector('#history-list');

    data.achievements.forEach((item) => {
      const li = document.createElement('li');
      li.textContent = item;
      achievementList.appendChild(li);
    });

    data.businesses.forEach((item) => {
      const article = document.createElement('article');
      article.className = 'business-card';
      article.innerHTML = `${iconMarkup}<h3>${item}</h3>`;
      businessGrid.appendChild(article);
    });

    data.history.forEach((item) => {
      const li = document.createElement('li');
      li.textContent = item;
      historyList.appendChild(li);
    });
  });

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
      }
    });
  },
  { threshold: 0.2 }
);

document.querySelectorAll('.fade-in').forEach((section) => {
  observer.observe(section);
});
