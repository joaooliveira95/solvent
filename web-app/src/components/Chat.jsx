import { Box, Flex, Container } from "@chakra-ui/react";
import { API_INSTANCE } from "../api/api.instance";
import { useState, useEffect , useRef} from "react";
import ChatInput from "./ChatInput";
import { ColorPalette } from "../utils/colors";
import { Fade } from "react-awesome-reveal";
import parse from 'html-react-parser';
import { useParams } from 'react-router-dom';

const USER_ROLE = "user        ";

export default function Chat(session) {
  const { id } = useParams();
  const [conversation, setConversation] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isLoading, setLoading] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    if (session) getChatHistory();
  }, [session]);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages]);

  const getChatHistory = async () => {
    setLoading(true);
    const response = await API_INSTANCE.get(
      `https://solventgpt-staging-r5i554wrlq-uc.a.run.app/v1/conversation?conversation_id=${id}`
    );
    if (response) {
      console.log(response);
      setConversation(response?.data);
      setMessages(response?.data?.messages);
    }
    setLoading(false);
  };

  const sendMessage = async (content) => {
    setLoading(true);

    setMessages([...messages, { role: USER_ROLE, content }]);
    const response = await API_INSTANCE.post(
      `https://solventgpt-staging-r5i554wrlq-uc.a.run.app/v1/agent/completion`,
      {
        conversation_id: conversation?.conversation_id,
        user_id: conversation?.user_id,
        messages: [
          ...messages,
          {
            role: "user",
            content,
          },
        ],
        temperature: 0.2,
      }
    );
    if (response) {
      console.log(response);
      setMessages([
        ...messages,
        { role: USER_ROLE, content },
        response.data?.message,
      ]);
    }
    setLoading(false);
  };

  console.log(conversation);

  return (
    <Container maxW={"8xl"}>
      <Flex
        flexDir={"column"}
        justifyContent={"space-between"}
        h={"100%"}
        minH={"80vh"}
      >
        <Flex
          flexDir={"column"}
          gap={8}
          py={16}
          maxH={"70vh"}
          ref={containerRef}
          overflowY={"auto"}
          justifyContent={"space-between"}
        >
          {messages.map((c, i) => (
            <Flex
              key={i}
              width={"full"}
              justifyContent={c.role === USER_ROLE ? "flex-end" : "flex-start"}
            >
              <Fade>
                <Box
                  bg={
                    c.role === USER_ROLE
                      ? ColorPalette.neutralPurple
                      : "blackAlpha.400"
                  }
                  borderRadius="15px"
                  py={4}
                  px={6}
                >
                  <Flex flexDir={"column"} gap={4}>{parse(c.content)}</Flex>
                </Box>
              </Fade>
            </Flex>
          ))}
        </Flex>
        <ChatInput onSubmit={(message) => sendMessage(message)} isLoading={isLoading}/>
      </Flex>
    </Container>
  );
}
