# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
  access_key = "AKIAUYTM6DYDACETSKES"
  secret_key = "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"
}

#1. Create the VPC
resource "aws_vpc" "prod-vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = "true"
  enable_dns_support = "true"
  instance_tenancy = "default"

  tags = {
      Name = "production"
    }

}

#2. Create Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id     = aws_vpc.prod-vpc.id

  tags = {
    Name = "prod-internet-gateway"
  }
}

#3. Create Public Subnets
resource "aws_subnet" "public_1" {
  vpc_id     = aws_vpc.prod-vpc.id
  map_public_ip_on_launch = true
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "public-subnet-1"
  }
}
resource "aws_subnet" "public_2" {
  vpc_id     = aws_vpc.prod-vpc.id
  map_public_ip_on_launch = true
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "public-subnet-2"
  }
}

#4. Create Private Subnets
resource "aws_subnet" "private_1" {
  vpc_id     = aws_vpc.prod-vpc.id
  map_public_ip_on_launch = false
  cidr_block = "10.0.3.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-1"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id     = aws_vpc.prod-vpc.id
  map_public_ip_on_launch = false
  cidr_block = "10.0.4.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-2"
  }
}

resource "aws_subnet" "private_3" {
  vpc_id     = aws_vpc.prod-vpc.id
  map_public_ip_on_launch = false
  cidr_block = "10.0.5.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-3"
  }
}

resource "aws_subnet" "private_4" {
  vpc_id     = aws_vpc.prod-vpc.id
  map_public_ip_on_launch = false
  cidr_block = "10.0.6.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-4"
  }
}

#5. Create NAT Gateway
resource "aws_eip" "nat1" {
  vpc      = true
}

resource "aws_nat_gateway" "nat_gw_1" {
  allocation_id = aws_eip.nat1.id
  subnet_id     = aws_subnet.public_1.id
  depends_on    = [aws_internet_gateway.gw]
}

resource "aws_eip" "nat2" {
  vpc      = true
}

resource "aws_nat_gateway" "nat_gw_2" {
  allocation_id = aws_eip.nat2.id
  subnet_id     = aws_subnet.public_2.id
  depends_on    = [aws_internet_gateway.gw]
}

#6. Create Routes for private subnets
resource "aws_route_table" "route_private_1" {
  vpc_id = aws_vpc.prod-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gw_1.id
  }

  tags = {
    Name = "prod-private-route-table-1"
  }
}

resource "aws_route_table" "route_private_2" {
  vpc_id = aws_vpc.prod-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gw_2.id
  }

  tags = {
    Name = "prod-private-route-table-2"
  }
}

resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.route_private_1.id
}
resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.route_private_1.id
}
resource "aws_route_table_association" "private_3" {
  subnet_id      = aws_subnet.private_3.id
  route_table_id = aws_route_table.route_private_2.id
}
resource "aws_route_table_association" "private_4" {
  subnet_id      = aws_subnet.private_4.id
  route_table_id = aws_route_table.route_private_2.id
}

#7. Route table for Public Subnets
resource "aws_route_table" "route-public" {
  vpc_id = aws_vpc.prod-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "prod-public-route-table"
  }
}

resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.route-public.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.route-public.id
}

#8. Create Bastion Host
resource "aws_instance" "Bastion_Host_1" {
  ami                         = "ami-033b95fb8079dc481"
  instance_type               = "t2.micro"
  associate_public_ip_address = false
  subnet_id     = aws_subnet.public_1.id
  availability_zone = "us-east-1a"
  security_groups = [ aws_security_group.bastion-sg.id ]

  tags = {
    Name = "Bastion Host 1"
  }
}


resource "aws_instance" "Bastion_Host_2" {
  ami                         = "ami-033b95fb8079dc481"
  instance_type               = "t2.micro"
  associate_public_ip_address = false
  subnet_id     = aws_subnet.public_2.id
  availability_zone = "us-east-1b"
  security_groups = [ aws_security_group.bastion-sg.id ]

    tags = {
    Name = "Bastion Host 2"
  }
}


resource "aws_security_group" "bastion-sg" {
  name   = "bastion-security-group"
  vpc_id = aws_vpc.prod-vpc.id

  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# #9. Create Security Group to allow port 22,80,443
# resource "aws_security_group" "allow_web" {
#   name        = "allow_web_traffic"
#   description = "Allow Web inbound traffic"
#   vpc_id      = aws_vpc.prod-vpc.id

#   ingress {
#     description = "HTTPS"
#     from_port   = 443
#     to_port     = 443
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   ingress {
#     description = "HTTP"
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   ingress {
#     description = "SSH"
#     from_port   = 22
#     to_port     = 22
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   tags = {
#     Name = "allow_web"
#   }
# }