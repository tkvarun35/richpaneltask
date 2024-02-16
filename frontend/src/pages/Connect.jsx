import { FacebookProvider, LoginButton } from "react-facebook";
import postRequest from "../../services/postRequest";
import { useNavigate } from "react-router-dom";
import { FaFacebookF } from "react-icons/fa";

export default function Connect() {
  const navigate = useNavigate();
  async function handleSuccess(response) {
    console.log(response);
    const data = {
      userid: response.authResponse.userID,
      accesstoken: response.authResponse.accessToken,
    };
    console.log(data);
    const req = await postRequest("syncUser/", data);
    console.log(req);
    navigate("/linkpage");
  }

  function handleError(error) {
    console.log(error);
  }

  return (
    <div className=" fixed inset-0 flex items-center justify-center">
      <FacebookProvider appId="780701930773171">
        <LoginButton
          scope="email,pages_show_list,pages_messaging"
          onError={handleError}
          onSuccess={handleSuccess}
        >
          <button className="bg-blue-700 text-white p-2 rounded-md flex ">
            <FaFacebookF className="m-3" />
            <span className="m-2">Connect with facebook</span>
          </button>
        </LoginButton>
      </FacebookProvider>
    </div>
  );
}
