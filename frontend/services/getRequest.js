const getRequest = (url, params = {}, method = "GET") => {
  let options = {
    method,
  };
  if ("GET" === method) {
    url += "?" + new URLSearchParams(params).toString();
    options.credentials = "include";
    options.mode = "cors";
    // options.AllowAnyHeader();
    // options.AllowAnyMethod();
    // options.AllowCredentials();
  } else {
    options.body = JSON.stringify(params);
  }

  return fetch(url, options).then((response) => response.json());
};

export default getRequest;
