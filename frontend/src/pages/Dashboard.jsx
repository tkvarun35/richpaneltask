import { useEffect, useState } from "react";
import postRequest from "../../services/postRequest";
import { IoIosSend } from "react-icons/io";
import { useForm } from "react-hook-form";
import formatTime from "../../services/timeFormatter";
import { RxExit } from "react-icons/rx";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [pageData, setPageData] = useState(null);
  const [conversation, setConversation] = useState(true);
  const {
    register,
    handleSubmit,
    resetField,
    formState: { errors },
  } = useForm();
  useEffect(() => {
    const getmessage = async () => {
      let page = localStorage.getItem("page");
      page = JSON.parse(page);
      setPageData(page);

      const req = await postRequest("getmessage/", { pageid: page.id });
      setData(req.data.conversations);
    };
    getmessage();
  }, [conversation]);

  const refreshConversation = async () => {
    if (!pageData) return;
    const savePage = await postRequest(
      "addpage/",
      JSON.stringify({
        ...pageData,
        request_for: "refreshData",
      })
    );
    setConversation(!conversation);
    // setData(req.data);
    console.log(pageData);
  };

  // setInterval(refreshConversation, 20000);

  const refreshChat = async () => {
    if (!chat || !convID) return;
    const req = await postRequest(
      "getChat/",
      JSON.parse({ conversation_id: convID })
    );
    setChat(req.data);
  };

  // setInterval(refreshChat, 20000);

  const [convID, setConvID] = useState();
  const [chat, setChat] = useState([]);
  const [profile, setProfile] = useState([]);
  const onSubmit = async (data) => {
    if (!convID) {
      resetField("msg");
      return;
    }
    const req = await postRequest("reply/", { ...data, convID: convID });
    console.log(...chat, { conversation: 1, message_content: data.msg });
    setChat([...chat, { conversation: 1, message_content: data.msg }]);

    resetField("msg");
  };

  const getChat = async (data) => {
    setConvID(data.conversation_id);
    const req = await postRequest("getChat/", data);
    // const profile=await postRequest('getProf/',data);
    const profile_name = data.message.user.username;
    const paccesstoken = data.message.user.pat;
    const userid = data.message.user.user_id;

    setProfile({
      profile_name: profile_name,
      paccesstoken: paccesstoken,
      userid: userid,
    });

    setChat(req.data);
  };

  const disconnect = async () => {
    const req = await postRequest("disconnect/", {});
    console.log(req);
    navigate("/connect");
  };
  return !data ? (
    <div className="fixed inset-0 flex items-center justify-center">
      Loading Conversations...
    </div>
  ) : (
    <div className=" bg-white h-screen p-24">
      <div className="relative m-4 ">
        <button
          className="fixed top-4 right-32 rounded-2xl bg-red-500 p-3 text-white flex hover:bg-red-600"
          onClick={() => disconnect()}
        >
          <RxExit className="m-1" />
          Disconnect
        </button>
      </div>
      <div className="container shadow-lg rounded-lg">
        <div className="px-5 py-5 flex justify-between items-center bg-white border-b-2  ">
          <div className="font-semibold text-2xl">Conversations</div>
        </div>

        {data.length !== 0 ? (
          <div className="flex flex-row justify-between bg-white w-full h-full rounded-lg">
            <div className="flex flex-col w-2/5 border-r-2 overflow-y-auto">
              {data.map((messages, key) => {
                return (
                  <div
                    className="flex flex-row py-4 px-2 justify-center items-center border-b-2 cursor-pointer"
                    key={key}
                    onClick={() => getChat(messages)}
                  >
                    <div className="w-1/4">
                      <img
                        src={`https://graph.facebook.com/v19.0/${messages.message.user.user_id}/picture?access_token=${messages.message.user.pat}`}
                        className="object-cover h-12 w-12 rounded-full"
                        alt=""
                      />
                    </div>

                    <div className="w-full flex flex-col">
                      <div className="text-lg font-semibold">
                        {messages.message.user.username}
                      </div>
                      <span className="text-gray-500">
                        {messages.message.message_content}
                      </span>
                      <span>{formatTime(messages.message.created_time)}</span>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="w-full h-[32rem] px-5 flex flex-col justify-between">
              <div className="flex-none h-[32rem] min-w-full px-4 sm:px-6 md:px-0 overflow-hidden lg:overflow-auto scrollbar:!w-1.5 scrollbar:!h-1.5 scrollbar:bg-transparent scrollbar-track:!bg-slate-100 scrollbar-thumb:!rounded scrollbar-thumb:!bg-slate-300 scrollbar-track:!rounded dark:scrollbar-track:!bg-slate-500/[0.16] dark:scrollbar-thumb:!bg-slate-500/50 max-h-96 lg:supports-scrollbars:pr-2 lg:max-h-96">
                {chat ? (
                  <>
                    {" "}
                    {chat.map((data, key) => {
                      if (data.conversation) {
                        return (
                          <div className="flex justify-end mb-4" key={key}>
                            <div className="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white">
                              {data.message_content}
                            </div>
                            <img
                              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                              className="object-cover h-8 w-8 rounded-full"
                              alt=""
                            />
                          </div>
                        );
                      } else {
                        return (
                          <div className="flex justify-start mb-4" key={key}>
                            <img
                              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                              className="object-cover h-8 w-8 rounded-full"
                              alt=""
                            />
                            <div className="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-white">
                              {data.message_content}
                            </div>
                          </div>
                        );
                      }
                    })}
                  </>
                ) : (
                  <></>
                )}
              </div>
              {chat ? (
                <form
                  className="py-5 flex items-center justify-center"
                  onSubmit={handleSubmit(onSubmit)}
                >
                  <input
                    className="w-5/6 bg-gray-300 py-5 px-3 rounded-xl"
                    type="text"
                    placeholder="type your message here..."
                    {...register("msg")}
                    required
                  />
                  <button
                    className=" inset-0 flex items-center justify-center rotate-12"
                    type="submit"
                  >
                    <IoIosSend color="blue" size={"2.6rem"} />
                  </button>
                </form>
              ) : (
                <></>
              )}
            </div>

            {profile ? (
              <div className="w-2/5 border-l-2 px-5 h-[100px]">
                <div className="flex flex-col">
                  <img
                    src={`https://graph.facebook.com/v19.0/${profile.userid}/picture?access_token=${profile.paccesstoken}`}
                    className="object-cover  h-56 m-4 rounded-full"
                  />
                  <div className="font-semibold py-4 flex justify-center text-xl">
                    {profile.profile_name}
                  </div>
                </div>
              </div>
            ) : (
              <></>
            )}
          </div>
        ) : (
          <div className="text-xl text-black font-semibold text-center  m-28 p-24">
            No conversation to show!
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
