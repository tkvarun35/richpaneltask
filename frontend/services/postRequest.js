const postRequest = (url, body) => {
  async function fetchAPI() {
    const BASE_URL = import.meta.env.VITE_BASE_URL;

    const response = await fetch(BASE_URL + url, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
      mode: "cors",
      credentials: "include",
    });

    const data = await response.json();
    const status = response.status;
    return { data: data, status: status };
  }
  const fetchResponse = fetchAPI();

  return fetchResponse;
};

export default postRequest;
