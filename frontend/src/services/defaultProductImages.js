import api from './api';

/**
 * Lista todas as imagens de produtos padrão.
 * GET /default-product-images/
 *
 * @param {Object} params - Parâmetros da listagem.
 * @param {number} params.page - Página da listagem.
 * @returns {Promise<Object>} Resposta paginada com a lista de imagens padrão.
 */
export async function listDefaultProductImages({ page = 1 } = {}) {
  const response = await api.get('/default-product-images/', {
    params: { page },
  });
  return response.data;
}

/**
 * Envia um arquivo de imagem para o backend via multipart/form-data.
 * POST /default-product-images/{id}/image/
 *
 * Aceita tanto objetos do tipo File/Blob quanto strings Base64 (dataURL).
 * Se receber um DataURL (retornado pelo componente de upload),
 * converte-o automaticamente para um Blob antes de montar o FormData.
 *
 * @param {string|number} id - O ID (do produto/imagem).
 * @param {File|Blob|string} imageInput - O arquivo de imagem ou a string base64.
 * @returns {Promise<Object>} Resposta da API.
 */
export async function uploadDefaultProductImage(id, imageInput) {
  const formData = new FormData();

  if (typeof imageInput === 'string' && imageInput.startsWith('data:')) {
    // Converte base64/dataURI para um objeto Blob
    const arr = imageInput.split(',');
    const mimeMatch = arr[0].match(/:(.*?);/);
    const mime = mimeMatch ? mimeMatch[1] : 'image/png';
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    const blob = new Blob([u8arr], { type: mime });
    const extension = mime.split('/')[1] || 'png';

    formData.append('image', blob, `product_image_${id}.${extension}`);
  } else {
    formData.append('image', imageInput);
  }

  // Faz o post como multipart/form-data usando o axios
  const response = await api.post(`/default-product-images/${id}/image/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}
