import axios from "axios";

const instance = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 120000,
      headers: {
    'Content-Type': 'multipart/form-data', // 设置请求头为表单数据类型
  },
})

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // const userToken = UserSession.getToken();
    // if (userToken && config.headers) {
    //   config.headers['Authorization'] = userToken;
    // }

    return config;
  },
  (error) => {
    // 请求失败
    return Promise.reject(error);
  }
);

export {instance};