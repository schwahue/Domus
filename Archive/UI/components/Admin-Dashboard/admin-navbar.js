import { useDisclosure } from '@chakra-ui/react'
import React from 'react'
import NextLink from 'next/link'
import {
    Drawer,
    DrawerBody,
    DrawerFooter,
    DrawerHeader,
    DrawerOverlay,
    DrawerContent,
    DrawerCloseButton,
    Button,
    IconButton,
    Link,
    Flex,
    Box,
    Heading,
    Container,
    Stack,
    Center
  } from '@chakra-ui/react'
import { HamburgerIcon } from '@chakra-ui/icons'


const SideBar = ({title}) => {
    const { isOpen, onOpen, onClose } = useDisclosure()
    const btnRef = React.useRef()
  
    return (
      <Container maxW="container.xl">
        <Button align='right' as={IconButton} ref={btnRef} colorScheme='teal' onClick={onOpen} icon={<HamburgerIcon />}/>
        <Center><Heading>{title}</Heading></Center>
        <Drawer
          isOpen={isOpen}
          placement='left'
          onClose={onClose}
          finalFocusRef={btnRef}
        >
          <DrawerOverlay />
          <DrawerContent>
            <DrawerCloseButton />
              <DrawerHeader>
                <NextLink href="/dashboard">
                  Domus Manager
                </NextLink>
              </DrawerHeader>

            <DrawerBody>
              <Stack>
                <NextLink href="/ticketing"> 
                  <Link>Ticketing Service</Link>
                </NextLink>
                <NextLink href="/">
                  <Button>Log out</Button>
                </NextLink>
              </Stack>
            </DrawerBody>

          </DrawerContent>
        </Drawer>
      </Container>
    )
}

export default SideBar