document.addEventListener("DOMContentLoaded", function() {
    const downloadBtn = document.querySelector('.download-btn');
    downloadBtn.addEventListener('click', function() {
        downloadBtn.classList.add('downloading');
    });
});
