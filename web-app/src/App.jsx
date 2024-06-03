import {
  Flex,
  Text,
  Container,
  Box,
  Input,
  InputGroup,
  InputRightElement,
} from "@chakra-ui/react";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import { ColorPalette } from "./utils/colors";
import { Fade } from "react-awesome-reveal";
import NewChat from "./components/NewChat";
import { useState, useEffect } from "react";
import { LoadingScreen } from "./components/LoadingScreen";
import "./app.css";
import bg from "./assets/office-bg-2.png";
import { IoIosSend } from "react-icons/io";
import { Auth } from "@supabase/auth-ui-react";
import { ThemeSupa } from "@supabase/auth-ui-shared";
import { supabase } from "./services/Supabase.service";
import { API_INSTANCE, addAuthorization } from "./api/api.instance";
import ChatHistory from "./components/ChatHistory";
import { Route, Routes } from "react-router-dom";
import Chat from "./components/Chat";

function App() {
  const [session, setSession] = useState(null);
  const [isLoading, setLoading] = useState(true);

  const getAuthorization = async () => {
    const response = await API_INSTANCE.post(
      "https://solventgpt-staging-r5i554wrlq-uc.a.run.app/test/login",
      {
        username: "user20@solvent.life",
        password: "dslaxLSl49",
      }
    );
    console.log("coiso", response);
    if (response?.data?.token) addAuthorization(response.data.token);
  };

  useEffect(() => {
    setTimeout(() => setLoading(false), 10000);

    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      getAuthorization();
    });
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      getAuthorization();
    });
    return () => subscription.unsubscribe();
  }, []);

  if (!session) {
    return (
      <div
        style={{
          width: "100vw",
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div>
          <Auth
            supabaseClient={supabase}
            appearance={{ theme: ThemeSupa }}
            providers={["google", "facebook", "github"]}
          />
        </div>
      </div>
    );
  }

  return (
    <>
      <Box display={isLoading ? "initial" : "none"} transition="250ms">
        <LoadingScreen />
      </Box>
      {!isLoading && <Fade triggerOnce delay={100}>
        <Flex
          flexDir={"row"}
          background={ColorPalette.blackPearl}
          width={"100vw"}
          maxW={"100vw"}
          height={"100vh"}
          maxH={"100vh"}
          gap={"16px"}
          backgroundImage={bg}
          backgroundSize={"cover"}
        >
          <Sidebar />
          <Flex width="100%" flexDir={"column"} justifyContent={"center"}>
            <Container
              minH={"4xl"}
              maxW={"8xl"}
              mb={2}
              background={"#1a202cb0"}
              box-shadow="0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);"
              backdropFilter="blur(10px)"
              borderRadius={"40px"}
              p={8}
              mr={60}
            >
              <Topbar />
              <Routes>
                <Route path="/" element={<NewChat />} />
                <Route path="/new" element={<NewChat />} />
                <Route path="/history" element={<ChatHistory />} />
                <Route path="/chat/:id" element={<Chat session={session} />} />
              </Routes>
            </Container>
          </Flex>
        </Flex>
      </Fade>}
    </>
  );
}

export default App;
