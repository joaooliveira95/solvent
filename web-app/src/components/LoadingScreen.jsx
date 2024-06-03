/* eslint-disable react/no-unknown-property */
import { Box, useColorModeValue } from "@chakra-ui/react";

export function LoadingScreen() {
  return (
    <Box
      position="absolute"
      zIndex="100"
      top="0"
      right="0"
      left="0"
      bottom="0"
      width="100vw"
      height="100vh"
      maxH={"100vh"}
      overflow={"hidden"}
      bg={useColorModeValue("gray.100", "gray.800")}
    >
      <video
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
        autoPlay
        loop
        muted
      >
        <source src="/loading.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </Box>
  );
}
