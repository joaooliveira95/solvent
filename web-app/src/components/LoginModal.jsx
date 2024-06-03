import {
  Modal,
  ModalOverlay,
  ModalContent,
  Text,
  ModalCloseButton,
  ModalBody,
  Link,
  Button,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Stack,
  Image,
  Flex,
} from "@chakra-ui/react";
import Logo from "../assets/Logo.png";
import { ColorPalette } from "../utils/colors";

export default function LoginModal({ isOpen, onClose }) {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent
        background={"#1a202cb0"}
        box-shadow="0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);"
        backdropFilter="blur(10px)"
        color={"#fff"}
      >
        <ModalCloseButton />
        <ModalBody py={8}>
          <Flex flexDir="column" alignItems="center" gap="4" mb={8}>
            <Image width={"xxs"} height={"auto"} src={Logo} ml={"-1"} />
            <Heading size={"md"} mt={2}>
              Login
            </Heading>
          </Flex>

          <Stack spacing={4} color={"white"}>
            <FormControl id="email"  color={"#fff"}>
              <FormLabel>Email</FormLabel>
              <Input type="email" placeholder="your email" />
            </FormControl>
            <FormControl id="password"  color={"#fff"}>
              <FormLabel>Password</FormLabel>
              <Input type="password" placeholder="your password" />
            </FormControl>
            <Button
              width={"100%"}
              borderRadius={"15px"}
              colorScheme="blue"
              background={ColorPalette.navyBlue}
              color={"white"}
              mt={2}
            >
              Login
            </Button>
            <Stack pt={6}>
              <Text
                align={"center"}
                color={"gray.200"}
              >
                Don't have an account?{" "}
                <Link
                  color={"white"}
                  textDecor={"underline"}
                >
                  Sign up here
                </Link>
              </Text>
            </Stack>
          </Stack>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
