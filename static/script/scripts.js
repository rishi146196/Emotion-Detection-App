const fileInput = document.getElementById('fileInput');
const previewImg = document.getElementById('previewImg');
const uploadForm = document.getElementById('uploadForm');
const emotionResult = document.getElementById('emotionResult');

// Display the uploaded image in preview
fileInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            previewImg.src = event.target.result;
            previewImg.style.display = "block";
        };
        reader.readAsDataURL(file);
    } else {
        previewImg.style.display = "none";
    }
});

// Handle form submission
uploadForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData();
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload an image file.");
        return;
    }

    formData.append("file", file);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                emotionResult.textContent = `Predicted Emotion: ${data.emotion}`;
                emotionResult.style.display = "block";
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while predicting the emotion.");
        });
});
