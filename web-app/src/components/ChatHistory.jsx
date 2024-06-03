/* eslint-disable react/jsx-key */
import {
  Heading,
  SimpleGrid,
  Flex,
  Button,
  Text,
  Box,
  Container,
} from "@chakra-ui/react";
import { ColorPalette } from "../utils/colors";
import { useEffect, useState } from "react";
import LoginModal from "./LoginModal";
import { Fade } from "react-awesome-reveal";
import RegisterModal from "./RegisterModal";
import FinancialChart from "./HighchartsDemo.component";
import { API_INSTANCE } from "../api/api.instance";
import { useNavigate } from "react-router-dom";

function GridElement({ conversation_id, created, title }) {
  const navigate = useNavigate();

  return (
    <Box
      width="100%"
      bg={ColorPalette.neutralPurple}
      borderRadius="15px"
      color={ColorPalette.white}
      py={4}
      px={6}
      cursor={"pointer"}
      transition={"250ms"}
      _hover={{
        background: ColorPalette.purple,
        transition: "250ms",
      }}
      onClick={() => navigate(`/chat/${conversation_id}`)}
    >
      <Text fontSize={"lg"}>
        {conversation_id} | {title}{" "}
      </Text>
      <Text opacity={0.5} fontSize={"lg"}>
        {created}
      </Text>
    </Box>
  );
}

export default function ChatHistory() {
  const [isLoginOpen, setLoginOpen] = useState(false);
  const [isRegisterOpen, setRegisterOpen] = useState(false);
  const [isDemoOpen, setDemoOpen] = useState(false);
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    getChatHistory();
  }, []);

  const getChatHistory = async () => {
    const response = await API_INSTANCE.get(
      "https://solventgpt-staging-r5i554wrlq-uc.a.run.app/v1/conversations/user"
    );
    if (response) {
      console.log("conversations", response);
      setConversations(response?.data?.conversations);
    }
  };

  return (
    <Container maxW={"8xl"}>
      <LoginModal isOpen={isLoginOpen} onClose={() => setLoginOpen(false)} />
      <RegisterModal
        isOpen={isRegisterOpen}
        onClose={() => setRegisterOpen(false)}
      />
      {!isDemoOpen && (
        <Flex flexDir={"column"} gap={8} py={16} alignItems={"center"}>
          <Fade triggerOnce delay={1500}>
            <Heading
              fontSize={"36px"}
              fontWeight={"500"}
              lineHeight={"54px"}
              letterSpacing={"-4%"}
              color={"#fff"}
            >
              Chat History
            </Heading>
          </Fade>
          <SimpleGrid columns={[1]} gap={4} minW={"4xl"} mt={8}>
            {conversations.map((conversation, index) => (
              <Fade triggerOnce direction="up" delay={2000 + index * 100}>
                <GridElement {...conversation} />
              </Fade>
            ))}
          </SimpleGrid>
        </Flex>
      )}
      {isDemoOpen && (
        <Flex flexDir={"column"} gap={8} py={16} alignItems={"center"}>
          <Button
            size={"lg"}
            background={ColorPalette.navyBlue}
            color={ColorPalette.white}
            borderRadius="15px"
            onClick={() => setDemoOpen(false)}
          >
            Go back
          </Button>
          <FinancialChart />
        </Flex>
      )}
    </Container>
  );
}
