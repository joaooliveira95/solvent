import {
  Heading,
  SimpleGrid,
  Flex,
  Button,
  Image,
  useColorModeValue,
  Text,
  Box,
  Container,
} from "@chakra-ui/react";
import { ColorPalette } from "../utils/colors";
import Logo from "../assets/Logo.png";
import { useState } from "react";
import LoginModal from "./LoginModal";
import { Fade } from "react-awesome-reveal";
import RegisterModal from "./RegisterModal";
import FinancialChart from "./HighchartsDemo.component";

function GridElement() {
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
    >
      <Text fontSize={"lg"}>Give me a summary</Text>
      <Text opacity={0.5} fontSize={"lg"}>
        of TSLA’s 2023 earning report.
      </Text>
    </Box>
  );
}

export default function NewChat() {
  const [isLoginOpen, setLoginOpen] = useState(false);
  const [isRegisterOpen, setRegisterOpen] = useState(false);
  const [isDemoOpen, setDemoOpen] = useState(false);

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
              How can I help you today?
            </Heading>
          </Fade>
          <Fade triggerOnce delay={2000}>
            <Flex gap={3}>
              {/* <Button
                size={"lg"}
                colorScheme="black"
                borderRadius="15px"
                background={ColorPalette.bunker}
                color={ColorPalette.white}
                onClick={() => setRegisterOpen(true)}
              >
                Sign up
              </Button>
              <Button
                size={"lg"}
                background={ColorPalette.purple}
                color={ColorPalette.white}
                borderRadius="15px"
                onClick={() => setLoginOpen(true)}
                _hover={{
                  background: ColorPalette.lightPurple,
                }}
              >
                Login
              </Button> */}
              {/* <Button
                size={"lg"}
                background={ColorPalette.purple}
                color={ColorPalette.white}
                borderRadius="15px"
                onClick={() => setDemoOpen(true)}
                _hover={{
                  background: ColorPalette.lightPurple,
                }}
              >
                Highcharts Demo
              </Button> */}
            </Flex>
          </Fade>
          <SimpleGrid columns={[2]} gap={4} minW={"4xl"} mt={8}>
            <Fade triggerOnce direction="up" delay={2500}>
              <GridElement />
            </Fade>
            <Fade triggerOnce direction="up" delay={2600}>
              <GridElement />
            </Fade>
            <Fade triggerOnce direction="up" delay={2700}>
              <GridElement />
            </Fade>
            <Fade triggerOnce direction="up" delay={2800}>
              <GridElement />
            </Fade>
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
