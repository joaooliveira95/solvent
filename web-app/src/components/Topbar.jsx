import {
  Avatar,
  Button,
  Flex,
  Image,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
} from "@chakra-ui/react";
import Logo from "../assets/Logo.png";
import { supabase } from "../services/Supabase.service";
import { useEffect, useState } from "react";
import { AiOutlineUser } from "react-icons/ai";

export default function Topbar() {
  const [session, setSession] = useState();

  const getSession = async () => {
    const { data, error } = await supabase.auth.getSession();
    if (!error && data) setSession(data);
  };

  const logout = async () => {
    const { error } = await supabase.auth.signOut();
    console.log(error);
  };

  useEffect(() => {
    getSession();
  }, []);

  console.log(session);

  return (
    <Flex
      width="100%"
      borderRadius={"15px"}
      height={"77px"}
      alignItems={"center"}
      justifyContent={"space-between"}
      p={"16px"}
    >
      <Image
        width={"240px"}
        height={"auto"}
        src={Logo}
        ml={"5"}
        borderRadius={"45px"}
      />

      {/* <Button
            background={ColorPalette.purple}
            color={ColorPalette.white}
            size={"lg"}
            borderRadius={"15px"}
          >
            Upgrade to Pro
          </Button> */}
      <Menu>
        <MenuButton
          as={Button}
          rounded={"full"}
          variant={"link"}
          cursor={"pointer"}
          minW={0}
        >
          <Avatar
            size={"md"}
            icon={<AiOutlineUser fontSize='1.5rem' />}
          />{" "}
        </MenuButton>
        <MenuList>
          <MenuItem>Profile</MenuItem>
          <MenuItem>Settings</MenuItem>
          <MenuDivider />
          <MenuItem onClick={() => logout()}>Logout</MenuItem>
        </MenuList>
      </Menu>
    </Flex>
  );
}
