const generateButton = document.getElementById('generate-button');
const imageInput = document.getElementById('image-input');
const captionDiv = document.getElementById('caption-text');
const imagePreview = document.getElementById('image-preview');
  
imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file); // Read the file as a Data URL for preview
    }
});

generateButton.addEventListener('click', async () => {
  const file = imageInput.files[0];
  if (file) {
    const formData = new FormData();
    formData.append('file', file);

    // Send the file to the backend
    const response = await fetch('/generate_caption', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    captionDiv.innerText = `Caption: ${result.caption}`;
  }
});
