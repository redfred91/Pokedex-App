import axios from 'axios';

const API_URL = 'http://192.168.86.41:5000/api/card';

export const uploadCardImage = (image) => {
    const formData = new FormData();
    formData.append('image', image);
    return axios.post(API_URL, formData);
};

