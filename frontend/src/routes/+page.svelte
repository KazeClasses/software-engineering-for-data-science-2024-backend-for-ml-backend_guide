<script>
  let selectedFile = null;
  let result = null;

  async function handleSubmit() {
    if (!selectedFile) {
      alert('Please select an image first');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/classifier/classify', {
        method: 'POST',
        body: formData,
      });

      console.log('Response:', response);
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      result = await response.json();
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while classifying the image');
    }
  }

  function handleFileChange(event) {
    selectedFile = event.target.files[0];
  }
</script>

<h1>Image Classifier</h1>

<input type="file" accept="image/*" on:change={handleFileChange} />

<button on:click={handleSubmit}>Classify Image</button>

{#if result}
  <h2>Classification Result:</h2>
  <pre>{JSON.stringify(result, null, 2)}</pre>
{/if}
