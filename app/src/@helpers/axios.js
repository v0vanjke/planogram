// 📍 Axios intercepter
// Прослойка для авторизации
//
import axios from 'axios'
import { useErrStore } from '@/store/err'


export function axiosSetUp() {
  const errStore = useErrStore()

  axios.defaults.baseURL = "/back";
  axios.defaults.method = "post";

  axios.interceptors.request.use(
    // преднастройка axios запросов
    function (config) {
      // const token = authStore.accessToken;
      // if (token) {
      //   config.headers.Authorization = `Bearer ${token}`;
      // }
      return config;
    },
    function (error) {
      console.log('axios request error: ' + error)
      return Promise.reject(error);
    }
  );

  axios.interceptors.response.use(
    // преднастройка axios ответов
    function (response) {
      return response;
    },
    async function (error) {
      // const originalRequest = error.config;
      // if (error.response.status === 401) {
      //   const isRefresh = await authStore.makeRefresh()
      //   if (isRefresh) {
      //     return axios(originalRequest);
      //   }
      //   else {
      //     authStore.makeLogout()
      //   }
      // }
      if (error.response.data) {
        errStore.add({
          title: 'сервер вернул ошибку ' + error.response.status,
          message: error.response.data.error,
          status: 'error',
          from: error.request.responseURL,
        })

      }
      return Promise.reject(error);
    }
  );
}