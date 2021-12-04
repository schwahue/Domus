import SideBar from "../Admin-Dashboard/admin-navbar"
import { Box, Container} from '@chakra-ui/react'
import Head from 'next/head'


const AdminLayout = ({ children, router, title}) => {
    return (
        <Box as="main" pb='8'>
            <Head>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <title>Admin</title>
            </Head>

            <SideBar title={title} />

            <Container maxW="container.md" pt={14}>
                {children}
            </Container>
        </Box>
    )
}

export default AdminLayout