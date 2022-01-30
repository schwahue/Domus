# Internet gateway to give our VPC access to the outside world
resource "aws_internet_gateway" "gw" {
  vpc_id = "${aws_vpc.vpc_demo.id}"

   tags = {
    Name = "internet-gateway-demo"
  }
}

# Grant the VPC internet access by creating a very generic
# destination CIDR ("catch all" - the least specific possible) 
# such that we route traffic to outside as a last resource for 
# any route that the table doesn't know about.
resource "aws_route" "internet_access" {
  route_table_id         = "${aws_vpc.main.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.main.id}"
}