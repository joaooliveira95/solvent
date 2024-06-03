import { Flex, IconButton, Tooltip } from "@chakra-ui/react";
import { GoHistory, GoPlus, GoSearch } from "react-icons/go";
import { MdSettingsVoice, MdSettings } from "react-icons/md";
import { useNavigate } from "react-router-dom";

export default function Sidebar() {
  const navigate = useNavigate();

  return (
    <Flex
      background={"#1a202cb0"}
      box-shadow="0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);"
      backdropFilter="blur(10px)"
      p="22px"
      flexDir={"column"}
      gap={"20px"}
      m="auto 52px"
      borderRadius={"45px"}
      height={"fit-content"}
    >
      <Tooltip label="New chat" placement={"right"}>
        <IconButton
          variant={"link"}
          icon={<GoPlus />}
          color={"white"}
          fontSize={"24px"}
          opacity={0.6}
          onClick={() => navigate("/new")}
          _hover={{
            opacity: 0.8,
          }}
        ></IconButton>
      </Tooltip>

      <Tooltip label="Voice activation" placement={"right"}>
        <IconButton
          variant={"link"}
          icon={<MdSettingsVoice />}
          color={"white"}
          fontSize={"24px"}
          opacity={0.6}
          _hover={{
            opacity: 0.8,
          }}
        ></IconButton>
      </Tooltip>

      <Tooltip label="Chat history" placement={"right"}>
        <IconButton
          variant={"link"}
          icon={<GoHistory />}
          color={"white"}
          fontSize={"24px"}
          opacity={0.6}
          onClick={() => navigate("/history")}
          _hover={{
            opacity: 0.8,
          }}
        ></IconButton>
      </Tooltip>
      <IconButton
        variant={"link"}
        icon={<GoSearch />}
        color={"white"}
        fontSize={"24px"}
        opacity={0.6}
        _hover={{
          opacity: 0.8,
        }}
      ></IconButton>
      <IconButton
        variant={"link"}
        icon={<MdSettings />}
        color={"white"}
        fontSize={"24px"}
        opacity={0.6}
        _hover={{
          opacity: 0.8,
        }}
      ></IconButton>
    </Flex>
  );
}
