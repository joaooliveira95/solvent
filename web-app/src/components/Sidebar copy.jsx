import { Flex, Image, Button, Text } from "@chakra-ui/react";
import Logo from "../assets/Logo.png";
import { ColorPalette } from "../utils/colors";

export default function Sidebar() {
  return (
      <Flex
        width="278px"
        minWidth="278px"
        background={"#1a202cb0"}
        box-shadow="0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);"
        backdropFilter="blur(10px)"
        p="32px"
        flexDir={"column"}
        gap={"16px"}
        m="auto 32px"
        borderRadius={"45px"}
        height={"fit-content"}
      >
        <Image width={"80%"} height={"auto"} src={Logo} ml={"5"} borderRadius={"45px"}/>
        <Button
          background={ColorPalette.purple}
          color={ColorPalette.white}
          w={"full"}
          size={"lg"}
          borderRadius={"15px"}
          textTransform={"uppercase"}
          fontSize={"15px"}
          fontWeight={"800"}
        >
          New Chat
        </Button>
        <Flex mt={"8"} flexDir={"column"}>
          <Text
            fontSize={"16px"}
            fontWeight={400}
            lineHeight={"22.4px"}
            color={ColorPalette.white}
            opacity={0.5}
          >
            Yesterday
          </Text>
          <Flex
            gap={"14px"}
            flexDir={"column"}
            mt={"14px"}
            color={ColorPalette.white}
          >
            <Text cursor={"pointer"}>Lorem ipsum...</Text>
            <Text cursor={"pointer"}>Lorem ipsum...</Text>
            <Text cursor={"pointer"}>Lorem ipsum...</Text>
            <Text cursor={"pointer"}>Lorem ipsum...</Text>
          </Flex>
        </Flex>
        <Flex mt={"16px"} flexDir={"column"}>
          <Text
            fontSize={"16px"}
            fontWeight={400}
            lineHeight={"22.4px"}
            color={ColorPalette.white}
            opacity={0.5}
          >
            Previous 30 Days
          </Text>
          <Flex
            gap={"14px"}
            flexDir={"column"}
            mt={"14px"}
            color={ColorPalette.white}
          >
            <Text cursor={"pointer"}>Lorem ipsum...</Text>
            <Text cursor={"pointer"}>Lorem ipsum...</Text>
            <Text cursor={"pointer"}>Lorem ipsum...</Text>
            <Text cursor={"pointer"}>Lorem ipsum...</Text>
          </Flex>
        </Flex>
        {/* <Image
          width={"100%"}
          height={"auto"}
          src={Plan}
          mt={"auto"}
          mb={0}
          cursor={"pointer"}
        /> */}
      </Flex>
  );
}
