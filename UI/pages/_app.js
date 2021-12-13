import { ChakraProvider } from '@chakra-ui/react'

function WebApp({ Component, pageProps }) {
  return (
    <ChakraProvider>
      <Component {...pageProps} />
    </ChakraProvider>
  )
}

export default WebApp

