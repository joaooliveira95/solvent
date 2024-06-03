import {
  InputGroup,
  InputRightElement,
  Input,
  Text,
  Flex,
  IconButton,
} from "@chakra-ui/react";
import { IoIosSend } from "react-icons/io";
import { ColorPalette } from "../utils/colors";
import { Fade } from "react-awesome-reveal";
import { useState } from "react";

export default function ChatInput({ onSubmit, isLoading }) {
  const [input, setInput] = useState("");

  return (
    <Fade triggerOnce>
      <Flex gap={8} alignItems={"center"}>
        <Input
          color={ColorPalette.white}
          placeholder="Ask Solvent.Life ™ Neural Network..."
          borderRadius={"15px"}
          onChange={(e) => setInput(e?.target?.value)}
          value={input}
          py={9}
        />
        <IconButton
          size={"lg"}
          icon={<IoIosSend color={ColorPalette.white} size={"20px"} />}
          onClick={() => {
            setInput("");
            onSubmit(input);
          }}
          isLoading={isLoading}
        />
      </Flex>

      <Text color={ColorPalette.white} opacity={0.4}>
        Solvent GPT ™ can make mistakes. Consider checking important
        information.
      </Text>
    </Fade>
  );
}
