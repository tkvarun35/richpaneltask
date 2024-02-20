import { useEffect, useState } from "react";
import getRequest from "../../services/getRequest";
import { MdMergeType } from "react-icons/md";
import { useForm } from "react-hook-form";
import postRequest from "../../services/postRequest";
import { useNavigate } from "react-router-dom";

function Linkpage() {
  const [data, setData] = useState(null);
  const { register, handleSubmit } = useForm();
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const onSubmit = async (data) => {
    setIsLoading(true);
    const page = JSON.parse(data.page);
    const savePage = await postRequest(
      "addpage/",
      JSON.stringify({
        ...page,
        request_for: "getData",
      })
    );
    console.log(savePage);
    if (savePage.status === 200) {
      localStorage.setItem(
        "page",
        JSON.stringify({
          id: page.id,
          accesstoken: page.access_token,
          name: page.name,
        })
      );
      navigate("/dashboard");
    } else setIsLoading(false);
  };

  useEffect(() => {
    async function fetch() {
      const request = await getRequest(
        import.meta.env.VITE_BASE_URL + "getAccessToken/"
      ).then(async (response) => {
        // console.log(data);
        if (!response.error) setData(response);
        else navigate("/connect");
      });
      console.log("dfnsj");
    }
    fetch();
    if (data) console.log(data.data);
  }, []);
  console.log(data);
  return !data || data.data === null ? (
    <div className="fixed inset-0 flex items-center justify-center ">
      {/* <button
        onClick={() => fetch()}
        className="bg-green-300  text-black p-2 rounded-md flex  "
      >
        <MdMergeType className="m-3" />
        <span className="m-2">Get Page</span>
      </button> */}
      <p>Loading pages....</p>
    </div>
  ) : (
    <div>
      <p className="flex justify-center mt-10 text-xl text">Select Your Page</p>
      <form className="max-w-sm mx-auto" onSubmit={handleSubmit(onSubmit)}>
        <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          Select an option
        </label>
        <select
          id="countries"
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          {...register("page")}
          defaultValue={"default"}
        >
          <option value="default" disabled hidden>
            Choose Page
          </option>
          {data.data.map((item, key) => {
            return (
              <>
                <option
                  onClick={(event) => {
                    console.log(event);
                  }}
                  key={key}
                  value={JSON.stringify(item)}
                >
                  {item.name}
                </option>
              </>
            );
          })}
        </select>
        <div className="flex justify-center">
          <input
            type="submit"
            value={isLoading ? "fetching data" : "Submit"}
            className=" bg-cyan-600 p-3 m-4 rounded-md text-white"
            disabled={isLoading}
          />
        </div>
      </form>
    </div>
  );
}

export default Linkpage;
