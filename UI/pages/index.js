import NextLink from 'next/link'
import { Box, Link, Stack } from '@chakra-ui/react'

function HomePage() {
	return (
		<Box>
			<Stack>
				<NextLink href='/dashboard'>
					<Link> Dashboard</Link>
				</NextLink>
				<NextLink href='/ticket-creation'>
					<Link> Create Ticket</Link>
				</NextLink>
			</Stack>
		</Box>
	)
}

export default HomePage
