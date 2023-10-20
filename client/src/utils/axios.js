import axios from "axios";

let config = {
  headers: {
    Connection: "keep-alive",
    ContentType: "application/json",
  },
  mode: "cors",
};

/**
 * API helper function to get results from the backend
 * @param {*} url backend API url
 * @param {*} data form data
 * @returns
 */

export async function axiosGet(url) {
  try {
    let response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.log(error);
  }
}

export async function axiosPost(url, data) {
  try {
    let response = await axios.post(url, data, config);
    return response.data;
  } catch (error) {
    console.log(error);
  }
}
